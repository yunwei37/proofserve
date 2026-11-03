# Conditional finite-worker model and observer pair
自审,2026-11-03, complete wall-20261103 diagnostic only.

Original-call service CPU388.3793s. For each barrier wave, max(largest-job CPU,
total-job CPU/n), then sum, gives an optimistic fixed-service bound:
n=1:388.3793s;2:206.6463s;4:126.6125s;8:95.2734s;
16:83.4963s;32:78.4678s;infinite:74.5318s.
Measured batch wall111.6578s. The16.3844s gap above the8worker bound includes
possible bin-packing imbalance, runtime/scheduling and coordination; a lower
bound need not be achievable, so it is NOT16.3844s proven avoidable waste.
All182.9294s outside batches retained. No prediction after complex-prefix
partition until its actual run. Local DAG span54.6950s removes barrier edges
between unrelated levels, but keeps the module order and assumes unchanged
observed node CPU costs. No hardware-independent scaling theorem.

The fallback is distributed over1231 modules. Rep1 largest4.4296s=3.83%,
top10=18.43%,top100=56.49%. Thus fixing one outlier cannot remove115s;
the whole-module nonordinary eligibility restriction is the relevant class.
All3 own-run concentrations are in fallback-concentration.csv.

## Observer cost: do not mix with plain curves
Diagnostic trace-on294.5872wall/550.4098CPU versus same-binary trace-off
266.6559wall/539.7943CPU. Observed differences27.9313wall/10.6155CPU;
both237863 checks/3283925639 units and4449 IDs match.
Read/deserialization26.4169s versus10.0116s: the first arm is colder after
host reboot. The full difference cannot be assigned solely to trace overhead.
Original profile code remains on in both, so this pair does not measure its
absolute cost. Published corrected Mathlib/Grid curves have neither profile
nor trace; neither diagnostic denominator is reused as their timing.
