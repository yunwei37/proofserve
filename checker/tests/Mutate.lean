
import Lean
open Lean
set_option maxHeartbeats 100000
unsafe def main (args : List String) : IO Unit := do
  let [input,moduleName,output,kind] := args | throw <| IO.userError "mutator arguments"
  let parts ← readModuleDataParts #[System.FilePath.mk input]
  let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "missing module"
  if kind=="imports" then
    unless data.constants.isEmpty do throw <| IO.userError "expected empty module"
    let imports : Array Import := #[{module:="ShadowLeft".toName},{module:="ShadowRight".toName}]
    saveModuleData output moduleName.toName {data with imports}
    return
  let mut changed := false
  let mut constants : Array ConstantInfo := #[]
  for original in data.constants do
    let mut ci := original
    if !changed then
      if let .thmInfo info := ci then
        changed := true
        let value := if kind=="bvar" then Expr.bvar 0
          else if kind=="unknown" then mkConst "ProofServeMissingConstant".toName
          else mkSort (.succ .zero)
        ci := .thmInfo {info with value}
    constants := constants.push ci
  unless changed do throw <| IO.userError "no theorem to mutate"
  saveModuleData output moduleName.toName {data with constants}
