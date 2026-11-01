import EnvelopeStreamBase
import Lean
open Lean Elab Command Meta
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
elab "prepare_stream_chunks" : command => do
  let some root ← IO.getEnv "PARALLEL_PREPARED_OUT" | throwError "missing output"
  let schemaText ← IO.FS.readFile (System.FilePath.mk root / "schemas.json")
  let schema ← ofExcept <| Json.parse schemaText
  let specs ← ofExcept <| schema.getObjValAs? (Array Json) "specs"
  let env ← getEnv
  for spec in specs do
    let ident ← ofExcept <| spec.getObjValAs? String "id"
    for k in [1,2,4,8] do
      let mut constants := #[]
      for i in [:k] do
        let goal := Name.str `MEnvelopeStream s!"goal_{ident}_{k}_{i}"
        let some (.defnInfo d) := env.find? goal | throwError "missing generated goal"
        let pf ← liftTermElabM do instantiateMVars (← mkDecideProof d.value)
        unless !pf.hasSorry && !pf.hasMVar && !pf.hasFVar do
          throwError "unclosed prepared proof"
        let name := Name.str `MEnvelopeStream s!"chunk_{ident}_{k}_{i}"
        constants := constants.push (ConstantInfo.thmInfo {
          name,levelParams:=[],type:=d.value,value:=pf,all:=[name]})
      let data : ModuleData := {isModule := false, imports := #[], constNames := constants.map (·.name), constants := constants, extraConstNames := #[], entries := #[]}
      saveModuleData (System.FilePath.mk root / s!"chunks_{ident}_{k}.olean") `MEnvelopeStream data
      IO.println s!"PREPARED_UNTRUSTED {ident} {k}"
prepare_stream_chunks
