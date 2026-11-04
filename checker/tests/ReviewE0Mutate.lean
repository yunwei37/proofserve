import Lean
open Lean
set_option maxHeartbeats 200000
unsafe def main (args : List String) : IO Unit := do
  let [input, moduleName, output, kind] := args | throw <| IO.userError "arguments"
  let parts ← readModuleDataParts #[System.FilePath.mk input]
  let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "module"
  if kind=="inactive-parts" then
    let bad := {data with isModule:=false, constants:=data.constants.map (fun ci => match ci with
      | .thmInfo th => .thmInfo {th with value:=.bvar 0}
      | _ => ci)}
    let good := {data with isModule:=false}
    saveModuleDataParts moduleName.toName #[
      (System.FilePath.mk output,bad),
      (System.FilePath.mk (output++".server"),good),
      (System.FilePath.mk (output++".private"),good)]
  else if kind=="unsafe-reference" then
    let constants := data.constants.map fun ci => match ci with
      | .thmInfo th => .thmInfo {th with value:=mkConst "foo".toName}
      | _ => ci
    saveModuleData output moduleName.toName {data with constants}
  else if kind=="native-print" then
    let truth := mkConst "Bool.true".toName
    let refl := mkApp2 (mkConst "Eq.refl".toName [.succ .zero]) (mkConst "Bool".toName) truth
    let proof := mkApp3 (mkConst "Lean.ofReduceBool".toName) (mkConst "printBool".toName) truth refl
    let constants := data.constants.map fun ci => match ci with
      | .thmInfo th => .thmInfo {th with value:=proof}
      | _ => ci
    saveModuleData output moduleName.toName {data with constants}
  else if kind=="quot-only" then
    initSearchPath (← findSysroot)
    let env ← importModules #[{module:="Init.Prelude".toName}] {} 0
    let mut todo := ["Quot".toName,"Quot.mk".toName,"Quot.lift".toName,"Quot.ind".toName]
    let mut seen : NameSet := {}
    let mut constants : Array ConstantInfo := #[]
    while !todo.isEmpty do
      let name := todo.head!
      todo := todo.tail!
      if seen.contains name then continue
      seen := seen.insert name
      let some ci := env.find? name | throw <| IO.userError s!"missing primitive {name}"
      constants := constants.push ci
      todo := ci.getUsedConstantsAsSet.toList ++ todo
      if let .inductInfo info := ci then
        todo := info.all ++ info.ctors ++ [Name.str info.name "rec"] ++ todo
    saveModuleData output moduleName.toName {data with isModule:=false, imports:=#[], constants, constNames:=constants.map (·.name), entries:=#[]}
  else if kind=="nonprop-theorem" then
    let constants := data.constants.map fun ci => match ci with
      | .defnInfo info => .thmInfo {name:=info.name,type:=info.type,levelParams:=info.levelParams,value:=info.value,all:=info.all}
      | _ => ci
    saveModuleData output moduleName.toName {data with constants}
  else if kind=="duplicate-imports" then
    saveModuleData output moduleName.toName {data with imports:=#[{module:="Aaa".toName},{module:="Bbb".toName}]}
  else
    let constants := data.constants.map fun ci => match ci with
      | .thmInfo th => .thmInfo {th with value:=.bvar 0}
      | _ => ci
    saveModuleData output moduleName.toName {data with constants}
