import Lean
import Lean.Util.CollectAxioms
open Lean Elab
set_option maxHeartbeats 2000000
@[extern "rv_thread_cpu_ns"] opaque threadCpuNs : IO UInt64

structure UnitRow where
  target : String
  rawHB : Nat
  cpuNS : UInt64
  wallNS : Nat
  verdict : String
  error : String
  tid : UInt64
  deriving ToJson

@[noinline] def checked (base : Kernel.Environment) (decl : Declaration) :
    IO (Except Kernel.Exception Unit) := do
  match base.addDeclCore 2000000000 20000 decl none with
  | .ok _ => pure (.ok ())
  | .error ex => pure (.error ex)

def one (base : Kernel.Environment) (v : TheoremVal) (i : Nat) : IO UnitRow := do
  let n := Name.str `ReproKernel s!"unit{i}"
  let decl := Declaration.thmDecl {v with name := n, all := [n]}
  let tid ← IO.getTID
  let t0 ← IO.monoNanosNow
  let c0 ← threadCpuNs
  let a ← IO.getNumHeartbeats
  let result ← checked base decl
  let z ← IO.getNumHeartbeats
  let c1 ← threadCpuNs
  let t1 ← IO.monoNanosNow
  match result with
  | .ok _ => return ⟨v.name.toString,z-a,c1-c0,t1-t0,"accepted","",tid⟩
  | .error ex => return ⟨v.name.toString,z-a,c1-c0,t1-t0,"kernel_error",
      ← ex.toMessageData {} |>.toString,tid⟩

partial def commands (rows : Array Json := #[]) (messages : Array Message := #[]) :
    Frontend.FrontendM (Array Json × Array Message) := do
  Frontend.updateCmdPos
  let st0 ← get
  let ictx ← Frontend.getInputContext
  let scope := st0.commandState.scopes.head!
  let pmctx := {env := st0.commandState.env, options := scope.opts, currNamespace := scope.currNamespace, openDecls := scope.openDecls}
  let (cmd,ps,parseMsgs) := Parser.parseCommand ictx pmctx st0.parserState {}
  modify fun st => {st with commands := st.commands.push cmd}
  Frontend.setParserState ps
  Frontend.setMessages parseMsgs
  let c0 ← threadCpuNs
  let a ← IO.getNumHeartbeats
  Frontend.elabCommandAtFrontend cmd
  let z ← IO.getNumHeartbeats
  let c1 ← threadCpuNs
  let st ← get
  let row := Json.mkObj [("rawHB",toJson (z-a)),("cpuNS",toJson (c1-c0)),
    ("start",toJson st0.parserState.pos.byteIdx),
    ("end",toJson ps.pos.byteIdx),("kind",toJson cmd.getKind.toString)]
  let rows := rows.push row
  let messages := messages ++ parseMsgs.toArray ++ st.commandState.messages.toArray
  if Parser.isTerminalCommand cmd then return (rows,messages)
  commands rows messages

unsafe def elaborateOne (base : Environment) (ctx : Parser.InputContext)
    (ps : Parser.ModuleParserState) (headerMsgs : MessageLog)
    (file moduleText : String) (workers index : Nat) : IO Json := do
  let opts := ({} : Options) |>.set `maxHeartbeats (2000000 : Nat)
    |>.set `maxRecDepth (20000 : Nat) |>.setBool `Elab.async false
  let ((rows,msgs),st) ← ((commands).run {inputCtx := ctx}).run
    {commandState := Command.mkState base {} opts,parserState := ps,cmdPos := ps.pos}
  let env := st.commandState.env
  let mut errors := #[]
  for m in headerMsgs.toArray ++ msgs do
    if m.severity == .error then errors := errors.push (← m.data.toString)
  let mut names : Array String := #[]
  let mut sorryNames : Array String := #[]
  let mut newAxioms : Array String := #[]
  for (n,ci) in env.constants.map₂.toList do
    unless base.contains n do
      if let .axiomInfo _ := ci then newAxioms := newAxioms.push n.toString
      if let .thmInfo _ := ci then
        names := names.push n.toString
        let (ax,_) ← (collectAxioms n : CoreM _).toIO
          {fileName := file,fileMap := ctx.fileMap} {env}
        if ax.contains `sorryAx then sorryNames := sorryNames.push n.toString
  let verdict := if !errors.isEmpty then "lean_error"
    else if !sorryNames.isEmpty || !newAxioms.isEmpty then "incomplete" else "accepted"
  let tid ← IO.getTID
  return Json.mkObj [
    ("module",toJson moduleText),("workers",toJson workers),("index",toJson index),("tid",toJson tid),("verdict",toJson verdict),
    ("errors",toJson errors),("sorry",toJson sorryNames),("new_axioms",toJson newAxioms),
    ("theorems",toJson <| names.qsort (· < ·)),("commands",toJson rows),
    ("scope",toJson "synchronous full-source elaboration; command CPU includes tactics and kernel; not stock async task total")]

unsafe def main (args : List String) : IO UInt32 := do
  let [mode,moduleText,file,workersText] := args
    | throw <| IO.userError "usage: ModuleProbe (kernel|front) MODULE SOURCE WORKERS"
  let workers := workersText.toNat!
  unless [1,2,4,8].contains workers do throw <| IO.userError "workers"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let moduleName := moduleText.toName
  if mode == "front" then
    let text ← IO.FS.readFile file
    let ctx := Parser.mkInputContext text file
    let (header,ps,headerMsgs) ← Parser.parseHeader ctx
    let imported ← importModules (Elab.HeaderSyntax.imports header) {} 0 (loadExts := true)
    let base := imported.setMainModule moduleName
    let gate ← IO.Promise.new
    let mut tasks := #[]
    for worker in [:workers] do
      let job : IO (Array Json) := do
        discard <| IO.wait gate.result!
        let mut rows := #[]
        for i in [:8] do
          if i % workers == worker then
            rows := rows.push (← elaborateOne base ctx ps headerMsgs file moduleText workers i)
        return rows
      tasks := tasks.push (← job.asTask)
    gate.resolve ()
    for task in tasks do
      match task.get with
      | .ok rows => for row in rows do IO.println <| "FRONT " ++ row.compress
      | .error e => throw e
  else if mode == "kernel" || mode == "inventory" then
    let env ← importModules #[{module := moduleName}] {} 0 (loadExts := true)
    let some modIdx := env.getModuleIdx? moduleName
      | throw <| IO.userError "module absent"
    let mut candidates : Array TheoremVal := #[]
    let compute := ["UMoments9","BarrierData41","EnvelopePsiB"].any (fun s => moduleText.endsWith s)
    for (n,ci) in env.constants.toList do
      unless env.getModuleIdxFor? n == some modIdx do continue
      let .thmInfo v := ci | continue
      if compute && !v.value.cleanupAnnotations.getAppFn.isConstOf `of_decide_eq_true then continue
      candidates := candidates.push v
    candidates := candidates.qsort fun a b => a.name.toString < b.name.toString
    unless candidates.size > 0 do throw <| IO.userError s!"only {candidates.size} eligible theorems"
    let mut targets := #[]
    let count := candidates.size
    for i in [:count] do targets := targets.push candidates[i * (candidates.size-1) / (count-1)]!
    if moduleText.endsWith "EnvelopePsiB" then
      let heavy := "OAI.AtomicTriangular.FiniteCertificate.envelopeExpB16_calc._proof_1_1"
      if let some v := candidates.find? (fun x => x.name.toString == heavy) then
        targets := #[v] ++ candidates.filter (fun x => x.name != v.name)
    for v in targets do
      unless !v.value.hasSorry && !v.value.hasFVar && !v.value.hasMVar do
        throw <| IO.userError "not a closed checked input"
    if mode == "inventory" then
      IO.println <| "INVENTORY " ++ (Json.mkObj [("module",toJson moduleText),
        ("eligible",toJson candidates.size),("targets",toJson <| targets.map (fun v => v.name.toString))]).compress
      return 0
    let gate ← IO.Promise.new
    let mut tasks := #[]
    let base := env.toKernelEnv
    for worker in [:workers] do
      let job : IO (Array UnitRow) := do
        discard <| IO.wait gate.result!
        let mut rows := #[]
        for i in [:targets.size] do
          if i % workers == worker then rows := rows.push (← one base targets[i]! i)
        return rows
      tasks := tasks.push (← job.asTask)
    gate.resolve ()
    let mut rows := #[]
    for t in tasks do
      match t.get with
      | .ok r => rows := rows ++ r
      | .error e => throw e
    for r in rows.qsort (fun a b => a.target < b.target) do
      IO.println <| "KERNEL " ++ (Json.mkObj [("module",toJson moduleText),
        ("workers",toJson workers),("eligible",toJson candidates.size),("selected",toJson targets.size),("result",toJson r),
        ("kernel_poll_count",Json.null)]).compress
  else throw <| IO.userError "mode"
  return 0
