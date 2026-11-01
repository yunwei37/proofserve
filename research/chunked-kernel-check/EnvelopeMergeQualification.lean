/- Historical v6control: run only with frozen v6Base and its v2child. It revealed Quot.sound; do not mix its child with the repaired Base binary. -/
import Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
open Lean Elab Command Meta
elab "qualify_kernel_only_merge" : command => do
  let imports : Array Import := #[{module := `EnvelopeK1Part0}]
  let (_, state) ← importModulesCore imports |>.run
  let imported ← finalizeImport state imports {} 0 false false (isModule := true)
  let some (.defnInfo root) := imported.find? `MEnvelopeBase.rootGoal | throwError "missing root"
  let value := mkApp (mkConst `MEnvelopeBase.merge_1) (mkConst `EnvelopeK1Part0.proof)
  let decl := Declaration.thmDecl {
    name := `MQualMerged.result
    levelParams := []
    type := root.value
    value
    all := [`MQualMerged.result] }
  let checked ← match imported.addDeclCore 2000000000 20000 decl none with
    | .ok e => pure e
    | .error _ => throwError "original kernel rejected final merge"
  let axs ← liftTermElabM <| withEnv checked <| collectAxioms `MQualMerged.result
  unless axs.toList == [`propext] do throwError "unexpected axioms {axs}"
  logInfo "KERNEL_ONLY_MERGE_VALID target=true axioms=[propext]"
qualify_kernel_only_merge
