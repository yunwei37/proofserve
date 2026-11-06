# Measured completed subset of openai/math 4eaee875

**162,170 / 163,096 source modules completed.**
There is also one uncharged Lake configuration unit.
926 source modules have no successful compilation
cost, including 926 postponed at the user's request.
This dependency-ordered, memory-selected subset is not a random sample.
**No whole-corpus point estimate or confidence interval is inferred.**

## Observed costs of completed modules

| Segment | Completed modules | P CPU h | E CPU h | Observed wall h |
|---|---:|---:|---:|---:|
| 1 | 128,331 | 134.651 | 256.668 | 24.625 |
| 2 | 33,788 | 32.718 | 45.731 | 6.179 |
| 3 | 51 | 1.587 | 0.000 | 0.726 |

Successful native CPU is P **168.956 h**
and E **302.399 h**.
Their raw OS CPU-hour sum is 471.355;
it is not a conversion to P-core equivalent work.
Primary user-mode instructions (the selected affinity-pool PMU, as in the
qualification analysis) total **5,276,120,533,386,849**. All four raw
core/atom user/kernel instruction counts remain available in module tables;
record-validation.json also reports other-pool counts. No rescaling is applied.

The sum of measured segment walls is 31.529 h.
Calendar span is 33.086 h, including a separately
reported transition gap of 5604.973 s.
Successful CPU excludes failed/interrupted attempts; segment wall includes
preparation, all attempts, hashing, publication and cleanup.
Per-module wall is observed fork-to-reap time and may include collection lag.
Do not add overlapping per-module walls to obtain whole-run wall.

These are observed lower bounds on cumulative work already spent in this
collection's per-module protocol, not a full-library cost estimate. Costs of unmeasured modules remain
unknown. Missing rows have blank costs, never imputed zero.

## Observed subset by static marker and build scope

The two partitions below each cover only completed modules; they are not
independent sets to add together. The lexical marker is not dynamic kernel
attribution.

| Group | Completed modules | P CPU h | E CPU h | User-mode instructions |
|---|---:|---:|---:|---:|
| outside default OAI import graph | 32,261 | 30.882 | 56.237 | 879,611,250,766,248 |
| inside default OAI import graph | 129,909 | 138.074 | 246.162 | 4,396,509,282,620,601 |
| static decide +kernel absent | 156,322 | 138.730 | 246.923 | 4,306,293,303,038,080 |
| static decide +kernel present | 5,848 | 30.226 | 55.476 | 969,827,230,348,769 |

## Input and execution

Source commit: 4eaee87548250b2682affda7d05d947c05554bae.
Lean 4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
The real exported Lake context has 44 search entries and 42 pinned packages,
with 23 verified repository compatibility patches for dependency packages.
The measured machine topology and late-run observation timestamp are recorded
in summary.json measured_hardware. All recorded segments use the same canonical folded import view, -j8,
LEAN_NUM_THREADS=8, and no -M. Pools are P CPU 0-7 and E CPU 10-23.
Implementation commits by segment are recorded in summary.json.

Segment 1 admits up to 22 concurrent modules under actual-memory guarding,
then drains for exclusive resource retries. It completed 128,331 sources.
Segment 2 changes admission and explicitly postpones observed memory-heavy
families (including remaining PadicHodge) and their dependent closure. It
keeps dependency-ready lexical ordering among memory-eligible work.
Already completed segment-1 modules in those families remain included.
Segment 3 continues the 51 eligible modules left by the superseded 03:00
admission boundary. It uses the segment-2 admission policy without UTC deadlines;
no completed work is repeated. The gap is reported separately, not hidden.
See ../census-plan.md for recorded boundaries and the user continuation decision.
summary.json metadata_errata identifies a stale inherited generic retry label
in the raw segment-2 config; its top-level segment-specific label and frozen
code describe the actual user-deferral behavior. Raw metadata is preserved.
This cohort change prevents attributing throughput differences to admission
alone. The omitted tail may have a substantially higher average cost.

Generated C is produced normally, then hashed/sized in a durable record
before successful C files are removed. Olean/ilean and companions remain on
the capture PVC for subsequent independent checking. External package builds,
a separate downstream compilation/link step for the emitted C files, and
downstream checking are outside these totals. Work invoked internally by Lean
is part of its inherited process accounting. Source compilation does not establish
axiom freedom or replace independent kernel checking.

## Counter choice and resource observations

The original TOTAL-instruction qualification failed: median 1.33%,
P95 3.15%; thresholds were not changed. Claude chose execution after the
user requested progress. User-only instructions were selected POST HOC:
the four-condition qualification sample had median 0.018% and P95 0.14%.
This is not a substitute passing gate or a universal invariance proof.
OS kernel-mode counters are retained but not used for cross-module ranking;
they do not attribute work to Lean's trusted C++ kernel.

record-validation.json reports every return's provenance/counter checks and
active-PMU coverage. Resource attempts are separate from native rejections. The raw
cgroup_memory_oom label records an OOM-kill counter accompanying a failed
return; limiting-kernel-context attribution was not independently established
for every attempt. Owned-job OOM counters do not certify absence of all system
OOM events.
The guard targets available memory by sampling; it is not a hard guarantee.
Across captures, minimum sampled node availability was
6.949 GiB,
with 15 samples below 8 GiB
and maximum observed sampling gap
7.448 s.
Per-segment observations and interruption categories are in summary.json.

## Tables and units

- modules.csv.gz: one row per frozen source/configuration unit, with fate,
  measured segment, native cost, PMU coverage, source/artifact provenance and
  explicit deferral or dependency reason.
- failed-attempts.csv.gz: unsuccessful attempts, including recovered ones;
  they never enter completed-module cost aggregates.
- unfinished-modules.csv.gz and unfinished-by-family.csv: all missing successful
  costs, separated by fate; deferred-modules.csv.gz isolates user postponements.
- aggregates.csv: completed costs by stratum, static marker, default-root graph
  membership and core pool. Frame counts are explicitly named as frame counts.
- segment-totals.csv: observed segment walls and successful native CPU.
- top20-user-instructions.csv: primary post hoc ranking; top20-cpu.csv records
  raw charged CPU with pool identity, without normalizing P and E.
- original42-pairs.csv: 42/42 calibration modules
  matched to completed observations. P-only ratios are descriptive; E
  assignments are listed without a P-equivalent ratio.
- summary.json: machine-readable totals and limitations; export.py reproduces
  these tables from the retained retired capture and its segment registry.

Segment-2/3 admission_state_json and active_at_launch are recorded natively;
active_at_launch counts other in-flight attempts before this launch, excluding
the new attempt itself. Those fields are blank for segment 1, which did not
record them. cgroup_peak is the observed own-job cgroup charge high-water,
including charged shared/file pages; it is not summed RSS or a required-memory
guarantee. Failed peaks may be censored.

Native-attempt interruptions, never-started units and user deferrals have
distinct statuses. The original controller status is retained alongside the
normalized unit fate.

The marker is static decide +kernel presence, not dynamic kernel cost ground
truth. Sampling-frame count differences are disclosed in summary.json; old
weights are preserved and are not used to fill missing costs.

## Historical comparison

The original quiet-P 42-module estimate was 279.12 P CPU h (nominal interval
95.18-463.06), under a different concurrency/environment context. It is a
historical calibration record, not an estimator for the excluded tail here.

The [nealmcb report](https://github.com/nealmcb/openai-math-lean-tooling/blob/c9570a82f79b78a1a969a6316ac0fdd69aabef55/REPORT.md)
uses corpus fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb, 122,458 OAI modules,
a different cloud machine and -j4. Its approximately 330 CPU h is a
26-module laptop extrapolation, distinct from its measured 13.8-hour cloud
wall. The reported 116 GB is the whole finished build including packages;
Lean lib artifacts are about 68 GB. These are different scopes and protocols.

Re-export from this directory after all recorded supervisors retire:

    python3 export.py --point CAPTURE_ROOT --out OUTPUT --package ..

A capture archive can be moved as a whole: registry descendants resolve
relative to CAPTURE_ROOT. Artifact paths in rows preserve original provenance.
The export starts no Lean process. The compressed tables themselves suffice
to recompute cost totals without the capture: read modules.csv.gz with Python's
gzip/csv modules, keep status=completed, and sum cpu_s or instructions_user
by segment and pool. Sum segment-totals.csv wall_s separately. No model or
hardware conversion is involved. For checker comparisons, restrict native rows
to the exact checked source-module set and state external dependency treatment.
