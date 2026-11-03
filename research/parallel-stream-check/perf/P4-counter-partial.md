# Count-only mode does not universally preserve final READ metadata
P4r2 native completed:351.719s wall,652.641s user,7.995s system;
same4,449 reference IDs/checks/units, no resource stop, native/cgroup retired.
Its five check-worker TIDs have seven-event shard-count vectors:
570955:8/8/8/8/8/7/7;570956:7/7/7/7/7/7/7;
570957:8/8/8/8/8/8/8;570958:8/7/7/7/7/7/7;
570959:7/7/7/7/7/7/7.
Event order and raw observed sums are explicit in the coverage CSV.
The strict exporter failed partial-worker-READ assertion; no complete CSV
or affected IPC was fabricated. Raw143,120bytes and all metadata remain.

P8r2 complete READs validate that point only. Removing DWARF/compression
does not guarantee complete exit counters. Next diagnostic varies only
post-native lifetime: an external parent waits5s AFTER GNUtime/Lean exit
before perf's workload ends. Native executable/input/work/timer boundaries
and counter settings remain unchanged; ordinary runtime is not compared.
The extra parent/5s belongs to recorder time, not original kernel CPU.

Run exactly one blocking lock task under the same14GiB/native1100s/
outer1740s limits. Actual drain markers, fixed work, reference IDs,
retirement and all worker READ sets must be checked. A success supports
tail-retirement involvement without proving a unique bug; a failure remains
unknown counters. No Lean or host setting is changed.
