
/- Metadata-only inspection for empty import aggregators. No kernel result is
claimed for a module with declarations; those always reach normal checking. -/
import ProofServe.Stream
open Lean
namespace ProofServe

def runModuleMetadata (args : List String) : IO UInt32 := do
  initSearchPath (← findSysroot)
  let mut roots : Array String := #[]
  for arg in args do
    if arg.startsWith "@" then
      let text ← IO.FS.readFile (arg.drop 1 |>.toString)
      let names := (text.splitOn "\n").filterMap (fun s =>
        let s := s.trimAscii.toString
        if s.isEmpty then none else some s)
      roots := roots ++ names.toArray
    else roots := roots.push arg
  let mut rows : Array Json := #[]
  let mut regions : Array CompactedRegion := #[]
  for root in roots do
    let mod := root.toName
    let parts ← moduleParts mod
    let some (first,_) := parts[0]? | throw <| IO.userError "empty module data"
    let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "empty module data"
    let empty := data.constants.isEmpty && data.constNames.isEmpty
    let imports := first.imports.map (fun i => String.ofList i.module.toString.toList)
    let mut inputs : Array (String × UInt64) := #[]
    if empty then
      let file ← findOLean mod
      for part in artifactCandidates file do
        if ← part.pathExists then
          inputs := inputs.push (part.toString,hash (← IO.FS.readBinFile part))
    rows := rows.push (Json.mkObj [
      ("module",toJson root),("empty",toJson empty),("imports",toJson imports),
      ("declarations",toJson data.constants.size),("inputs",toJson inputs)])
    regions := regions ++ parts.map (·.2)
  IO.println (Json.mkObj [
    ("module_metadata",toJson rows),("retained_region_parts",toJson regions.size)]).compress
  return 0

/-- Loading the original declared import context still checks name compatibility.
Proof bodies in those imports have already been checked by independent children. -/
unsafe def runEmptyContext (args : List String) : IO UInt32 := do
  let [root] := args | throw <| IO.userError "empty-context arguments"
  initSearchPath (← findSysroot)
  let parts ← moduleParts root.toName
  let some (data,_) := parts[parts.size-1]? | throw <| IO.userError "missing module"
  unless data.constants.isEmpty && data.constNames.isEmpty do
    throw <| IO.userError "empty module classification changed"
  try
    localReplay root.toName "none"
  catch e =>
    IO.eprintln e.toString
    return 1
  IO.println (Json.mkObj [
    ("empty_context_checked",toJson true),("module",toJson root)]).compress
  return 0

end ProofServe
