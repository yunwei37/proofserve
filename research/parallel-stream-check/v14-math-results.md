# Repaired single-process Mathlib stream

Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14. Frozen source 8c62fc3; all values in seconds.
Complete matrix: True. Native control cases: 20; actual certificate qualification: True.

| Method | Repeats | Wall median [min,max] | CPU median | Peak RSS MiB median | Reference / wall |
|---|---:|---:|---:|---:|---:|
| reference | 3 | 68.605 [65.989,71.805] | 68.570 | 732.4 | 1.000 |
| audited | 3 | 71.326 [71.304,72.125] | 71.180 | 747.7 | 0.962 |
| parallel1 | 3 | 77.859 [76.171,77.967] | 77.438 | 812.8 | 0.881 |
| parallel2 | 3 | 57.569 [57.529,58.216] | 80.811 | 818.9 | 1.192 |
| parallel4 | 3 | 47.598 [47.362,49.214] | 84.644 | 818.8 | 1.441 |
| parallel8 | 3 | 45.050 [44.270,45.292] | 93.430 | 825.8 | 1.523 |

## Paired repetitions

| Method | Same-repeat reference / wall, all three | Median CPU / reference CPU |
|---|---|---:|
| reference | 1.000, 1.000, 1.000 | 1.000 |
| audited | 0.951, 1.007, 0.925 | 1.038 |
| parallel1 | 0.901, 0.921, 0.848 | 1.129 |
| parallel2 | 1.178, 1.248, 1.146 | 1.179 |
| parallel4 | 1.441, 1.516, 1.341 | 1.234 |
| parallel8 | 1.515, 1.594, 1.491 | 1.363 |

All configurations traverse the same exact artifact path and 1,330 module IDs.
The matrix checks IDs against the reference; unsafe/partial counts follow upstream replay.
Declaration jobs and waves, local fallback counts and per-cell exits are in v14-math-cells.csv.
Native bad-proof, sibling-context, duplicate-cycle and token corruption controls are separate qualifications.

The ordered 18-cell matrix repeats reference/audited/1/2/4/8 three times in the same order.
It is not randomized or an isolated production-service benchmark. No Lean -M or perf overhead.
Only the bounded finite mathematical artifact cohort is measured. A requested worker count does
not mean all workers are busy throughout serial fallback modules or narrow frontiers.
The optional Fin proof rewrite is inactive in this mathematical cohort.

Historical v4 tables remain unchanged and are not pooled with this repaired version.

Total CPU here means aggregate process CPU seconds. It is not an instruction
count or a controlled-frequency estimate of algorithmic work. No causal split
between synchronization, allocation, reference counting, cache effects and
clock frequency is available from this non-profiled matrix.
