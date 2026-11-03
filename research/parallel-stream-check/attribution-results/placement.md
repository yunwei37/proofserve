# Natural-placement versus deliberate pinning — observer off
Same frozen binary, same complete4,449-module closure and reference accepted
IDs. No-M; all native/cgroups retired, no resource stop. Single ordered points.

| Configuration | Placement | Wall s | CPU s |
|---|---|---:|---:|
|8P|per-frontier CPU0–7 / coordinator0|324.134|728.351|
|8P+16E|P-first CPU0–23 / coordinator0|322.949|1101.513|
|8P|ordinary OS placement within0–7|304.470|699.597|
|8P+16E|ordinary OS placement within0–23|321.320|1123.067|

Under ordinary OSplacement, mixed24takes16.850smore wall(+5.534%)and
423.470smore CPU(+60.531%)than8P. Under the deliberate map, the single
mixed point is1.185sfaster. Pinning itself also changes P8(+19.664s);
the maps therefore cannot be treated as a free control of heterogeneous speed.

The wall comparison's direction depends on policy/run conditions in this new
cohort. Its CPUtax survives both policies and both observer settings. This is
why the pending natural-placement/profile-on pair is needed to locate where
the OSplacement delta falls instead of importing the pinned decomposition.
It is the last cell of the placement x observation control, not a new method.

The historical unpinned+34.985sremains historical; these new absolute times
are not assigned as its old phase costs. No clean causal separation of pin
policy from frequency/drift is possible from single ordered observations.
The24worker50-target residency/byte check is currently the actual next native
phase. No target result is claimed until complete.

Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2 .
