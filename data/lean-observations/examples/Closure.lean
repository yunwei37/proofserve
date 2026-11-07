import Lean
open Lean
set_option maxHeartbeats 500000
unsafe def main (args : List String) : IO Unit := do
  let [root] := args | throw <| IO.userError "root"
  initSearchPath (← findSysroot)
  let env ← importModules #[{module := root.toName}] {} 0
  let rows ← env.header.moduleNames.mapM fun n => do
    return Json.mkObj [("module", toJson n.toString), ("path", toJson (← findOLean n).toString)]
  IO.println (Json.arr rows).compress
