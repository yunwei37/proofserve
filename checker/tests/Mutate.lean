
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
  if kind=="staged" || kind=="staged-good" then
    -- The O review fixture: good exported/server parts plus an invalid private
    -- theorem. The optional parts are installed only after a genuine receipt.
    let good := {data with isModule:=true}
    let some (.axiomInfo ax) := data.constants.find? (fun ci => match ci with
      | .axiomInfo a => a.type.isSort
      | _ => false) | throw <| IO.userError "no proposition axiom template"
    let some (.thmInfo th) := data.constants.find? (fun ci => match ci with
      | .thmInfo _ => true
      | _ => false) | throw <| IO.userError "no theorem template"
    let freshAx := "ReviewUnwitnessed".toName
    let freshThm := "ReviewSmuggled".toName
    let extraAx := ConstantInfo.axiomInfo {ax with name:=freshAx}
    let extraThm := ConstantInfo.thmInfo {th with name:=freshThm, all := [freshThm], type:=mkConst freshAx, value:=.bvar 0}
    let bad := { good with constants := good.constants ++ #[extraAx, extraThm], constNames := good.constNames ++ #[freshAx, freshThm] }
    saveModuleDataParts moduleName.toName #[
      (System.FilePath.mk output,good),
      (System.FilePath.mk (output++".server"),good),
      (System.FilePath.mk (output++".private"),if kind=="staged-good" then good else bad)]
    return
  let mut changed := false
  let mut constants : Array ConstantInfo := #[]
  for original in data.constants do
    let mut ci := original
    if !changed then
      if let .thmInfo info := ci then
        changed := true
        let value := if kind=="bvar" then Expr.bvar 0
          else if kind=="sibling" then mkConst "Shared.externalProof".toName
          else if kind=="unknown" then mkConst "ProofServeMissingConstant".toName
          else mkSort (.succ .zero)
        ci := .thmInfo {info with value}
    constants := constants.push ci
  unless changed do throw <| IO.userError "no theorem to mutate"
  saveModuleData output moduleName.toName {data with constants}
