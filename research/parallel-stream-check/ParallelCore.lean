/- Checked declaration frontiers for a kernel-only stream.
   Original kernel handles all mathematics. This module and checked_commit.c
   are trusted coordination glue with explicit differential/fault qualification.
 -/
import Lean
import Std.Sync.Mutex
open Lean

@[extern "ps_process_ns"] opaque processNs : IO UInt64
@[extern "ps_thread_ns"] opaque threadNs : IO UInt64

/-- Structural comparison copied read-only from O's audited reader. -/
def sameQuotKind (a b : QuotKind) : Bool :=
  match a,b with
  | .type,.type | .ctor,.ctor | .lift,.lift | .ind,.ind => true
  | _,_ => false

def sameConstant (a b : ConstantInfo) : Bool :=
  match a,b with
  | .axiomInfo a,.axiomInfo b => a == b
  | .defnInfo a,.defnInfo b => a == b
  | .thmInfo a,.thmInfo b => a == b
  | .opaqueInfo a,.opaqueInfo b => a == b
  | .quotInfo a,.quotInfo b =>
    a.name==b.name && a.levelParams==b.levelParams && a.type==b.type && sameQuotKind a.kind b.kind
  | .inductInfo a,.inductInfo b =>
    a.name==b.name && a.levelParams==b.levelParams && a.type==b.type &&
    a.numParams==b.numParams && a.numIndices==b.numIndices && a.all==b.all &&
    a.ctors==b.ctors && a.numNested==b.numNested && a.isRec==b.isRec &&
    a.isUnsafe==b.isUnsafe && a.isReflexive==b.isReflexive
  | .ctorInfo a,.ctorInfo b => a==b
  | .recInfo a,.recInfo b => a==b
  | _,_ => false

/-- Prepared certificate payloads are untrusted: every helper/chunk/merge goes
through the original kernel in the current streaming context. -/
structure ChunkBundle where
  reference : ConstantInfo
  support : Std.HashMap Name ConstantInfo
  children : Array ConstantInfo
  mergeName : Name
  k : Nat

private structure CheckedToken where
  frontier : Kernel.Environment
  info : ConstantInfo
  index : Nat

@[extern "ps_commit_checked"]
private opaque commitChecked (base : Kernel.Environment) (tokens : Array CheckedToken) :
  IO Kernel.Environment

def ordinary (ci : ConstantInfo) : Bool :=
  match ci with
  | .defnInfo _ | .thmInfo _ | .axiomInfo _ | .opaqueInfo _ => !ci.isUnsafe && !ci.isPartial
  | _ => false

def declarationOf (ci : ConstantInfo) : IO Declaration :=
  match ci with
  | .defnInfo d => pure <| .defnDecl d
  | .thmInfo d => pure <| .thmDecl d
  | .axiomInfo d => pure <| .axiomDecl d
  | .opaqueInfo d => pure <| .opaqueDecl d
  | _ => throw <| IO.userError "invariant: nonordinary declaration reached worker"

structure Plan where
  constants : Array ConstantInfo
  waves : Array (Array Nat)

/-- Complete graph planning happens before any commit; cycles use upstream replay. -/
def makePlan (data : ModuleData) (map : Std.HashMap Name ConstantInfo) : Option Plan := Id.run do
  let mut constants := #[]
  let mut names : Std.HashMap Name Nat := {}
  for original in data.constants do
    if let some ci := map[original.name]? then
      if ci.isUnsafe || ci.isPartial then continue
      if names.contains ci.name then return none
      if !ordinary ci then return none
      names := names.insert ci.name constants.size
      constants := constants.push ci
  let mut degrees : Array Nat := Array.replicate constants.size 0
  let mut children : Array (Array Nat) := Array.replicate constants.size #[]
  for i in [:constants.size] do
    let deps := constants[i]!.getUsedConstantsAsSet.toList.filterMap (names[·]?)
    degrees := degrees.set! i deps.length
    for d in deps do children := children.set! d (children[d]!.push i)
  let mut ready := (Array.range constants.size).filter (degrees[·]! == 0)
  let mut waves := #[]
  let mut total := 0
  while !ready.isEmpty do
    let current := ready.qsort (· < ·)
    waves := waves.push current
    total := total + current.size
    ready := #[]
    for i in current do
      for child in children[i]! do
        degrees := degrees.set! child (degrees[child]!-1)
        if degrees[child]! == 0 then ready := ready.push child
  if total != constants.size then return none
  return some {constants,waves}

@[noinline] private def originalCheck (base : Kernel.Environment) (decl : Declaration) :
    IO (Except Kernel.Exception Kernel.Environment) := do
  match base.addDeclCore 0 0 decl (cancelTk? := none) with
  | .ok checked => pure (.ok checked)
  | .error ex => pure (.error ex)

private def checkOne (base : Kernel.Environment) (ci : ConstantInfo) (index : Nat)
    (observe : NameSet := {}) :
    IO CheckedToken := do
  let decl ← declarationOf ci
  let record := observe.contains ci.name
  let tid ← if record then IO.getTID else pure 0
  let c0 ← if record then threadNs else pure 0
  let h0 ← if record then IO.getNumHeartbeats else pure 0
  let result ← originalCheck base decl
  let h1 ← if record then IO.getNumHeartbeats else pure 0
  let c1 ← if record then threadNs else pure 0
  match result with
  | .error error =>
    let message ← error.toMessageData {} |>.toString
    throw <| IO.userError s!"kernel_reject:{ci.name}:{message}"
  | .ok checked =>
    let some actual := checked.find? ci.name |
      throw <| IO.userError "invariant: checked kernel result missing"
    unless sameConstant actual ci do
      throw <| IO.userError s!"invariant: checked result representation differs:{ci.name}"
    if record then
      IO.println <| Json.compress <| Json.mkObj [
        ("event",toJson "unit_check"),("target",toJson ci.name.toString),
        ("raw_HB",toJson (h1-h0)),("cpu_ns",toJson (c1-c0)),
        ("tid",toJson tid),("accept",toJson true)]
    return {frontier:=base,info:=actual,index}

private def worker (base : Kernel.Environment) (plan : Plan)
    (jobs : Array Nat) (queue : Std.Mutex Nat) (observe : NameSet) : IO (Array CheckedToken) := do
  let mut results := #[]
  repeat
    let position ← queue.atomically do
      let i ← get
      set (i+1)
      pure i
    if position >= jobs.size then break
    let index := jobs[position]!
    results := results.push (← checkOne base plan.constants[index]! index observe)
  return results

private def checkedBatch (base : Kernel.Environment) (plan : Plan)
    (wave : Array Nat) (workers : Nat) (fault : String) (observe : NameSet := {}) : IO Kernel.Environment := do
  let queue ← Std.Mutex.new 0
  let count := min workers wave.size
  let gate ← IO.Promise.new
  let mut tasks := #[]
  let mut error : Option IO.Error := none
  -- Lean grows its standard pool only on enqueue with no idle worker. A
  -- private queue in long-lived tasks otherwise hides runnable work. Wait for
  -- each task to enter the common gate before enqueueing its successor.
  try
    for _ in [:count] do
      if count > 1 then
        let started ← IO.Promise.new
        let task ← IO.asTask do
          started.resolve (1 : Nat)
          unless gate.result?.get == some (1 : Nat) do
            throw <| IO.userError "invariant: worker gate abandoned"
          worker base plan wave queue observe
        tasks := tasks.push task
        unless started.result?.get == some (1 : Nat) do
          throw <| IO.userError "invariant: worker did not start"
      else
        tasks := tasks.push (← IO.asTask <| worker base plan wave queue observe)
  catch e => error := some e
  -- Release and join all launched tasks even if creation failed. A failure
  -- cannot commit a partial frontier or leave a worker blocked on this gate.
  gate.resolve (1 : Nat)
  let mut tokens : Array CheckedToken := #[]
  for task in tasks do
    match task.get with
    | .ok values => tokens := tokens ++ values
    | .error e => if error.isNone then error := some e
  if let some e := error then throw e
  if fault=="duplicate" && tokens.size>1 then
    if let some second := tokens[1]? then tokens := tokens.set! 0 second
  tokens := tokens.qsort fun a b => a.index < b.index
  unless tokens.map (·.index) == wave do
    throw <| IO.userError "invariant: base-index cover differs"
  for token in tokens do
    unless sameConstant token.info plan.constants[token.index]! do
      throw <| IO.userError "invariant: base payload does not match job"
    if (base.find? token.info.name).isSome then
      throw <| IO.userError "invariant: base commit would overwrite constant"
  let checked ← if fault=="stale" && !tokens.isEmpty then do
    let other ← mkEmptyEnvironment
    commitChecked other.toKernelEnv tokens
    else commitChecked base tokens
  return checked

partial def axiomsOf (env : Kernel.Environment) (todo : List Name) (seen : NameSet := {})
    (axioms : NameSet := {}) : NameSet :=
  match todo with
  | [] => axioms
  | n :: rest =>
    if seen.contains n then axiomsOf env rest seen axioms
    else match env.find? n with
    | none => axiomsOf env rest (seen.insert n) axioms
    | some (.axiomInfo _) => axiomsOf env rest (seen.insert n) (axioms.insert n)
    | some ci => axiomsOf env (ci.getUsedConstantsAsSet.toList ++ rest) (seen.insert n) axioms

private def checkChunkedWave (base : Kernel.Environment)
    (parents : Array (ConstantInfo × ChunkBundle)) (workers : Nat) : IO Kernel.Environment := do
  let before ← IO.monoNanosNow
  let mut support := {}
  let mut children := #[]
  for (original,bundle) in parents do
    unless sameConstant original bundle.reference do
      throw <| IO.userError "invariant: chunk input does not match pinned reference"
    for (name,ci) in bundle.support do
      if let some old := base.find? name then
        unless sameConstant old ci do throw <| IO.userError "certificate namespace conflict"
      else if let some old := support[name]? then
        unless sameConstant old ci do throw <| IO.userError "certificate support conflict"
      else support := support.insert name ci
    children := children ++ bundle.children
  let mut checked ← base.replay support
  let prepared ← IO.monoNanosNow
  let plan : Plan := {constants:=children,waves:=#[]}
  -- All eligible parents' chunks share one pool; never nested k-by-k workers.
  checked ← checkedBatch checked plan (Array.range children.size) workers "none"
  let childrenDone ← IO.monoNanosNow
  let mut merged := #[]
  for (original,bundle) in parents do
    let .thmInfo thm := original | throw <| IO.userError "chunk target is not a theorem"
    let value := mkAppN (mkConst bundle.mergeName) (bundle.children.map (fun ci => mkConst ci.name))
    merged := merged.push (ConstantInfo.thmInfo {thm with value})
  checked ← checkedBatch checked {constants:=merged,waves:=#[]} (Array.range merged.size) 1 "none"
  let axioms := axiomsOf checked (parents.toList.map (·.1.name))
  unless axioms.toList.all (· == `propext) do
    throw <| IO.userError s!"chunk unexpected axiom dependency: {axioms.toList}"
  IO.println <| Json.compress <| Json.mkObj [
    ("event",toJson "chunk_work"),("constants",toJson (parents.map (·.1.name.toString))),
    ("parents",toJson parents.size),("children",toJson children.size),("workers",toJson workers),
    ("support_ns",toJson (prepared-before)),("chunks_ns",toJson (childrenDone-prepared)),
    ("merge_audit_ns",toJson ((← IO.monoNanosNow)-childrenDone)),
    ("axioms",toJson (axioms.toList.map Name.toString)),("sorry",toJson false)]
  return checked

/-- Original mathematical checker, ordered checked-frontier commits. Optional
chunking is confined to one exact prepared constant; unknown inputs are replayed. -/
def parallelReplay (data : ModuleData) (map : Std.HashMap Name ConstantInfo)
    (base : Kernel.Environment) (workers : Nat) (fault : String := "none")
    (chunks : Array ChunkBundle := #[]) (observe : NameSet := {}) :
    IO (Kernel.Environment × Nat × Nat × String) := do
  let some plan := makePlan data map |
    return (← base.replay map,0,0,"upstream_complex_or_cycle")
  let mut checked := base
  let mut jobsDone := 0
  for wave in plan.waves do
    let chunkJobs := wave.filter fun i => chunks.any (fun b => sameConstant plan.constants[i]! b.reference)
    let plainJobs := wave.filter fun i => !chunkJobs.contains i
    checked ← checkedBatch checked plan plainJobs workers fault observe
    let mut parents := #[]
    for i in chunkJobs do
      let some bundle := chunks.find? (fun b => sameConstant plan.constants[i]! b.reference) |
        throw <| IO.userError "missing chunk bundle"
      parents := parents.push (plan.constants[i]!,bundle)
    if !parents.isEmpty then checked ← checkChunkedWave checked parents workers
    jobsDone := jobsDone + wave.size
  return (checked,plan.waves.size,jobsDone,"parallel")

/-- A compatible duplicate theorem still checks its incoming proof under a fresh
name. Self-reference uses module-local replay, never the prior binding. -/
def validateDuplicate (base : Kernel.Environment) (ci : ConstantInfo) (fresh : Name) : IO Unit := do
  match ci with
  | .thmInfo v =>
    if (base.find? fresh).isSome then throw <| IO.userError "duplicate validation name collision"
    let decl := Declaration.thmDecl { v with name := fresh, all := [fresh] }
    match base.addDeclCore 0 0 decl (cancelTk? := none) with
    | .ok _ => pure ()
    | .error ex => throw <| IO.userError (← ex.toMessageData {} |>.toString)
  | _ => throw <| IO.userError "duplicate validation requires theorem"
