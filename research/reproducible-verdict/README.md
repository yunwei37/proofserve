# Reproducing budgeted Lean outcomes

B/M lane, 2026-11-01. Experimental, disabled in the production service.
This directory owns the budget-replay prototype, focused prior-work audit and
finite native differential tests. It does not change the kernel or main engine.

The requested universal claim (all machines, all observers, all thread counts)
is a hypothesis, not a guarantee. A proof rejected because a machine crashed
is not a proof of falsity. Operational interruption is kept separate.

Initial evidence: the retained 200-source Lean4.9 diagnostic changed seven
frontend error flags under trace.profiler (3.5% of source pairs). This is not a
production acceptance-set measurement; see ../mechanisms-2026-10-30/profiler-heartbeat-methodology.md.
Fresh experiments pin Lean4.34.1 and distinguish the stock frontend from an
explicit synchronous accounting path. Version effects are not hardware effects.

Captures and generated artifacts live outside Git on the existing PVC:
`/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v1`.
No global cache eviction, host security changes, new Workspace or old queue restart.

See [prior-work.md](prior-work.md) and [Probe.lean](Probe.lean).

## Native request and replay

A request contains id, exact code, target theorem, budget (Lean user units),
mode and observer. Stock mode preserves the stock asynchronous frontend.
Sync mode is an explicitly different accounting path; v1 loses parser messages,
and v2 captures them. No transparency guarantee is inferred from small controls.

On a machine with the same Lean4.34.1 and matching Mathlib:
    LEAN_PATH=<matching compiled imports> lean -j1 --run Probe.lean requests.json

For our timed measurements that command is wrapped by the shared P-core lock and
finite native.py collector. Probe runs the original Lean elaborator/kernel,
forces checked theorem information, checks transitive sorryAx and new axioms,
and outputs REPRO JSON (verdict, raw command counts, errors and axiom policy).
Budget scope is stock maxHeartbeats per Core context, NOT a global candidate cap.

replay.py bundles requests + native rows + environment + process terminal into
rerunnable evidence. Its compare command reports verdict, unit, diagnostic and
axiom divergence. It never accepts a receipt as a proof of success or failure.
The supplied qualification receipt contains real results; tests check metadata
integrity only. No producer failure cache or service behavior is enabled.

See matrix-v1-results.md for actual counter/observer findings and the adapter
defect. The broad cross-machine/cross-observer hypothesis remains unproved.

[protocol.md](protocol.md) specifies counter families, ordered replay inputs and the still-unmet global-budget obligation. ReplayProbe.lean adds original-kernel rechecking; compile-qualified only until native controls finish.

Corrected1536-observation results: [matrix-v2-results.md](matrix-v2-results.md). No thread-count mismatch; low-budget sync acceptance changes under trace. Lab incomplete.

[Budget ladder](budget-monotonicity-results.md):0/100tested lower-pass/larger-budget violations; not a universal guarantee. Full private runtime cache test complete: 0/256verdict differences; synchronous counts 0/128differences. Actual math coexecution has84/192counter-vector differences and0verdict differences; see cache-and-coexecution-results.md. Computation expansion remains pending.

Current actual three-repeat module results: [module-results-v11/results.md](module-results-v11/results.md). Judgments agree; sampled computation allocations stable; mathematical source ranges up to0.138453%. Full2524helper census is a separate foreground task, not yet a completed result.
