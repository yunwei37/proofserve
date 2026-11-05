import ProofServe.Stream
open Lean
set_option maxHeartbeats 200000

private def mappings (file : String) : IO Nat := do
  return ((← IO.FS.readFile "/proc/self/maps").splitOn file).length - 1

def main (args : List String) : IO Unit := do
  let [sig, ir] := args | throw <| IO.userError "expected signature and IR paths"
  let before ← mappings ir
  for _ in [:16] do
    validateIRArtifacts #[sig, ir]
    unless (← mappings ir) == before do
      throw <| IO.userError "IR validation retained a file mapping"
  let released ← mappings ir
  -- A separate owner's live data must survive temporary validation reads.
  let owner ← IO.mkRef (← readModuleDataParts #[sig, ir])
  let ownedBefore ← mappings ir
  for _ in [:16] do
    validateIRArtifacts #[sig, ir]
    unless (← mappings ir) == ownedBefore do
      throw <| IO.userError "IR validation unmapped another owner's data"
  let kept ← owner.get
  let entries := kept.foldl (fun n part => n + part.1.imports.size + part.1.entries.size) 0
  IO.println (Json.mkObj [
    ("ir_region_lifetime", toJson true), ("reads", toJson (32 : Nat)),
    ("file_mappings_before", toJson before), ("file_mappings_after", toJson released),
    ("retained_owner_mappings_before", toJson ownedBefore),
    ("retained_owner_mappings_after", toJson (← mappings ir)),
    ("retained_owner_entries", toJson entries)]).compress
