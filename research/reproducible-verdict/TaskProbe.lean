import Lean
set_option maxHeartbeats 1000000
open Lean

/-- Eager IO tasks keep the measured allocation in its executing context.
    This is an accounting control, not a real candidate benchmark. -/
def work (n : Nat) : BaseIO (Nat × Nat) := do
  let start ← IO.getNumHeartbeats
  let mut xs : List Nat := []
  for i in [:n] do xs := i :: xs
  let sum := xs.foldl (·+·) 0
  let stop ← IO.getNumHeartbeats
  return (stop-start,sum)

def main (args : List String) : IO Unit := do
  let n := args.head!.toNat!
  let a ← IO.getNumHeartbeats
  let mut tasks := #[]
  for _ in [:8] do tasks := tasks.push (← (work n).asTask)
  let results := tasks.map Task.get
  let b ← IO.getNumHeartbeats
  IO.println <| "TASKS " ++ (Json.mkObj [
    ("main_thread_delta",toJson (b-a)),
    ("child_raw_deltas",toJson (results.map Prod.fst)),
    ("checksums",toJson (results.map Prod.snd))]).compress
