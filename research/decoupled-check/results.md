# Decoupled native checking: measured status
Updated 2026-11-01T01:38:04Z. Review: self-review.
Raw observations: /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031. P cores0-7; shared lock; no Lean -M;
11.875GiB child cgroup plus128MiB parent reserve within O12GiB.
Fixed native kernel and compiler: Lean4.34.1, release5045d0056413266e57c625dcd7c365b10e377c52.

## Complete closure accounting
- math (Mathlib.Data.Nat.Basic): constructed 1330/1330; source compiler work 622.379412s; matched stream 65.69264411274344; ratio 0.10555079879889155; matched oracle modules 1330; parity complete=True.
- compute-grid (OAI.Analysis.PlanarPacking.Grid): constructed 3793/3793; source compiler work 3878.706740s; matched stream ; ratio ; matched oracle modules 1330; parity complete=False.
- compute-amplitudes (OAI.Analysis.PlanarPacking.Certificate.Amplitudes): constructed 3793/5083; source compiler work 3878.706740s; matched stream ; ratio ; matched oracle modules 1330; parity complete=False.
- ordinary-oai (OAI.MeasureTheory.Falconer.Estimates.NearPinDeletion): constructed 3239/3333; source compiler work 2445.402175s; matched stream ; ratio ; matched oracle modules 1330; parity complete=False.

A blank ratio is pending, not zero. The primary numerator consumes the exact
newly constructed olean artifacts, not the original distributed cache.
The source denominator sums actual native compiler subprocess durations for
**every member** of the closure, including each member's imports, tactics,
kernel checks and standard olean/ilean/C output. Failed attempts remain charged.
This is serial compiler work, not parallel Lake wall time, C++ toolchain
bootstrap, a continuous cross-window clock, or an inferred population speedup.
One union source DAG is built; common immutable modules are measured once and
included once in each applicable closure total. Lock wait and orchestration
overhead are outside these native-process durations. Warm OS/cache conditions
and one-pass construction limit generalization.

## Ordinary versus computational root components
root-components.csv separates predeclared ordinary roots (Nat.Basic and
NearPinDeletion) from computational roots (Grid and Amplitudes). Its numerator
is that root's read/map/kernel-replay component **after dependencies are checked**.
It is not standalone process latency: shared library verification remains in
the whole-closure table. Neither component fraction nor sampled C++ producer
cycle fraction is a guaranteed end-to-end speedup.
- Mathlib.Data.Nat.Basic: component 0.026844s / producer 0.410718s = 0.065358.

## Correctness and trust scope
The preflight checks a real13-module closure against bundled leanchecker and
three malformed proofs in distinct real Nat theorems. All three are rejected
by the original kernel through both streaming and module-local paths.
Each completed measured cohort additionally requires a matched acceptance set
from independently finalized single-module import environments (source-equivalent
to the bundled checker), with no checked environment reused across modules.
Successful oracle records for identical, already-built immutable dependencies
can contribute to multiple enclosing closures; no failed/timeout record does.
This is differential evidence on these inputs, not a proof of universal
transparency. Upstream replay skips unsafe/partial declarations; counts remain
in raw module events. Axioms keep Lean's semantics. No external checker joins TCB.

## Retained non-successes
No measured non-success recorded at this checkpoint.
