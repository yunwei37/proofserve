# Step023: complete matched P-core model and localize saturation
EXPERIMENT: p48completed normally; all four same-source complete P1/P2/P4/P8
points now available. Wall655.448/433.980/346.351/315.062s; CPU647.069/625.008/
648.965/723.951s. Original4,449reference IDs match, no interruptions, all
native/cgroups retired. Exact per-wave physical pins and recorded original
kernel/core counters exclude the former sticky-slot alias defect.

RQ3result: effective two-term serial parameter38.9408%, RMSE11.375s,
not an inherent fraction. Only158.457sof fitted252.283sintercept comes from
implementation-serialized windows;70.525sis ordinary-kernel saturation and
the rest coordination/residual. P4->P8extraCPU74.986smostly(95.96%)occurs in
original kernel call intervals rather than external batch cooperation.
Allocation sums remain fixed. The same effect on homogeneous P cores rules out
a solely heterogeneous-core explanation. No cache/atomic root cause is asserted.

The dependency/computation distinction is directly visible: Mathlib prefix
85.71%of P1frontier-span proxy, OAI20modules1.65%despite one-third of ordinary
kernel CPU. This is scheduler-wave span, not intrinsic DAGspan.
Full table/model residuals/namespace CSV under attribution-results/pcores.

WRITE: small model/component/CPU/resource and namespace tables, interpretation
and limitations. Prepared one final finite natural-placement/profile-on pair
because the original sequence lacks that cell of the placement x observation
control. It uses the same frozen binary after the original finite sequence
actually retires. Prepared does not mean queued or executed; active execution
source and binary remain unchanged. Offline analysis consumer supports the
pair, actual original-byte comparison and target-specific hardware calibration.

REVIEW 自审: did not combine older invalid v1, old serial implementations,
leaf curves or historical unpinned timings with the fit. The 38.94%parameter
is effective, with sizable residuals retained. Negative overhead coefficient
is not clipped or given a physical fraction. Unpinned per-core CPUis attributed
to start core and endpoint migration is only a lower bound. Self-review only.
An obsolete local tool handle returned a disconnected preflight transcript;
actual original series485768/birth771540558was reverified healthy and no task
was restarted. Its typescontroller489094/birth771716186held the P lock at
00:09:49UTC. Only owned files; goal active, no host/network/config/agent change.
