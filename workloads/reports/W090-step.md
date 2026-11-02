# W090: make CPU versus duration interpretation reproducible
## EXPERIMENT_GATE
No additional native experiment while current84job queue remains active.
Reanalyzed the source33 staircase across both clocks: full class-mean parallel
CPU adds35.992–36.051%, while sum-of-module durations falls37.21–38.44%.
These transferred per-module duration sums are not a measured library makespan.
## WRITE_GATE
Single staircase command now emits parallel-CPU-duration-tradeoff.csv and README
explains resource-hours versus serial duration versus dependency-constrained
makespan. This is arithmetic interpretation of W088 evidence, not a new speedup.
## REVIEW_GATE — 自审
All-stage/domain sums checked, parallel factors kept CPU/elapsed-specific and
raw calibrations identified. No dividing CPU by wall speedup or eight cores.
No capture mutation or new timed job. Continue blocking for original returns.
