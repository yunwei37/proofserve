# Step010 — first complete repaired computational curve

## EXPERIMENT
Barrier full-prefix finite task acquired the existing P0–7 lock, no-M, v14 source.
All4,449 modules accepted, native/cgroup/controller retired. All five leaf curves
complete from the same independently checked4,448-module prefix;3,425 new leaf
constants match the original serial kernel under1/2/4/8 workers. Actual8-worker
mean utilization7.87cores. Serial53.960s ->10.186s (5.297x), CPU53.934->80.155s.
One repetition; no variance or full-closure single-config speedup claimed.

## WRITE
Added barrier-stream-results.md and refreshed compute CSVs without pooling old
versions. Includes whole process468.112s and3.12GiB peak, and explicitly keeps
prefix+five-trial cost separate from incremental leaf cost. selection-scope.md
documents exact source family, generation exclusion and unsafe population
extrapolation. README/correctness clarify stable topological commit order,
not original serialized byte order, especially when adding chunk support.

## REVIEW — 自审
Checked full source leaf count3425=all ordinary jobs, five passes, no fallback,
actual measuredCPU/wall and retirement. Scope: serial-leaf differential equality;
full4,449-module serial acceptance reference remains unmeasured. Final1330-module
Mathlib parity is separately complete. Do not substitute earlier stock-imported
controls for cold Envelope. Next one bounded task: repaired cold Envelope curve
with all ten prepared targets, preserving the14GiB stop and prior failure.
