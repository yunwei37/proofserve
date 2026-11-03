# P8 per-worker counts repaired by dedicated counting
Separate full-closure -n/-s capture:4,449 reference IDs,237,863 checks and
3,283,925,639 allocation units, native/cgroup retirement and no stop.
Wall330.649s/user716.985s/system12.457s are instrumented control time,
not ordinary timing or a speedup. Original16 and sample tables unchanged.

All9 historical checking TIDs have every8 CPU-shard IDs for7 PMU events;
one READ per expected worker/event/ID, no fabricated missing values.
Actual attrs retain inherit/inherit_stat, cycle samples zero. Raw173,032
bytes. The CSV includes work, cycles/instructions/IPC/L3 misses/coherence.
PMUs cover thread lifetime; C CPU covers original call intervals.
Unequal TID work means unweighted mean IPC is not whole-program IPC.

Installed perf report-T emits no histogram/table in no-sample mode, despite
exit0; its actual stderr says no samples. Use original perf report-D READ
records directly. The same aggregation was independently checked against
200 actual report-T values in original P1/P2/P8 recordings:40/56/104,
all exactly equal. This limitation and raw stderr are preserved on PVC.
read_worker_counts.py verifies complete unique shard sets before ratios.

This repairs evidence collection, not the original file or the cause of
missing READs. New counts are not a denominator for original sampling/time.
Original partial P8 remains. Matched P4 count-only measurement follows.
No Lean/host change, same14GiB/lock/native limits.
