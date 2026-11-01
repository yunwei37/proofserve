import Lean
import Lean.Util.CollectAxioms
open Lean Elab

set_option maxHeartbeats 2000000

/-- Count each command on its executing thread, before allocating receipt JSON.
    This path deliberately disables asynchronous elaboration; its counters are
    not silently presented as stock async whole-process accounting. -/
partial def countedCommands
    (counts : Array Nat := #[]) (messages : Array Message := #[]) :
    Frontend.FrontendM (Array Nat × Array Message) := do
  let a ← IO.getNumHeartbeats
  -- Keep parser diagnostics before elabCommandTopLevel resets its message log.
  -- v1's legacy frontend call lost them; its captures stay unmodified.
  Frontend.updateCmdPos
  let st0 ← get
  let ictx ← Frontend.getInputContext
  let scope := st0.commandState.scopes.head!
  let pmctx := {env := st0.commandState.env,options := scope.opts, currNamespace := scope.currNamespace,openDecls := scope.openDecls}
  let (cmd,ps,parseMsgs) := Parser.parseCommand ictx pmctx st0.parserState {}
  modify fun st => {st with commands := st.commands.push cmd}
  Frontend.setParserState ps
  Frontend.setMessages parseMsgs
  Frontend.elabCommandAtFrontend cmd
  let done := Parser.isTerminalCommand cmd
  let b ← IO.getNumHeartbeats
  let st ← get
  let counts := counts.push (b-a)
  let messages := messages ++ parseMsgs.toArray ++ st.commandState.messages.toArray
  if done then return (counts,messages)
  countedCommands counts messages

def field [FromJson α] (j : Json) (key : String) (fallback : α) : α :=
  (j.getObjValAs? α key).toOption.getD fallback


/-- Only ordinary new declarations are supported by this prototype's extra
    kernel replay. Complex inductive groups explicitly fall back as unsupported. -/
def replayDeclaration (ci : ConstantInfo) : Option Declaration :=
  match ci with
  | .defnInfo d => some <| .defnDecl d
  | .thmInfo d => some <| .thmDecl d
  | .opaqueInfo d => some <| .opaqueDecl d
  | _ => none

partial def constantReferences : Expr → List Name
  | .const n _ => [n]
  | .app f a => constantReferences f ++ constantReferences a
  | .lam _ t b _ | .forallE _ t b _ => constantReferences t ++ constantReferences b
  | .letE _ t v b _ => constantReferences t ++ constantReferences v ++ constantReferences b
  | .mdata _ e | .proj _ _ e => constantReferences e
  | _ => []

partial def replayOrdinary (kenv : Kernel.Environment)
    (pending : List ConstantInfo) (budget : Nat) : IO (String × String) := do
  if pending.isEmpty then return ("checked","")
  let ready := pending.find? fun ci =>
    (constantReferences ci.type ++ (ci.value? true).toList.flatMap constantReferences).all
      fun n => (kenv.find? n).isSome
  let some ci := ready | return ("unsupported","cyclic or complex new declarations")
  let some decl := replayDeclaration ci | return ("unsupported","nonordinary declaration")
  match kenv.addDeclCore (budget*1000).toUSize (4000 : Nat).toUSize decl none with
  | .error ex => return ("rejected", ← ex.toMessageData {} |>.toString)
  | .ok next => replayOrdinary next (pending.filter (·.name != ci.name)) budget

unsafe def main (args : List String) : IO UInt32 := do
  let [path] := args | throw <| IO.userError "usage: lean --run Probe.lean requests.json"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let reqs ← IO.ofExcept <| (← IO.ofExcept <| Json.parse (← IO.FS.readFile path)).getArr?
  let base ← importModules #[{module := `Mathlib}] {} 0 (loadExts := true)
  let base := base.setMainModule `ReproCandidate
  for j in reqs do
    let id := field j "id" "unknown"
    let source := field j "code" ""
    let mode := field j "mode" "sync"
    let observer := field j "observer" "off"
    let budget := field j "budget" (3000 : Nat)
    let target := (field j "target" "").toName
    let opts := ({} : Options) |>.set `maxHeartbeats budget
      |>.set `maxRecDepth (4000 : Nat) |>.setBool `Elab.async (mode == "stock")
      |>.setBool `trace.profiler (observer == "trace")
      |>.set `trace.profiler.threshold (0 : Nat)
      |>.setBool `profiler (observer == "native")
    let ctx := Parser.mkInputContext source id
    let before ← IO.getNumHeartbeats
    let (env,msgs,units) ← if mode == "stock" then do
      let st ← IO.processCommands ctx {} (Command.mkState base {} opts)
      pure (st.commandState.env,st.commandState.messages.toArray,#[])
    else do
      let ((units,msgs),st) ← ((countedCommands).run {inputCtx := ctx}).run
        {commandState := Command.mkState base {} opts,parserState := {},cmdPos := 0}
      pure (st.commandState.env,msgs,units)
    -- Force all checked environment tasks before classifying anything.
    let ci := env.constants.find? target
    let after ← IO.getNumHeartbeats
    let mut errors : Array String := #[]
    let mut warnings : Array String := #[]
    for m in msgs do
      if m.severity == .error then errors := errors.push (← m.data.toString)
      if m.severity == .warning then warnings := warnings.push (← m.data.toString)
    let axioms ← (if ci.isSome then collectAxioms target else pure #[] : CoreM _).toIO
      {fileName := id,fileMap := ctx.fileMap} {env}
    let ax := axioms.1.map Name.toString
    let isTheorem := match ci with | some (.thmInfo _) => true | _ => false
    let sorryUsed := ax.contains "sorryAx"
    let newAxioms := env.constants.map₂.toList.filterMap fun (n,c) =>
      if base.contains n then none else match c with
        | .axiomInfo _ => some n.toString
        | _ => none
    let replayStart ← IO.getNumHeartbeats
    let (recheck,recheckError) ← if errors.isEmpty && isTheorem && !sorryUsed && newAxioms.isEmpty then
      replayOrdinary base.toKernelEnv
        (env.constants.map₂.toList.filterMap fun (n,c) => if base.contains n then none else some c) budget
      else pure ("not-attempted","")
    let replayStop ← IO.getNumHeartbeats
    let verdict := if errors.any (·.contains "heartbeats") then "budget_exhausted"
      else if !errors.isEmpty then "lean_error"
      else if !isTheorem || sorryUsed || !newAxioms.isEmpty then "incomplete"
      else if recheck == "checked" then "accepted" else "recheck_" ++ recheck
    IO.println <| "REPRO " ++ (Json.mkObj [
      ("id",toJson id),("mode",toJson mode),("observer",toJson observer),
      ("budget",toJson budget),("verdict",toJson verdict),
      ("kernel_replay",toJson recheck),("kernel_replay_error",toJson recheckError),
      ("kernel_replay_allocation_delta",toJson (replayStop-replayStart)),
      ("kernel_poll_counter",Json.null),
      ("main_thread_raw_heartbeats",toJson (after-before)),
      ("command_raw_heartbeats",toJson units),("errors",toJson errors),
      ("warnings",toJson warnings),("target",toJson target.toString),
      ("theorem_present",toJson isTheorem),("axioms",toJson ax),
      ("new_axioms",toJson newAxioms),
      ("accounting",toJson (if mode == "stock" then "main-thread-only-not-total"
        else "synchronous-command-deltas-not-arbitrary-child-tasks"))]).compress
    (← IO.getStdout).flush
  return 0
