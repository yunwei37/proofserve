import Lean
open Lean
set_option maxHeartbeats 200000
/-- Exactly the second review's proposed malformed quotient metadata control. -/
unsafe def main (args : List String) : IO Unit := do
  let [root, output] := args | throw <| IO.userError "arguments"
  initSearchPath (← findSysroot)
  let env ← importModules #[{module:=root.toName}] {} 0
  let mut todo := ["quotValue".toName,"quotRfl".toName]
  let mut seen : NameSet := {}
  let mut constants : Array ConstantInfo := #[]
  while !todo.isEmpty do
    let name := todo.head!
    todo := todo.tail!
    if seen.contains name then continue
    seen := seen.insert name
    let some ci := env.find? name | throw <| IO.userError s!"missing {name}"
    todo := ci.getUsedConstantsAsSet.toList ++ todo
    if let .inductInfo info := ci then
      todo := info.all ++ info.ctors ++ [Name.str info.name "rec"] ++ todo
    let ci := match ci with
      | .quotInfo info => .axiomInfo {name:=info.name,type:=info.type,levelParams:=info.levelParams,isUnsafe:=false}
      | _ => ci
    constants := constants.push ci
  saveModuleData output "ZFake".toName {
    isModule:=false,imports:=#[],constNames:=constants.map (·.name),constants,extraConstNames:=#[],entries:=#[]}
