import ProofServe.ModulePlan
open Lean ProofServe

@[extern "ps_checkpoint_lock"] opaque checkpointLock (path : @& String) : IO Unit

structure CheckOptions where
  project : System.FilePath := "."
  workers : Nat := 0
  directory : System.FilePath := ".proofserve"
  quota : Nat := 500
  maxSegments : Nat := 0
  roots : Array String := #[]
  rootFile : Option System.FilePath := none
  persist : Bool := true
  split : Bool := true
  strictTheoremBodies : Bool := false
  official : Bool := false
  closureRoots : Nat := 500
  reuseImports : Bool := true
  moduleCache : Option System.FilePath := none

def theoremBodyPolicy (o : CheckOptions) : String :=
  if o.strictTheoremBodies then "strict" else "shared-checked"

partial def parseOptions (args : List String) (o : CheckOptions := {}) : Except String CheckOptions :=
  match args with
  | [] => .ok o
  | "--replay-shared-imports"::xs => parseOptions xs {o with reuseImports:=false}
  | "--trusted-module-cache"::f::xs => parseOptions xs {o with moduleCache:=some f}
  | "--closure-roots"::n::xs => do
    let some k := n.toNat? | throw "invalid closure batch size"
    parseOptions xs {o with closureRoots:=k}
  | "--workers"::n::xs => do
    let some k := n.toNat? | throw "invalid workers"
    if k==0 then throw "workers must be positive"
    parseOptions xs {o with workers:=k}
  | "--max-segments"::n::xs => do
    let some k := n.toNat? | throw "invalid max segments"
    parseOptions xs {o with maxSegments:=k}
  | "--checkpoint-dir"::d::xs => parseOptions xs {o with directory:=d}
  | "--segment-modules"::n::xs => do
    let some k := n.toNat? | throw "invalid segment size"
    if k==0 then throw "segment size must be positive"
    parseOptions xs {o with quota:=k}
  | "--root"::m::xs => parseOptions xs {o with roots:=o.roots.push m}
  | "--root-file"::f::xs => parseOptions xs {o with rootFile:=some f}
  | "--no-persistence"::xs => parseOptions xs {o with persist:=false}
  | "--no-split-fallback"::xs => parseOptions xs {o with split:=false}
  | "--strict-theorem-bodies"::xs => parseOptions xs {o with strictTheoremBodies:=true}
  | "--official"::xs => parseOptions xs {o with official:=true}
  | "--json"::xs => parseOptions xs o
  | x::xs =>
    if x.startsWith "-" then .error s!"unknown option {x}"
    else parseOptions xs {o with project:=x}


/-- A root manifest avoids OS argument limits for large compiled libraries. -/
def requestedRoots (o : CheckOptions) : IO (Array String) := do
  let fromFile ← match o.rootFile with
    | none => pure #[]
    | some file => do
      let text ← IO.FS.readFile file
      let names := (text.splitOn "\n").filterMap (fun line =>
        let name := line.trimAscii.toString
        if name.isEmpty then none else some name) |>.toArray
      unless !names.isEmpty do
        throw <| IO.userError "root-file contains no module names"
      pure names
  return o.roots ++ fromFile

@[extern "ps_write_atomic"] opaque writeAtomic (path content : @& String) : IO Unit

def writeAtomicFile (file : System.FilePath) (value : String) : IO Unit :=
  writeAtomic file.toString value

def writeJson (file : System.FilePath) (value : Json) : IO Unit :=
  writeAtomicFile file (value.pretty++"\n")

initialize binaryIdentity : IO.Ref (Option UInt64) ← IO.mkRef none
def executableHash : IO UInt64 := do
  if let some value ← binaryIdentity.get then return value
  let value := hash (← IO.FS.readBinFile (← IO.appPath))
  binaryIdentity.set (some value)
  return value

def projectDirty (project directory : System.FilePath) : IO Json := do
  let r ← IO.Process.output {cmd:="git",args:=#["-c","status.relativePaths=true",
    "status","--porcelain","-z","--untracked-files=all"],cwd:=some project}
  if r.exitCode != 0 then return Json.null
  let state ← IO.FS.realPath directory
  let statePrefix := state.toString++"/"
  let dirty := (r.stdout.splitOn (String.singleton (Char.ofNat 0))).any fun entry =>
    if entry.isEmpty then false
    else if entry.startsWith "?? " && state != project then
      !((project/(entry.drop 3).toString).toString.startsWith statePrefix)
    else true
  return toJson dirty

partial def discover (root : System.FilePath) (path : System.FilePath) : IO (Array String) := do
  let mut out := #[]
  for d in ← path.readDir do
    if ← d.path.isDir then out := out ++ (← discover root d.path)
    else if d.path.extension == some "olean" then
      let rel := (d.path.toString.drop (root.toString.length+1)).toString
      if !rel.endsWith ".server.olean" && !rel.endsWith ".private.olean" then
        let name := ((rel.dropEnd 6).toString.splitOn "/").foldl Name.str .anonymous
        out := out.push name.toString
  return out

def objectEvents (text : String) : Array Json :=
  text.splitOn "\n" |>.filterMap (fun s => (Json.parse s).toOption) |>.toArray

def fieldString (j : Json) (key : String) : String :=
  (j.getObjValAs? String key).toOption.getD ""

partial def inputIdentity (mod : Name) (seen : NameSet := {}) :
    IO (NameSet × Array (String × UInt64)) := do
  if seen.contains mod then return (seen,#[])
  let parts ← moduleParts mod
  let some (first,_) := parts[0]? | throw <| IO.userError "empty module"
  let imports := first.imports.map (·.module)
  for (data,_) in parts do
    unless data.imports.map (·.module)==imports do
      throw <| IO.userError s!"unsupported module-part import layout: {mod}"
  let mut seen := seen.insert mod
  let mut files := #[]
  let file ← findOLean mod
  for f in artifactCandidates file do
    if ← f.pathExists then files := files.push (f.toString,hash (← IO.FS.readBinFile f))
  for imp in first.imports do
    let (next,more) ← inputIdentity imp.module seen
    seen := next
    files := files ++ more
  return (seen,files)

/-- Isolate compacted-region lifetime: identity scanning finishes before any
kernel replay process is started. The traversal and byte hashes are unchanged. -/
def runInputIdentity (args : List String) : IO UInt32 := do
  let [file] := args | throw <| IO.userError "input identity arguments"
  initSearchPath (← findSysroot)
  let some paths ← IO.getEnv "LEAN_PATH" | throw <| IO.userError "input identity search path"
  searchPathRef.set ((paths.splitOn ":").map System.FilePath.mk)
  let text ← IO.FS.readFile file
  let roots := (text.splitOn "\n").filterMap (fun line =>
    let line := line.trimAscii.toString
    if line.isEmpty then none else some line)
  let mut seen : NameSet := {}
  let mut inputs : Array (String × UInt64) := #[]
  for root in roots do
    let (next,more) ← inputIdentity root.toName seen
    seen := next
    inputs := inputs ++ more
  IO.println (Json.mkObj [
    ("modules",toJson (seen.toList.map Name.toString)),
    ("inputs",toJson inputs)]).compress
  return 0


/-- Resolve the current project afresh, including optional module-part inventory. -/
def currentInputMetadata (project dir : System.FilePath) (roots : Array String)
    (paths : List String) : IO Json := do
  let rootFile := dir/"input-identity-roots.txt"
  writeAtomicFile rootFile (String.intercalate "\n" roots.toList)
  let result ← IO.Process.output {
    cmd:=(← IO.appPath).toString,args:=#["--internal-input-identity",rootFile.toString],
    cwd:=some project,env:=[("LEAN_PATH",some (String.intercalate ":" paths))].toArray}
  writeAtomicFile (dir/"input-identity.stdout") result.stdout
  writeAtomicFile (dir/"input-identity.stderr") result.stderr
  unless result.exitCode==0 do
    throw <| IO.userError s!"input identity scan failed: {result.stderr}"
  IO.ofExcept (Json.parse result.stdout)

/-- A completed receipt is valid only in the same project and checker ABI. -/
def validateCertificateContext (identity receipt : Json) (project : System.FilePath)
    (roots : Array String) (paths : List String) (version : String)
    (manifest : Json) (o : CheckOptions) : IO Unit := do
  let binary ← executableHash
  unless (identity.getObjValAs? UInt64 "checker_binary_hash").toOption==some binary &&
      (receipt.getObjValAs? UInt64 "checker_binary_hash").toOption==some binary do
    throw <| IO.userError "closure certificate checker executable differs"
  unless (identity.getObjValAs? Nat "checker_checkpoint_abi").toOption==some 6 do
    throw <| IO.userError "closure certificate child ABI differs"
  unless (receipt.getObjValAs? Nat "checker_checkpoint_abi").toOption==some 6 &&
      (receipt.getObjValAs? Nat "schema_version").toOption==some 1 &&
      (receipt.getObjValAs? String "lean_version").toOption==some version do
    throw <| IO.userError "closure certificate receipt ABI or toolchain differs"
  unless (identity.getObjValAs? String "project").toOption==some project.toString &&
      (identity.getObjValAs? (List String) "search_path").toOption==some paths do
    throw <| IO.userError "closure certificate project or resolved search path differs"
  unless (identity.getObjValAs? Bool "persistence").toOption==some o.persist &&
      (identity.getObjValAs? Bool "split_fallback").toOption==some o.split &&
      (identity.getObjValAs? String "theorem_body_policy").toOption==some (theoremBodyPolicy o) &&
      (receipt.getObjValAs? String "theorem_body_policy").toOption==some (theoremBodyPolicy o) &&
      (identity.getObjValAs? (Array String) "roots").toOption==some (roots.qsort (· < ·)) &&
      (identity.getObjValAs? String "lean").toOption==some version &&
      (identity.getObjVal? "manifest").toOption==some manifest do
    throw <| IO.userError "closure certificate configuration differs"

def projectRevision (project : System.FilePath) : IO Json := do
  try
    let r ← IO.Process.output {cmd:="git",args:=#["rev-parse","HEAD"],cwd:=some project}
    if r.exitCode==0 then pure (toJson r.stdout.trimAscii.toString) else pure Json.null
  catch _ => pure Json.null

def readManifest (project : System.FilePath) : IO Json := do
  if ← (project/"lake-manifest.json").pathExists then
    IO.ofExcept (Json.parse (← IO.FS.readFile (project/"lake-manifest.json")))
  else pure Json.null

/-- Foreign artifacts are never decoded by this executable.
    Official fresh mode has a different duplicate-proof and coverage protocol. -/
def officialFallback (o : CheckOptions) (project dir : System.FilePath)
    (version : String) (start : Nat) (cpuStart : UInt64) : IO UInt32 := do
  IO.eprintln "ProofServe: using the project's official leanchecker --fresh; parallel checking and checkpoint resume are unavailable on this path."
  let lib := project/".lake/build/lib/lean"
  let requested ← requestedRoots o
  let roots ← if requested.isEmpty then discover lib lib else pure requested
  unless !roots.isEmpty do throw <| IO.userError "no compiled roots for official checker"
  let mut rows := #[]
  let mut accepted := #[]
  let mut rejected := #[]
  let mut failed := false
  let mut operational := false
  for root in roots.qsort (· < ·) do
    let r ← IO.Process.output {cmd:="lake",args:=#["env","leanchecker","--fresh",root],cwd:=some project}
    let row := Json.mkObj [("root",toJson root),("exit_code",toJson r.exitCode.toNat),
      ("stdout",toJson r.stdout),("stderr",toJson r.stderr)]
    rows := rows.push row
    if r.exitCode==0 then accepted := accepted.push root
    else
      failed := true
      if r.exitCode != 1 then operational := true
      rejected := rejected.push row
  let receipt := Json.mkObj [("schema_version",toJson 1),("execution_path",toJson "official-leanchecker"),("theorem_body_policy",toJson "official-fresh"),
    ("parallel",toJson false),("project_revision",← projectRevision project),("project_dirty",← projectDirty project dir),("project_revision_binds_artifacts",toJson false),("mathlib_manifest",← readManifest project),("lean_version",toJson version),("roots",toJson roots),
    ("coverage",toJson "official --fresh final imported environment for each root; no per-module ledger"),
    ("status",toJson (if failed then "official_failure" else "complete")),
    ("accepted_roots",toJson accepted),("rejected_roots",toJson rejected),
    ("accepted",Json.null),("rejected",Json.null),("module_set_hash",Json.null),
    ("axioms",Json.null),("cpu_ns",toJson ((← totalCpuNs)-cpuStart)),
    ("wall_ns",toJson ((← IO.monoNanosNow)-start)),("official_results",toJson rows)]
  writeJson (dir/"receipt.json") receipt
  IO.println receipt.compress
  return if operational then 2 else if failed then 1 else 0


/-- Recheck each recorded artifact once per invocation. A certificate is local
trusted state, exactly as a restored environment checkpoint is local trusted state. -/
def validateBatchInputs (identity : Json) (seen : Std.HashMap String UInt64) :
    IO (Std.HashMap String UInt64) := do
  let inputs ← IO.ofExcept (identity.getObjValAs? (Array (String × UInt64)) "inputs")
  let expectedInputs : Std.HashMap String UInt64 := Std.HashMap.ofList inputs.toList
  -- Optional parts must remain absent too. Checking only recorded files permits
  -- a newly added private part to inherit an exported-only certificate.
  for (path, _) in inputs do
    if path.endsWith ".olean" then
      for part in artifactCandidates (System.FilePath.mk path) do
        unless (← part.pathExists)==expectedInputs.contains part.toString do
          throw <| IO.userError s!"certified closure input part inventory changed: {part}"
  let mut seen := seen
  for (path, expected) in inputs do
    match seen[path]? with
    | some actual =>
      unless actual == expected do
        throw <| IO.userError s!"conflicting input identities across closure batches: {path}"
    | none =>
      unless hash (← IO.FS.readBinFile path) == expected do
        throw <| IO.userError s!"certified closure input changed: {path}"
      seen := seen.insert path expected
  return seen

/-- Discard only generated snapshots after an atomic complete-batch certificate.
Partial batches keep their snapshots. Original input artifacts are never removed. -/
def retireBatchSnapshots (directory : System.FilePath) (identity receipt : Json) : IO Unit := do
  let inputs ← IO.ofExcept (identity.getObjValAs? (Array (String × UInt64)) "inputs")
  let segments ← IO.ofExcept (receipt.getObjValAs? (Array Json) "segments")
  let mut removed : Array String := #[]
  for segment in segments do
    let index ← IO.ofExcept (segment.getObjValAs? Nat "segment")
    let snapshotStem := (identity.getObjValAs? String "snapshot_prefix").toOption.getD "ProofServeSegment"
    let file := directory/s!"{snapshotStem}{index}.olean"
    if ← file.pathExists then
      unless !(inputs.any (fun x => x.1 == file.toString)) do
        throw <| IO.userError "refusing to remove an input artifact"
      IO.FS.removeFile file
      removed := removed.push file.toString
  if !removed.isEmpty then
    writeJson (directory/"retired-snapshots.json") (toJson removed)



/-- Order requested proof roots after their recorded requested dependencies.
External imports remain checked by each native child's actual closure walk. -/
def dependencyRootOrder (graph : Std.HashMap String (Array String))
    (wanted : Std.HashSet String) : IO (Array String) := do
  let mut degrees : Std.HashMap String Nat := {}
  let mut users : Std.HashMap String (Array String) := {}
  let mut ready : Std.TreeSet String := {}
  for (name,imports) in graph.toList do
    let deps := imports.filter graph.contains
    degrees := degrees.insert name deps.size
    if deps.isEmpty then ready := ready.insert name
    for dep in deps do users := users.insert dep ((users[dep]?.getD #[]).push name)
  let mut visited := 0
  let mut ordered : Array String := #[]
  while let some name := ready.min? do
    ready := ready.erase name
    visited := visited+1
    if wanted.contains name then ordered := ordered.push name
    for user in users[name]?.getD #[] do
      let degree := (degrees[user]?.getD 0)-1
      degrees := degrees.insert user degree
      if degree==0 then ready := ready.insert user
  unless visited==graph.size && ordered.size==wanted.size do
    throw <| IO.userError "cyclic or incomplete dependency root plan"
  return ordered

/-- Only compiled modules with no own constants can be replaced by their imports.
Neither namespace naming nor lexical source text establishes emptiness. -/
def prepareClosurePlan (_o : CheckOptions) (project dir exe : System.FilePath)
    (roots : Array String) (absolutePaths : List String) : IO Json := do
  let file := dir/"closure-plan.json"
  if ← file.pathExists then
    return ← IO.ofExcept (Json.parse (← IO.FS.readFile file))
  let mut todo := roots
  let requested : Std.HashSet String := Std.HashSet.ofArray roots
  let mut inspected : Std.HashSet String := {}
  let mut graph : Std.HashMap String (Array String) := {}
  let mut emptyNames : Std.HashSet String := {}
  let mut emptyRows : Array Json := #[]
  let mut extra : Std.HashSet String := {}
  let mut part := 0
  while !todo.isEmpty do
    let pending := ((Std.HashSet.ofArray todo).toArray.filter (fun name => !inspected.contains name)).qsort (· < ·)
    todo := #[]
    let mut offset := 0
    while offset<pending.size do
      let stop := min pending.size (offset+100)
      let selected := pending.extract offset stop
      let rootFile := dir/s!"module-plan-{part}.txt"
      writeAtomicFile rootFile (String.intercalate "\n" selected.toList)
      let result ← IO.Process.output {cmd:=exe.toString,args:=#["--internal-module-meta","@"++rootFile.toString],cwd:=some project,env:=#[("LEAN_PATH",some (String.intercalate ":" absolutePaths))]}
      writeAtomicFile (dir/s!"module-plan-{part}.stdout") result.stdout
      writeAtomicFile (dir/s!"module-plan-{part}.stderr") result.stderr
      unless result.exitCode==0 do
        throw <| IO.userError s!"module metadata inspection failed: {result.stderr}"
      let output ← IO.ofExcept (Json.parse result.stdout)
      let rows ← IO.ofExcept (output.getObjValAs? (Array Json) "module_metadata")
      unless rows.size==selected.size do throw <| IO.userError "module plan coverage differs"
      for row in rows do
        let name := fieldString row "module"
        unless selected.contains name do throw <| IO.userError "unexpected module metadata"
        inspected := inspected.insert name
        let imports ← IO.ofExcept (row.getObjValAs? (Array String) "imports")
        graph := graph.insert name imports
        if (row.getObjValAs? Bool "empty").toOption.getD false then
          unless (row.getObjValAs? Nat "declarations").toOption==some 0 do
            throw <| IO.userError "nonempty module cannot use import-only expansion"
          emptyNames := emptyNames.insert name
          emptyRows := emptyRows.push row
          for imp in (row.getObjValAs? (Array String) "imports").toOption.getD #[] do
            unless requested.contains imp do
              extra := extra.insert imp
              unless inspected.contains imp do todo := todo.push imp
      offset := stop
      part := part+1
  let proofRoots := (roots ++ extra.toArray).filter (fun name => !emptyNames.contains name)
  let unique : Std.HashSet String := Std.HashSet.ofArray proofRoots
  let ordered ← if _o.reuseImports && roots.size>_o.closureRoots then
      dependencyRootOrder graph unique
    else pure (unique.toArray.qsort (· < ·))
  let plan := Json.mkObj [
    ("order",toJson (if _o.reuseImports && roots.size>_o.closureRoots then "dependencies-first" else "lexical")),
    ("roots",toJson ordered),
    ("import_only",toJson emptyRows),
    ("meaning",toJson "actual compiled declaration count is zero; imports still require checking")]
  writeJson file plan
  return plan


/-- The module cache is local trusted checkpoint state, not a proof object.
Hash comparison binds only modules in this invocation's actual closure. -/
def prepareModuleCache (file directory : System.FilePath) (seen : NameSet)
    (inputs : Array (String × UInt64)) (version policy : String) : IO System.FilePath := do
  let cache ← IO.ofExcept (Json.parse (← IO.FS.readFile file))
  unless (cache.getObjValAs? String "kind").toOption==some "proofserve-local-module-cache-v1" &&
      (cache.getObjValAs? String "lean").toOption==some version &&
      (cache.getObjValAs? String "theorem_body_policy").toOption==some policy do
    throw <| IO.userError "local module cache kind, toolchain or theorem-body policy differs"
  let names ← IO.ofExcept (cache.getObjValAs? (Array String) "modules")
  let old ← IO.ofExcept (cache.getObjValAs? (Array (String × UInt64)) "inputs")
  let expected : Std.HashMap String UInt64 := Std.HashMap.ofList old.toList
  let actual : Std.HashMap String UInt64 := Std.HashMap.ofList inputs.toList
  let mut selected : Array String := #[]
  for name in names do
    unless seen.contains name.toName do continue
    let artifact ← findOLean name.toName
    for path in artifactCandidates artifact do
      match expected[path.toString]? with
      | some value =>
        unless actual[path.toString]?==some value do
          throw <| IO.userError s!"certified module input changed: {path}"
      | none =>
        if ← path.pathExists then
          throw <| IO.userError s!"certified module input is missing: {path}"
    selected := selected.push name
  let validated := directory/"validated-module-cache.json"
  writeJson validated (Json.mkObj [
    ("kind",toJson "input-validated-local-module-cache"),
    ("modules",toJson selected),("source",toJson file.toString)])
  return validated


/-- Independent dependency closures bound the retained kernel frontier by one
batch. Shared imports require prior successful original-kernel receipts and
matching input bytes; merely building an artifact never certifies it. -/
def closureBatches (o : CheckOptions) (project dir : System.FilePath)
    (version : String) (roots : Array String) (absolutePaths : List String)
    (start : Nat) (cpuStart : UInt64) : IO UInt32 := do
  searchPathRef.set (absolutePaths.map System.FilePath.mk)
  let manifest ← readManifest project
  let revision ← projectRevision project
  let dirty ← projectDirty project dir
  let binary ← executableHash
  let identity := Json.mkObj [
    ("checker_checkpoint_abi",toJson "independent-closures-v8"),("checker_binary_hash",toJson binary),
    ("lean",toJson version),("project",toJson project.toString),
    ("roots",toJson roots),("search_path",toJson absolutePaths),
    ("manifest",manifest),("closure_roots",toJson o.closureRoots),
    ("reuse_checked_imports",toJson o.reuseImports),
    ("persistence",toJson o.persist),("split_fallback",toJson o.split),
    ("theorem_body_policy",toJson (theoremBodyPolicy o))]
  let identityFile := dir/"identity.json"
  if ← identityFile.pathExists then
    unless (← IO.FS.readFile identityFile) == identity.pretty++"\n" do
      throw <| IO.userError "closure-batch checkpoint configuration changed; use a new directory"
  else writeJson identityFile identity
  let workers ← if o.workers==0 then pure (← defaultWorkers).toNat else pure o.workers
  if o.workers==0 then pinPerformance
  let exe ← IO.appPath
  let plan ← prepareClosurePlan o project dir exe roots absolutePaths
  let proofRoots ← IO.ofExcept (plan.getObjValAs? (Array String) "roots")
  let emptyRows ← IO.ofExcept (plan.getObjValAs? (Array Json) "import_only")
  let mut accepted : Array String := #[]
  let mut acceptedSet : Std.HashSet String := {}
  let mut axioms : NameSet := {}
  let mut inputsSeen : Std.HashMap String UInt64 := {}
  for row in emptyRows do inputsSeen ← validateBatchInputs row inputsSeen
  let mut rejected : Array Json := #[]
  let mut operationalErrors : Array Json := #[]
  let mut batches : Array Json := #[]
  let mut segments : Array Json := #[]
  let mut cumulativeCPU : UInt64 := 0
  let mut cacheSources : Array String := #[]
  let mut kernelModules := 0
  let mut verifications : Std.HashMap String Json := {}
  let mut trustedEntries := 0
  let mut newSegments := 0
  let mut offset := 0
  let mut batchIndex := 0
  let mut complete := true
  let mut operational := false
  while offset < proofRoots.size do
    -- A previous complete dependency closure may already cover later roots.
    while offset < proofRoots.size && acceptedSet.contains proofRoots[offset]! do
      offset := offset+1
    if offset==proofRoots.size then break
    if o.maxSegments>0 && newSegments>=o.maxSegments then
      complete := false
      operational := true
      break
    let stop := min proofRoots.size (offset+o.closureRoots)
    let selected := (proofRoots.extract offset stop).filter (fun root => !acceptedSet.contains root)
    let batchDir := dir/s!"batch-{batchIndex}"
    IO.FS.createDirAll batchDir
    let certificateFile := batchDir/"certified.json"
    let reused ← certificateFile.pathExists
    let (receipt, childIdentity) ← if reused then do
        let certificate ← IO.ofExcept (Json.parse (← IO.FS.readFile certificateFile))
        let receipt ← IO.ofExcept (certificate.getObjVal? "receipt")
        let childIdentity ← IO.ofExcept (certificate.getObjVal? "input_identity")
        pure (receipt,childIdentity)
      else do
        let mut args := #[project.toString,"--workers",toString workers,
          "--checkpoint-dir",batchDir.toString,"--closure-roots","0",
          "--segment-modules",toString o.quota,"--json"]
        if o.maxSegments>0 then
          args := args ++ #["--max-segments",toString (o.maxSegments-newSegments)]
        if !o.persist then args := args.push "--no-persistence"
        if !o.split then args := args.push "--no-split-fallback"
        if o.strictTheoremBodies then args := args.push "--strict-theorem-bodies"
        for root in selected do args := args ++ #["--root",root]
        if o.reuseImports && !accepted.isEmpty then
          let cacheFile := batchDir/"completed-module-cache.json"
          writeJson cacheFile (Json.mkObj [
            ("kind",toJson "proofserve-local-module-cache-v1"),("lean",toJson version),
            ("theorem_body_policy",toJson (theoremBodyPolicy o)),
            ("modules",toJson accepted),("inputs",toJson inputsSeen.toList.toArray),
            ("source_certificates",toJson cacheSources)])
          args := args ++ #["--trusted-module-cache",cacheFile.toString]
        let result ← IO.Process.output {cmd:=exe.toString,args,cwd:=some project}
        let mut invocation := 0
        while ← (batchDir/s!"driver-{invocation}.stdout").pathExists do
          invocation := invocation+1
        writeAtomicFile (batchDir/s!"driver-{invocation}.stdout") result.stdout
        writeAtomicFile (batchDir/s!"driver-{invocation}.stderr") result.stderr
        if result.exitCode != 0 && result.stdout.trimAscii.toString.isEmpty then
          throw <| IO.userError s!"closure child failed before receipt: {result.stderr}"
        let receipt ← IO.ofExcept (Json.parse result.stdout)
        unless (result.exitCode==0) == (fieldString receipt "status"=="complete") do
          throw <| IO.userError "child exit code and closure receipt disagree"
        let childIdentity ← IO.ofExcept (Json.parse (← IO.FS.readFile (batchDir/"identity.json")))
        pure (receipt,childIdentity)
    unless fieldString receipt "execution_path"=="proofserve-parallel" do
      throw <| IO.userError "closure batch did not use the native kernel checker"
    unless (childIdentity.getObjValAs? (Array String) "roots").toOption == some (selected.qsort (· < ·)) do
      throw <| IO.userError "closure certificate roots differ"
    unless (childIdentity.getObjValAs? String "lean").toOption == some version do
      throw <| IO.userError "closure certificate toolchain differs"
    unless (childIdentity.getObjVal? "manifest").toOption == some manifest do
      throw <| IO.userError "closure certificate manifest differs"
    validateCertificateContext childIdentity receipt project selected absolutePaths version manifest o
    inputsSeen ← validateBatchInputs childIdentity inputsSeen
    if reused then
      let current ← currentInputMetadata project batchDir selected absolutePaths
      let actual ← IO.ofExcept (current.getObjValAs? (Array (String × UInt64)) "inputs")
      let recorded ← IO.ofExcept (childIdentity.getObjValAs? (Array (String × UInt64)) "inputs")
      unless actual.qsort (fun a b => a.1 < b.1)==recorded.qsort (fun a b => a.1 < b.1) do
        throw <| IO.userError "closure certificate no longer matches currently resolved inputs"
    let names ← IO.ofExcept (receipt.getObjValAs? (Array String) "accepted")
    for row in (receipt.getObjValAs? (Array Json) "module_verifications").toOption.getD #[] do
      let name := fieldString row "module"
      let action := if reused then "certificate_reuse" else fieldString row "action"
      let current := Json.mkObj [
        ("module",toJson name),("action",toJson action),
        ("context",toJson (fieldString row "context")),
        ("safe_input_constants",(row.getObjVal? "safe_input_constants").toOption.getD Json.null),
        ("frontier_insert_candidates",(row.getObjVal? "frontier_insert_candidates").toOption.getD Json.null),
        ("kernel_call_count",Json.null)]
      if action=="kernel_replay" || !(verifications[name]?).any (fun old => fieldString old "action"=="kernel_replay") then
        verifications := verifications.insert name current
    let reusedModules := (receipt.getObjValAs? (Array String) "certificate_reused_modules").toOption.getD #[]
    trustedEntries := trustedEntries+reusedModules.size
    kernelModules := kernelModules+names.size-reusedModules.size
    let batchComplete := fieldString receipt "status"=="complete"
    if batchComplete then
      for root in selected do
        unless names.contains root do
          throw <| IO.userError s!"complete closure omitted requested root: {root}"
      if !reused then
        writeJson certificateFile (Json.mkObj [
          ("receipt",receipt),("input_identity",childIdentity)])
      retireBatchSnapshots batchDir childIdentity receipt
      cacheSources := cacheSources.push certificateFile.toString
    else
      unless !reused do throw <| IO.userError "incomplete certificate cannot be reused"
      complete := false
      operational := fieldString receipt "status"!="rejected"
    for name in names do
      unless acceptedSet.contains name do
        acceptedSet := acceptedSet.insert name
        accepted := accepted.push name
    for name in (receipt.getObjValAs? (Array String) "axioms").toOption.getD #[] do
      axioms := axioms.insert name.toName
    rejected := rejected ++ (receipt.getObjValAs? (Array Json) "rejected").toOption.getD #[]
    for error in (receipt.getObjValAs? (Array Json) "operational_errors").toOption.getD #[] do
      operationalErrors := operationalErrors.push (Json.mkObj [("batch",toJson batchIndex),("diagnostic",error)])
    cumulativeCPU := cumulativeCPU +
      (receipt.getObjValAs? UInt64 "cumulative_segment_cpu_ns").toOption.getD 0
    for segment in (receipt.getObjValAs? (Array Json) "segments").toOption.getD #[] do
      let old := reused || (segment.getObjValAs? Bool "reused").toOption.getD false
      if !old then newSegments := newSegments+1
      segments := segments.push (Json.mkObj [
        ("segment",toJson segments.size),("batch",toJson batchIndex),("reused",toJson old)])
    batches := batches.push (Json.mkObj [
      ("batch",toJson batchIndex),("roots",toJson selected),
      ("modules",toJson names.size),("reused",toJson reused),
      ("status",toJson (fieldString receipt "status")),
      ("certificate",toJson certificateFile.toString)])
    if !batchComplete then break
    offset := stop
    batchIndex := batchIndex+1
  let mut emptyAccepted : Array String := #[]
  if complete then
    let mut remaining := emptyRows
    while !remaining.isEmpty do
      let mut next : Array Json := #[]
      let mut progress := false
      for row in remaining do
        let name := fieldString row "module"
        let imports ← IO.ofExcept (row.getObjValAs? (Array String) "imports")
        if acceptedSet.contains name || imports.all acceptedSet.contains then
          do
            -- Planning may have happened several batches ago. Re-read the
            -- empty parent's own bytes before trusting its recorded imports.
            let _ ← validateBatchInputs row {}
            -- Individually valid imports may still conflict when combined.
            -- Use the upstream module-local importer and empty replay, without
            -- replaying any imported proof body a second time.
            let contextResult ← IO.Process.output {cmd:=exe.toString,args:=#["--internal-empty-context",name],cwd:=some project,env:=#[("LEAN_PATH",some (String.intercalate ":" absolutePaths))]}
            let contextIndex := emptyAccepted.size
            writeAtomicFile (dir/s!"empty-context-{contextIndex}.stdout") contextResult.stdout
            writeAtomicFile (dir/s!"empty-context-{contextIndex}.stderr") contextResult.stderr
            if contextResult.exitCode==1 then
              rejected := rejected.push (Json.mkObj [("module",toJson name),
                ("context",toJson "import_only"),("error",toJson contextResult.stderr)])
              accepted := accepted.filter (· != name)
              acceptedSet := acceptedSet.erase name
              verifications := verifications.erase name
              complete := false
              operational := false
              progress := true
              break
            unless contextResult.exitCode==0 do
              throw <| IO.userError s!"import-only context validation failed for {name}: {contextResult.stderr}"
            let checked ← IO.ofExcept (Json.parse contextResult.stdout)
            unless (checked.getObjValAs? Bool "empty_context_checked").toOption==some true &&
                fieldString checked "module"==name do
              throw <| IO.userError "empty-context result differs"
            unless acceptedSet.contains name do
              acceptedSet := acceptedSet.insert name
              accepted := accepted.push name
          emptyAccepted := emptyAccepted.push name
          unless verifications.contains name do
            verifications := verifications.insert name (Json.mkObj [
              ("module",toJson name),("action",toJson "empty_context"),
              ("safe_input_constants",toJson 0),("kernel_call_count",Json.null)])
          progress := true
        else next := next.push row
      if !complete then break
      unless progress do
        throw <| IO.userError "import-only modules have unchecked or cyclic dependencies"
      remaining := next
    if complete then
      for root in roots do
        unless acceptedSet.contains root do
          throw <| IO.userError s!"complete partitioned check omitted requested root: {root}"
  if complete then
    -- A completed but no longer needed module can change between batches too.
    -- Final acceptance binds the current union, not only later used imports.
    let _ ← validateBatchInputs (Json.mkObj [("inputs",toJson inputsSeen.toList.toArray)]) {}
    -- Also re-resolve accepted names: a newly shadowing search-path artifact
    -- must not inherit a prior path's acceptance at final publication.
    for name in accepted do
      let file ← findOLean name.toName
      for level in [OLeanLevel.exported,OLeanLevel.server,OLeanLevel.private] do
        let part := level.adjustFileName file
        unless (← part.pathExists)==inputsSeen.contains part.toString do
          throw <| IO.userError s!"current module resolution differs from certified inputs: {name}"
  let failedNames := rejected.map (fun row => fieldString row "module")
  accepted := accepted.filter (fun name => !failedNames.contains name)
  verifications := verifications.filter (fun name _ => !failedNames.contains name)
  let receipt := Json.mkObj [
    ("schema_version",toJson 1),("execution_path",toJson "proofserve-parallel"),("theorem_body_policy",toJson (theoremBodyPolicy o)),("checker_checkpoint_abi",toJson 6),("checker_binary_hash",toJson binary),
    ("parallel",toJson true),("context_strategy",toJson "independent-closures"),
    ("checkpoint_kind",toJson "input-validated-local-certificates"),
    ("reuse_checked_imports",toJson o.reuseImports),
    ("module_check_entries",toJson kernelModules),
    ("trusted_import_entries",toJson trustedEntries),
    ("operational_errors",toJson operationalErrors),
    ("module_verifications",toJson (verifications.toList.map (fun (_,v) => v) |>.toArray)),
    ("new_module_check_entries",toJson (verifications.toList.filter (fun (_,v) => fieldString v "action"=="kernel_replay")).length),
    ("entry_count_meaning",toJson "module replay entries, not declaration checks or kernel calls"),
    ("trusted_import_basis",toJson "trusted editable local certificates bound to this project, toolchain, resolved input paths and complete part inventory; manual certificate edits can forge acceptance or axioms"),
    ("status",toJson (if complete then "complete" else if operational then "incomplete" else "rejected")),
    ("lean_version",toJson version),("project_revision",revision),("project_dirty",dirty),("project_revision_binds_artifacts",toJson false),
    ("mathlib_manifest",manifest),("roots",toJson roots),("accepted",toJson accepted),
    ("rejected",toJson rejected),("axioms",toJson (axioms.toList.map Name.toString |>.toArray.qsort (· < ·))),
    ("module_set_hash",toJson (hash (accepted.qsort (· < ·)))),
    ("module_set_hash_algorithm",toJson "lean-hash64-toolchain-specific-noncryptographic"),
    ("workers",toJson workers),("closure_roots",toJson o.closureRoots),
    ("batches",toJson batches),("segments",toJson segments),
    ("import_only_modules",toJson emptyAccepted),
    ("cumulative_segment_cpu_ns",toJson cumulativeCPU),
    ("cpu_ns",toJson ((← totalCpuNs)-cpuStart)),
    ("wall_ns",toJson ((← IO.monoNanosNow)-start)),
    ("trusted_local_checkpoints",toJson true)]
  writeJson (dir/"receipt.json") receipt
  IO.println receipt.compress
  return if complete then 0 else if operational then 2 else 1

unsafe def frontend (args : List String) : IO UInt32 := do
  let start ← IO.monoNanosNow
  let cpuStart ← totalCpuNs
  let o ← IO.ofExcept (parseOptions args)
  let project ← IO.FS.realPath o.project
  let dir := if o.directory.isAbsolute then o.directory else project/o.directory
  IO.FS.createDirAll dir
  checkpointLock (dir/".lock").toString
  let declared ← IO.FS.readFile (project/"lean-toolchain")
  let declared := declared.trimAscii.toString
  unless declared.startsWith "leanprover/lean4:v" do
    throw <| IO.userError "unsupported Lean toolchain identifier"
  let expected := (declared.drop "leanprover/lean4:v".length).toString
  let version ← IO.Process.output {cmd:="lake",args:=#["env","lean","--version"],cwd:=some project}
  unless version.exitCode==0 && version.stdout.startsWith s!"Lean (version {expected}," do
    throw <| IO.userError s!"unsupported or mismatched project toolchain: {declared}; {version.stdout} {version.stderr}"
  if o.official || expected != Lean.versionString then
    return ← officialFallback o project dir version.stdout start cpuStart
  let paths ← IO.Process.output {cmd:="lake",args:=#["env","printenv","LEAN_PATH"],cwd:=some project}
  unless paths.exitCode==0 do throw <| IO.userError paths.stderr
  let pathText := paths.stdout.trimAscii.toString
  let absolutePaths := (pathText.splitOn ":").map fun p =>
    let f := System.FilePath.mk p
    if f.isAbsolute then f.toString else (project/f).toString
  let lib := project/".lake/build/lib/lean"
  let requested ← requestedRoots o
  let roots ← if requested.isEmpty then discover lib lib else pure requested
  unless !roots.isEmpty do throw <| IO.userError "no compiled project roots; run lake build or pass --root MODULE"
  let roots := roots.qsort (· < ·)
  let mut namespaceRoot := false
  for i in [:roots.size] do
    if i+1<roots.size && roots[i+1]!.startsWith (roots[i]!++".") then
      namespaceRoot := true
  if roots.size==1 && o.closureRoots>0 then
    for base in absolutePaths do
      if ← (System.FilePath.mk base / (roots[0]!.replace "." "/")).isDir then
        namespaceRoot := true
  if o.closureRoots>0 && (roots.size>o.closureRoots || o.closureRoots==1 || namespaceRoot) then
    return ← closureBatches o project dir version.stdout roots absolutePaths start cpuStart
  let rootFile := dir/"roots.txt"
  let rootsText := String.intercalate "\n" roots.toList
  -- Current receipt1 checkpoint is local trusted state; validate identity before reuse.
  searchPathRef.set (absolutePaths.map System.FilePath.mk)
  let metadata ← currentInputMetadata project dir roots absolutePaths
  let names ← IO.ofExcept (metadata.getObjValAs? (Array String) "modules")
  let mut snapshotPrefix := "ProofServeSegment"
  while names.any (·.startsWith snapshotPrefix) do snapshotPrefix := snapshotPrefix++"X"
  let seen := names.foldl (fun (s : NameSet) n => s.insert n.toName) {}
  let inputs ← IO.ofExcept (metadata.getObjValAs? (Array (String × UInt64)) "inputs")
  let manifest ← readManifest project
  let revision ← projectRevision project
  let dirty ← projectDirty project dir
  let binary ← executableHash
  let validatedCache ← match o.moduleCache with
    | none => pure none
    | some file => pure (some (← prepareModuleCache file dir seen inputs version.stdout (theoremBodyPolicy o)))
  let cacheIdentity ← match validatedCache with
    | none => pure Json.null
    | some file => IO.ofExcept (Json.parse (← IO.FS.readFile file))
  let identity := Json.mkObj [("checker_checkpoint_abi",toJson 6),("checker_binary_hash",toJson binary),("snapshot_prefix",toJson snapshotPrefix),("module_cache",cacheIdentity),("lean",toJson version.stdout),("roots",toJson roots),
    ("inputs",toJson inputs),("manifest",manifest),("project",toJson project.toString),("search_path",toJson absolutePaths),
    ("persistence",toJson o.persist),("split_fallback",toJson o.split),
    ("theorem_body_policy",toJson (theoremBodyPolicy o))]
  let identityFile := dir/"identity.json"
  if ← identityFile.pathExists then
    unless (← IO.FS.readFile identityFile) == identity.pretty++"\n" do
      throw <| IO.userError "checkpoint configuration changed; use a new checkpoint directory"
  else writeJson identityFile identity
  writeAtomicFile rootFile rootsText
  let workers ← if o.workers==0 then pure (← defaultWorkers).toNat else pure o.workers
  let exe ← IO.appPath
  let mut previous := ""
  let mut part := 0
  let mut newParts := 0
  let mut accepted : Array String := #[]
  let mut trustedModules : Array String := #[]
  let mut verificationRows : Array Json := #[]
  let mut moduleSizes : Std.HashMap String Nat := {}
  let mut operationalErrors : Array Json := #[]
  let mut rejected : Array Json := #[]
  let mut axioms : Array String := #[]
  if o.workers==0 then pinPerformance
  let mut currentChildCPU : UInt64 := 0
  let mut cpu : UInt64 := 0
  let mut complete := false
  let mut operational := false
  let mut segments := #[]
  repeat
    let key := s!"segment-{part}"
    let logFile := dir/(key++".json")
    let saved ← if ← logFile.pathExists then
      pure <| some (← IO.ofExcept (Json.parse (← IO.FS.readFile logFile)))
      else pure none
    let record ← match saved with
      | some r => pure r
      | none =>
        let snapshot := s!"{snapshotPrefix}{part}"
        let eventFile := dir/(key++".events")
        writeAtomicFile eventFile ""
        let e := #[("LEAN_PATH",some (String.intercalate ":" absolutePaths)),
          ("PROOFSERVE_EVENT_LOG",some eventFile.toString),
          ("LEAN_NUM_THREADS",some (toString workers)),("PROOFSERVE_WORKERS",some (toString workers)),
          ("PROOFSERVE_PERSIST",some (if o.persist then "1" else "0")),
          ("PROOFSERVE_SPLIT",some (if o.split then "1" else "0")),
          ("PROOFSERVE_STRICT_THEOREM_BODIES",some (if o.strictTheoremBodies then "1" else "0")),
          ("PROOFSERVE_VALIDATED_MODULE_CACHE",validatedCache.map System.FilePath.toString),
          ("PROOFSERVE_CHECKPOINT_DIR",some dir.toString),("PROOFSERVE_SNAPSHOT_PREFIX",some snapshotPrefix),
          ("DECOUPLED_CHECKPOINT_INPUT",if previous.isEmpty then none else some previous),
          ("DECOUPLED_CHECKPOINT_OUTPUT",some ((dir/(snapshot++".olean")).toString)),
          ("DECOUPLED_CHECKPOINT_MODULE",some snapshot),
          ("DECOUPLED_SEGMENT_MODULES",some (toString o.quota))]
        let result ← IO.Process.output {cmd:=exe.toString,args:=#["--internal-segment","audit","none","@"++rootFile.toString],cwd:=some project,env:=e}
        writeAtomicFile (dir/(key++".stdout")) result.stdout
        writeAtomicFile (dir/(key++".stderr")) result.stderr
        let eventText ← IO.FS.readFile eventFile
        writeAtomicFile eventFile eventText
        let ev := objectEvents eventText
        let r := Json.mkObj [("exit",toJson result.exitCode.toNat),("stderr",toJson result.stderr),("events",toJson ev)]
        -- A failed/incomplete segment is never reused as a certified prefix.
        if result.exitCode==0 then writeJson logFile r
        pure r
    if saved.isNone then newParts := newParts+1
    let ev ← IO.ofExcept (record.getObjValAs? (Array Json) "events")
    let exitCode := (record.getObjValAs? Nat "exit").toOption.getD 2
    let terminalCount := ev.filter (fun e => ["complete","checkpoint"].contains (fieldString e "event")) |>.size
    if exitCode==0 && terminalCount != 1 then
      throw <| IO.userError "segment event channel has no unique terminal"
    for event in ev do
      match fieldString event "event" with
      | "module_header" =>
        moduleSizes := moduleSizes.insert (fieldString event "module")
          ((event.getObjValAs? Nat "safe_constants").toOption.getD 0)
      | "accept" =>
        let name := fieldString event "module"
        accepted := accepted.push name
        verificationRows := verificationRows.push (Json.mkObj [
          ("module",toJson name),("action",toJson (if saved.isSome then "checkpoint_reuse" else if fieldString event "context"=="shared" && (event.getObjValAs? Nat "frontier_insert_candidates").toOption==some 0 then "interface_or_empty" else "kernel_replay")),
          ("context",toJson (fieldString event "context")),
          ("safe_input_constants",toJson moduleSizes[name]?),
          ("frontier_insert_candidates",(event.getObjVal? "frontier_insert_candidates").toOption.getD Json.null),
          ("kernel_call_count",Json.null)])
      | "trusted_import" =>
        accepted := accepted.push (fieldString event "module")
        trustedModules := trustedModules.push (fieldString event "module")
        verificationRows := verificationRows.push (Json.mkObj [
          ("module",toJson (fieldString event "module")),
          ("action",toJson (if saved.isSome then "checkpoint_reuse" else "certificate_import")),
          ("safe_input_constants",Json.null),("kernel_call_count",Json.null)])
      | "reject" => rejected := rejected.push event
      | "checkpoint" => previous := s!"{snapshotPrefix}{part}"
                        axioms := (event.getObjValAs? (Array String) "axioms").toOption.getD #[]
      | "complete" => complete := true
                      axioms := (event.getObjValAs? (Array String) "axioms").toOption.getD #[]
      | "segment_cpu" =>
        let units := (event.getObjValAs? UInt64 "cpu_ns").toOption.getD 0
        cpu := cpu+units
        if saved.isNone then currentChildCPU := currentChildCPU+units
      | _ => pure ()
    segments := segments.push (Json.mkObj [("segment",toJson part),("reused",toJson saved.isSome)])
    if (record.getObjValAs? Nat "exit").toOption.getD 2 != 0 then
      operationalErrors := operationalErrors.push (Json.mkObj [
        ("segment",toJson part),("exit_code",toJson exitCode),("stderr",toJson (fieldString record "stderr"))])
      complete := false
      operational := rejected.isEmpty
      break
    if !rejected.isEmpty then
      complete := false
      break
    if complete then break
    unless ev.any (fun j => fieldString j "event" == "checkpoint") do
      operational := true
      break
    part := part+1
    if o.maxSegments>0 && newParts>=o.maxSegments then
      operational := true
      break
  if complete then
    unless rejected.isEmpty && roots.all accepted.contains && names.all accepted.contains do
      complete := false
      operational := rejected.isEmpty
  let failedNames := rejected.map (fun row => fieldString row "module")
  accepted := accepted.filter (fun name => !failedNames.contains name)
  trustedModules := trustedModules.filter (fun name => !failedNames.contains name)
  verificationRows := verificationRows.filter (fun row => !failedNames.contains (fieldString row "module"))
  let receipt := Json.mkObj [("schema_version",toJson 1),("execution_path",toJson "proofserve-parallel"),("theorem_body_policy",toJson (theoremBodyPolicy o)),("checker_checkpoint_abi",toJson 6),("checker_binary_hash",toJson binary),("parallel",toJson true),("lean_version",toJson version.stdout),
    ("status",toJson (if complete then "complete" else if operational then "incomplete" else "rejected")),
    ("project_revision",revision),("project_dirty",dirty),("project_revision_binds_artifacts",toJson false),("mathlib_manifest",manifest),("roots",toJson roots),("accepted",toJson accepted),("rejected",toJson rejected),
    ("module_set_hash",toJson (hash (accepted.qsort (· < ·)))),
    ("module_set_hash_algorithm",toJson "lean-hash64-toolchain-specific-noncryptographic"),
    ("axioms",toJson ((axioms.toList.foldl (fun (s : NameSet) n => s.insert n.toName) {}).toList.map Name.toString |>.toArray.qsort (· < ·))),("workers",toJson workers),
    ("cumulative_segment_cpu_ns",toJson cpu),("cpu_ns",toJson ((← totalCpuNs)-cpuStart)),("wall_ns",toJson ((← IO.monoNanosNow)-start)),
    ("segments",toJson segments),("trusted_local_checkpoints",toJson true),
    ("certificate_reused_modules",toJson trustedModules),
    ("missing_modules",toJson (names.filter (fun n => !accepted.contains n))),
    ("operational_errors",toJson operationalErrors),
    ("module_verifications",toJson verificationRows),
    ("new_module_check_entries",toJson (verificationRows.filter (fun j => fieldString j "action"=="kernel_replay")).size),
    ("entry_count_meaning",toJson "module replay entries, not declaration checks or kernel calls"),
    ("trusted_import_basis",toJson "trusted editable local certificates with current input identities; manual certificate edits can forge acceptance or axioms")]
  writeJson (dir/"receipt.json") receipt
  IO.println receipt.compress
  return if complete then 0 else if operational then 2 else 1

unsafe def main (args : List String) : IO UInt32 := do
  try
    if args.head? == some "--internal-input-identity" then
      return ← runInputIdentity args.tail!
    if args.head? == some "--internal-module-meta" then
      return ← runModuleMetadata args.tail!
    if args.head? == some "--internal-empty-context" then
      return ← runEmptyContext args.tail!
    if args.head? == some "--internal-segment" then
      let start ← processNs
      let code ← runSegment args.tail!
      event [("event",toJson "segment_cpu"),("cpu_ns",toJson ((← processNs)-start))]
      return code
    if args==["--help"] then
      IO.println "proofserve-check PROJECT [--workers N] [--checkpoint-dir D] [--root MODULE] [--root-file FILE] [--segment-modules N] [--max-segments N] [--closure-roots N] [--replay-shared-imports] [--json] [--official] [--no-persistence] [--no-split-fallback] [--strict-theorem-bodies]"
      return 0
    frontend args
  catch e =>
    IO.eprintln (Json.mkObj [("schema_version",toJson 1),("status",toJson "error"),("error",toJson e.toString)]).compress
    return 2
