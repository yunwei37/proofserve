# Three-repeat matched 4P-to-8P interaction
All four worker/flag groups below have3 complete plain repetitions.
Same binary/full4,449-module closure. Per-repetition pairing is kept; do not
silently exchange the median of paired differences for a difference of
independently aggregated medians.

| Metric | Off growth median | On growth median | Removed seconds median[range] | Fraction of off growth median[range] |
|---|---:|---:|---:|---:|
| CPU_s | 66.527 | 23.147 | 43.380[40.089,53.346] | 65.21%[61.80,71.76] |
| observer_CPU_s | 63.399 | 17.961 | 45.438[41.719,52.623] | 71.67%[66.54,75.03] |

All20 returned cells have exact reference module IDs and module-level observed
check/allocation-unit vectors. Runtime marking remains before worker enqueue
and after joining prior tasks. No proof/kernel change. This supports the
hypothesis that much of the observed extra CPU was a prototype shared-object
lifetime choice. The residual growth remains; this is not a universal Lean
scalability law or an exact decomposition into atomic stall seconds.
Marking also touches graph data and changes reclamation behavior.

Original-check observer includes timer/heartbeat glue and excludes other work.
Stat/IPC/coherence and aligned anonymous-memory diagnostics remain pending.
Historical3.33x/1.88x curves use other workload/baseline scopes and are preserved;
their corrected gains require exact-workload retiming rather than extrapolation.
