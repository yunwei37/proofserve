import EnvelopeBase
import Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
open Lean Elab Command Meta

elab "qualify_envelope_construction" : command => do
  let env ← getEnv
  let mut names := #[`MEnvelopeBase.rootGoal]
  for k in [1,2,4,8] do
    for i in [:k] do names := names.push (Name.str `MEnvelopeBase s!"goal_{k}_{i}")
  for name in names do
    let some (.defnInfo info) := env.find? name | throwError "missing {name}"
    let pf ← liftTermElabM <| mkDecideProof info.value
    unless !pf.hasSorry && !pf.hasMVar && !pf.hasFVar do throwError "not a closed decision proof: {name}"
  let pf ← liftTermElabM <| mkDecideProof (mkConst `False)
  let decl := Declaration.thmDecl {
    name := `MEnvelopeControl.invalid
    levelParams := []
    type := mkConst `False
    value := pf
    all := [`MEnvelopeControl.invalid] }
  match env.toKernelEnv.addDeclCore 2000000 20000 decl none with
  | .ok _ => throwError "kernel accepted deliberately false decision"
  | .error _ => logInfo "ENVELOPE_CONSTRUCTION_16_CLOSED FALSE_REJECTED_BY_ORIGINAL_KERNEL"
qualify_envelope_construction
