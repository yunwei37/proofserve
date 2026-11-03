# Full-closure attribution / hardware comparison
Same4,449-module Barrier closure, same-implementation P1/P2/P4/P8points,
E16and mixed24, matched profile-off P8/mixed24, resident P1/E1/mixed24leaf
with50observed computation helpers and3repeats each. One finite P-lock task
at a time; no-M,14GiBsampled/charged own guard inside16GiB. Entire goal active.

The optional observer measures each original kernel call in thread-local
buffers. Registration mutex once per OSthread; no global lock per check.
Joined frontiers aggregate interval union (wall occupied by kernel calls), CPU
and allocation work, per-worker TID/actual core, narrow-wave checks and work.
Per-module summaries avoid per-declaration JSON. Observer overhead is measured
with profile-off full P8/mixed24controls; timing/merging itself is not free.

Measure dependency/context preparation and topology separately from upstream
complex replay and duplicate-proof serial checking. These are implementation-
serialized windows, not proved inherent dependency lower bounds. Kernel interval
union is wall occupancy, not exclusive CPU. Process residual includes queue,
gate, validation, commit, logging, startup/cleanup; do not label it all necessary
collaboration. Batch wall minus kernel union and batch CPU minus kernel CPU
provide narrower cooperation measurements, with same-process denominators.

Distinct active-task affinity per frontier: P1map0,P2map0-1,P4map0-3,P8map0-7,
coordinator0; E16map8-23,coordinator8; mixed24map0-23,coordinator0.
Actual per-check core and TID aggregates are retained. Only one NUMAnode exists,
so cross-NUMA is not an explanation here. Cache/core-type effects require
evidence, not a frequency-based25%assumption. No host/config/security change.
The resident leaf calibrates identical kernel computations on P1and E1,
and checks count/bytes with24workers, not a full closure per leaf trial.

Fit S+P/n only to the matched complete P1/2/4/8points. Retain residuals and
direct phase comparisons: fitted S may absorb overhead, not inherent seriality.
Estimate E/Pwork rate from matched kernel costs. Fixed S with positive added
Ecapacity cannot explain a slowdown; an additional overhead/placement/capacity
loss term is required. Single-run full points are descriptive, without a
replication confidence interval; leaf triplets have min/median/max.
Primary corrected frozen sources/binaries/raw live on PVC parallel-stream-attribution-20261102-v2. The unsuffixed point is retained invalid-placement evidence.

## Qualification correction before primary fit
The v1sticky TIDmodulomapping aliased two active threads ontoCPU0atrequested
two workers, because the Lean pool used three OSthreads. v1P2is invalid for
scaling; v1data and source remain unchanged. CPU membership alone was an
insufficient preflight. v2assigns a distinct slot0..count-1at each frontier,
rejects duplicate maps/oversubscription and repins the selected active tasks.
Per-check migration remains separately counted. Refresh all primary points
on the corrected source; old timings are not silently mixed into the fit.

## Placement ablation
The corrected per-frontier map is P-first for mixed CPUs: narrow waves use
the available P entries first. This is an explicit policy, not unweighted OS
scheduling. OSthreads may change core between frontiers; within-check migrations
are counted separately. Add profile-off unpinned P8/mixed24 on the same binary,
paired to the already-planned profile-off pinned P8/mixed24. This isolates
placement from observer cost and avoids attributing the old unpinned slowdown
to a new deliberate placement policy. No new background service or host change.
