# Step039: P8samples returned; per-worker counter READ completeness failure
EXPERIMENT_GATE: P8record7th/native and its aftercontrol8thcompleted, same
4,449reference accepted IDs/ordinary work.38,717positiveperiod samples,
zero reported sample loss. All9observed check-worker TIDs have cycles samples
from all8inheritedevent IDs. However5/9have terminalcycles/instruction READs
from only5of8CPUshards; other events have different partial cardinalities.
Actual native READdump877records has all timing fields/no reportedlostvalues.
Positive TIDcounts/zero lostsamples had not qualified finalcounter completeness.
Initial checks were insufficient for this scope, and now corrected.

Observed READsum instructions2.891272525010T versus the separate complete
stat3.341009573905T illustrates a large undercount, not13%less native work.
Treat per-worker fields with missing shards as partial; do not compute IPCor
L3miss/instruction ratios across unmatched shard sets. Analyzer now leaves
ratios blank unless all7events have allcapturedallowedCPUshards.4Ptimes weren't
retained before authorized rawdeletion and remain unknown.8Prawis retained
for this actual unresolved measurement defect; it is not silently discarded.
All nine workers have actual samples on missing-READIDs, so this is final
counter-metadata incompleteness, not complete absence of cycle sampling there.
Exact cause/repair remains to test without changing the healthy native matrix.

WRITE_GATE: P8scopes/categories/READtime fields/sample-IDcounts saved. Main
strict category increase4→8is84.764billion estimatedsampledperiods;hash/
lookup44.985billion(53.1%),explicitRC/destruction18.610billion(22.0%).
Adding unanchoredworker-kernel candidates gives170.711billiontotalincrease,
hash107.035billion(62.7%),RC29.050billion(17.0%). Wider scope is separate,
not relabeled exact original-call coverage. Fine-grain RCinside lookup remains.
Native/perf overhead points remain separate; P8after320.868sversusbefore315.390s.

New ordinary Cworker workload/core-set table shows each observed poolthread
has check starts across all0..3or0..7cores. These are per-frontier pins, not
permanently fixed thread placement; privateheap/cachemigration remains an
alternative to same-object RCcontention. No migration-time or causal fraction
is derived from unorderedcore sets. No native or sampling change.

REVIEW_GATE 自审: sample-IDaudit runs on the actual retainedP8record with
maxstack1(offline1GiBguard/E8-15), all38,717samples accounted, no new native.
Source uses complete records before assigning full IPC; old ratio versions
remain Git history. Incomplete READmetadata is not a proof rejection or native
resource failure. Native matrixcontinues, P1stat has also returned10/16.
Need all remaining native cells and a measured recorder repair before claiming
complete per-worker hardware counts. Goalactive; preserve rawcounter defect.
