# Full one-worker result: counters complete, ordinary bracket pending
The P1 record returned 4,449 reference module IDs, 237,863 checks and
3,283,925,639 allocation-counter units, as in P4/P8. Its 662.333 s wall,
652.477 s user and 4.221 s system include perf; they are not an ordinary
one-worker timing. The P1 trailing ordinary point is still live or queued.

The single observed check-worker TID548214 has every captured CPU-shard READ
for all seven PMU events. Its full-thread lifetime counters give
1,228,077,675,400 user cycles, 2,505,687,214,549 instructions, IPC2.0403,
182,046,350 retired L3 misses. This is not hardware counting confined to the
C-measured check interval. P8 has five incomplete worker READ sets; P4
completeness is unknown after earlier raw cleanup. Those fields remain
qualified in the CSV, not repaired by borrowing a stat denominator.

45,766 cycle samples have periods. Strict checkOne+C++kernel anchored mass
is674.023 billion cycles; the additional worker/kernel unanchored mass is
336.899 billion. Strict families are lookup262.802, whnf/defeq140.998,
explicit RC/destruction87.889, allocation77.343, other inference104.861
billion. The coarse lookup group includes inlined ownership bookkeeping;
see ownership-localization.md. Sampling mass is not exact hardware counting
or a removable-cost bound. No Lean code, event or native setting changed.

This is cell11/16, not matrix completion. The foreground collector remains
blocked on the real next native exit; the original waiting parent is
deliberately stopped between collections. No repeated or competing native.
