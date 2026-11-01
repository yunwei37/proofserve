# Step 001: evidence boundary and executable measurement plan

2026-11-01 UTC; M lane; self-review (自审). EXPERIMENT: implement/qualify;
WRITE: focused source map; REVIEW: self-audit, no independent reviewer or acceptance claim.

The newest direct user request is reproducibility, not further speedup tuning.
Only research/reproducible-verdict is writable by this lane for this task.
Read current docs/user-instruction.md and idea-story.md; their historical gates
do not override the current direct instruction.

Existing Envelope reference actually exited 124 after 1680.158s, all native
processes retired. It remains a partial independent-stream reference, not a
completed acceptance-set comparison. Its raw summary is in parallel-stream-check-v14.

Actual PVC now has about 37GiB free (df, this step), rather than the request's
older 7.9GiB estimate. No cleanup necessary and no foreign data touched.
Two other finite timed controllers own/queue the P-core lock. New measurement
will use blocking flock and verify owner/waiter identity before claiming queued.

Hypotheses and admitted experiments:
1. Retained 200-source profiler diagnostic: reproduce denominator and concrete
   counterexamples, preserve hasErrors vs full acceptance distinction.
2. Fresh fixed candidates: native stock frontend, threads1/2/4/8; observer off,
   native C profiler and allocating trace profiler; cache warmed vs scoped own-file
   DONTNEED eviction. No host drop_caches. A scoped eviction is not globally cold.
3. Measure allocation heartbeats inside a synchronous frontend command path.
   Whole process/thread-local deltas are not sums of asynchronous child work.
   Source-level workload order and options are part of replay identity.
4. Budgets around measured transitions and increasing ladder: test monotonicity,
   do not assert it for arbitrary metaprograms that can inspect their budget.
5. Lab comparison requires an existing authorized test environment. No migration,
   extra Workspace or host development is implied; other cells proceed independently.

All finite native tasks: no -M, P0-7, same shared lock, external own-tree memory
protection <=14GiB plus controller reserve within M16GiB; max1740s whole task.
Preparation goes on E8-15. Native and wall time, error kind, missing result,
operational interruption, sorry/new axioms and accepted declarations are separate.
No numerical gain or new novelty established by this plan.
