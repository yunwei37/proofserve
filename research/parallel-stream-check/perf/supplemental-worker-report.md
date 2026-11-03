# Complete supplemental per-worker PMU evidence

P8 count-only r2 and P4 count-only r3 (external parent/drain) have returned.
All seven inherited PMU events have all eight expected CPU-shard READ IDs
exactly once for every checking TID. Both verify the same 4,449 reference
module IDs, 237,863 checks and 3,283,925,639 allocation-counter units.
Native/decoder processes and cgroups retired; no resource stop.

These are separate evidence-repair points, not substitutes for the original
16-cell timing matrix or its record sampling denominators. Original P8
sampled metadata and P4 r2 counting metadata remain incomplete and preserved.

## Qualified checking-thread totals

| Workers | Historical TIDs | Check CPU s | Thread cycles T | Thread instructions T | Aggregate IPC | L3-miss loads M | Locked loads B | Modified-line forwarding M | RFO snoop-HITM M |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 5 | 474.359 | 1.367 | 2.506 | 1.834 | 212.642 | 5.287 | 530.642 | 351.934 |
| 8 | 9 | 537.001 | 1.511 | 2.507 | 1.659 | 290.179 | 5.293 | 758.859 | 500.140 |

Aggregate IPC is sum(instructions)/sum(cycles), not mean(thread IPC).
Individual TIDs have unequal workloads: P4 IPC 1.819–1.869; P8 1.626–1.751.
P4-drain-worker-counters.csv and P8-count-only-worker-counters.csv retain
every TID with its own check count, allocation units, CPU and hardware counts.
PMUs cover each thread lifetime; C CPU is the original-call interval only.
They are not perfectly hardware-gated counts for the C timer region.

4P→8P in these supplemental checking-thread totals: cycles +10.60%,
instructions +0.037%, locked operations +0.108%, L3-miss loads +36.46%,
modified-line forwarding +43.01%, RFO snoop-HITM +42.11%; IPC -9.55%.
C-measured kernel-call CPU grows 13.21%. The worker cycles/reference-cycle
ratio changes -2.18%; actual frequency variation is retained rather
than assuming equal nominal caps mean equal effective frequency. These observed points independently
support coherence/cache cost increasing with nearly fixed instruction work.
They do not isolate RC from every other coherence source. Main cycle-family
localization still comes from the separately scoped original sampled records.

## Metadata failure and qualification

P4 r2 no-samples still lacked four workers complete READ sets. Its native
verification succeeded; the strict exporter rejected incomplete ratios.
The raw 143,120-byte file and coverage CSV remain. P8 r2 was complete, so
neither no-samples nor no-DWARF is claimed to universally fix final READs.

P4 r3 keeps an outer parent for 5 seconds after the timed Lean child exits.
Actual marker duration is 5.000239286 s. GNUtime child wall is 349.94 s;
the recorder guard wall is 355.723 s. P8 child/guard walls are 329.24/
330.649 s. These are instrumented observations, not an ordinary speedup.
The new parent changes process ancestry as well as teardown timing: this
does not isolate the delay from parentage or prove a universal perf fix.
Neither the new parent nor its wait runs inside checking-thread counters.
The input/executable/PMU selectors and native timer boundaries are fixed.

Installed perf report-T emits no table with zero samples despite exit0.
Use actual perf report-D READ records, independently crosschecked against
200 native report-T values from the original sampled P1/P2/P8 recordings.
All expected IDs must be present and unique before IPC is exported.
Per-CPU enabled/running contexts are not naively scaled as multiplex ratios.

## Original evidence stays reproducible

The original summary now explicitly selects its declared 16 r1 keys instead
of accidentally treating later no-sample controls as original histograms.
Executed on the complete real capture point, all nine original CSVs are
byte-identical to the frozen publication-original16 copy. This source repair
does not change any original number or hot-patch a native process.

Reproduce: summarize.py POINT ORIGINAL_OUT; comparison_tables.py ORIGINAL_OUT
OUT. For supplemental workers: read_worker_counts.py POINT RUN_KEY OUT.csv.
All native commands, marker events, READ records/attrs and failed/raw data
are on the original PVC point. No Lean code or host setting changed.

The strongest supported conclusion remains: original-check growth concentrates
in lookup/ownership paths, with coherence traffic increasing at nearly fixed
work. RC involvement is supported; an exclusive causal or removable-cost
fraction remains unproved. Review: 自审.
