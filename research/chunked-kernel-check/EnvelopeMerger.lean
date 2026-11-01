import Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
open Lean Elab Command Meta
@[extern "ck_cpu_ns"] opaque cpuNs : IO UInt64

elab "merge_envelope_run" : command => do
  if (← IO.getEnv "CK_PREPARE") == some "1" then return
  let k := ((← IO.getEnv "CK_K").getD "1").toNat!
  unless [1,2,4,8].contains k do throwError "invalid k"
  let some root ← IO.getEnv "CK_OUT" | throwError "missing output"
  let before ← IO.monoNanosNow
  let cpuBefore ← cpuNs
  let imports : Array Import := (Array.range k).map fun i =>
    {module := Name.mkSimple s!"EnvelopeK{k}Part{i}"}
  let (_, state) ← importModulesCore imports |>.run
  let imported ← finalizeImport state imports {} 0 false false (isModule := true)
  let importStop ← IO.monoNanosNow
  let some (.defnInfo goal) := imported.find? `MEnvelopeBase.rootGoal | throwError "missing goal"
  let values := (Array.range k).map fun i => mkConst (Name.str (Name.mkSimple s!"EnvelopeK{k}Part{i}") "proof")
  let value := mkAppN (mkConst (Name.str `MEnvelopeBase s!"merge_{k}")) values
  let name := `EnvelopeCombined.result
  let decl := Declaration.thmDecl {name,levelParams:=[],type:=goal.value,value,all:=[name]}
  let checked ← match (imported.setMainModule `EnvelopeCombined).addDeclCore 2000000000 20000 decl none with
    | .ok env => pure env
    | .error _ => throwError "original C++ kernel rejected combined theorem"
  let finalStop ← IO.monoNanosNow
  let axioms ← liftTermElabM <| withEnv checked <| collectAxioms name
  unless axioms.toList == [`propext] do throwError "unexpected axioms {axioms}"
  let some (.thmInfo final) := checked.find? name | throwError "missing final theorem"
  unless final.type == goal.value && !final.value.hasSorry do throwError "final target or proof changed"
  let auditStop ← IO.monoNanosNow
  writeModule checked (System.FilePath.mk root / "EnvelopeCombined.olean") (writeIR := false)
  let stop ← IO.monoNanosNow
  let cpuStop ← cpuNs
  IO.println s!"CK_MERGE_PARTS {importStop-before} {finalStop-importStop} {auditStop-finalStop} {stop-auditStop}"
  IO.println s!"CK_MERGE_RESULT {stop-before} {cpuStop-cpuBefore}"
  IO.println s!"CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={k}"
merge_envelope_run
