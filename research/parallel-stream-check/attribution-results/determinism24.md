# Complete24-worker determinism and hardware calibration

Original finite six-phase sequence ended2026-11-03T00:57:31Z. This last native
process independently checked the4,449-module reference closure, then repeated
the resident3,425-declaration Barrier leaf under P1/E1/mixed24three times,
with the middle trial order reversed. It is one compound diagnostic native
process, not nine independent full-closure throughput runs.
Native wall782.484s/CPU1688.835s/peakRSS3548.758MiB; all native/cgroups retired,
no resource interruption. Per-mode costs below have their own resident scope.

50real stored of_decide_eq_true helpers x3modes x3repeats=450observations:
all accepted, all50per-target allocation ranges0%. Nine actually emitted
Barrier.oleanfiles(each9,160,440bytes)match one another AND the original input
byte for byte. There are no .server/.private companion outputs in this case.
This is evidence for the selected ordinary checks, not all extension payloads,
all mathematical candidates or native kernel poll-budget units.

| Resident leaf mode | Wall median s [min,max] | Total CPU median s |50helper kernel CPU median s |
|---|---|---:|---:|
|P1 CPU0|63.158 [62.496,63.810]|62.710|2.519|
|E1 CPU8|86.185 [85.815,87.133]|86.133|3.486|
|mixed24 CPU0–23|9.233 [9.129,9.437]|200.686|8.255|

For these matched50helpers, solo E/Pwork rate=0.722555(27.74%less work per
CPUsecond on CPU8than CPU0). It is not an all-kernel/core-frequency constant.
The leaf wall improves~6.84xP1->mixed24, while leaf CPUgrows~3.20x.
Whole-closure scaling remains different because of its dependency prefix.

## Slow Ecores are not enough to explain per-check CPUgrowth
Normalize each mixed observation by that SAME target's median solo CPUcost
on the same core TYPE. Solo reference CPUs are0and8; mixed observations can
use any P/Ecore, so this is not a same-physical-core or frequency-controlled test.

| Mixed execution type | Observations / distinct targets | Per-observation ratio median [min,max] | Sum mixed CPU / sum matched solo costs |
|---|---:|---|---:|
|P|66 /41|2.301 [1.607,3.202]|2.419|
|E|84 /48|2.834 [1.971,4.159]|2.900|

Every observed mixed check costs more CPUthan its matched solo-type median,
with identical observed allocation count and mathematical result. Aggregating
P/Einto one median would hide this distinction. This supports concurrency-
associated CPUinflation beyond merely assigning work to slower Ecores.
It does NOT identify atomic RC, caches, frequency or other causes. The
new perf experiment will test those alternatives without changing Lean.

Source/binary/data scope and coordinator-glue trust limits remain as in the
parent plan. Raw:
 /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2 .
The final extra natural-placement/profile-on pair is a separate finite
followup, submitted only after this original series retired, and is pending.
