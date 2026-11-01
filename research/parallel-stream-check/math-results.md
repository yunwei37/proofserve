# Same-artifact 1330-module Mathlib stream

All 18 native cells completed; each accepted the same 1330 module IDs.
Input: 132484 entries; 2269 upstream unsafe/partial exclusions. No resource stop,
timeout or native process failure. P0-7, no -M, existing blocking flock.
Each configuration has three complete fresh-process repetitions.

| Mode | Wall median [range] s | CPU median s | Peak RSS median MiB | Ratio of wall medians vs O |
|---|---:|---:|---:|---:|
|reference|65.940 [65.925, 70.316]|65.906|736.4|1.000×|
|audited|74.531 [72.900, 77.303]|74.475|753.6|0.885×|
|parallel1|78.404 [77.568, 80.172]|78.088|815.4|0.841×|
|parallel2|75.265 [59.095, 77.678]|77.688|820.7|0.876×|
|parallel4|59.090 [58.566, 67.696]|80.306|822.1|1.116×|
|parallel8|57.052 [47.224, 64.978]|77.267|823.6|1.156×|

8-worker ratio of medians: 1.155779×; paired ratios 1.232486, 1.396330, 1.014561.
These are different estimators. All ratios and broad ranges are retained;
three sequential repetitions do not establish a precise general speedup.
External load/frequency variation was not independently isolated.

The 8-worker median wall cost is 13.48% lower, but CPU cost is 17.24% higher.
The 1- and 2-worker medians are slower than the original stream.

Parallel execution covers 858 modules / 55255 ordinary declaration jobs in
3616 waves. 472 modules use original serial replay for complex declarations or
cycles. No context-conflict module-local fallback occurs on this fixed closure.
The first paired audit/parallel8 kernel-work split is 45.347→30.079s for eligible
modules and 21.807→21.464s for serial fallbacks. Those instrumented stage
values belong to their own cells, not a rescaled breakdown of O reference.
O reference has no matching stage timer; its missing kernel-work field is unknown.

## Cost staircase

| Operation | Seconds | Scope |
|---|---:|---|
| Source construction | 622.379 | O recorded serial sum of compiler subprocess wall; same constructed artifacts |
| Original serial stream | 65.940 | Fresh paired median of complete artifact closure |
| Parallel stream, 8 worker | 57.052 | Fresh paired median, same accepted module IDs |

Construction includes elaboration and artifact production; checking consumes those
artifacts. This is an operation-cost staircase, not speedup for identical tasks.
The source-construction row is reused provenance from O cohort-costs.csv; it was
not repeated in this matrix. No strongest-library-checker or source-build speedup
claim follows. Stock LeanChecker already parallelizes modules.

## Trust and limitations

The pinned checked-token coordinator/C adapter are additional trusted code.
Original kernel checks mathematics. 18 native boundary controls qualify the v4
implementation; this is not a universal correctness proof. O reader files remain
unchanged. Under input corruption, compare explicit native rejection rather than
treating timeout/process failure as mathematical rejection. Chunking was disabled
in every cell here; its pending implementation cannot explain these measurements.

Raw results/source/segments/memory and full module accept events: `/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v4`.
The earlier v3 real-closure rejection and initial stopped control are retained.


## Subsequent negative control and version boundary

Frozen v4 accepts an invalid indirect local proof cycle if an earlier sibling
already supplied a compatible theorem. Isolated original-kernel module replay
rejects that raw input. This was actually reproduced, not just a source concern.
The combined prototype's cycle guard rejects it at workers1/8 and passes20
native controls. Thus v4 is historical positive-input performance evidence,
**not final safe-prototype throughput**. Fresh complete repaired-version
library measurements remain pending.
