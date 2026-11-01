# Real Grid target: matched-output flat partition result

2026-11-01 UTC. This is one automatically extracted PointBox.calc equality
from the real Grid module, not a complete Grid compilation or service benchmark.

The corrected matrix has15/15completed native cells, all accepting.
Every final theorem has the original target and the same [propext] axiom
dependencies; no sorry or new axiom dependency was found. Same-k artifacts
are byte-identical across all three repetitions. Different k values use
different proofs and intentionally different module artifacts.

The first finite controller completed two cells and retired after waiting
behind another lane's lock; its exact exit status is unknown. The missing
13cells were run later with the identical frozen native source. Every cell's
own measured interval excludes its queue. The continuation completed at
01:20:14UTC with clientexit0 and all native processes retired. These intervals
are not concatenated into service throughput.

## Scaling curve

Medians; parenthesized values are min–max of three repetitions.
Pure-kernel CPU is the sum of per-worker thread clocks, not process CPU
over an overlapping wall interval.

| Arm | Pure kernel span ms | Pure kernel CPU ms | Mean active cores in kernel span | Whole native wall s | Whole native CPU s |
|---|---:|---:|---:|---:|---:|
| Original record equality |146.08 (142.89–151.84)|146.03 (142.82–151.83)|1.000|1.974 (1.972–1.983)|2.045 (2.041–2.051)|
| k1 |144.07 (143.28–149.22)|144.04 (143.25–149.17)|1.000|5.973 (5.926–6.542)|6.035 (6.001–6.608)|
| k2 |140.50 (138.70–140.55)|149.35 (147.68–149.51)|1.064|5.862 (5.862–5.865)|5.982 (5.982–5.989)|
| k4 |151.68 (148.39–166.05)|237.61 (236.96–251.81)|1.566|5.897 (5.881–5.912)|6.139 (6.117–6.162)|
| k8 |178.02 (174.94–180.72)|392.06 (375.43–396.50)|2.194|5.927 (5.927–5.934)|6.364 (6.359–6.376)|

Relative to the same field-conjunction pipeline at k1, pure-kernel scaling is
about1.025x at k2,0.950x at k4,0.809x at k8. The8-job version spends about
2.72times k1's pure-kernel CPU. More occupied cores do not imply useful speedup.
No confidence interval or population inference is attached to three attempts.

The original also exports its checked module in this corrected point.
Median peakRSS is3.116GiB original versus about6.72GiB split.
All captures have no sampled-budget stop or timeout.

## Complete cost matters

For k2/4/8, merge-stage medians are3.794/3.815/3.816s. Normal module import is
3.643/3.659/3.660s, roughly96%of that stage within each cell. The final theorem's
kernel check itself is only about0.16–0.20ms, the dependency/shape audit about
0.09–0.11ms, and final export about0.15s. This separates merge proof complexity
from normal environment reconstruction instead of attributing all merge cost
to the kernel or axiom traversal.

The entire native process is roughly3times the original, even though the
original now writes an artifact too. It includes initial imports/frontend;
the split process additionally loads the newly checked modules. This is a
standalone target pipeline, not a measured warmed service. Importing a batch
once could amortize costs; no such amortization or full-module gain is measured.
The pinned import code rebuilds constant maps/extensions. No unchecked
environment union is substituted to improve the graph.

## Why this does not reject all decomposition

The generator divides18Int-field equalities into equal-sized contiguous
groups. Source inspection shows two record-valued exponential computations,
each using Horner evaluation and squaring. At k2 both end up in the same job.
At k8 the two outputs are touched by five distinct checker/component pairs.
Independent checker states do not share their reduction/conversion caches.

That observation supports a repeated-work/imbalance hypothesis; it does not
attribute all added CPU. The transformation also changes record decision into
field conjunctions, and scheduling/clock overhead remains in the small spans.
A source-only component-preserving control has been generated, with the same
target and kernel API, and separately queued after review of this complete
negative point. Its acceptance and curve are unknown until native qualification
and all repetitions actually finish.

The result rejects a claim of useful speedup from this flat partition on this
target under this protocol. It does not establish a fundamental bound for
all closed reductions, a universal maximum parallelism, or a whole-library
negative result. Source semantic coverage and actual check-time grain remain
separate quantities.

## Reproducibility and limits

See v3-per-repeat.csv, v3-summary.csv, v3-artifacts.csv and v3-validation.json.
Each cell used no-M/P0–7 and the existing common lock, same pinned SDK,
finite heartbeats,180s self alarm and14GiB sampled own-tree stop within M16GiB.
Per-worker clocks satisfy physical wall/CPU bounds. The parent samples at1s;
it is not a hard kernel RSS quota.

The native source is frozen-grid-v3; the continuation manifest preserves
exact per-cell paths, both old completed cells and later ones. Queue windows,
other-lane activity and old setup failures remain in raw PVC records.
P-core locking does not isolate shared memory/cache/I/O. Background preparation
on E cores is allowed and is not silently treated as full-host isolation.
Per-child heartbeats do not implement aggregate monolithic-budget equivalence.
