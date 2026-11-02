import Lean

open Lean

/-- This experimental adapter uses the original kernel; a context conflict is
not a mathematical rejection and is sent to module-local replay. -/
structure AuditState where
  checked : Kernel.Environment
  ancestorMasks : Std.HashMap Name Nat := {}
  moduleIndices : Std.HashMap Name Nat := {}
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

/-- Matches the upstream replay duplicate-theorem policy only within imports. -/
def sameTheoremInterface (a b : ConstantInfo) : Bool :=
  match a, b with
  | .thmInfo a, .thmInfo b =>
    a.name == b.name && a.levelParams == b.levelParams && a.type == b.type && a.all == b.all
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
    for name in data.constNames, ci in data.constants do
      if ci.isUnsafe || ci.isPartial then skipped := skipped + 1
      let mut ci := ci
      if mutation != "none" && !changed then
        if let .thmInfo v := ci then
          let value := if mutation == "sibling" then mkConst `Shared.externalProof
            else Expr.bvar 0
          ci := .thmInfo { v with value }
          changed := true
      map := map.insert name ci
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
def memorySnapshot (state : AuditState) (force : Bool := false) : IO Unit := do
  if (← IO.getEnv "DECOUPLED_MEMORY_PROFILE") == some "1" then
    let step := ((← IO.getEnv "DECOUPLED_MEMORY_STEP").getD "100").toNat?.getD 100
    if force || (step > 0 && state.modules % step == 0) then
      let checkedCount : Nat := SMap.fold (fun n _ _ => n + 1) 0 state.checked.constants
      event [("event", toJson "memory_checkpoint"), ("modules", toJson state.modules),
        ("input_entries", toJson state.constants),
        ("processed_eligible_entries", toJson (state.constants - state.skipped)),
        ("shared_kernel_declarations", toJson checkedCount),
        ("module_local_checks", toJson state.fallbacks),
        ("process_status", toJson (← IO.FS.readFile "/proc/self/status")),
        ("smaps_rollup", toJson (← IO.FS.readFile "/proc/self/smaps_rollup"))]


/-- Pure audit metadata. Kernel declarations are exported separately by Lean. -/
structure CheckpointMeta where
  visited : NameSet
  imports : Std.HashMap Name (Array Name)
  origins : Std.HashMap Name NameSet
  segregated : NameSet
  modules : Nat
  constants : Nat
  skipped : Nat
  fallbacks : Nat
  ancestorMasks : Std.HashMap Name Nat
  moduleIndices : Std.HashMap Name Nat

initialize checkpointDone : IO.Ref Bool ← IO.mkRef false
initialize checkpointBase : IO.Ref Nat ← IO.mkRef 0
initialize checkpointNames : IO.Ref NameSet ← IO.mkRef {}

/-- Only constants already accepted by the original kernel are exported. -/
unsafe def saveCheckpoint (s : AuditState) (file : System.FilePath) (mod : Name) : IO Unit := do
  let oldNames ← checkpointNames.get
  let constants : Array ConstantInfo :=
    SMap.fold (fun acc name ci => if oldNames.contains name then acc else acc.push ci) #[] s.checked.constants
  let imports := match ← IO.getEnv "DECOUPLED_CHECKPOINT_INPUT" with
    | some name => #[({ module := name.toName } : Import)]
    | none => #[]
  let auditMeta : CheckpointMeta := {
    visited := s.visited, imports := s.imports, origins := s.origins,
    segregated := s.segregated, modules := s.modules, constants := s.constants,
    skipped := s.skipped, fallbacks := s.fallbacks,
    ancestorMasks := s.ancestorMasks, moduleIndices := s.moduleIndices }
  let data : ModuleData := {
    isModule := false, imports, constNames := constants.map (·.name),
    constants, extraConstNames := #[],
    entries := #[(`ProofserveAuditCheckpoint, #[unsafeCast auditMeta])] }
  saveModuleData file mod data

/-- This input is exclusively the successful preceding original-kernel segment. -/
unsafe def restoreCheckpoint (mod : Name) : IO AuditState := do
  let parts ← moduleParts mod
  let some (data, _) := parts[0]? | throw <| IO.userError "empty checkpoint"
  let some entry := data.entries.find? (·.1 == `ProofserveAuditCheckpoint) |
    throw <| IO.userError "missing checkpoint metadata"
  unless entry.2.size == 1 do throw <| IO.userError "invalid checkpoint metadata"
  let some value := entry.2[0]? | throw <| IO.userError "missing checkpoint value"
  let auditMeta : CheckpointMeta := unsafeCast value
  let env ← importModules #[{ module := mod }] {} 0
  return {
    checked := env.toKernelEnv, regions := env.header.regions,
    visited := auditMeta.visited, imports := auditMeta.imports, origins := auditMeta.origins,
    segregated := auditMeta.segregated, modules := auditMeta.modules,
    constants := auditMeta.constants, skipped := auditMeta.skipped, fallbacks := auditMeta.fallbacks,
    ancestorMasks := auditMeta.ancestorMasks, moduleIndices := auditMeta.moduleIndices }

def maybeCheckpoint (s : AuditState) : IO Unit := do
  if let some file ← IO.getEnv "DECOUPLED_CHECKPOINT_OUTPUT" then
    let quota := ((← IO.getEnv "DECOUPLED_SEGMENT_MODULES").getD "500").toNat?.getD 500
    if s.modules - (← checkpointBase.get) >= quota then
      let name := ((← IO.getEnv "DECOUPLED_CHECKPOINT_MODULE").getD "VerifiedPrefix").toName
      let _ ← unsafe saveCheckpoint s file name
      event [("event", toJson "checkpoint"), ("modules", toJson s.modules),
        ("snapshot", toJson file)]
      checkpointDone.set true
      throw <| IO.userError "successful bounded checkpoint"

partial def visit (mode mutation : String) (mutateOnly : Option Name) (mod : Name) : AuditM Unit := do
  if (← get).visited.contains mod then return
  if (← get).pending.contains mod then throw <| IO.userError s!"cyclic import {mod}"
  modify fun s => { s with pending := s.pending.insert mod }
  let parts ← moduleParts mod
  let some (first, _) := parts[0]? | throw <| IO.userError "empty module"
  let some (data, _) := parts[parts.size - 1]? | throw <| IO.userError "empty module"
  modify fun s => { s with
    regions := s.regions ++ parts.map (·.2),
    imports := s.imports.insert mod (first.imports.map (·.module)) }
  for imp in first.imports do visit mode mutation mutateOnly imp.module
  let chosen := if mutateOnly == some mod then mutation else "none"
  let (map, skipped) := constantsOf data chosen
  let aliases := Id.run do
    let mut n := 0
    for name in data.constNames, ci in data.constants do
      if name != ci.name then n := n + 1
    return n
  event [("event", toJson "module_header"), ("module", toJson mod.toString),
    ("imports", toJson (first.imports.map (·.module.toString))),
    ("constants", toJson data.constants.size), ("aliased_constant_entries", toJson aliases)]
  let s ← get
  -- Every imported module has completed visit. Its cached ancestry plus its
  -- own bit equals its transitive import closure. No kernel replay is omitted.
  let mut visible : Nat := 0
  for imp in first.imports do
    let some index := s.moduleIndices[imp.module]? |
      throw <| IO.userError s!"unvisited import {imp.module}"
    visible := visible ||| (s.ancestorMasks[imp.module]?.getD 0) ||| (2 ^ index)
  let mut reason : Option String := none
  let mut separate := false
  let mut insertMap : Std.HashMap Name ConstantInfo := {}
  if mode == "audit" then
    for imported in s.segregated do
      if ((s.moduleIndices[imported]?).any (fun i => visible.testBit i)) then
        separate := true
        reason := some "segregated_dependency"
    for (_, ci) in map do
      unless ci.isUnsafe || ci.isPartial do
        if let some old := s.checked.find? ci.name then
          let origins := s.origins[ci.name]?.getD {}
          let mut imported := false
          for origin in origins do
            if ((s.moduleIndices[origin]?).any (fun i => visible.testBit i)) then imported := true
          if !sameConstant old ci then
            if sameTheoremInterface old ci then
              unless imported do reason := some s!"duplicate_proof_requires_native:{ci.name}"
            else
              separate := true
              reason := some s!"different_constant:{ci.name}"
        else insertMap := insertMap.insert ci.name ci
        for n in ci.getUsedConstantsAsSet do
          unless map.contains n do
            let origins := s.origins[n]?.getD {}
            let mut found := false
            for origin in origins do
              if ((s.moduleIndices[origin]?).any (fun i => visible.testBit i)) then found := true
            unless found do
              separate := true
              reason := some s!"unimported_reference:{ci.name}:{n}"
  else insertMap := map
  if let some why := reason then
    try
      let _ ← unsafe localReplay mod chosen
      event [("event", toJson "accept"), ("module", toJson mod.toString),
        ("context", toJson "module_local"), ("fallback_reason", toJson why)]
      if separate then
        modify fun s => { s with segregated := s.segregated.insert mod, fallbacks := s.fallbacks + 1 }
      else
        -- A locally checked duplicate theorem interface does not quarantine
        -- unrelated new declarations or all future dependent modules.
        let checked ← s.checked.replay insertMap
        let mut origins := s.origins
        for (name, ci) in map do
          unless ci.isUnsafe || ci.isPartial do
            origins := origins.insert name ((origins[name]?.getD {}).insert mod)
        modify fun s => { s with checked, origins, fallbacks := s.fallbacks + 1 }
    catch e =>
      event [("event", toJson "reject"), ("module", toJson mod.toString),
        ("context", toJson "module_local"), ("error", toJson e.toString),
        ("fallback_reason", toJson why)]
      throw e
  else
    try
      let checked ← s.checked.replay insertMap
      let mut origins := s.origins
      for (name, ci) in map do
        unless ci.isUnsafe || ci.isPartial do
          origins := origins.insert name ((origins[name]?.getD {}).insert mod)
      modify fun s => { s with checked, origins }
      event [("event", toJson "accept"), ("module", toJson mod.toString),
        ("context", toJson "shared"), ("constants", toJson data.constants.size),
        ("imports", toJson (first.imports.map (·.module.toString)))]
    catch e =>
      event [("event", toJson "reject"), ("module", toJson mod.toString),
        ("context", toJson "shared"), ("error", toJson e.toString)]
      throw e
  modify fun s => { s with
    ancestorMasks := s.ancestorMasks.insert mod visible,
    moduleIndices := s.moduleIndices.insert mod s.modules,
    pending := s.pending.erase mod, visited := s.visited.insert mod,
    modules := s.modules + 1, constants := s.constants + data.constants.size,
    skipped := s.skipped + skipped }
  let s ← get
  memorySnapshot s
  maybeCheckpoint s

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
    let initial ← if let some name ← IO.getEnv "DECOUPLED_CHECKPOINT_INPUT" then
        restoreCheckpoint name.toName
      else do
        let empty ← mkEmptyEnvironment
        pure ({ checked := empty.toKernelEnv } : AuditState)
    checkpointBase.set initial.modules
    checkpointNames.set (SMap.fold (fun names n _ => names.insert n) {} initial.checked.constants)
    try
      let (_, s) ← (do
        for mod in roots do visit mode mutation mutateOnly mod).run initial
      memorySnapshot s true
      let checkedCount : Nat := SMap.fold (fun n _ _ => n + 1) 0 s.checked.constants
      event [("event", toJson "complete"), ("mode", toJson mode), ("modules", toJson s.modules),
        ("unique_shared_kernel_declarations", toJson checkedCount),
        ("constants", toJson s.constants), ("skipped_unsafe_partial", toJson s.skipped),
        ("module_local_fallbacks", toJson s.fallbacks), ("retained_regions", toJson s.regions.size)]
    catch e =>
      unless ← checkpointDone.get do throw e
  return 0
