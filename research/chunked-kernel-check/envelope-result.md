# EnvelopePsiB: complete large-goal chunk curve

## Exact case and scope
Automatically selected the measured largest Envelope helper,
envelopeExpB16_calc over Fin31, from the pinned source/native profile.
Each chunk retains the whole per-index interval-exponential computation.
Generated merge lemmas use direct Nat boundary proofs and are checked by
the original Lean4.34.1 kernel. Source/target type equivalence is qualified.

This is a runtime recheck over a **prepared transformation**. Source
generation, Base/merge-lemma compilation and the original OAI producer build
are excluded, and were not timed on P cores. Do not call these numbers a
complete automatic source-transform workflow, whole-module source compilation,
whole-library speedup or production service throughput.

All runtime cells use P0–7 and the common lease, no-M, same14GiB own-child
guard within M16GiB. Chunk cases have strictly sequential checked producer
and thin kernel-only merger processes. Both native startup/import/export
costs, interphase cleanup and final original-kernel audit enter whole runtime.
Original cases have one native check/export phase. Native CPU excludes the
small Python parent. Raw code frozen at0d67cd6.

## Three repetitions per setting

|Setting|Kernel span median[min,max],s|Whole runtime median[min,max],s|Native CPU median,s|
|---|---:|---:|---:|
|Original goal|6.125[6.093,6.140]|9.848[9.817,9.854]|9.836|
|1chunk|6.177[6.141,6.361]|14.347[14.291,14.551]|14.319|
|2chunks|3.531[3.524,3.549]|11.490[11.479,12.274]|14.892|
|4chunks|1.967[1.771,2.013]|10.331[9.963,10.597]|15.307|
|8chunks|0.973[0.959,1.705]|8.982[8.931,10.342]|15.110|

Ratio of medians at8chunks:6.29x pure checker span, only1.096x whole runtime
(8.79%less wall). Native CPU increases53.6%. Worker checker threadCPU rises
from6.122s to6.848s, so the parallel work is not free.

The paired whole-runtime ratios for8chunks are1.096,1.103,0.949x. The third
observed repetition is5.35%slower than its original; keep it. Its cause was
not separately measured. Three repetitions are not a strong statistical
population guarantee and no guaranteed nonregression is claimed.

At8chunks the merger's in-process import median is3.142s, final kernel
assembly check0.296ms, dependency/shape audit7.27ms and final export0.243s.
Whole merger interior is3.389s; its process startup and the producer's initial
load also enter the full runtime. Paired nonkernel residual overhead relative
to the original is4.24–4.91s (median4.30s). Residual includes several operations,
not an exact attribution to any one loader function. These measured costs
absorb most of the parallel checker gain.

## Correctness and resources
15/15 performance cells accept the same extracted original target.
Every child is originally kernel-checked before export, and the assembled
theorem is originally kernel-checked after normal checked-module import.
All final dependency sets are exactly[propext], with no added axioms or sorry.
This is the same original-kernel/module-loader trust boundary, not a new
independently implemented verifier.

28actual native phases:27successful performance phases plus one genuine
kernel rejection of the deliberately false decision. All processes/scopes
actually retired. Peak sampled own-tree RSS9,086,930,944bytes, below14GiB;
charged memory is separately recorded and must not be confused with RSS.
Sampling is not a kernel hard RSS guarantee.

All84output.olean parts (including server/private files) have identical
same-configuration repetition bytes. Across-k proof artifacts intentionally
differ. Aggregate heartbeat-budget transparency and arbitrary source tactic
backtracking parity are not implemented; these successful true-target checks
do not establish unchanged classifications for all budget-limited candidates.

## Earlier failures remain part of the record
v1failed before the curve because ordinary predicate def blocked Decidable
construction. v2passed the true kernel negative and original goal, then hit
the sampled RSS stop after exporting a valid child. Its original cell is not
reused here. A matching child/import qualification also revealed an old
omega bridge's Quot.sound dependency; direct Nat lemmas removed it. All old
raw directories, sources, failed/partial results and unknown interrupted CPU
remain unchanged. The successful fresh v3uses neither a higher memory budget
nor an old denominator.

Raw:
 /workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/envelope-curve-v3
Actual run04:28:14–04:31:05UTC,2026-11-01, proven lock holder and exit event.

## Relation to the other measured case
BarrierData41 declaration-parallel replay yields3.33x whole-module recheck
speedup versus direct stock serial replay. This Envelope target yields strong
local checker parallelism but a small, variable runtime gain. The two cases
have different baseline/runtime interfaces; do not combine their ratios into
a library estimate. Upstream module concurrency and prior parallel proof work
remain required context. These are workload characterization and mechanism
feasibility results, not novelty or broad end-to-end acceptance claims.
