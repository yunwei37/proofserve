import Lean
open Lean
set_option maxHeartbeats 200000
-- Produce a deliberately invalid serialized body with a valid module header.
-- This is a test artifact; Lean source elaboration would reject this proof.
unsafe def main (args : List String) : IO Unit := do
  let [input, moduleName, output] := args | throw <| IO.userError "arguments: INPUT MODULE OUTPUT"
  let parts ← readModuleDataParts #[System.FilePath.mk input]
  let some (data, _) := parts[0]? | throw <| IO.userError "no data"
  let constants := data.constants.map fun ci => match ci with
    | .thmInfo th => .thmInfo {th with value := .bvar 0}
    | _ => ci
  unless data.constants.any (fun ci => match ci with | .thmInfo _ => true | _ => false) do
    throw <| IO.userError "no theorem"
  saveModuleData output moduleName.toName {data with constants}
