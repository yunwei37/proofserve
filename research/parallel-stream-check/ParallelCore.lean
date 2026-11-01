/- Checked declaration frontiers for a kernel-only stream.
   Original kernel handles all mathematics. This module and checked_commit.c
   are trusted coordination glue with explicit differential/fault qualification.
 -/
import Lean
import Std.Sync.Mutex
open Lean

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

private def checkOne (base : Kernel.Environment) (ci : ConstantInfo) (index : Nat) :
    IO CheckedToken := do
  let decl ← declarationOf ci
  let result := base.addDeclCore 0 0 decl (cancelTk? := none)
  match result with
  | .error error =>
    let message ← error.toMessageData {} |>.toString
    throw <| IO.userError s!"kernel_reject:{ci.name}:{message}"
  | .ok checked =>
    let some actual := checked.find? ci.name |
      throw <| IO.userError "invariant: checked kernel result missing"
    unless sameConstant actual ci do
      throw <| IO.userError s!"invariant: checked result representation differs:{ci.name}"
    return {frontier:=base,info:=actual,index}

private def worker (base : Kernel.Environment) (plan : Plan)
    (jobs : Array Nat) (queue : Std.Mutex Nat) : IO (Array CheckedToken) := do
  let mut results := #[]
  repeat
    let position ← queue.atomically do
      let i ← get
      set (i+1)
      pure i
    if position >= jobs.size then break
    let index := jobs[position]!
    results := results.push (← checkOne base plan.constants[index]! index)
  return results

/-- A checked frontier is committed in original input-index order, after all jobs finish. -/
def parallelReplay (data : ModuleData) (map : Std.HashMap Name ConstantInfo)
    (base : Kernel.Environment) (workers : Nat) (fault : String := "none") :
    IO (Kernel.Environment × Nat × Nat × String) := do
  let some plan := makePlan data map |
    return (← base.replay map,0,0,"upstream_complex_or_cycle")
  let mut checked := base
  let mut jobsDone := 0
  for wave in plan.waves do
    let queue ← Std.Mutex.new 0
    let mut tasks := #[]
    for _ in [:min workers wave.size] do
      tasks := tasks.push (← IO.asTask <| worker checked plan wave queue)
    let mut tokens : Array CheckedToken := #[]
    let mut error : Option IO.Error := none
    for task in tasks do
      match task.get with
      | .ok values => tokens := tokens ++ values
      | .error e => if error.isNone then error := some e
    if let some e := error then throw e
    if fault=="duplicate" && tokens.size>1 then
      if let some second := tokens[1]? then tokens := tokens.set! 0 second
    tokens := tokens.qsort fun a b => a.index < b.index
    unless tokens.map (·.index) == wave do
      throw <| IO.userError "invariant: checked-index cover differs"
    for token in tokens do
      unless sameConstant token.info plan.constants[token.index]! do
        throw <| IO.userError "invariant: checked payload does not match job"
      if (checked.find? token.info.name).isSome then
        throw <| IO.userError "invariant: checked commit would overwrite constant"
    if fault=="stale" && !tokens.isEmpty then
      let other ← mkEmptyEnvironment
      checked ← commitChecked other.toKernelEnv tokens
    else checked ← commitChecked checked tokens
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
