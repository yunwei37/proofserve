/- Derived from Lean4.34.1 Lean/Replay.lean, Copyright2023 Kim Morrison.
Released under Apache2.0, as upstream. Dependency ordering/generated-form
checks are unchanged; the local adaptation adds native-call timing only. -/
import Lean
open Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
@[extern "ck_cpu_ns"] opaque cpuNs : IO UInt64
@[extern "ck_thread_cpu_ns"] opaque threadCpuNs : IO UInt64
namespace MTimed

namespace Replay

structure Context where
  newConstants : Std.HashMap Name ConstantInfo

structure State where
  env : Kernel.Environment
  remaining : NameSet := {}
  pending : NameSet := {}
  postponedConstructors : NameSet := {}
  postponedRecursors : NameSet := {}

abbrev M := ReaderT Context <| StateRefT State IO

/-- Check if a `Name` still needs processing. If so, move it from `remaining` to `pending`. -/
def isTodo (name : Name) : M Bool := do
  let r := (← get).remaining
  if r.contains name then
    modify fun s => { s with remaining := s.remaining.erase name, pending := s.pending.insert name }
    return true
  else
    return false

/-- Use the current `Environment` to throw a `Kernel.Exception`. -/
def throwKernelException (ex : Kernel.Exception) : M Unit := do
  throw <| .userError <| (← ex.toMessageData {} |>.toString)

/-- Add a declaration, possibly throwing a `Kernel.Exception`. -/
def addDecl (d : Declaration) : M Unit := do
  let env := (← get).env
  let names := d.getNames
  let mut decision := false
  let mut goal := ""
  let mut goalHead := ""
  for name in names do
    if let some (.thmInfo ci) := (← read).newConstants[name]? then
      if ci.value.cleanupAnnotations.getAppFn.isConstOf (Name.mkSimple "of_decide_eq_true") then
        decision := true
        goal := toString ci.type
        goalHead := if ci.type.isForall then "forall" else toString ci.type.getAppFn
  let before ← IO.monoNanosNow
  let cpuBefore ← threadCpuNs
  let result := env.addDeclCore 0 0 d (cancelTk? := none)
  let cpuAfter ← threadCpuNs
  let after ← IO.monoNanosNow
  IO.println <| Json.compress <| Json.mkObj [
    ("event",toJson "kernel_declaration"),("names",toJson <| names.map Name.toString),
    ("decide_helper",toJson decision),("goal",toJson goal),("goal_head",toJson goalHead),
    ("wall_ns",toJson (after-before)),("thread_cpu_ns",toJson (cpuAfter-cpuBefore)),
    ("accepted",toJson result.isOk)]
  match result with
  | .ok checked => modify fun s => { s with env := checked }
  | .error ex => throwKernelException ex


mutual
/--
Check if a `Name` still needs to be processed (i.e. is in `remaining`).

If so, recursively replay any constants it refers to,
to ensure we add declarations in the right order.

The construct the `Declaration` from its stored `ConstantInfo`,
and add it to the environment.
-/
partial def replayConstant (name : Name) : M Unit := do
  if ← isTodo name then
    let some ci := (← read).newConstants[name]? | unreachable!
    replayConstants ci.getUsedConstantsAsSet
    -- Check that this name is still pending: a mutual block may have taken care of it.
    if (← get).pending.contains name then
      try
        match ci with
        | .defnInfo   info =>
          addDecl (Declaration.defnDecl   info)
        | .thmInfo    info =>
          -- Ignore duplicate theorems. This code is identical to that in `finalizeImport` before it
          -- added extended duplicates support for the module system, which is not relevant for us
          -- here as we always load all .olean information. We need this case *because* of the module
          -- system -- as we have more data loaded than it, we might encounter duplicate private
          -- theorems where elaboration under the module system would have only one of them in scope.
          if let some (.thmInfo info') := (← get).env.find? ci.name then
            if info.name == info'.name &&
              info.type == info'.type &&
              info.levelParams == info'.levelParams &&
              info.all == info'.all
            then
              return
          addDecl (Declaration.thmDecl    info)
        | .axiomInfo  info =>
          addDecl (Declaration.axiomDecl  info)
        | .opaqueInfo info =>
          addDecl (Declaration.opaqueDecl info)
        | .inductInfo info =>
          let lparams := info.levelParams
          let nparams := info.numParams
          let all ← info.all.mapM fun n => do pure <| ((← read).newConstants[n]!)
          for o in all do
            modify fun s =>
              { s with remaining := s.remaining.erase o.name, pending := s.pending.erase o.name }
          let ctorInfo ← all.mapM fun ci => do
            pure (ci, ← ci.inductiveVal!.ctors.mapM fun n => do
              pure ((← read).newConstants[n]!))
          -- Make sure we are really finished with the constructors.
          for (_, ctors) in ctorInfo do
            for ctor in ctors do
              replayConstants ctor.getUsedConstantsAsSet
          let types : List InductiveType := ctorInfo.map fun ⟨ci, ctors⟩ =>
            { name := ci.name
              type := ci.type
              ctors := ctors.map fun ci => { name := ci.name, type := ci.type } }
          addDecl (Declaration.inductDecl lparams nparams types false)
        -- We postpone checking constructors,
        -- and at the end make sure they are identical
        -- to the constructors generated when we replay the inductives.
        | .ctorInfo info =>
          modify fun s => { s with postponedConstructors := s.postponedConstructors.insert info.name }
        -- Similarly we postpone checking recursors.
        | .recInfo info =>
          modify fun s => { s with postponedRecursors := s.postponedRecursors.insert info.name }
        | .quotInfo _ =>
          -- `Quot.lift` and `Quot.ind` have types that reference `Eq`,
          -- so we need to ensure `Eq` is replayed before adding the quotient declaration.
          replayConstant `Eq
          addDecl (Declaration.quotDecl)
        modify fun s => { s with pending := s.pending.erase name }
      catch ex =>
        throw <| .userError s!"while replaying declaration '{name}':\n{ex}"

/-- Replay a set of constants one at a time. -/
partial def replayConstants (names : NameSet) : M Unit := do
  for n in names do replayConstant n

end

/--
Check that all postponed constructors are identical to those generated
when we replayed the inductives.
-/
def checkPostponedConstructors : M Unit := do
  for ctor in (← get).postponedConstructors do
    match (← get).env.find? ctor, (← read).newConstants[ctor]? with
    | some (.ctorInfo info), some (.ctorInfo info') =>
      if ! (info == info') then throw <| IO.userError s!"Invalid constructor {ctor}"
    | _, _ => throw <| IO.userError s!"No such constructor {ctor}"

/--
Check that all postponed recursors are identical to those generated
when we replayed the inductives.
-/
def checkPostponedRecursors : M Unit := do
  for ctor in (← get).postponedRecursors do
    match (← get).env.find? ctor, (← read).newConstants[ctor]? with
    | some (.recInfo info), some (.recInfo info') =>
      if ! (info == info') then throw <| IO.userError s!"Invalid recursor {ctor}"
    | _, _ => throw <| IO.userError s!"No such recursor {ctor}"

end Replay

open Replay

/--
"Replay" some constants into a `Kernel.Environment`, sending them to the kernel for checking.

Throws a `IO.userError` if the kernel rejects a constant,
or if there are malformed recursors or constructors for inductive types.
-/
def replay (newConstants : Std.HashMap Name ConstantInfo) (env : Kernel.Environment) :
    IO Kernel.Environment := do
  let mut remaining : NameSet := ∅
  for (n, ci) in newConstants.toList do
    -- We skip unsafe constants, and also partial constants.
    -- Later we may want to handle partial constants.
    if !ci.isUnsafe && !ci.isPartial then
      remaining := remaining.insert n
  let (_, s) ← StateRefT'.run (s := { env, remaining }) do
    ReaderT.run (r := { newConstants }) do
      for n in remaining do
        replayConstant n
      checkPostponedConstructors
      checkPostponedRecursors
  return s.env

end MTimed

/-- Same reader as O lane and stock checker; original data is never modified. -/
def modulePartsAt (file : System.FilePath) : IO (Array (ModuleData × CompactedRegion)) := do
  unless ← file.pathExists do throw <| IO.userError s!"missing artifact {file}"
  let mut files := #[file]
  let server := OLeanLevel.server.adjustFileName file
  if ← server.pathExists then
    files := files.push server
    let priv := OLeanLevel.private.adjustFileName file
    if ← priv.pathExists then files := files.push priv
  readModuleDataParts files

unsafe def main (args : List String) : IO UInt32 := do
  let mode :: mod :: path :: rest := args |
    throw <| IO.userError "usage: TimedReplay (stock|timed|metadata) MODULE OLEAN"
  let mutation := rest.headD "none"
  unless ["none","bvar"].contains mutation do throw <| IO.userError "invalid mutation"
  unless ["stock","timed","metadata"].contains mode do throw <| IO.userError "invalid mode"
  initSearchPath (← findSysroot)
  let parts ← modulePartsAt path
  let some (first, _) := parts[0]? | throw <| IO.userError "empty module"
  let some (data, _) := parts[parts.size-1]? | throw <| IO.userError "empty module"
  let mut constants : Std.HashMap Name ConstantInfo := {}
  let mut eligible := #[]
  let mut decisions := 0
  let mut changed := false
  for original in data.constants do
    let mut ci := original
    if mutation == "bvar" && !changed then
      if let .thmInfo info := ci then
        ci := .thmInfo {info with value := Expr.bvar 0}
        changed := true
    constants := constants.insert ci.name ci
    unless ci.isUnsafe || ci.isPartial do
      eligible := eligible.push ci.name.toString
    if let .thmInfo info := ci then
      if info.value.cleanupAnnotations.getAppFn.isConstOf (Name.mkSimple "of_decide_eq_true") then
        decisions := decisions + 1
  IO.println <| Json.compress <| Json.mkObj [
    ("event",toJson "input"),("module",toJson mod),("mode",toJson mode),
    ("entries",toJson data.constants.size),("eligible_entries",toJson eligible.size),
    ("native_decide_helpers",toJson decisions),("input_file",toJson path)]
  if mode == "metadata" then
    for ci in data.constants do
      let refs := ci.getUsedConstantsAsSet.toList.filter constants.contains
      IO.println <| Json.compress <| Json.mkObj [
        ("event",toJson "dependency"),("name",toJson ci.name.toString),
        ("refs",toJson <| refs.map Name.toString),("unsafe_or_partial",toJson (ci.isUnsafe || ci.isPartial))]
    return 0
  let (_, imports) ← importModulesCore first.imports |>.run
  -- Target is not imported: only its declared dependencies are trusted here.
  let env ← finalizeImport imports first.imports {} 0 false false (isModule := true)
  let t0 ← IO.monoNanosNow
  let cpu0 ← cpuNs
  let checked ← if mode == "stock" then env.toKernelEnv.replay constants
                 else MTimed.replay constants env.toKernelEnv
  let cpu1 ← cpuNs
  let t1 ← IO.monoNanosNow
  for name in eligible do
    unless (checked.find? name.toName).isSome do
      throw <| IO.userError s!"missing accepted eligible declaration {name}"
  IO.println <| Json.compress <| Json.mkObj [
    ("event",toJson "complete"),("module",toJson mod),("mode",toJson mode),
    ("replay_wall_ns",toJson (t1-t0)),("replay_process_cpu_ns",toJson (cpu1-cpu0)),
    ("eligible_names",toJson eligible),("all_eligible_present",toJson true),
    ("native_decide_helpers",toJson decisions)]
  -- Keep all raw module/import regions alive until process exit.
  return 0
