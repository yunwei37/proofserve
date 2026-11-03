# Avoidable serial fallback: uninstrumented paired result
自审,2026-11-03. Six complete fresh-process runs under one P0–7 lease,
same executable/default persistence8workers, only PARALLEL_SPLIT_COMPLEX differs.
Raw parallel-stream-wall-hybrid-20261103/hybrid-plain-P8-s{0,1}-r{1,2,3}.
Each native has1100s wall budget,14GiB outer guards,
no-M/no profile/no wave/dependency trace.3 repeats, reverse arm order in repeat2.
Native/cgroup retirement, no resource stops, identical ordered4449 IDs required.

| Arm | Wall median[range]s | CPU median[range]s | PeakRSS median[range]GiB |
|---|---:|---:|---:|
| whole-module fallback |257.659[257.410,257.711]|542.369[541.691,543.049]|3.217[3.207,3.231]|
| closed serial prefix + ordinary parallel |196.669[194.488,199.060]|542.942[539.968,544.446]|3.277[3.261,3.287]|

Ratio of medians1.310111839,23.6706% less wall. Paired ratios1.29464/1.32352/
1.31011. CPU median+0.10565%; no statistical/no-overhead guarantee from3 samples.
PeakRSS+0.06015GiB (about61.6MiB), observed peak not exact persistent leak cost.
Same4,449-module closure, all successful; no mathematical declaration rewriting,
no new axioms, no changed original kernel. Existing reader/checked-token adapter
and safe/unsafe exclusions retained. Eight native good/bad inductive controls
qualified separately and do not enter these timings.

This ratio is an engineering ablation of this same8worker checker, NOT a comparison
against all strong services or original serial. Do not multiply it with the
separately measured Mathlib/Grid ratios, nor use an old full-Barrier serial time
as its denominator. No global service throughput claim.
Canonical marker-only retiming remains separate; optional partition code lives
in HybridCore.lean, not silently enabled in canonical ParallelCore.

Diagnostic94.479→1.792 serial reduction and graph95.776/67.952 spans explain
the cause on their own instrumented denominator. They are not scaled into
these196.669s native-plain costs. The conditional166.427s/138.602s model figures
are diagnostic-version scenarios, not measured plain infinite-core times.

Conclusion supported: the old115s whole-module fallback was mostly avoidable
prototype policy. Fixing it improves this closure's wall about24% at similar
total CPU. Remaining declaration barriers/heavy jobs and metadata preparation
matter much more than0.297s of commitChecked; further conclusions require the
fixed-cost/finite-workload qualifications in complex-prefix-diagnostic.md.
