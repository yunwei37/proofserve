# C-observer controls — complete, fixed-order single observations
All four points use the same frozen corrected binary/4,449-module input and
P-first pin policy. The observer flag changes; no mathematical checker changes.
All accepted reference IDs match; native/cgroups retired without interruption.

| Workers | Observer on wall s | Observer off wall s | On CPU s | Off CPU s |
|---|---:|---:|---:|---:|
|8P|315.062|324.134|723.951|728.351|
|mixed24|325.296|322.949|1100.116|1101.513|

Observed wall-on minus wall-off is-9.072s(P8)and+2.347s(mixed24). These
single ordered points do not demonstrate negative or zero observer overhead.
There is no replication interval; code path, job placement, frequency and
ambient variation are unresolved. The fresh perf experiment must keep this
observer flag fixed and use its own ordinary controls.

CPUinflation is present either way: mixed/P8CPUratio1.520with observer and
1.512without. Wallmixed-P8changes from+10.234s(on)to-1.185s(off), so a robust
new pinned latency regression is not established. Preserve this contradiction,
rather than choosing the on-pair to exaggerate the old slowdown.
The earlier unpinned+34.985sresult remains unchanged; natural-placement
controls and the final complete factorial pair are still pending.

Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2 .
