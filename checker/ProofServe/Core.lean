/- Original Lean kernel checks; audited scheduling and checked-frontier commits. -/
import Lean
import Std.Sync.Mutex
open Lean
namespace ProofServe
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

/-- Conservative dependency closure for declarations that the ordinary
    per-declaration checker cannot construct. Every inductive/constructor/recursor
    stays in upstream replay, together with its ordinary prerequisites.
    This is not a claim that distinct inductive groups must run serially. -/
def complexPrefix (map : Std.HashMap Name ConstantInfo) : Std.HashMap Name ConstantInfo := Id.run do
  let mut keep : Std.HashMap Name ConstantInfo := {}
  let mut todo := map.toList.filterMap fun (_,ci) =>
    if !ci.isUnsafe && !ci.isPartial && !ordinary ci then some ci.name else none
  while !todo.isEmpty do
    let name := todo.head!
    todo := todo.tail!
    if keep.contains name then continue
    if let some ci := map[name]? then
      if ci.isUnsafe || ci.isPartial then continue
      keep := keep.insert name ci
      todo := ci.getUsedConstantsAsSet.toList ++ todo
  return keep


private structure CheckedToken where
  frontier : Kernel.Environment
  info : ConstantInfo
  index : Nat
@[extern "ps_commit_checked"] private opaque commitChecked
  (base : Kernel.Environment) (tokens : Array CheckedToken) : IO Kernel.Environment
@[extern "ps_persist_base"] private opaque persistBase (base : Kernel.Environment) : IO Kernel.Environment
@[extern "ps_total_cpu_ns"] opaque totalCpuNs : IO UInt64
@[extern "ps_process_ns"] opaque processNs : IO UInt64
@[extern "ps_default_workers"] opaque defaultWorkers : IO UInt32
@[extern "ps_pin_performance"] opaque pinPerformance : IO Unit

private def checkOne (base : Kernel.Environment) (ci : ConstantInfo) (index : Nat) :
    IO CheckedToken := do
  let decl ← declarationOf ci
  match base.addDeclCore 0 0 decl (cancelTk? := none) with
  | .error ex => throw <| IO.userError s!"kernel_reject:{ci.name}:{← ex.toMessageData {} |>.toString}"
  | .ok checked =>
    let some actual := checked.find? ci.name | throw <| IO.userError "checked result missing"
    unless sameConstant actual ci do throw <| IO.userError "checked payload differs"
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

private def batch (base : Kernel.Environment) (plan : Plan) (wave : Array Nat)
    (workers : Nat) : IO Kernel.Environment := do
  -- Every prior worker is joined. No concurrent access while marking.
  let base ← persistBase base
  let queue ← Std.Mutex.new 0
  let count := min workers wave.size
  let gate ← IO.Promise.new
  let mut tasks := #[]
  let mut error : Option IO.Error := none
  try
    for _ in [:count] do
      if count > 1 then
        let started ← IO.Promise.new
        let task ← IO.asTask do
          started.resolve (1 : Nat)
          unless gate.result?.get == some (1 : Nat) do
            throw <| IO.userError "worker gate abandoned"
          worker base plan wave queue
        tasks := tasks.push task
        unless started.result?.get == some (1 : Nat) do
          throw <| IO.userError "worker did not start"
      else tasks := tasks.push (← IO.asTask <| worker base plan wave queue)
  catch e => error := some e
  gate.resolve (1 : Nat)
  let mut tokens := #[]
  for task in tasks do
    match task.get with
    | .ok values => tokens := tokens ++ values
    | .error e => if error.isNone then error := some e
  if let some e := error then throw e
  tokens := tokens.qsort fun a b => a.index < b.index
  unless tokens.map (·.index) == wave do throw <| IO.userError "frontier cover differs"
  for token in tokens do
    unless sameConstant token.info plan.constants[token.index]! do
      throw <| IO.userError "frontier payload differs"
    if (base.find? token.info.name).isSome then
      throw <| IO.userError "frontier overwrites a constant"
  commitChecked base tokens

/-- Nonordinary declarations and their dependencies use upstream replay.
    All remaining acyclic ordinary declarations use original-kernel workers. -/
def parallelReplay (data : ModuleData) (map : Std.HashMap Name ConstantInfo)
    (base : Kernel.Environment) (workers : Nat) : IO Kernel.Environment := do
  let serialPart := if (← IO.getEnv "PROOFSERVE_SPLIT") == some "0" then map else complexPrefix map
  let remaining := map.filter fun n _ => !serialPart.contains n
  let checked ← if serialPart.isEmpty then pure base else base.replay serialPart
  let some plan := makePlan data remaining | return ← checked.replay remaining
  let mut checked := checked
  for wave in plan.waves do checked ← batch checked plan wave workers
  return checked

def validateDuplicate (base : Kernel.Environment) (ci : ConstantInfo) (fresh : Name) : IO Unit := do
  let .thmInfo v := ci | throw <| IO.userError "duplicate validation requires theorem"
  if (base.find? fresh).isSome then throw <| IO.userError "duplicate name collision"
  match base.addDeclCore 0 0 (.thmDecl {v with name:=fresh,all:=[fresh]}) (cancelTk? := none) with
  | .ok _ => pure ()
  | .error ex => throw <| IO.userError (← ex.toMessageData {} |>.toString)
end ProofServe
