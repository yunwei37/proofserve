import Lean

open Lean

/-- This experimental adapter uses the original kernel; a context conflict is
not a mathematical rejection and is sent to module-local replay. -/
structure AuditState where
  checked : Kernel.Environment
  visited : NameSet := {}
  pending : NameSet := {}
  regions : Array CompactedRegion := #[]
  imports : Std.HashMap Name (Array Name) := {}
  origins : Std.HashMap Name NameSet := {}
  segregated : NameSet := {}
  modules : Nat := 0
  constants : Nat := 0
  skipped : Nat := 0
  fallbacks : Nat := 0

abbrev AuditM := StateRefT AuditState IO

def event (fields : List (String × Json)) : IO Unit :=
  IO.println (Json.compress (Json.mkObj fields))

def moduleParts (mod : Name) : IO (Array (ModuleData × CompactedRegion)) := do
  let file ← findOLean mod
  unless ← file.pathExists do throw <| IO.userError s!"missing module {mod}"
  let mut files := #[file]
  let server := OLeanLevel.server.adjustFileName file
  if ← server.pathExists then
    files := files.push server
    let priv := OLeanLevel.private.adjustFileName file
    if ← priv.pathExists then files := files.push priv
  readModuleDataParts files

def sameQuotKind (a b : QuotKind) : Bool :=
  match a, b with
  | .type, .type | .ctor, .ctor | .lift, .lift | .ind, .ind => true
  | _, _ => false

/-- Structural comparisons retain actual typed fields, not just a hash. -/
def sameConstant (a b : ConstantInfo) : Bool :=
  match a, b with
  | .axiomInfo a, .axiomInfo b => a == b
  | .defnInfo a, .defnInfo b => a == b
  | .thmInfo a, .thmInfo b => a == b
  | .opaqueInfo a, .opaqueInfo b => a == b
  | .quotInfo a, .quotInfo b =>
    a.name == b.name && a.levelParams == b.levelParams && a.type == b.type &&
    sameQuotKind a.kind b.kind
  | .inductInfo a, .inductInfo b =>
    a.name == b.name && a.levelParams == b.levelParams && a.type == b.type &&
    a.numParams == b.numParams && a.numIndices == b.numIndices &&
    a.all == b.all && a.ctors == b.ctors && a.numNested == b.numNested &&
    a.isRec == b.isRec && a.isUnsafe == b.isUnsafe && a.isReflexive == b.isReflexive
  | .ctorInfo a, .ctorInfo b => a == b
  | .recInfo a, .recInfo b => a == b
  | _, _ => false

partial def closure (graph : Std.HashMap Name (Array Name)) (todo : List Name)
    (seen : NameSet := {}) : NameSet :=
  match todo with
  | [] => seen
  | m :: rest =>
    if seen.contains m then closure graph rest seen
    else closure graph ((graph[m]?.getD #[]).toList ++ rest) (seen.insert m)

def constantsOf (data : ModuleData) (mutation : String) :
    Std.HashMap Name ConstantInfo × Nat :=
  Id.run do
    let mut map : Std.HashMap Name ConstantInfo := {}
    let mut skipped := 0
    let mut changed := false
    for ci in data.constants do
      if ci.isUnsafe || ci.isPartial then skipped := skipped + 1
      let mut ci := ci
      if mutation != "none" && !changed then
        if let .thmInfo v := ci then
          let value := if mutation == "sibling" then mkConst `Shared.externalProof
            else Expr.bvar 0
          ci := .thmInfo { v with value }
          changed := true
      map := map.insert ci.name ci
    return (map, skipped)

/-- Module-local baseline is source-equivalent to the stock leanchecker path. -/
unsafe def localReplay (mod : Name) (mutation : String) : IO Unit := do
  let parts ← moduleParts mod
  let some (first, _) := parts[0]? | throw <| IO.userError "empty module"
  let some (data, _) := parts[parts.size - 1]? | throw <| IO.userError "empty module"
  let (_, imports) ← importModulesCore first.imports |>.run
  let env ← finalizeImport imports first.imports {} 0 false false (isModule := true)
  let (map, _) := constantsOf data mutation
  discard <| env.toKernelEnv.replay map
  env.freeRegions

/-- Optional memory snapshots are explicitly a profiling mode, off for primary timing. -/
def memorySnapshot (modules constants : Nat) : IO Unit := do
  if (← IO.getEnv "DECOUPLED_MEMORY_PROFILE") == some "1" then
    let step := ((← IO.getEnv "DECOUPLED_MEMORY_STEP").getD "100").toNat?.getD 100
    if step > 0 && modules % step == 0 then
      event [("event", toJson "memory_checkpoint"), ("modules", toJson modules),
        ("input_entries", toJson constants),
        ("smaps_rollup", toJson (← IO.FS.readFile "/proc/self/smaps_rollup"))]

partial def visit (mode mutation : String) (mutateOnly : Option Name) (mod : Name) : AuditM Unit := do
  if (← get).visited.contains mod then return
  if (← get).pending.contains mod then throw <| IO.userError s!"cyclic import {mod}"
  modify fun s => { s with pending := s.pending.insert mod }
  let parts ← moduleParts mod
  let some (first, _) := parts[0]? | throw <| IO.userError "empty module"
  let some (data, _) := parts[parts.size - 1]? | throw <| IO.userError "empty module"
  modify fun s => { s with regions := s.regions ++ parts.map (·.2),
    imports := s.imports.insert mod (first.imports.map (·.module)) }
  for imp in first.imports do visit mode mutation mutateOnly imp.module
  let chosen := if mutateOnly == some mod then mutation else "none"
  let (map, skipped) := constantsOf data chosen
  let s ← get
  let visible := closure s.imports (first.imports.map (·.module)).toList
  let mut reason : Option String := none
  let mut insertMap : Std.HashMap Name ConstantInfo := {}
  if mode == "audit" then
    for imported in visible do
      if s.segregated.contains imported then reason := some "segregated_dependency"
    for (_, ci) in map do
      unless ci.isUnsafe || ci.isPartial do
        if let some old := s.checked.find? ci.name then
          if !sameConstant old ci then reason := some s!"different_constant:{ci.name}"
        else insertMap := insertMap.insert ci.name ci
        for n in ci.getUsedConstantsAsSet do
          unless map.contains n do
            let origins := s.origins[n]?.getD {}
            let mut found := false
            for origin in origins do
              if visible.contains origin then found := true
            unless found do reason := some s!"unimported_reference:{ci.name}:{n}"
  else insertMap := map
  if let some why := reason then
    try
      unsafe localReplay mod chosen
      event [("event", toJson "accept"), ("module", toJson mod.toString),
        ("context", toJson "module_local"), ("fallback_reason", toJson why)]
      modify fun s => { s with segregated := s.segregated.insert mod, fallbacks := s.fallbacks + 1 }
    catch e =>
      event [("event", toJson "reject"), ("module", toJson mod.toString),
        ("context", toJson "module_local"), ("error", toJson e.toString),
        ("fallback_reason", toJson why)]
      throw e
  else
    try
      let checked ← s.checked.replay insertMap
      let mut origins := s.origins
      for (_, ci) in map do
        unless ci.isUnsafe || ci.isPartial do
          origins := origins.insert ci.name ((origins[ci.name]?.getD {}).insert mod)
      modify fun s => { s with checked, origins }
      event [("event", toJson "accept"), ("module", toJson mod.toString),
        ("context", toJson "shared"), ("constants", toJson data.constants.size),
        ("imports", toJson (first.imports.map (·.module.toString)))]
    catch e =>
      event [("event", toJson "reject"), ("module", toJson mod.toString),
        ("context", toJson "shared"), ("error", toJson e.toString)]
      throw e
  modify fun s => { s with pending := s.pending.erase mod, visited := s.visited.insert mod,
    modules := s.modules + 1, constants := s.constants + data.constants.size,
    skipped := s.skipped + skipped }
  let s ← get
  memorySnapshot s.modules s.constants

unsafe def main (args : List String) : IO UInt32 := do
  let mode :: mutation :: rawRoots := args |
    throw <| IO.userError "usage: audited-stream (audit|naive|one) (none|bvar|sibling) MODULE|@ROOTFILE..."
  unless ["audit","naive","one"].contains mode do throw <| IO.userError "invalid mode"
  unless ["none","bvar","sibling"].contains mutation do throw <| IO.userError "invalid mutation"
  initSearchPath (← findSysroot)
  let mut roots : List Name := []
  for arg in rawRoots do
    if arg.startsWith "@" then
      let text ← IO.FS.readFile (arg.drop 1 |>.toString)
      roots := roots ++ (text.splitOn "\n").filterMap (fun s =>
        let s := s.trimAscii.toString
        if s.isEmpty then none else some s.toName)
    else roots := roots ++ [arg.toName]
  if roots.isEmpty then throw <| IO.userError "at least one root"
  let mutateOnly := (← IO.getEnv "DECOUPLED_MUTATE_MODULE").map String.toName
  if mode == "one" then
    for mod in roots do
      let chosen := if mutateOnly == some mod then mutation else "none"
      try
        localReplay mod chosen
        event [("event", toJson "accept"), ("module", toJson mod.toString), ("context", toJson "module_local")]
      catch e =>
        event [("event", toJson "reject"), ("module", toJson mod.toString), ("error", toJson e.toString)]
        throw e
  else
    let empty ← mkEmptyEnvironment
    let (_, s) ← (do
      for mod in roots do visit mode mutation mutateOnly mod).run { checked := empty.toKernelEnv }
    event [("event", toJson "complete"), ("mode", toJson mode), ("modules", toJson s.modules),
      ("constants", toJson s.constants), ("skipped_unsafe_partial", toJson s.skipped),
      ("module_local_fallbacks", toJson s.fallbacks), ("retained_regions", toJson s.regions.size)]
  return 0
