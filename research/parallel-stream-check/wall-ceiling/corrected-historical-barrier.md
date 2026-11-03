# Exact historical Barrier single-module retest
自审,2026-11-03. Raw parallel-stream-barrier-corrected-20261103.
Fifteen completed points: stock replay and1/2/4/8 workers,three repeats each.
All3425 original declarations have identical ordered names and typed payloads.
Both stock and8-worker mutated-proof controls reach the original kernel and reject
a loose bound variable in C41.fourth226. Every native stage retired normally,
without resource stops. Dependencies are trusted imports,as in the historical
module-local workflow; this is NOT the4449-module closure or resident stream leaf.

| workers(0=stock) | Wall median[range]s | TotalCPU median[range]s | PeakRSS medianKiB |
|---|---:|---:|---:|
|0|48.351[48.001,48.816]|48.339[47.986,48.803]|2844000|
|1|52.978[52.963,53.036]|52.830[52.827,52.889]|2853864|
|2|29.964[29.933,30.239]|53.794[53.723,54.149]|2912524|
|4|18.512[18.490,18.540]|55.568[55.532,55.580]|2962168|
|8|13.740[13.650,13.764]|59.039[58.736,59.082]|3044964|

Ratio of medians stock/8=3.519086718 versus historical3.326370868.
The historical stock median46.992 and8-worker14.127 differ in date/kernel and
host state: the new stock is slower and new parallel faster. Their difference
cannot be attributed wholly to persistence. The earlier same-executable
persistence toggle remains the causal experiment.
This can replace3.33 only for the exact stock/export/reimport/final-audit protocol.
It does not replace the separate resident-stream5.297 figure. Eight-workerCPU
still exceeds stock by22.13%; no zero-cost parallelism claim.

The copied historical driver and source are in barrier-historical/,leaving the
original chunked-kernel-check tree read-only. Quiescent persistence is the sole
wave-checker correction. The stock branch is unchanged. P0–7,no-M/no profile,
blocking per-cell lease; each whole cell300s,individual wave120s and plan/audit90s,
14GiB external guard within the16GiB lane. Lease waiting is excluded.
Raw binaries and emitted artifacts stay on PVC,not Git.

Fairness sensitivity is pending separately: serial reference with the same
official persistence optimization versus unmarked serial and marked8-worker,
same new executable and3 balanced repeats. Until complete,3.519 is explicitly
the exact historical unmodified-stock comparison,not a best-optimized-serial claim.
