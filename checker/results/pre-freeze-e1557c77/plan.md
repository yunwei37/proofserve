# Real-closure regression before the checker freeze

Dependency validation requested by the coordinator, not paper performance data.
Fixed source/binary: e1557c77. Run Nat.Basic (1,330 modules) then Grid
(3,793 modules), two workers, fresh state, CPU 8–9, no P-core lock or Lean -M,
at most 12 GiB own tree and an 8 GiB node reserve. Preserve every failed/partial
attempt. Stop Grid if the memory point does not fit. Checker freeze deadline:
2026-11-05 06:00 UTC. No further read-only review is opened.

Compare actual acceptance and declared axiom sets with retained ba316991
preview receipts and relevant 3fe83c5a evidence. Count accept events with
context=module_local as whole-module serial replay; report exact reason names
and counts, separately from within-module complex-prefix replay. The earlier
P2 preview has 4 such Nat.Basic and 7 Grid modules. Threshold supplied by the
coordinator: equal acceptance/axioms, at most 10% more fallbacks or serial modules,
and no obvious CPU regression. Preserve correctness if the cost cannot be fixed
before the deadline.

Old ba316991 timing used P cores; this qualification is on E cores. Raw P/E CPU
ratios are not a matched cost comparison. Reuse same-hardware data where present;
if necessary replay the retained 3fe binary on the same roots and E-core point
as the minimal reference control. This is one regression comparison, not the
post-census performance matrix. Freeze even with an honestly reported remaining
cost if a correctness-preserving fix is not practical within the deadline.

Positive result allows freezing and final evaluation; an increase exposes
quarantine propagation or other added checking cost and requires a bounded
correctness-preserving repair or an explicit known cost. Initial results go to
the raw PVC path recorded in launch.json; lightweight reports go here.
