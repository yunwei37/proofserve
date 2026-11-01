import Lean
open Lean
set_option maxHeartbeats 200000
def main : IO Unit := do
  let some root ← IO.getEnv "PARALLEL_CONTROL_OUT" | throw <| IO.userError "missing output"
  let helper := `Shared.helper
  let theoremName := `Shared.t
  let makeThm (name body : Name) : ConstantInfo := .thmInfo {
    name,levelParams:=[],type:=mkConst `True,value:=mkConst body,all:=[name]}
  let constants := #[makeThm helper theoremName,makeThm theoremName helper]
  saveModuleData (System.FilePath.mk root / "Cyclic.olean") `Cyclic {isModule := false, imports := #[{module := `Init.Prelude}], constNames := constants.map (·.name), constants := constants, extraConstNames := #[], entries := #[]}
