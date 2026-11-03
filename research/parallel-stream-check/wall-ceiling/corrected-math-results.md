# Corrected Mathlib1330 closure —3 independent repeats
自审,2026-11-03. Raw parallel-stream-wall-20261103.
Original Mathlib.Data.Nat.Basic resolution and all1330 modules match historical
v14; original O serial executable unchanged. Strong baseline is original serial,
not this prototype's slower parallel1. No-M/no-profile/no chunk rewriting.
All P0–7 affinity, configured pool1/8, no per-worker pin. Each fresh native process
1100s/14GiB outer safeguards, all retired normally, no resource failures.

| Arm | Wall median[range]s | CPU median[range]s | PeakRSS medianGiB |
|---|---:|---:|---:|
| original serial |66.128[66.113,66.490]|66.105[65.880,66.111]|0.696|
| default persistent1worker |71.767[71.671,72.491]|71.402[71.313,72.142]|0.771|
| default persistent8workers |39.653[39.629,39.762]|72.992[72.880,73.076]|0.784|

Ratio of medians, strong serial/8=1.667685.8workers still consume10.418% more CPU
than original serial; do not claim zero overhead or speedup relative to hardware
cores. Every repeat has exactly the same ordered1330 accepted module IDs.
Original mathematical declarations unchanged; common checked-token path validates
original ConstantInfo. Corrupted theorem controls1/8 explicitly fail original
kernel loose-bound-variable check, not import lookup. Existing unsafe/partial
exclusions and reader/glue TCB retained; no claim of replacing the original kernel.

## Relation to old1.52x
Historical v14 reference68.605s vs8workers45.050s (1.523x) remains archived.
This same closure/reference family may use corrected1.668x as new scoped final
performance evidence, with these fresh dates/configuration/source and three-repeat
ranges. It is not a causal estimate of marking alone: old/new dates, reboot,
runtime and generated code changed; isolated same-binary toggle1d742e3 remains the
causal experiment. In particular old1worker used runtime thread setting8 whereas
new1worker explicitly requests1. Both8worker settings8. Shared-host/finite ordered
repetition limits remain. No workload-wide or whole-Mathlib extrapolation.

Other requested Grid and exact historical Barrier protocols still in progress.
No full matrix completion is implied by this completed dataset boundary.
