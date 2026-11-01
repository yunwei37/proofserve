
import Lean
import Std.Sync.Mutex
open Lean
@[extern "ps_process_ns"] opaque processNs : IO UInt64
@[extern "ps_pool_spin"] opaque spin : UInt64 → IO UInt64

def loopJobs (q : Std.Mutex Nat) : IO Nat := do
 let mut n := 0
 repeat
  let i ← q.atomically do
   let x ← get
   set (x+1)
   pure x
  if i >= 64 then break
  let v ← spin 50000000
  unless v > 0 do throw <| IO.userError "spin optimized away"
  n := n+1
 return n

def trial (label : String) (workers : Nat) (gated : Bool) : IO Unit := do
 let q ← Std.Mutex.new 0
 let gate ← IO.Promise.new
 let mut tasks := #[]
 let start ← IO.monoNanosNow
 let cpu ← processNs
 for _ in [:workers] do
  if gated then
   let started ← IO.Promise.new
   let t ← IO.asTask do
    started.resolve (1 : Nat)
    unless gate.result?.get == some (1 : Nat) do
     throw <| IO.userError "gate abandoned"
    loopJobs q
   tasks := tasks.push t
   unless started.result?.get == some (1 : Nat) do
    throw <| IO.userError "worker start abandoned"
  else
   tasks := tasks.push (← IO.asTask <| loopJobs q)
 gate.resolve (1 : Nat)
 let mut counts := #[]
 for t in tasks do
  match t.get with
  | .ok n => counts := counts.push n
  | .error e => throw e
 let elapsed := (← IO.monoNanosNow)-start
 let consumed := (← processNs)-cpu
 IO.println <| Json.compress <| Json.mkObj [
  ("event",toJson "pool_control"),("label",toJson label),
  ("wall_ns",toJson elapsed),("cpu_ns",toJson consumed),("counts",toJson counts)]
 (← IO.getStdout).flush

def main : IO Unit := do
 trial "warm4" 4 true
 for i in [:3] do
  trial s!"ordinary8-{i}" 8 false
  trial s!"gated8-{i}" 8 true
