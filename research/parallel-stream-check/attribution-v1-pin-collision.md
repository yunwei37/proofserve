# Invalid v1two-worker placement point — retained, not model input
Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102 .
Both whole4,449-module checks accepted the serial reference IDset and retired.
P1wall526.124748s, CPU525.368714s; requestedP2wall500.604562s, CPU539.995112s.
These are retained observations of the faulty placement variant, not primary
scaling points. The refreshed matched model must use the corrected v2source.

The sticky TIDmodulo2map encountered three OSworkers. Two different TIDs
(481169,481171)were bound toCPU0; one(481170)toCPU1.
For the root leaf, two workers performed26.937and26.885CPUsonCPU0while
CPU1performed only0.067CPUs. Requested2workers did not yield2heavy compute
cores. The observer caught this: total full-run ordinary-kernel CPU347.664s
onCPU0versus44.871sonCPU1. CPU-membership-only preflight was inadequate.

The bug is in M's added pinning adapter, not the original Lean checker or the
earlier unpinned8/12/16/24curve. Original v16results/17c4989remain unchanged.
v2resets a per-frontier slot counter and gives each active job a unique core,
rejecting duplicate maps/oversubscription. Actual TIDs can migrate between
frontiers; within-check migrations are tracked. A new two-core positive control
is required before new full points. Old captures/source/compiler failures remain.

P1direct phase result is descriptive only: read/context26.314s, plan8.940s,
upstream serial checking94.446s, parallel-path kernel occupancy379.388s,
remaining17.009s. Its ordinary kernel work379.021CPUshas75.323ssum-of-frontier-
maxCPUproxy, average5.032. That proxy includes algorithmic wave barriers and is
not the inherent declaration DAGspan. No serial fraction is inferred from the
invalidP2point, and no old/new source timings are pooled.
