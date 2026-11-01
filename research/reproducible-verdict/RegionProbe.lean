import Lean
import Lean.Util.CollectAxioms
open Lean

set_option maxHeartbeats 2000000

structure Result where
  target : String
  rawHB : Nat
  wallNS : Nat
  verdict : String
  error : String
  tid : UInt64
  startNS : Nat
  stopNS : Nat
  deriving ToJson

@[noinline] def checkOutcome (base : Kernel.Environment) (decl : Declaration) :
    IO (Except Kernel.Exception Unit) := do
  match base.addDeclCore 2000000000 20000 decl none with
  | .ok _ => pure (.ok ())
  | .error ex => pure (.error ex)

def checkOne (base : Kernel.Environment) (v : TheoremVal) (index : Nat) :
    IO Result := do
  let name := Name.str `ReproKernel s!"unit{index}"
  let decl := Declaration.thmDecl {v with name, all := [name]}
  let tid ← IO.getTID
  let time0 ← IO.monoNanosNow
  let start ← IO.getNumHeartbeats
  let result ← checkOutcome base decl
  let stop ← IO.getNumHeartbeats
  let time1 ← IO.monoNanosNow
  match result with
  | .ok _ => return ⟨v.name.toString,stop-start,time1-time0,"accepted","",tid,time0,time1⟩
  | .error ex => return ⟨v.name.toString,stop-start,time1-time0,"kernel_error",
      ← ex.toMessageData {} |>.toString,tid,time0,time1⟩

unsafe def main (args : List String) : IO UInt32 := do
  let [moduleText,workersText] := args
    | throw <| IO.userError "usage: RegionProbe module workers"
  let workers := workersText.toNat!
  unless [1,2,4,8].contains workers do throw <| IO.userError "unsupported workers"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let moduleName := moduleText.toName
  let env ← importModules #[{module := moduleName}] {} 0 (loadExts := true)
  let some modIdx := env.getModuleIdx? moduleName
    | throw <| IO.userError "module absent"
  let mut targets : Array TheoremVal := #[]
  for (n,ci) in env.constants.toList do
    unless env.getModuleIdxFor? n == some modIdx do continue
    let .thmInfo v := ci | continue
    -- Actual stored decide-kernel proof objects, no generated toy computation.
    unless v.value.cleanupAnnotations.getAppFn.isConstOf `of_decide_eq_true do continue
    targets := targets.push v
  targets := targets.qsort fun a b => a.name.toString < b.name.toString
  if moduleText == "OAI.Analysis.Triangular.Envelope.EnvelopePsiB" then
    let priority := "OAI.AtomicTriangular.FiniteCertificate.envelopeExpB16_calc._proof_1_1".toName
    let some heavy := targets.find? (fun x => x.name == priority)
      | throw <| IO.userError "retained measured-heavy Envelope target missing"
    targets := #[heavy] ++ targets.filter (fun x => x.name != priority)
  targets := targets.extract 0 (min 8 targets.size)
  unless targets.size == 8 do throw <| IO.userError s!"need8 actual targets, got{targets.size}"
  for v in targets do
    unless !v.value.hasSorry && !v.value.hasMVar && !v.value.hasFVar do
      throw <| IO.userError "source proof not closed"
  -- Preparation forces proof thunks before the measured check. Its cost is in
  -- whole-process wall, but not in the per-unit allocation counter.
  let base := env.toKernelEnv
  let gate ← IO.Promise.new
  let mut tasks := #[]
  for worker in [:workers] do
    let job : IO (Array Result) := do
      discard <| IO.wait gate.result!
      let mut results := #[]
      for i in [:targets.size] do
        if i % workers == worker then
          results := results.push (← checkOne base targets[i]! i)
      return results
    tasks := tasks.push (← job.asTask)
  gate.resolve ()
  let mut results := #[]
  for task in tasks do
    match task.get with
    | .ok rows => results := results ++ rows
    | .error ex => throw ex
  results := results.qsort fun a b => a.target < b.target
  for row in results do
    IO.println <| "REGION " ++ (Json.mkObj [
      ("module",toJson moduleText),("workers",toJson workers),("result",toJson row),
      ("scope",toJson "kernel-only original proof-object replay after explicit preparation"),
      ("native_kernel_poll_count",Json.null)]).compress
  return 0
