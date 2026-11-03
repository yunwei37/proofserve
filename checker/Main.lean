import ProofServe.Stream
open Lean ProofServe

@[extern "ps_checkpoint_lock"] opaque checkpointLock (path : @& String) : IO Unit

structure CheckOptions where
  project : System.FilePath := "."
  workers : Nat := 0
  directory : System.FilePath := ".proofserve"
  quota : Nat := 500
  maxSegments : Nat := 0
  roots : Array String := #[]
  persist : Bool := true
  split : Bool := true
  official : Bool := false

partial def parseOptions (args : List String) (o : CheckOptions := {}) : Except String CheckOptions :=
  match args with
  | [] => .ok o
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
  | "--no-persistence"::xs => parseOptions xs {o with persist:=false}
  | "--no-split-fallback"::xs => parseOptions xs {o with split:=false}
  | "--official"::xs => parseOptions xs {o with official:=true}
  | "--json"::xs => parseOptions xs o
  | x::xs =>
    if x.startsWith "-" then .error s!"unknown option {x}"
    else parseOptions xs {o with project:=x}

def writeJson (file : System.FilePath) (value : Json) : IO Unit := do
  let pending := System.FilePath.mk (file.toString++".pending")
  IO.FS.writeFile pending (value.pretty++"\n")
  IO.FS.rename pending file

partial def discover (root : System.FilePath) (path : System.FilePath) : IO (Array String) := do
  let mut out := #[]
  for d in ← path.readDir do
    if ← d.path.isDir then out := out ++ (← discover root d.path)
    else if d.path.extension == some "olean" then
      let rel := (d.path.toString.drop (root.toString.length+1)).toString
      if !rel.endsWith ".server.olean" && !rel.endsWith ".private.olean" then
        out := out.push ((rel.dropEnd 6).toString.replace "/" ".")
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
  let mut seen := seen.insert mod
  let mut files := #[]
  let file ← findOLean mod
  for level in [OLeanLevel.exported,OLeanLevel.server,OLeanLevel.private] do
    let f := level.adjustFileName file
    if ← f.pathExists then files := files.push (f.toString,hash (← IO.FS.readBinFile f))
  for imp in first.imports do
    let (next,more) ← inputIdentity imp.module seen
    seen := next
    files := files ++ more
  return (seen,files)

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
  let roots ← if o.roots.isEmpty then discover lib lib else pure o.roots
  unless !roots.isEmpty do throw <| IO.userError "no compiled roots for official checker"
  let mut rows := #[]
  let mut accepted := #[]
  let mut rejected := #[]
  let mut failed := false
  for root in roots.qsort (· < ·) do
    let r ← IO.Process.output {cmd:="lake",args:=#["env","leanchecker","--fresh",root],cwd:=some project}
    let row := Json.mkObj [("root",toJson root),("exit_code",toJson r.exitCode.toNat),
      ("stdout",toJson r.stdout),("stderr",toJson r.stderr)]
    rows := rows.push row
    if r.exitCode==0 then accepted := accepted.push root
    else
      failed := true
      rejected := rejected.push row
  let receipt := Json.mkObj [("schema_version",toJson 1),("execution_path",toJson "official-leanchecker"),
    ("parallel",toJson false),("project_revision",← projectRevision project),("mathlib_manifest",← readManifest project),("lean_version",toJson version),("roots",toJson roots),
    ("coverage",toJson "official --fresh final imported environment for each root; no per-module ledger"),
    ("status",toJson (if failed then "official_failure" else "complete")),
    ("accepted_roots",toJson accepted),("rejected_roots",toJson rejected),
    ("accepted",Json.null),("rejected",Json.null),("module_set_hash",Json.null),
    ("axioms",Json.null),("cpu_ns",toJson ((← totalCpuNs)-cpuStart)),
    ("wall_ns",toJson ((← IO.monoNanosNow)-start)),("official_results",toJson rows)]
  writeJson (dir/"receipt.json") receipt
  IO.println receipt.compress
  return if failed then 2 else 0

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
  let roots ← if o.roots.isEmpty then discover lib lib else pure o.roots
  unless !roots.isEmpty do throw <| IO.userError "no compiled project roots; run lake build or pass --root MODULE"
  let roots := roots.qsort (· < ·)
  let rootFile := dir/"roots.txt"
  let rootsText := String.intercalate "\n" roots.toList
  -- Current receipt1 checkpoint is local trusted state; validate identity before reuse.
  searchPathRef.set (absolutePaths.map System.FilePath.mk)
  let mut seen : NameSet := {}
  let mut inputs : Array (String × UInt64) := #[]
  for root in roots do
    let (next,more) ← inputIdentity root.toName seen
    seen := next
    inputs := inputs ++ more
  let manifest ← readManifest project
  let revision ← projectRevision project
  let identity := Json.mkObj [("checker_checkpoint_abi",toJson 1),("lean",toJson version.stdout),("roots",toJson roots),
    ("inputs",toJson inputs),("manifest",manifest),("project",toJson project.toString),("search_path",toJson absolutePaths),
    ("persistence",toJson o.persist),("split_fallback",toJson o.split)]
  let identityFile := dir/"identity.json"
  if ← identityFile.pathExists then
    unless (← IO.FS.readFile identityFile) == identity.pretty++"\n" do
      throw <| IO.userError "checkpoint configuration changed; use a new checkpoint directory"
  else writeJson identityFile identity
  IO.FS.writeFile rootFile rootsText
  let workers ← if o.workers==0 then pure (← defaultWorkers).toNat else pure o.workers
  let exe ← IO.appPath
  let mut previous := ""
  let mut part := 0
  let mut accepted : Array String := #[]
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
        let snapshot := s!"ProofServeSegment{part}"
        let e := #[("LEAN_PATH",some (dir.toString++":"++String.intercalate ":" absolutePaths)),
          ("LEAN_NUM_THREADS",some (toString workers)),("PROOFSERVE_WORKERS",some (toString workers)),
          ("PROOFSERVE_PERSIST",some (if o.persist then "1" else "0")),
          ("PROOFSERVE_SPLIT",some (if o.split then "1" else "0")),
          ("DECOUPLED_CHECKPOINT_INPUT",if previous.isEmpty then none else some previous),
          ("DECOUPLED_CHECKPOINT_OUTPUT",some ((dir/(snapshot++".olean")).toString)),
          ("DECOUPLED_CHECKPOINT_MODULE",some snapshot),
          ("DECOUPLED_SEGMENT_MODULES",some (toString o.quota))]
        let result ← IO.Process.output {cmd:=exe.toString,args:=#["--internal-segment","audit","none","@"++rootFile.toString],cwd:=some project,env:=e}
        IO.FS.writeFile (dir/(key++".stdout")) result.stdout
        IO.FS.writeFile (dir/(key++".stderr")) result.stderr
        let ev := objectEvents result.stdout
        let r := Json.mkObj [("exit",toJson result.exitCode.toNat),("events",toJson ev)]
        -- A failed/incomplete segment is never reused as a certified prefix.
        if result.exitCode==0 then writeJson logFile r
        pure r
    let ev ← IO.ofExcept (record.getObjValAs? (Array Json) "events")
    for event in ev do
      match fieldString event "event" with
      | "accept" => accepted := accepted.push (fieldString event "module")
      | "reject" => rejected := rejected.push event
      | "checkpoint" => previous := s!"ProofServeSegment{part}"
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
      operational := rejected.isEmpty
      break
    if complete then break
    unless ev.any (fun j => fieldString j "event" == "checkpoint") do
      operational := true
      break
    part := part+1
    if o.maxSegments>0 && part>=o.maxSegments then
      operational := true
      break
  let receipt := Json.mkObj [("schema_version",toJson 1),("execution_path",toJson "proofserve-parallel"),("parallel",toJson true),("lean_version",toJson version.stdout),
    ("status",toJson (if complete then "complete" else if operational then "incomplete" else "rejected")),
    ("project_revision",revision),("mathlib_manifest",manifest),("roots",toJson roots),("accepted",toJson accepted),("rejected",toJson rejected),
    ("module_set_hash",toJson (hash (accepted.qsort (· < ·)))),
    ("module_set_hash_algorithm",toJson "lean-hash64-toolchain-specific-noncryptographic"),
    ("axioms",toJson ((axioms.toList.foldl (fun (s : NameSet) n => s.insert n.toName) {}).toList.map Name.toString |>.toArray.qsort (· < ·))),("workers",toJson workers),
    ("cumulative_segment_cpu_ns",toJson cpu),("cpu_ns",toJson ((← totalCpuNs)-cpuStart)),("wall_ns",toJson ((← IO.monoNanosNow)-start)),
    ("segments",toJson segments),("trusted_local_checkpoints",toJson true)]
  writeJson (dir/"receipt.json") receipt
  IO.println receipt.compress
  return if complete then 0 else if operational then 2 else 1

unsafe def main (args : List String) : IO UInt32 := do
  try
    if args.head? == some "--internal-segment" then
      let start ← processNs
      let code ← runSegment args.tail!
      event [("event",toJson "segment_cpu"),("cpu_ns",toJson ((← processNs)-start))]
      return code
    if args==["--help"] then
      IO.println "proofserve-check PROJECT [--workers N] [--checkpoint-dir D] [--root MODULE] [--segment-modules N] [--json] [--official] [--no-persistence] [--no-split-fallback]"
      return 0
    frontend args
  catch e =>
    IO.eprintln (Json.mkObj [("schema_version",toJson 1),("status",toJson "error"),("error",toJson e.toString)]).compress
    return 2
