import Lean
open Lean
set_option maxHeartbeats 5000000
unsafe def main (args : List String) : IO Unit := do
  let [root, paths] := args | throw <| IO.userError "root"
  let sysroot ← findSysroot
  initSearchPath sysroot
  searchPathRef.set (System.SearchPath.parse paths ++ (← getBuiltinSearchPath sysroot))
  let sp ← searchPathRef.get
  let start ← IO.monoNanosNow
  let files ← SearchPath.findAllWithExt sp "olean"
  let afterWalk ← IO.monoNanosNow
  let mut hits : List Name := []
  for path in files do
    if let some m ← searchModuleNameOfFileName path sp then
      if root.toName.isPrefixOf m then hits := hits.insert m
  let stop ← IO.monoNanosNow
  IO.println (Json.mkObj [("search_entries", toJson sp.length),
    ("olean_path_entries", toJson files.size), ("walk_ns", toJson (afterWalk-start)),
    ("resolve_filter_ns", toJson (stop-afterWalk)), ("targets", toJson hits)]).compress
