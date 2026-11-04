import Lean
open Lean
set_option maxHeartbeats 200000

unsafe def main (args : List String) : IO Unit := do
  match args with
  | ["hash", file] =>
    IO.println (toJson (hash (← IO.FS.readBinFile file))).compress
  | "axioms" :: roots =>
    initSearchPath (← findSysroot)
    if let some paths ← IO.getEnv "LEAN_PATH" then
      searchPathRef.set ((paths.splitOn ":").map System.FilePath.mk)
    let imports := roots.toArray.map (fun s => ({module:=s.toName,importAll:=true} : Import))
    let env ← importModules imports {} 0
    let names := SMap.fold (fun a n ci => match ci with
      | .axiomInfo _ => a.push n.toString
      | _ => a) (#[] : Array String) env.toKernelEnv.constants
    IO.println (toJson (names.qsort (· < ·))).compress
  | [input, moduleName, output, kind] =>
    let parts ← readModuleDataParts #[System.FilePath.mk input]
    let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "no module data"
    let mut changed := false
    let mut constants := data.constants
    if kind == "bad" || kind == "staged" then
      constants := data.constants.map fun ci =>
        match ci with
        | .thmInfo info => .thmInfo {info with value:=.bvar 0}
        | _ => ci
      changed := data.constants.any (fun ci => match ci with | .thmInfo _ => true | _ => false)
    let imports := if kind=="conflict" then
      #[({module:="ClashLeft".toName} : Import),{module:="ClashRight".toName}] else data.imports
    if kind=="bad" && !changed then throw <| IO.userError "no theorem"
    if kind=="staged" then
      let good := {data with isModule:=true}
      let some templateAx := data.constants.find? (fun ci => match ci with
        | .axiomInfo a => a.type.isSort
        | _ => false) | throw <| IO.userError "no proposition axiom template"
      let .axiomInfo ax := templateAx | throw <| IO.userError "axiom template"
      let some templateThm := data.constants.find? (fun ci => match ci with
        | .thmInfo _ => true | _ => false) | throw <| IO.userError "no theorem template"
      let .thmInfo th := templateThm | throw <| IO.userError "theorem template"
      let freshAx := "ReviewUnwitnessed".toName
      let freshThm := "ReviewSmuggled".toName
      let extraAx := ConstantInfo.axiomInfo {ax with name:=freshAx}
      let extraThm := ConstantInfo.thmInfo {th with name:=freshThm,all:=[freshThm],
        type:=mkConst freshAx,value:=.bvar 0}
      let bad := {good with constants:=good.constants++#[extraAx,extraThm],
        constNames:=good.constNames++#[freshAx,freshThm]}
      saveModuleDataParts moduleName.toName #[
        (System.FilePath.mk output,good),
        (System.FilePath.mk (output++".server"),good),
        (System.FilePath.mk (output++".private"),bad)]
    else
      saveModuleData output moduleName.toName {data with constants,imports}
  | _ => throw <| IO.userError "review mutator arguments"
