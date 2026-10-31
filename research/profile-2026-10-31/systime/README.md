# M: OS-time attribution in native Lean compilation

**The frozen 90-cell matrix is complete.** See the [final attribution](final/README.md),
[all configuration medians and ranges](final/native-results.md), and
[W's paired-panel handoff](final/w-handoff-design.md).

Grid and UMoments9 have substantial native memory-guard accounting cost;
EnvelopePsiB is the low-system-time control. Removing native -M while retaining
the same outer protection reduces their wall medians by50.85%,37.76%,1.44%.
All90 decisions/diagnostics/.olean outputs match; all210 artifact comparisons
match. This is a three-module benchmark-policy result, not an engine gain or
a measured full-library correction. All review is same-thread 自审.

[Plan](plan.md), [frozen matrix](matrix.csv), [step005](step-005-report.md),
[outer audit](step-005-audit.md). The earlier [Grid interim](grid-interim/README.md)
and setup/queue steps retain their original observation boundaries.

All timed/profiled runs used CPU0–7 under the existing pcore.lock, with a
constant temporary15GiB native cgroup and at most1200s native self wall.
Analysis/preparation uses E cores. Source, raw perf.data, syscall captures,
artifact bytes, native/process identities and memory records remain outsideGit:

    /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/

Reproduce the small tables without launching Lean:

    taskset -c 8-15 python3 research/profile-2026-10-31/systime/analyze_final.py

Plain, stat, record and trace clocks remain separate. Trace elapsed can overlap
across threads; record percentages refer to sampled cycles. Grid has trace
event loss; no-M has no recorded-stack arm, so residual system-time percentages
are not fabricated. See the final report for these and the caller-unwind limits.

Historical failed setup controls stay preserved on PVC: one wrong-affinity
helper was stopped; three imports failed under15GiB address-space caps.
They are excluded from the90 valid matrix cells. The qualified runs have no
fixed AS cap, no parent quota change, no host sysctl/module change.
[Historical26-module concentration](historical-attribution-prior.md) remains a
different resource/artifact/observation point and is not pooled with this matrix.
Root owns characterization-paper integration; M edits only this directory.
