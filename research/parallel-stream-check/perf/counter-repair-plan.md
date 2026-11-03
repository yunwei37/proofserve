# Repair incomplete per-worker PMU READ evidence
No current native cell is modified or repeated. First collect the original
16-cell matrix and all four immediate decodes. The original partial P8 READ
records and raw capture are retained. P4 metadata completeness is unknown;
P1 is complete. This defect concerns PMU counter evidence, not proof verdicts.

If P8 still lacks matching per-worker counter shards at the end, run one
additional P8 recorder control, with exactly one changed perf option: remove
--compression-level=1 and use the default uncompressed format. The original
fd1e9be executable, inputs, PMU selectors, sampling frequency, DWARF size,
worker placement, C observer, no-M setting and memory limits are unchanged.
The adapter calls the frozen native cell implementation and edits only its
perf argv before execution; actual command and terminal are retained normally.
It asserts the original foreground16-cell terminal before any native launch.

Use one blocking P-core flock, after-lock wrapper1740s, native1100s,
same14GiB sampled own-tree/cgroup budget inside the16GiB M allocation.
Decode serially on E8-15 after native retirement. Verify reference accepted IDs,
fixed checks/units, all expected worker/event CPU-shard IDs, sample losses and
reported enabled/running fields. Do not call missing metadata zero or fix it
using a different command's denominator. Compare new counts with their own
run, not as a repeat of original r1 timing. Perf time stays instrumented.

A full result repairs evidence only. It does not optimize Lean or identify
compression as causal without the actual control. If it fails too, preserve
both and state that per-worker counts remain partial. Any further intervention
must follow the actual evidence; no blind perf grouping/inheritance changes.
A matched P4 recorder control is needed if the new method succeeds and a
complete four-worker per-worker comparison is claimed. Raw data is never Git.
