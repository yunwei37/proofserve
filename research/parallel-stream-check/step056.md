# Step056: second matched persistence sweep and memory-scale evidence
EXPERIMENT_GATE:16/32 native points complete; two complete plain sweeps,
all4,449 accepted IDs and every module's check/allocation vector equal.
4-to-8 total CPU growth66.527/64.873s off versus23.147/24.785s on;
growth reductions65.21%/61.80%. Original-check observer growth reductions
71.67%/66.54%. Residual18-to-21s observer growth remains. Third sweep is
actually queued/running; no stat data yet.

WRITE_GATE: retain16-cell actual CSVs. Add metadata-only footprint source,
snapshot, and explicit memory projection method. Exact compiled closure
artifact count13,307 agrees with retained-region metadata. Complete Mathlib/
primary families suggest a conditional~7.4GiB resident projection; other
dependencies/heaps are not included. OAI1299 compiled modules are not the
163,097-file source frame; same-density extrapolation would be~260GiB,
very biased and not a bound. Do not claim whole-OAI residency under16GiB.

REVIEW_GATE 自审: per-repeat factorial differences checked against returned
terminals. No partial groups presented as final3-repeat medians; no atomic
stalls inferred from time-only evidence. PMU parser was exercised on seven
historical completed counters only as offline parsing qualification; those
counts were not inserted into the new matrix. Native/binary/current flags
unchanged. Future memory pair includes all boundaries, excludes its own clocks
from primary timing, and is not yet run. No competing M native collection.
