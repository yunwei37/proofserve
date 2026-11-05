/-
Module-local replay is adapted from Lean 4's LeanChecker.lean.
Copyright (c) 2023 Kim Morrison. All rights reserved.
Released under the Apache 2.0 license in the repository LICENSE.
Upstream authors: Kim Morrison, Sebastian Ullrich.

The checkpoint algorithm is the project-owned streaming reader, integrated with
original-kernel parallel checking.
-/
import ProofServe.Core
open ProofServe

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
  declaredAxioms : NameSet := {}
  localOnly : Bool := false
  skippedNames : NameSet := {}

abbrev AuditM := StateRefT AuditState IO

initialize eventHandle : IO.Ref (Option IO.FS.Handle) ← IO.mkRef none

def event (fields : List (String × Json)) : IO Unit := do
  let text := Json.compress (Json.mkObj fields)
  if let some handle ← eventHandle.get then
    handle.putStrLn text
    handle.flush
  else IO.println text

initialize nativeSensitive : IO.Ref (Std.HashMap Name NameSet) ← IO.mkRef {}
def nativePrimitive (n : Name) : Bool :=
  ["Lean.reduceBool","Lean.reduceNat","Lean.ofReduceBool","Lean.ofReduceNat"].any (·.toName == n)

/-- Open primitive applications are mentions, not executable closed reductions.
Closed calls remain a conservative unsupported case; arbitrary evaluation is
not decided by this syntactic check. -/
partial def onlyOpenNativeCalls (e : Expr) (sensitive : NameSet) (asFn := false) (asArg := false) : Bool :=
  match e with
  | .app f a =>
    let callOK := match e.getAppFn with
      | .const n _ =>
        if sensitive.contains n then
          if nativePrimitive n then (e.getAppArgs[0]?).all (fun x => x.consumeMData matches .bvar _)
          else e.getAppArgs.all (fun x => x.consumeMData matches .bvar _)
        else true
      | .lam .. => false
      | _ => true
    callOK && onlyOpenNativeCalls f sensitive true asArg && onlyOpenNativeCalls a sensitive false true
  | .forallE _ t b _ =>
    onlyOpenNativeCalls t sensitive && onlyOpenNativeCalls b sensitive
  | .lam _ t b _ =>
    !asArg && onlyOpenNativeCalls t sensitive && onlyOpenNativeCalls b sensitive
  | .letE .. => false
  | .const n _ => asFn || !sensitive.contains n
  | .mdata _ b | .proj _ _ b => onlyOpenNativeCalls b sensitive asFn asArg
  | _ => true

def checkNativeEvaluation (mod : Name) (data : ModuleData) : IO Unit := do
  let all ← nativeSensitive.get
  let mut tainted : NameSet := {}
  for name in ["Lean.reduceBool","Lean.reduceNat"] do tainted := tainted.insert name.toName
  for parent in data.imports do
    for name in (all[parent.module]?.getD {}).toList do tainted := tainted.insert name
  for ci in data.constants do
    unless nativePrimitive ci.name do tainted := tainted.erase ci.name
  let mut more := true
  while more do
    more := false
    for ci in data.constants do
      if !tainted.contains ci.name && ci.getUsedConstantsAsSet.toList.any tainted.contains then
        tainted := tainted.insert ci.name
        more := true
  nativeSensitive.set (all.insert mod tainted)
  for ci in data.constants do
    if ci.isUnsafe || ci.isPartial then continue
    if ci.getUsedConstantsAsSet.toList.any tainted.contains then
      unless onlyOpenNativeCalls ci.type tainted &&
          (ci.value? (allowOpaque := true)).all (fun value => onlyOpenNativeCalls value tainted) do
        throw <| IO.userError s!"unsupported native IR evaluation dependency (closed call): {ci.name}; official --fresh may also lack the required IR; use the project toolchain explicitly"

def artifactCandidates (file : System.FilePath) : Array System.FilePath :=
  #[file, OLeanLevel.server.adjustFileName file, OLeanLevel.private.adjustFileName file,
    file.withExtension "ir.sig", file.withExtension "ir"]

/-- The importer may enable quotient reduction for any nonempty import list.
A user-defined axiom carrying a reserved primitive name is not that primitive. -/
def validateQuotientMetadata (parts : Array (ModuleData × CompactedRegion)) : IO Unit := do
  let primitive := fun n => ["Quot","Quot.mk","Quot.lift","Quot.ind"].any (·.toName == n)
  let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "empty module"
  for name in data.constNames, ci in data.constants do
    if primitive name || primitive ci.name then
      unless (ci matches .quotInfo _) && name==ci.name do
        throw <| IO.userError s!"unsupported nonprimitive quotient metadata: {name}"

/-- Drop all ModuleData references before returning ownership of validation-only
regions. The noinline boundary keeps their lifetime separate from unmapping. -/
@[noinline] private def readValidationRegions (files : Array System.FilePath) :
    IO (Array CompactedRegion) := do
  return (← readModuleDataParts files).map (·.2)

/-- Validate IR without retaining its unused mapped data in the checking process. -/
def validateIRArtifacts (files : Array System.FilePath) : IO Unit := do
  let regions ← readValidationRegions files
  unsafe regions.reverse.forM CompactedRegion.free

def moduleParts (mod : Name) : IO (Array (ModuleData × CompactedRegion)) := do
  let file ← findOLean mod
  unless ← file.pathExists do throw <| IO.userError s!"missing module {mod}"
  let sig := file.withExtension "ir.sig"
  if ← sig.pathExists then
    validateIRArtifacts #[sig,file.withExtension "ir"]
  let exported ← readModuleDataParts #[file]
  let some (header,_) := exported[0]? | throw <| IO.userError "empty module"
  if !header.isModule then
    validateQuotientMetadata exported
    return exported
  let server := OLeanLevel.server.adjustFileName file
  let priv := OLeanLevel.private.adjustFileName file
  unless (← server.pathExists) && (← priv.pathExists) do
    throw <| IO.userError s!"module-system artifact requires server and private parts: {mod}"
  let parts ← readModuleDataParts #[file,server,priv]
  validateQuotientMetadata parts
  return parts

/-- Interface comparison; proof bodies needing validation use module-local replay. -/
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
            else if mutation == "unknown" then mkConst `ProofServeMissingConstant
            else if mutation == "sort" then mkSort (.succ .zero)
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


initialize certifiedNames : IO.Ref NameSet ← IO.mkRef {}
initialize checkpointSeedImports : IO.Ref (Array Import) ← IO.mkRef #[]

/-- Only the public coordinator can supply this local, input-validated cache.
The importer loads the real combined context; it does not establish proofs. -/
partial def cachedBoundary (roots : List Name) (allowed : NameSet)
    (seen : NameSet := {}) (boundary : NameSet := {}) : IO (NameSet × NameSet) := do
  match roots with
  | [] => return (seen,boundary)
  | mod :: rest =>
    if seen.contains mod then return ← cachedBoundary rest allowed seen boundary
    let seen := seen.insert mod
    if allowed.contains mod then
      return ← cachedBoundary rest allowed seen (boundary.insert mod)
    let parts ← moduleParts mod
    let some (first,_) := parts[0]? | throw <| IO.userError "empty module header"
    cachedBoundary ((first.imports.map (·.module)).toList ++ rest) allowed seen boundary

unsafe def certifiedBase (roots : List Name) (file : System.FilePath) : IO AuditState := do
  let cache ← IO.ofExcept (Json.parse (← IO.FS.readFile file))
  let names ← IO.ofExcept (cache.getObjValAs? (Array String) "modules")
  let allowed := names.foldl (fun (s : NameSet) n => s.insert n.toName) {}
  certifiedNames.set allowed
  let (_,boundary) ← cachedBoundary roots allowed
  if boundary.isEmpty then
    let env ← mkEmptyEnvironment
    return { checked := env.toKernelEnv }
  try
    let imports := boundary.toList.toArray.map (fun n => ({module:=n,importAll:=true} : Import))
    let env ← importModules imports {} 0
    let mut state : AuditState := { checked:=env.toKernelEnv,regions:=env.header.regions }
    for imp in env.header.modules, data in env.header.moduleData do
      if !imp.hasData then continue
      let mod := imp.module
      unless allowed.contains mod do
        throw <| IO.userError s!"uncertified module in imported cache context: {mod}"
      -- Identity qualification checked every part's import names against the
      -- exported header. Reuse the importer's resident data instead of loading
      -- a second compacted copy of every certified module.
      checkNativeEvaluation mod data
      let first := data
      let mut visible : Nat := 0
      for parent in first.imports do
        let some index := state.moduleIndices[parent.module]? |
          throw <| IO.userError s!"certified dependency not imported in order: {parent.module}"
        visible := visible ||| (state.ancestorMasks[parent.module]?.getD 0) ||| (2^index)
      let mut origins := state.origins
      let mut axioms := state.declaredAxioms
      for ci in data.constants do
        unless ci.isUnsafe || ci.isPartial do
          if let some loaded := state.checked.find? ci.name then
            unless sameConstant loaded ci do
              throw <| IO.userError s!"certified import constant differs: {ci.name}"
            origins := origins.insert ci.name ((origins[ci.name]?.getD {}).insert mod)
          if let .axiomInfo _ := ci then axioms := axioms.insert ci.name
      state := { state with
        visited := state.visited.insert mod
        imports := state.imports.insert mod (first.imports.map (·.module))
        ancestorMasks := state.ancestorMasks.insert mod visible
        moduleIndices := state.moduleIndices.insert mod state.modules
        modules := state.modules+1
        constants := state.constants+data.constants.size
        skipped := state.skipped+(data.constants.filter (fun ci => ci.isUnsafe || ci.isPartial)).size
        origins := origins
        skippedNames := data.constants.foldl (fun names ci =>
          if ci.isUnsafe || ci.isPartial then names.insert ci.name else names) state.skippedNames
        declaredAxioms := axioms }
    for imp in env.header.modules do
      if state.visited.contains imp.module then
        event [("event",toJson "trusted_import"),("module",toJson imp.module.toString),
          ("trust",toJson "input-validated local completed-module certificates")]
    checkpointSeedImports.set imports
    return state
  catch e =>
    -- Different independent contexts can conflict in their union. Check each
    -- new module in its original context, while reusing only certified imports.
    event [("event",toJson "certified_context_fallback"),("error",toJson e.toString)]
    let env ← mkEmptyEnvironment
    return {checked:=env.toKernelEnv,localOnly:=true}


def memorySnapshot (_ : AuditState) (_ : Bool := false) : IO Unit := pure ()

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
  declaredAxioms : NameSet
  localOnly : Bool
  nativeSensitive : Std.HashMap Name NameSet
  skippedNames : NameSet
  ancestorMasks : Std.HashMap Name Nat
  moduleIndices : Std.HashMap Name Nat

def axiomNames (env : Kernel.Environment) : Array String :=
  SMap.fold (fun acc name ci => match ci with
    | .axiomInfo _ => acc.push name.toString | _ => acc) #[] env.constants

initialize checkpointDone : IO.Ref Bool ← IO.mkRef false
initialize checkpointBase : IO.Ref Nat ← IO.mkRef 0
initialize checkpointNames : IO.Ref NameSet ← IO.mkRef {}

/-- Only constants already accepted by the original kernel are exported. -/
unsafe def saveCheckpoint (s : AuditState) (file : System.FilePath) (mod : Name) : IO Unit := do
  let oldNames ← checkpointNames.get
  let constants : Array ConstantInfo :=
    SMap.fold (fun acc name ci => if oldNames.contains name then acc else acc.push ci) #[] s.checked.constants
  let imports ← match ← IO.getEnv "DECOUPLED_CHECKPOINT_INPUT" with
    | some name => pure #[({ module := name.toName } : Import)]
    | none => checkpointSeedImports.get
  let auditMeta : CheckpointMeta := {
    visited := s.visited, imports := s.imports, origins := s.origins,
    segregated := s.segregated, modules := s.modules, constants := s.constants,
    skipped := s.skipped, fallbacks := s.fallbacks, declaredAxioms := s.declaredAxioms,
    ancestorMasks := s.ancestorMasks, moduleIndices := s.moduleIndices, localOnly := s.localOnly, skippedNames := s.skippedNames, nativeSensitive := ← nativeSensitive.get }
  let data : ModuleData := {
    isModule := false, imports, constNames := constants.map (·.name),
    constants, extraConstNames := #[],
    entries := #[(`ProofserveAuditCheckpoint, #[unsafeCast auditMeta])] }
  saveModuleData file mod data

/-- This input is exclusively the successful preceding original-kernel segment. -/
unsafe def restoreCheckpoint (mod : Name) : IO AuditState := do
  let some directory ← IO.getEnv "PROOFSERVE_CHECKPOINT_DIR" |
    throw <| IO.userError "missing checkpoint directory"
  let snapshotStem := (← IO.getEnv "PROOFSERVE_SNAPSHOT_PREFIX").getD "ProofServeSegment"
  let some index := (mod.toString.drop snapshotStem.length).toString.toNat? |
    throw <| IO.userError "invalid checkpoint name"
  let mut artifacts : NameMap ImportArtifacts := {}
  for i in [:index+1] do
    let name := s!"{snapshotStem}{i}".toName
    artifacts := artifacts.insert name (.ofArrays #[#[System.FilePath.mk directory/s!"{snapshotStem}{i}.olean"]])
  let file := System.FilePath.mk directory/s!"{mod}.olean"
  let parts ← readModuleDataParts #[file]
  let some (data, _) := parts[0]? | throw <| IO.userError "empty checkpoint"
  let some entry := data.entries.find? (·.1 == `ProofserveAuditCheckpoint) |
    throw <| IO.userError "missing checkpoint metadata"
  unless entry.2.size == 1 do throw <| IO.userError "invalid checkpoint metadata"
  let some value := entry.2[0]? | throw <| IO.userError "missing checkpoint value"
  let auditMeta : CheckpointMeta := unsafeCast value
  nativeSensitive.set auditMeta.nativeSensitive
  let mut imports : Array Import := #[{ module := mod }]
  if !auditMeta.localOnly then
    if let some cache ← IO.getEnv "PROOFSERVE_VALIDATED_MODULE_CACHE" then
      -- Older successful segments did not serialize their imported certified
      -- base. Recover it only from the coordinator's byte-validated cache.
      let cache ← IO.ofExcept (Json.parse (← IO.FS.readFile cache))
      let modules ← IO.ofExcept (cache.getObjValAs? (Array String) "modules")
      imports := imports ++ modules.map (fun n => ({module:=n.toName,importAll:=true} : Import))
  let env ← importModules imports {} 0 (arts := artifacts)
  return {
    checked := env.toKernelEnv, regions := env.header.regions,
    visited := auditMeta.visited, imports := auditMeta.imports, origins := auditMeta.origins,
    segregated := auditMeta.segregated, modules := auditMeta.modules,
    constants := auditMeta.constants, skipped := auditMeta.skipped, fallbacks := auditMeta.fallbacks, declaredAxioms := auditMeta.declaredAxioms,
    ancestorMasks := auditMeta.ancestorMasks, moduleIndices := auditMeta.moduleIndices, localOnly := auditMeta.localOnly, skippedNames := auditMeta.skippedNames }

def maybeCheckpoint (s : AuditState) : IO Unit := do
  if let some file ← IO.getEnv "DECOUPLED_CHECKPOINT_OUTPUT" then
    let quota := ((← IO.getEnv "DECOUPLED_SEGMENT_MODULES").getD "500").toNat?.getD 500
    if s.modules - (← checkpointBase.get) >= quota then
      let name := ((← IO.getEnv "DECOUPLED_CHECKPOINT_MODULE").getD "VerifiedPrefix").toName
      let _ ← unsafe saveCheckpoint s file name
      event [("event", toJson "checkpoint"), ("modules", toJson s.modules),
        ("snapshot", toJson file),("axioms",toJson (axiomNames s.checked ++ s.declaredAxioms.toList.toArray.map Name.toString))]
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
  checkNativeEvaluation mod data
  let (map, skipped) := constantsOf data chosen
  let aliases := Id.run do
    let mut n := 0
    for name in data.constNames, ci in data.constants do
      if name != ci.name then n := n + 1
    return n
  event [("event", toJson "module_header"), ("module", toJson mod.toString),
    ("imports", toJson (first.imports.map (·.module.toString))),
    ("constants", toJson data.constants.size),
    ("safe_constants",toJson (map.toList.filter (fun (_,ci) => !ci.isUnsafe && !ci.isPartial)).length),
    ("aliased_constant_entries", toJson aliases)]
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
  if aliases>0 then
    separate := true
    reason := some "aliased_constant_entry"
  if mode == "audit" && !s.localOnly then
    for imported in s.segregated do
      if ((s.moduleIndices[imported]?).any (fun i => visible.testBit i)) then
        separate := true
        reason := some "segregated_dependency"
    for (_, ci) in map do
      if s.skippedNames.contains ci.name ||
          ((ci.isUnsafe || ci.isPartial) && (s.checked.find? ci.name).isSome) then
        separate := true
        reason := some s!"skipped_constant_conflict:{ci.name}"
      unless ci.isUnsafe || ci.isPartial do
        if let some old := s.checked.find? ci.name then
          let origins := s.origins[ci.name]?.getD {}
          let mut imported := false
          for origin in origins do
            if ((s.moduleIndices[origin]?).any (fun i => visible.testBit i)) then imported := true
          if sameTheoremInterface old ci then
            -- A repeated theorem is validated in its declared context, even
            -- when the earlier matching interface came from another root.
            -- This does not waive duplicate definition/axiom import checks.
            if !sameConstant old ci then
              separate := true
              reason := some s!"different_theorem_body:{ci.name}"
            else if !imported then
              reason := some s!"duplicate_proof_requires_native:{ci.name}"
          else
            separate := true
            reason := some s!"different_constant:{ci.name}"
        else insertMap := insertMap.insert ci.name ci
        for n in ci.getUsedConstantsAsSet do
          unless (map[n]?).any (fun own => own.name==n && !own.isUnsafe && !own.isPartial) do
            let origins := s.origins[n]?.getD {}
            let mut found := false
            for origin in origins do
              if ((s.moduleIndices[origin]?).any (fun i => visible.testBit i)) then found := true
            unless found do
              separate := true
              reason := some s!"unimported_reference:{ci.name}:{n}"
  else insertMap := map
  if s.localOnly then
    let cached := (← certifiedNames.get).contains mod
    try
      unless cached do
        let _ ← unsafe localReplay mod chosen
      event [("event",toJson (if cached then "trusted_import" else "accept")),
        ("module",toJson mod.toString),("context",toJson "module_local_certified")]
      let mut axioms := s.declaredAxioms
      for ci in data.constants do
        if let .axiomInfo _ := ci then axioms := axioms.insert ci.name
      modify fun s => {s with declaredAxioms:=axioms, fallbacks:=s.fallbacks+(if cached then 0 else 1)}
    catch e =>
      event [("event",toJson "reject"),("module",toJson mod.toString),("error",toJson e.toString)]
      throw e
  else if let some why := reason then
    try
      let _ ← unsafe localReplay mod chosen
      if separate then
        modify fun s => { s with segregated := s.segregated.insert mod, fallbacks := s.fallbacks + 1 }
      else
        -- A locally checked duplicate theorem interface does not quarantine
        -- unrelated new declarations or all future dependent modules.
        try
          let checked ← parallelReplay data insertMap s.checked ((← IO.getEnv "PROOFSERVE_WORKERS").getD "4" |>.toNat?.getD 4)
          let mut origins := s.origins
          for (name, ci) in map do
            unless ci.isUnsafe || ci.isPartial do
              origins := origins.insert name ((origins[name]?.getD {}).insert mod)
          modify fun s => { s with checked, origins, fallbacks := s.fallbacks + 1 }
        catch _ =>
          -- Local replay already succeeded. A combined-frontier failure is
          -- not evidence that the module's declared context is invalid.
          modify fun s => { s with segregated := s.segregated.insert mod, fallbacks := s.fallbacks + 1 }
      event [("event", toJson "accept"), ("module", toJson mod.toString),
        ("context", toJson "module_local"), ("fallback_reason", toJson why)]
    catch e =>
      event [("event", toJson "reject"), ("module", toJson mod.toString),
        ("context", toJson "module_local"), ("error", toJson e.toString),
        ("fallback_reason", toJson why)]
      throw e
  else
    try
      let checked ← parallelReplay data insertMap s.checked ((← IO.getEnv "PROOFSERVE_WORKERS").getD "4" |>.toNat?.getD 4)
      let mut origins := s.origins
      for (name, ci) in map do
        unless ci.isUnsafe || ci.isPartial do
          origins := origins.insert name ((origins[name]?.getD {}).insert mod)
      modify fun s => { s with checked, origins }
      event [("event", toJson "accept"), ("module", toJson mod.toString),
        ("context", toJson "shared"), ("constants", toJson data.constants.size),
        ("frontier_insert_candidates",toJson insertMap.size),
        ("imports", toJson (first.imports.map (·.module.toString)))]
    catch sharedError =>
      try
        let _ ← unsafe localReplay mod chosen
        modify fun s => { s with segregated := s.segregated.insert mod, fallbacks := s.fallbacks + 1 }
        event [("event", toJson "accept"), ("module", toJson mod.toString),
          ("context", toJson "module_local"), ("fallback_reason",toJson "shared_kernel_context_failure"),
          ("shared_error",toJson sharedError.toString)]
      catch e =>
        event [("event", toJson "reject"), ("module", toJson mod.toString),
          ("context", toJson "module_local"), ("error", toJson e.toString)]
        throw e
  let declared := data.constants.foldl (fun names ci =>
    if ci matches .axiomInfo _ then names.insert ci.name else names) (← get).declaredAxioms
  modify fun s => { s with
    declaredAxioms := declared,
    skippedNames := data.constants.foldl (fun names ci =>
      if ci.isUnsafe || ci.isPartial then names.insert ci.name else names) s.skippedNames,
    ancestorMasks := s.ancestorMasks.insert mod visible,
    moduleIndices := s.moduleIndices.insert mod s.modules,
    pending := s.pending.erase mod, visited := s.visited.insert mod,
    modules := s.modules + 1, constants := s.constants + data.constants.size,
    skipped := s.skipped + skipped }
  let s ← get
  memorySnapshot s
  maybeCheckpoint s

unsafe def runSegment (args : List String) : IO UInt32 := do
  let mode :: mutation :: rawRoots := args |
    throw <| IO.userError "usage: audited-stream (audit|naive|one) (none|bvar|sibling) MODULE|@ROOTFILE..."
  unless ["audit","naive","one"].contains mode do throw <| IO.userError "invalid mode"
  unless ["none","bvar","sibling","unknown","sort"].contains mutation do throw <| IO.userError "invalid mutation"
  if let some path ← IO.getEnv "PROOFSERVE_EVENT_LOG" then
    eventHandle.set (some (← IO.FS.Handle.mk path .append))
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
  if let some file ← IO.getEnv "PROOFSERVE_VALIDATED_MODULE_CACHE" then
    let cache ← IO.ofExcept (Json.parse (← IO.FS.readFile file))
    let names ← IO.ofExcept (cache.getObjValAs? (Array String) "modules")
    certifiedNames.set (names.foldl (fun (s : NameSet) n => s.insert n.toName) {})
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
      else if let some cache ← IO.getEnv "PROOFSERVE_VALIDATED_MODULE_CACHE" then
        certifiedBase roots cache
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
        ("module_local_fallbacks", toJson s.fallbacks), ("retained_regions", toJson s.regions.size),("axioms",toJson (axiomNames s.checked ++ s.declaredAxioms.toList.toArray.map Name.toString))]
    catch e =>
      unless ← checkpointDone.get do throw e
  return 0
