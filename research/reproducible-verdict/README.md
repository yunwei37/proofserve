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
