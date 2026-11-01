# Step 008 — completed repaired Mathlib matrix and cost staircase

## EXPERIMENT
Frozen native v14 / 8c62fc3: all 18 planned cells completed (reference, audited,
parallel1/2/4/8, three ordered repetitions). All 1,330 accepted module sets equal
the same-artifact reference. Each has 132,484 entries and 2,269 upstream unsafe/
partial exclusions. Repaired parallel routes: 858 modules, 55,255 jobs and 3,616
waves; 472 upstream complex/cycle module fallbacks, zero module-local context
fallbacks. All native groups and controller retired; lock released. No -M or
profiling instrumentation. Own peak RSS stayed below 0.84 GiB per cell.

Wall medians: reference68.605, audited71.326, parallel1=77.859,
parallel2=57.569, parallel4=47.598, parallel8=45.050 s. Reference/parallel8=1.523.
Three same-repeat ratios1.515/1.594/1.491. Median CPU68.570 ->93.430 s (+36.3%).
Ranges, CPU, actual resource ledgers and accepted-set checks in the small CSVs.

## WRITE
v14-math-results.md is the final repaired-version table, separate from historical
v4. v14-cost-staircase.csv keeps O's622.379 s source compiler work sum distinct
from whole-stream wall time: source construction ->68.605 serial ->45.050
eight-worker artifact checking. Construction is a serial sum of source compiler
invocations, not parallel Lake wall or identical work to verification.
Added data-only ranking of remaining serial module fallbacks and correct scope
for new-constant comparisons when a certificate intentionally changes a proof.
No paper file outside M ownership edited.

## REVIEW — 自审
Verified all18 exits, explicit retirement, accepted sets, exact same input path,
upstream exclusions, ratio arithmetic and final analysis reproduction. Corrected
a Grid prose typo:7,898 jobs is per trial, not per wave. The first Grid curve and
failed cold Envelope attempt remain preserved, not pooled into the Mathlib result.
Single-order three-repeat design, additional CPU, whole-module serial fallback,
coordinator/C trust and inactive mathematical-cohort chunk rewriting are explicit.
Next: one bounded Barrier full-prefix stream curve after checking the shared lock;
then remaining computational curves, including cold Envelope's resource limit.
No completion of the entire user task or new proof-parallelism novelty claimed.
