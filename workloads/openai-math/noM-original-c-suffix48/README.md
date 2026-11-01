# No-M original-C suffix: 48 completed compilations

All 48/48 exact-source Lean 4.34.1 / pinned Mathlib modules compiled with no
diagnostics. Native processes and owned cgroups actually retired; generated
.olean/.ilean/.c artifact sizes and cache-publication receipts checked.
No source generation or sample replacement.

Two original probability targets now have qualified costs:
- MixedTargets.OriginalBlock81: 3.586463 wall s, 3.643856 CPU s.
- MixedTargets.KeySound82: 23.285536 wall s, 26.319027 CPU s.

All48 native sum: 179.255830 wall s / 201.060628 CPU s. Group elapsed
9,217.807695 s includes contention/setup/cleanup; it is not native compiler
work or uninterrupted full-library throughput. One stock blocking flock
request at a time, released after each actual invocation, allowed other lanes
to acquire P0–7. Queued time was excluded from native allowances/costs.

No -M; P0–7/j8/shared lock; authored/default heartbeats; standard three
facets. Owned outer cgroup 15GiB charged-memory protection, one-second
native+controller16GiB RSS stop. Maximum sampled combined RSS7,869,591,552
bytes; native leader HWM7,703,044KiB; charged cgroup peak1,511,088,128bytes.
Charges differ from RSS for shared/file-backed pages; no hard whole-W quota
claim. No OOM kill, resource failure, timeout or sorry warning.

Original random-frame coverage rises29→31/42; complete strata12→14/21.
Whole-library CPU hours/CI remain unavailable:11 original draws incomplete.
Prerequisites have no population weight. New sample tables combine only
fresh qualified no-M costs; no old -M clock or purposeful heavy-module weight.

Raw commands, logs, samples, identities, artifact/source copies and terminal:
PVC captures/workloads/openai4341-noM-original-c-suffix48-prepared-20261101.
The old26-case prefix remains intact in its separate capture/report.

After actual retirement and W-only disk cleanup, next36 dependency/target
jobs for unchanged hard draws LowBlock15_1 and DihedralIntervals launched
2026-11-01T18:24:59UTC. See that point's actual launch/current/terminal, not
this note, for liveness. Each task independently takes/releases the shared
lock. No second W group or legacy -M queue was started.
