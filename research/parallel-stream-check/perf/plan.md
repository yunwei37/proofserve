# RQ3: why checking a fixed declaration set consumes more CPU with workers

User-directed hypothesis: shared atomic reference-count traffic and cache
competition make each original-kernel call more expensive. The positive
alternative is increased hash/cache lookup, allocator or whnf/defeq work, or
lower frequency. Do not modify Lean. Reuse the same frozen fd1e9be binary and
complete4,449-module Barrier closure; all inputs/accepted reference IDs fixed.

## Actual measurement, after the existing finite series is archived
One native process and one blocking P-core lock task at a time, taskset0–7,
per-frontier worker pins0..n-1/coordinator0. No-M, <=14GiB sampled own RSS and
charged cgroup guard inside16GiB lane. One cell <=1100s; outer <=1740s after
the lock. No host sysctl/security/config change. Native, perf, children and
wait4/cgroup retirement are all recorded; partial/unsupported data retained.

Qualify on the existing actual ComputeControl input, not a new synthetic
benchmark. Verify command completion, inherited worker events, positive
cycles/instructions, observer work and original verdicts, stack ancestry and
actual per-thread read counts. Parser-only dry-run already passed, but no PMU
event has yet been opened in this new study. Qualification is not a result.

Then at each n=4,8,1,2 run a perf-free control before, perf stat, perf record,
and a perf-free control after. Each gets a fresh lock; one initial observation
per stat/record cell and a bracket of plain runs. C-observer remains on in all
arms to retain measured TIDs/work sums and compare exactly the same code path.
Report plain, stat and record times separately. No performance speedup is
computed by mixing ordinary and perf-instrumented observations. The two plain
points bound observed drift, not a confidence interval. Repeat targeted4/8
comparisons if that drift leaves the category inflation unresolved.

## Counters / inheritance
Actual cpu_core event metadata is saved on PVC. Use cycles, instructions and
reference cycles; retired L3miss loads; retired locked loads; L3modified-line
forwarding(HITM); and RFOsnoop-HITM. Report raw counts, enabled/running coverage,
IPC and counts per1,000instructions, not just percentages.

perf record -s and perf report -T provide per-thread final counters. Independent
auxiliary events have period=0; only cycles samples at99Hz with16KiB DWARF
stacks, zstd1. Do not use record --per-thread or :Ssample-read groups: those can
disable inheritance and silently miss dynamic Lean workers. Check actual
recorded attributes and thread coverage during native preflight. Missing
events/counters remain missing, never zero. Counter values concern full command/
thread lifetimes; call-stack sample attribution is a separate scope.

Primary references read:
- https://raw.githubusercontent.com/torvalds/linux/v6.12/tools/perf/Documentation/perf-record.txt
- https://raw.githubusercontent.com/torvalds/linux/v6.12/tools/perf/Documentation/perf-list.txt
- https://raw.githubusercontent.com/torvalds/linux/v6.12/tools/perf/util/evsel.c
The installed tool is6.12.113; native qualification checks actual behavior.

## Exclusive sample attribution
Use perf's native Python process_event API, stream aggregation on CPU8–15,
no huge expanded script text or UI. Separate call chains anchored by the
ordinary checkOne and C++kernel from truncated/unanchored worker stacks,
serial replay kernel and outside work. Report uncovered weighted periods.
Classify each anchored sample once by its nearest operation: RC/destruction,
allocation/free(including actual mimalloc), hash/cache lookup, whnf/defeq,
other type inference, memory copy, other/unresolved. Category cycles are
period-weighted sampling estimates, not exact hardware counts.

The shipped C++code has symbols but incomplete inline debug information.
Hot whnf/defeq symbols may contain inline RC. Inspect their weighted sample IPs
and disassembly; do not count all such cycles as semantic reduction, or treat
an absent lean_inc_ref symbol as no RCcost. The actual installed lean.h uses
inline atomic increments for negative MTcounts; rc=0persistent/compacted inputs
bypass updates. P1also dispatches IOtasks, so ST->MTis not assumed to occur
only when n>1. Stable locked-instruction count plus higher RCcycles/HITMwould
support contention; extra instructions indicate more work; stable cycles with
higher CPUtime can indicate frequency. None alone proves a causal mechanism.

If attribution remains ambiguous, report it and use a targeted locked-load
PEBS/address sample on4/8only to distinguish shared cache lines, rather than
changing the runtime. Counter-to-cacheline mapping is not inferred from LLC
misses alone. No optimization is part of this experiment.

## Storage and outputs
Raw on PVC parallel-stream-perf-20261103; record files never enter Git.
Small category-by-worker/worker-count, per-thread counters/IPC/LLC/HITM and
overhead tables plus interpretation go under this owned path. Decode serially
relative to own heavy native work to respect16GiBaggregate. After analysis is
committed/referenced, clean only our large raw intermediates and log each
deletion. Unanalyzed and failed raw records are preserved.
