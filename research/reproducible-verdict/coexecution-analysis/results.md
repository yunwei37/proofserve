# Actual coexecution: theorem-command counts and diagnostic locations
2026-11-01UTC. Completed mathematical subset of PVC reproducible-verdict-v5;
the later Envelope import failed, so the whole region point remains partial.

16actual retained miniF2F sources x2budgets x4workers x2repeats=256observations.
Each worker executes its own synchronous candidate context against shared
imported Mathlib. Actual unique executing TIDs are1/2/4/8in the corresponding
cells, in both repeats. Inputs and observers fixed; allocation counters sampled
per command before output serialization.

Againstj1,192matched pairs:
-0verdict differences;0transitive axiom-set differences.
-84pairs differ in their command heartbeat vector.
-83pairs differ in the theorem command;26in the opening command;0in terminal.
  Counts overlap, so83+26is not the number of differing vectors.
-3pairs differ in error text: same budget-exhausted category, nested
  deterministic timeout location changes isDefEq→whnf for minif2f-945(two
  worker settings) and minif2f-5777(one). Full strings retained.
-Per source/budget, across all8repeat/thread observations, maximum theorem-HB
  relative range is2.333868%; this includes an accepted candidate. It is a
  finite observed range, not a margin that guarantees future acceptance.

This rules out explaining every changed vector as mere opening-command work.
It does not establish changed tactic branches. Shared realization, memoization,
allocation attribution and first-use effects are alternatives; no search tree
or proof-object identity comparison was captured in this point.

No budget number is recommended from these allocation totals: maxHeartbeats is
per Lean Core context, not the sum of candidate command deltas. Prior tested
budget ladders show no monotonic acceptance violation for16sources, but that is
not a universal larger-budget guarantee or a proven normalization rule.

Next actual task (v10) separately checks three computation modules and two
mathematical source modules. Mathematical source accounting remains explicitly
synchronous, and stored-proof kernel CPU is a separate estimand. The proposed
mathematical-only need for deterministic budgets awaits those observations.
