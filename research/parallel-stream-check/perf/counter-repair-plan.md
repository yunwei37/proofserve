# Repair incomplete per-worker PMU READ evidence
The original16 native cells and four immediate decodes must finish first.
Their source, settings and outputs remain untouched. P8 original missing
READ shards remain actual incomplete counter evidence, not a proof failure.

## Purpose-specific collection, not a compression-causality experiment
The earlier uncompressed-only proposal was prepared but never launched.
After reading the matched perf6.12 documentation, prefer the official
record --no-samples --stat path: only inherited per-thread event counts are
needed for this repair. Remove DWARF sampling/frequency and compression
options, keep the same seven user-mode PMU selectors, running-time metadata
and default inheritance. This reduces unnecessary data/decoding rather than
attempting to identify compression as a cause. It is explicitly not a
single-variable performance intervention. Do not mix its time with ordinary
timing or reuse its counters as the original record's denominator.

[Primary perf6.12 documentation](https://raw.githubusercontent.com/torvalds/linux/v6.12/tools/perf/Documentation/perf-record.txt)
documents -s as per-thread counts/report-T and -n as no sampling. Neither
requests --per-thread or grouped sample reads, which can disable inheritance.
Actual attrs, expected shard IDs/READ coverage and native outcomes must still
be checked. Documentation alone is not successful capture evidence.

The adapter calls the frozen native cell implementation and edits only its
perf argv. Same fd1e9be executable, full4,449-module closure, worker placement,
C observer, no-M policy and14GiB guard inside16GiB M budget. One blocking
P-core lock task, native1100s/outer1740s after lock; serial E-core decoding.
Native work/reference acceptance and retirement must match the original.
Labels r2-count-only distinguish the repair. First P8, then a matched P4 if
valid per-worker counts are obtained. No current native restarted or modified.

If the purpose-specific capture remains incomplete, preserve it and leave
affected values unknown. Do not manufacture IPC from mismatched subsets,
interpret enabled/running per-CPU contexts as simple multiplex scaling, or
claim a repaired Lean/runtime. No Lean code or host setting is changed.
