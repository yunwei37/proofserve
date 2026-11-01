import Lean

open Lean

/-- Only the upstream 4.34.1 replay API inserts declarations into the checked environment. -/
structure CheckState where
  checked : Kernel.Environment
  visited : NameSet := {}
  pending : NameSet := {}
  regions : Array CompactedRegion := #[]
  modules : Nat := 0
  constants : Nat := 0
  skipped : Nat := 0
  mutated : Nat := 0

abbrev CheckM := StateRefT CheckState IO

def event (fields : List (String × Json)) : IO Unit :=
  IO.println (Json.compress (Json.mkObj fields))

def moduleParts (mod : Name) : IO (Array (ModuleData × CompactedRegion)) := do
  let file ← findOLean mod
  unless ← file.pathExists do
    throw <| IO.userError s!"missing module {mod}: {file}"
  let mut files := #[file]
  let server := OLeanLevel.server.adjustFileName file
  if ← server.pathExists then
    files := files.push server
    let priv := OLeanLevel.private.adjustFileName file
    if ← priv.pathExists then files := files.push priv
  readModuleDataParts files

/-- Deliberately malformed proof expressions; never mutate imported native files. -/
def corrupt (ci : ConstantInfo) (kind : String) : ConstantInfo :=
  match ci with
  | .thmInfo val =>
    let value := if kind == "bvar" then Expr.bvar 0
      else if kind == "unknown" then mkConst (Name.mkSimple "__decoupled_missing_proof_constant")
      else mkSort .zero
    .thmInfo { val with value }
  | _ => ci

def constantsOf (data : ModuleData) (mutation : String) :
    IO (Std.HashMap Name ConstantInfo × Nat × List String) := do
  let mut map : Std.HashMap Name ConstantInfo := {}
  let mut skipped := 0
  let mut names : List String := []
  let mut theoremIndex := 0
  let desired := if mutation == "unknown" then 1 else if mutation == "sort" then 2 else 0
  let mut changed := false
  for ci in data.constants do
    if ci.isUnsafe || ci.isPartial then skipped := skipped + 1
    let mut ci := ci
    if let .thmInfo _ := ci then
      if names.length < 3 then names := names ++ [ci.name.toString]
      if mutation != "none" && theoremIndex == desired then
        ci := corrupt ci mutation
        changed := true
      theoremIndex := theoremIndex + 1
    map := map.insert ci.name ci
  if mutation != "none" && !changed then
    throw <| IO.userError s!"requested corruption {mutation} has no matching theorem"
  return (map, skipped, names)

partial def visit (timed : Bool) (mode mutation : String) (roots : List Name) (mod : Name) : CheckM Unit := do
  if (← get).visited.contains mod then return
  if (← get).pending.contains mod then throw <| IO.userError s!"cyclic import {mod}"
  modify fun s => { s with pending := s.pending.insert mod }
  let readStart ← if timed then IO.monoNanosNow else pure 0
  let parts ← moduleParts mod
  let readEnd ← if timed then IO.monoNanosNow else pure 0
  let some (first, _) := parts[0]? | throw <| IO.userError s!"empty module data {mod}"
  let some (data, _) := parts[parts.size - 1]? | throw <| IO.userError s!"empty module data {mod}"
  modify fun s => { s with regions := s.regions ++ parts.map (·.2) }
  for imp in first.imports do visit timed mode mutation roots imp.module
  let mutateHere := if roots.contains mod then mutation else "none"
  let mapStart ← if timed then IO.monoNanosNow else pure 0
  let (map, skipped, names) ← constantsOf data mutateHere
  let replayStart ← if timed then IO.monoNanosNow else pure 0
  if mode != "manifest" then
    try
      let checked ← (← get).checked.replay map
      modify fun s => { s with checked }
    catch err =>
      event [("event", toJson "reject"), ("module", toJson mod.toString),
        ("error", toJson err.toString), ("mutation", toJson mutateHere)]
      throw err
  let replayEnd ← if timed then IO.monoNanosNow else pure 0
  modify fun s => { s with
    pending := s.pending.erase mod, visited := s.visited.insert mod,
    modules := s.modules + 1, constants := s.constants + data.constants.size,
    skipped := s.skipped + skipped, mutated := s.mutated + if mutateHere == "none" then 0 else 1 }
  event [("event", toJson (if mode == "manifest" then "manifest" else "accept")),
    ("module", toJson mod.toString), ("imports", toJson (first.imports.map (·.module.toString))),
    ("constants", toJson data.constants.size), ("skipped_unsafe_partial", toJson skipped),
    ("theorem_examples", toJson names)]
  if timed then event [("event", toJson "module_timing"), ("module", toJson mod.toString),
    ("read_ns", toJson (readEnd - readStart)), ("map_ns", toJson (replayStart - mapStart)),
    ("replay_ns", toJson (replayEnd - replayStart))]

/-- Source-equivalent single-module oracle; imports are trusted exactly as leanchecker. -/
unsafe def checkOne (mod : Name) (mutation : String) : IO Unit := do
  let parts ← moduleParts mod
  let some (first, _) := parts[0]? | throw <| IO.userError "empty module data"
  let some (data, _) := parts[parts.size - 1]? | throw <| IO.userError "empty module data"
  let (_, imports) ← importModulesCore first.imports |>.run
  let env ← finalizeImport imports first.imports {} 0 false false (isModule := true)
  let (map, skipped, names) ← constantsOf data mutation
  try
    discard <| env.toKernelEnv.replay map
    event [("event", toJson "accept"), ("module", toJson mod.toString),
      ("mutation", toJson mutation), ("skipped_unsafe_partial", toJson skipped),
      ("theorem_examples", toJson names)]
  catch err =>
    event [("event", toJson "reject"), ("module", toJson mod.toString), ("error", toJson err.toString)]
    throw err
  -- Module parts and import regions stay alive until after checking.
  event [("event", toJson "one_complete"), ("parts", toJson parts.size)]
  env.freeRegions

unsafe def main (args : List String) : IO UInt32 := do
  let mode :: mutation :: rootStrings := args | throw <| IO.userError "usage: stream-check (manifest|stream|one) (none|bvar|unknown|sort) MODULE..."
  unless ["manifest", "stream", "one"].contains mode do throw <| IO.userError "invalid mode"
  unless ["none", "bvar", "unknown", "sort"].contains mutation do throw <| IO.userError "invalid mutation"
  if rootStrings.isEmpty then throw <| IO.userError "at least one module required"
  initSearchPath (← findSysroot)
  let roots := rootStrings.map String.toName
  let timed := (← IO.getEnv "DECOUPLED_TIMING") == some "1"
  if mode == "one" then
    for mod in roots do checkOne mod mutation
  else
    let empty ← mkEmptyEnvironment
    let (_, state) ← (do
      for mod in roots do visit timed mode mutation roots mod
      ).run { checked := empty.toKernelEnv }
    event [("event", toJson "complete"), ("mode", toJson mode),
      ("modules", toJson state.modules), ("constants", toJson state.constants),
      ("skipped_unsafe_partial", toJson state.skipped), ("mutated", toJson state.mutated),
      ("retained_regions", toJson state.regions.size)]
  return 0
