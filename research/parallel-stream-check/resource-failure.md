# First cold Envelope stream: resource interruption (自审)

The repaired v10 cold stream stops before any leaf-curve cell.
Observed complete accepted-module records:10743. Mathlib's zero-declaration
kernel-work event completed; buffered output ends in its large acceptance event.
It does **not** identify the subsequent exact instruction/module at interruption.

Native-group RSS sampling (1s) crosses the14GiB stop at14.61985GiB; controller
calls cgroup.kill. The sample response can overshoot, not a hard RSS quota.
External charged-memory peak is9.0693GiB, a different metric.
Lane allocation remains16GiB; controller/headroom are outside the14GiB native
stop. No cap was raised. Wall to interruption1313.59964s (<1680s native deadline).
This is resource_failure, not kernel rejection, timeout or method failure.

The killed timeout wrapper's wait4 reports only0.001918 CPU seconds and9516KiB
peak, which do not cover its simultaneously killed Lean child. Total native CPU
and true peak RSS are unknown; sampled-tree peak is retained as a sampled lower
bound. Do not report those parent-only values as Lean workload metrics.
Future native runs capture cgroup cpu.stat before removal and label wait4
completeness. Compilation actually exercised the new CPU ledger.

All processes retired; a transient EBUSY cgroup was inspected empty and removed
later. Original failure/cleanup-pending record stays unchanged and a dated
cleanup record is separate. The exit callback correctly refused a second Lean
while retirement was not yet verified.

Module events now flush so a future interruption retains its last phase.
This is an observability repair, not a measured memory/performance improvement.
The next computational candidate uses4 prefix workers with unchanged14GiB
guard and1/2/4/8 leaf trials. It tests a resource alternative, not an established
cause/fix. The original8-prefix capture is retained.

Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v10
