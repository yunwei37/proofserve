import ParallelCore

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
  chunkBundle : Array ChunkBundle := #[]

abbrev AuditM := StateRefT AuditState IO

def event (fields : List (String × Json)) : IO Unit := do
  IO.println (Json.compress (Json.mkObj fields))
  (← IO.getStdout).flush

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

/-- A duplicate must not hide a cycle through a new local helper. Shared
previous bindings can otherwise make an invalid isolated module look valid. -/
partial def reachesLocal (map : Std.HashMap Name ConstantInfo) (target : Name)
    (todo : List Name) (seen : NameSet := {}) : Bool :=
  match todo with
  | [] => false
  | n::rest =>
    if n == target then true
    else if seen.contains n then reachesLocal map target rest seen
    else match map[n]? with
    | none => reachesLocal map target rest (seen.insert n)
    | some ci => reachesLocal map target (ci.getUsedConstantsAsSet.toList ++ rest) (seen.insert n)

partial def closure (graph : Std.HashMap Name (Array Name)) (todo : List Name)
    (seen : NameSet := {}) : NameSet :=
  match todo with
  | [] => seen
  | m :: rest =>
    if seen.contains m then closure graph rest seen
    else closure graph ((graph[m]?.getD #[]).toList ++ rest) (seen.insert m)

def constantsOf (data : ModuleData) (mutation : String) (target : Option Name := none) :
    Std.HashMap Name ConstantInfo × Nat :=
  Id.run do
    let mut map : Std.HashMap Name ConstantInfo := {}
    let mut skipped := 0
    let mut changed := false
    for ci in data.constants do
      if ci.isUnsafe || ci.isPartial then skipped := skipped + 1
      let mut ci := ci
      if mutation != "none" && !changed && (target.isNone || target == some ci.name) then
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
  let target := (← IO.getEnv "DECOUPLED_MUTATE_CONSTANT").map String.toName
  let (map, _) := constantsOf data mutation target
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

/-- Read a prepared untrusted certificate payload without importing any proof.
Each helper/chunk is rechecked in the streaming frontier before use. -/
def pathParts (path : System.FilePath) : IO (Array (ModuleData × CompactedRegion)) := do
  let mut files := #[path]
  for level in [OLeanLevel.server,OLeanLevel.private] do
    let other := level.adjustFileName path
    if ← other.pathExists then files := files.push other
  readModuleDataParts files

def loadSingleBundle (root : System.FilePath) (k : Nat) : IO (Array ChunkBundle × Array CompactedRegion) := do
  unless [1,2,4,8].contains k do throw <| IO.userError "unsupported chunk k"
  let referenceParts ← pathParts (root / "reference.olean")
  let some (referenceData,_) := referenceParts[referenceParts.size-1]? | throw <| IO.userError "empty reference"
  let target := `OAI.AtomicTriangular.FiniteCertificate.envelopeExpB16_calc._proof_1_1
  let some reference := referenceData.constants.find? (·.name == target) |
    throw <| IO.userError "prepared target missing"
  let supportParts ← pathParts (root / "EnvelopeBase.olean")
  let some (supportData,_) := supportParts[supportParts.size-1]? | throw <| IO.userError "empty support"
  let mut support := {}
  for ci in supportData.constants do
    if ci.isUnsafe || ci.isPartial || ci.getUsedConstantsAsSet.contains `sorryAx then
      throw <| IO.userError "unsupported certificate support"
    if let .axiomInfo _ := ci then throw <| IO.userError "certificate adds an axiom"
    support := support.insert ci.name ci
  let mut regions := (referenceParts ++ supportParts).map (·.2)
  let mut children := #[]
  for i in [:k] do
    let parts ← pathParts (root / s!"EnvelopeK{k}Part{i}.olean")
    regions := regions ++ parts.map (·.2)
    let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "empty child"
    let name := Name.str (Name.mkSimple s!"EnvelopeK{k}Part{i}") "proof"
    let some ci := data.constants.find? (·.name == name) |
      throw <| IO.userError "prepared child missing"
    if ci.getUsedConstantsAsSet.contains `sorryAx then throw <| IO.userError "sorry in chunk"
    let ci := if (← IO.getEnv "PARALLEL_CHUNK_FAULT") == some "bvar" && i==0 then
      match ci with | .thmInfo t => .thmInfo {t with value:=Expr.bvar 0} | _ => ci
      else ci
    children := children.push ci
  return (#[{reference,support,children,k,mergeName:=Name.str `MEnvelopeBase s!"merge_{k}"}],regions)

/-- Only transitive support actually read by this target/k is installed. -/
partial def supportClosure (available : Std.HashMap Name ConstantInfo) (todo : List Name)
    (seen : NameSet := {}) (selected : Std.HashMap Name ConstantInfo := {}) :
    Std.HashMap Name ConstantInfo :=
  match todo with
  | [] => selected
  | n::rest =>
    if seen.contains n then supportClosure available rest seen selected
    else match available[n]? with
    | none => supportClosure available rest (seen.insert n) selected
    | some ci => supportClosure available (ci.getUsedConstantsAsSet.toList ++ rest)
        (seen.insert n) (selected.insert n ci)

def loadBundle (root : System.FilePath) (k : Nat) : IO (Array ChunkBundle × Array CompactedRegion) := do
  unless [1,2,4,8].contains k do throw <| IO.userError "unsupported chunk k"
  unless ← (root / "schemas.json").pathExists do return ← loadSingleBundle root k
  let json ← match Json.parse (← IO.FS.readFile (root / "schemas.json")) with
    | .ok j => pure j
    | .error e => throw <| IO.userError e
  let .ok specs := json.getObjValAs? (Array Json) "specs" | throw <| IO.userError "missing schemas"
  let referenceParts ← pathParts (root / "reference.olean")
  let some (referenceData,_) := referenceParts[referenceParts.size-1]? | throw <| IO.userError "empty reference"
  let supportParts ← pathParts (root / "EnvelopeStreamBase.olean")
  let some (supportData,_) := supportParts[supportParts.size-1]? | throw <| IO.userError "empty support"
  let mut available := {}
  for ci in supportData.constants do
    if ci.isUnsafe || ci.isPartial || ci.getUsedConstantsAsSet.contains `sorryAx then
      throw <| IO.userError "unsupported certificate support"
    if let .axiomInfo _ := ci then throw <| IO.userError "certificate adds an axiom"
    available := available.insert ci.name ci
  let mut regions := (referenceParts ++ supportParts).map (·.2)
  let mut bundles := #[]
  for spec in specs do
    let .ok ident := spec.getObjValAs? String "id" | throw <| IO.userError "missing schema ID"
    let .ok target := spec.getObjValAs? String "original_name" | throw <| IO.userError "missing target name"
    let some reference := referenceData.constants.find? (·.name == target.toName) |
      throw <| IO.userError "profiled original missing"
    let childParts ← pathParts (root / s!"chunks_{ident}_{k}.olean")
    regions := regions ++ childParts.map (·.2)
    let some (childData,_) := childParts[childParts.size-1]? | throw <| IO.userError "empty chunks"
    let mut children := childData.constants
    unless children.size==k do throw <| IO.userError "wrong chunk count"
    for ci in children do
      if ci.getUsedConstantsAsSet.contains `sorryAx then throw <| IO.userError "sorry in chunk"
      unless ci matches .thmInfo _ do throw <| IO.userError "non-theorem chunk"
    if (← IO.getEnv "PARALLEL_CHUNK_FAULT") == some "bvar" then
      children := children.map fun ci => match ci with
        | .thmInfo t => .thmInfo {t with value:=Expr.bvar 0} | _ => ci
    let mergeName := Name.str `MEnvelopeStream s!"merge_{ident}_{k}"
    let seeds := mergeName :: (children.toList.flatMap (·.getUsedConstantsAsSet.toList))
    let support := supportClosure available seeds
    bundles := bundles.push {reference,support,children,mergeName,k}
  return (bundles,regions)

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
  let target := (← IO.getEnv "DECOUPLED_MUTATE_CONSTANT").map String.toName
  let (map, skipped) := constantsOf data chosen target
  event [("event", toJson "module_header"), ("module", toJson mod.toString),
    ("imports", toJson (first.imports.map (·.module.toString))),
    ("constants", toJson data.constants.size)]
  let s ← get
  let visibleNames := closure s.imports (first.imports.map (·.module)).toList
  let visibleSet := visibleNames.toList
  let mut reason : Option String := none
  let mut insertMap : Std.HashMap Name ConstantInfo := {}
  let mut duplicateProofs : Array ConstantInfo := #[]
  if mode == "audit" || mode == "parallel" then
    for imported in visibleSet do
      if s.segregated.contains imported then reason := some "segregated_dependency"
    for (_, ci) in map do
      unless ci.isUnsafe || ci.isPartial do
        if let some old := s.checked.find? ci.name then
          if !sameConstant old ci then
            match old,ci with
            | .thmInfo a,.thmInfo b =>
              if a.type == b.type && a.levelParams == b.levelParams && a.all == b.all &&
                  !reachesLocal map ci.name ci.getUsedConstantsAsSet.toList then
                duplicateProofs := duplicateProofs.push ci
              else reason := some s!"different_constant:{ci.name}"
            | _,_ => reason := some s!"different_constant:{ci.name}"
        else insertMap := insertMap.insert ci.name ci
        for n in ci.getUsedConstantsAsSet do
          unless map.contains n do
            let origins := s.origins[n]?.getD {}
            let mut found := false
            for origin in origins do
              if visibleNames.contains origin then found := true
            unless found do reason := some s!"unimported_reference:{ci.name}:{n}"
  else insertMap := map
  if let some why := reason then
    try
      let _ ← unsafe localReplay mod chosen
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
      let workers := ((← IO.getEnv "PARALLEL_WORKERS").getD "1").toNat?.getD 1
      let fault := (← IO.getEnv "PARALLEL_FAULT").getD "none"
      let before ← IO.monoNanosNow
      let curveModules := ((← IO.getEnv "PARALLEL_CURVE_MODULES").getD "").splitOn ","
      let mut selected : Option Kernel.Environment := none
      if curveModules.contains mod.toString then
        let bundleRoot ← IO.getEnv "PARALLEL_CHUNK_ASSETS_CURVE"
        let mut oracle : Option Kernel.Environment := none
        let kinds := if bundleRoot.isSome && mod.toString.endsWith "EnvelopePsiB" then
          ["serial","parallel1","parallel2","parallel4","parallel8","chunk1","chunk2","chunk4","chunk8"]
          else ["serial","parallel1","parallel2","parallel4","parallel8"]
        for kind in kinds do
          let n := (kind.toList.filter Char.isDigit |> String.ofList).toNat?.getD 1
          let t0 ← IO.monoNanosNow
          let c0 ← processNs
          let (chunkBundle,retained) ← if kind.startsWith "chunk" then do
            let some root := bundleRoot | throw <| IO.userError "missing curve assets"
            let (b,rs) ← loadBundle root n
            pure (b,rs)
            else pure (#[],#[])
          let (trial,waveCount,jobCount,route) ← if kind == "serial" then do
            let env ← s.checked.replay insertMap
            pure (env,0,0,"serial")
            else parallelReplay data insertMap s.checked n "none" chunkBundle
          if let some reference := oracle then
            for (_,ci) in insertMap do
              let some expected := reference.find? ci.name | throw <| IO.userError "serial result missing constant"
              let some actual := trial.find? ci.name | throw <| IO.userError "parallel result missing constant"
              let rewritten := chunkBundle.any (fun b => sameConstant ci b.reference)
              unless sameConstant expected actual ||
                  (rewritten && expected.name==actual.name && expected.type==actual.type &&
                    expected.levelParams==actual.levelParams) do
                throw <| IO.userError s!"curve result mismatch: {ci.name}"
          else oracle := some trial
          let c1 ← processNs
          let t1 ← IO.monoNanosNow
          event [("event",toJson "curve_cell"),("module",toJson mod.toString),("kind",toJson kind),
            ("workers",toJson n),("elapsed_ns",toJson (t1-t0)),("cpu_ns",toJson (c1-c0)),
            ("waves",toJson waveCount),("jobs",toJson jobCount),("route",toJson route),
            ("retained_certificate_regions",toJson retained.size),("accept",toJson true)]
          -- Region lifetime extends through the entire stream: a committed proof can
          -- reference the prepared payload's compacted objects.
          modify fun state => {state with regions:=state.regions ++ retained}
          selected := some trial
      let result : IO (Kernel.Environment × Nat × Nat × String) := if let some chosen := selected then
        pure (chosen,0,0,"curve_selected")
        else if mode == "parallel" then
        parallelReplay data insertMap s.checked workers fault s.chunkBundle
        else do
          let checked ← s.checked.replay insertMap
          pure (checked,0,0,"serial")
      let (checked,waves,jobs,path) ← result
      for h : i in [:duplicateProofs.size] do
        validateDuplicate checked duplicateProofs[i] (Name.num (Name.num `_proofserveDuplicate s.modules) i)
      event [("event",toJson "kernel_work"),("module",toJson mod.toString),
        ("waves",toJson waves),("jobs",toJson jobs),("path",toJson path),
        ("elapsed_ns",toJson ((← IO.monoNanosNow)-before))]
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
  modify fun s => { s with
    pending := s.pending.erase mod, visited := s.visited.insert mod,
    modules := s.modules + 1, constants := s.constants + data.constants.size,
    skipped := s.skipped + skipped }
  let s ← get
  memorySnapshot s.modules s.constants

unsafe def main (args : List String) : IO UInt32 := do
  let mode :: mutation :: rawRoots := args |
    throw <| IO.userError "usage: audited-stream (audit|naive|one) (none|bvar|sibling) MODULE|@ROOTFILE..."
  unless ["audit","naive","one","parallel"].contains mode do throw <| IO.userError "invalid mode"
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
    let (bundle,regions) ← match ← IO.getEnv "PARALLEL_CHUNK_ASSETS" with
      | none => pure (#[],#[])
      | some root => do
        let k := ((← IO.getEnv "PARALLEL_WORKERS").getD "1").toNat?.getD 1
        let (bundle,regions) ← loadBundle root k
        pure (bundle,regions)
    let (_, s) ← (do
      for mod in roots do visit mode mutation mutateOnly mod).run { checked := empty.toKernelEnv,chunkBundle:=bundle,regions }
    event [("event", toJson "complete"), ("mode", toJson mode), ("modules", toJson s.modules),
      ("constants", toJson s.constants), ("skipped_unsafe_partial", toJson s.skipped),
      ("module_local_fallbacks", toJson s.fallbacks), ("retained_regions", toJson s.regions.size)]
  return 0
