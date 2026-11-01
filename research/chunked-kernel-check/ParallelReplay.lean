/- Native declaration-level wave prototype.
   Only checked stock replay output is exported via standard Lean modules.
   No unchecked union, temporary axioms, or replacement kernel. -/
import Lean
import Std.Sync.Mutex
open Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000

def emit (fields : List (String × Json)) : IO Unit :=
  IO.println <| Json.compress <| Json.mkObj fields

def readParts (file : System.FilePath) : IO (Array (ModuleData × CompactedRegion)) := do
  let mut files := #[file]
  let server := OLeanLevel.server.adjustFileName file
  if ← server.pathExists then
    files := files.push server
    let priv := OLeanLevel.private.adjustFileName file
    if ← priv.pathExists then files := files.push priv
  readModuleDataParts files

def inputMap (data : ModuleData) (mutation : String) :
    IO (Std.HashMap Name ConstantInfo) := do
  let mut map := {}
  let mut changed := false
  for original in data.constants do
    let mut ci := original
    if mutation != "none" && !changed then
      if let .thmInfo info := ci then
        let value := if mutation == "bvar" then Expr.bvar 0
          else if mutation == "unknown" then mkConst (Name.mkSimple "__m_parallel_missing")
          else mkSort .zero
        ci := .thmInfo {info with value}
        changed := true
    map := map.insert ci.name ci
  if mutation != "none" && !changed then throw <| IO.userError "no theorem to mutate"
  return map

/-- Restrict prototype to safe acyclic ordinary declarations. Other forms fail explicitly. -/
def ordinary (ci : ConstantInfo) : Bool :=
  !ci.isUnsafe && !ci.isPartial && match ci with
  | .thmInfo _ | .defnInfo _ | .opaqueInfo _ | .axiomInfo _ => true
  | _ => false

def sameOrdinary (a b : ConstantInfo) : Bool :=
  match a,b with
  | .thmInfo a,.thmInfo b => a == b
  | .defnInfo a,.defnInfo b => a == b
  | .opaqueInfo a,.opaqueInfo b => a == b
  | .axiomInfo a,.axiomInfo b => a == b
  | _,_ => false

def imported (first : ModuleData) (prior : Array String) : IO Environment := do
  let extra : Array Import := prior.map fun n => {module := n.toName}
  let imports := first.imports ++ extra
  let (_, state) ← importModulesCore imports |>.run
  finalizeImport state imports {} 0 false false (isModule := true)

def audit (data : ModuleData) (map : Std.HashMap Name ConstantInfo)
    (env : Kernel.Environment) : IO Unit := do
  let mut accepted := #[]
  for original in data.constants do
    let some ci := map[original.name]? | throw <| IO.userError "missing original map entry"
    unless ordinary ci do throw <| IO.userError s!"unsupported constant {ci.name}"
    let some actual := env.find? ci.name | throw <| IO.userError s!"missing checked {ci.name}"
    unless sameOrdinary ci actual do throw <| IO.userError s!"typed constant differs {ci.name}"
    accepted := accepted.push ci.name.toString
  emit [("event",toJson "accepted"),("names",toJson accepted),
    ("typed_constants_identical",toJson true),("count",toJson accepted.size)]

/-- Metadata only; original Name objects determine edges and original array indices are retained. -/
def plan (data : ModuleData) : IO Unit := do
  let indices := data.constants.foldl (fun (p : Nat × Std.HashMap Name Nat) ci =>
    (p.1+1,p.2.insert ci.name p.1)) (0,{}) |>.2
  let mut assigned : Std.HashMap Nat Nat := {}
  let mut levels : Array (Array Nat) := #[]
  let mut remaining := data.constants.size
  while remaining > 0 do
    let mut ready := #[]
    for i in [:data.constants.size] do
      if assigned.contains i then continue
      let ci := data.constants[i]!
      unless ordinary ci do throw <| IO.userError s!"unsupported declaration {ci.name}"
      let deps := ci.getUsedConstantsAsSet.toList.filterMap (indices[·]?)
      if deps.all assigned.contains then ready := ready.push i
    if ready.isEmpty then throw <| IO.userError "cyclic or unresolved local dependency graph"
    for i in ready do assigned := assigned.insert i levels.size
    remaining := remaining - ready.size
    levels := levels.push ready
  let mut rows := #[]
  for i in [:data.constants.size] do
    let ci := data.constants[i]!
    rows := rows.push <| Json.mkObj [
      ("index",toJson i),("name",toJson ci.name.toString),
      ("level",toJson assigned[i]!),
      ("dependencies",toJson <| ci.getUsedConstantsAsSet.toList.filterMap (indices[·]?))]
  emit [("event",toJson "plan"),("levels",toJson levels),("nodes",toJson rows)]

/-- A job index lock only; native checking and serialization never hold the queue lock. -/
def worker (id : Nat) (queue : Std.Mutex Nat) (jobs : Array Nat)
    (data : ModuleData) (map : Std.HashMap Name ConstantInfo) (base : Kernel.Environment)
    (modName : Name) (outFile : System.FilePath) : IO Json := do
  let mut checked := base
  let mut accepted := #[]
  let start ← IO.monoNanosNow
  repeat
    let index ← queue.atomically do
      let i ← get
      set (i+1)
      pure i
    if index >= jobs.size then break
    let ci := map[data.constants[jobs[index]!]!.name]!
    checked ← checked.replay (({} : Std.HashMap Name ConstantInfo).insert ci.name ci)
    let some actual := checked.find? ci.name | throw <| IO.userError s!"kernel lost {ci.name}"
    unless sameOrdinary actual ci do throw <| IO.userError s!"kernel result differs {ci.name}"
    accepted := accepted.push jobs[index]!
  let checkingStop ← IO.monoNanosNow
  -- This is stock checked-module serialization, not an unchecked environment join.
  writeModule ((Environment.ofKernelEnv checked).setMainModule modName) outFile (writeIR := false)
  let stop ← IO.monoNanosNow
  return Json.mkObj [
    ("worker",toJson id),("indices",toJson accepted),
    ("check_wall_ns",toJson (checkingStop-start)),("export_wall_ns",toJson (stop-checkingStop)),
    ("module",toJson modName.toString)]

unsafe def main (args : List String) : IO UInt32 := do
  let [mode,path,configPath] := args |
    throw <| IO.userError "usage: ParallelReplay (plan|stock|wave|audit) OLEAN CONFIG"
  initSearchPath (← findSysroot)
  let parts ← readParts path
  let some (first,_) := parts[0]? | throw <| IO.userError "empty original module"
  let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "empty original module"
  if mode == "plan" then
    plan data
    return 0
  let config ← IO.ofExcept <| Json.parse (← IO.FS.readFile configPath)
  let mutation ← IO.ofExcept <| config.getObjValAs? String "mutation"
  unless ["none","bvar","unknown","sort"].contains mutation do
    throw <| IO.userError "unsupported mutation"
  let map ← inputMap data mutation
  let prior ← IO.ofExcept <| config.getObjValAs? (Array String) "prior"
  let base ← imported first prior
  if mode == "stock" then
    let checked ← base.toKernelEnv.replay map
    audit data map checked
    return 0
  if mode == "audit" then
    audit data map base.toKernelEnv
    return 0
  unless mode == "wave" do throw <| IO.userError "unsupported mode"
  let jobs ← IO.ofExcept <| config.getObjValAs? (Array Nat) "jobs"
  let k ← IO.ofExcept <| config.getObjValAs? Nat "k"
  let fragmentPrefix ← IO.ofExcept <| config.getObjValAs? String "prefix"
  let out ← IO.ofExcept <| config.getObjValAs? String "out"
  unless [1,2,4,8].contains k do throw <| IO.userError "invalid k"
  -- Verify plan eligibility and the committed dependency frontier afresh.
  let mut seen : Std.HashSet Nat := {}
  for i in jobs do
    unless i < data.constants.size && !seen.contains i do
      throw <| IO.userError "invalid or duplicate job"
    seen := seen.insert i
    let ci := map[data.constants[i]!.name]!
    unless ordinary ci do throw <| IO.userError s!"unsupported job {ci.name}"
    if (base.find? ci.name).isSome then throw <| IO.userError s!"job already imported {ci.name}"
    for dep in ci.getUsedConstantsAsSet do
      if map.contains dep && !(base.find? dep).isSome then
        throw <| IO.userError s!"dependency not yet committed: {ci.name} needs {dep}"
  let queue ← Std.Mutex.new 0
  let mut tasks := #[]
  for i in [:min k jobs.size] do
    let name := Name.mkSimple s!"{fragmentPrefix}P{i}"
    let file := System.FilePath.mk out / s!"{name}.olean"
    tasks := tasks.push (← IO.asTask <| worker i queue jobs data map base.toKernelEnv name file)
  let mut results := #[]
  -- Ordered task result collection. Ordinary imports in the next wave commit checked artifacts.
  for task in tasks do
    match task.get with
    | .error e => throw e
    | .ok j => results := results.push j
  emit [("event",toJson "wave_complete"),("jobs",toJson jobs.size),("workers",toJson results)]
  return 0
