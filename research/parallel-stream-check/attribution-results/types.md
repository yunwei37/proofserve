# Complete physical P8 / E16 / mixed24 comparison
Same corrected frozen binary/4,449-module closure. All original serial
reference accepted IDs match, native/cgroups retired, no memory interruption.
Three hardware configurations each have one fixed-order observation, with
observation enabled. P1/P2/P4/P8model is separately retained in pcores.md.

| Configuration | Worker pins | Coordinator | Wall s | CPU s | Peak RSS MiB |
|---|---|---:|---:|---:|---:|
|8P|0–7|0|315.062|723.951|3348.371|
|16E|8–23|8|425.347|1121.948|3609.953|
|8P+16E|0–23, P-first|0|325.296|1100.116|3686.379|

E-only uses an E coordinator as well as E check workers. Its32.6%longer
serialized windows209.708vs158.166sand longer ordinary-kernel occupancy
169.540vs133.737sare measured separately. This is not a pure fixed-serial
calibration of Eparallel capacity. The same resident helpers' P/Ework-rate
calibration is still pending.

## Why this new mixed point is slower

P8->mixed24wall+10.233695s(+3.248%); CPU+376.164788s(+51.960%).
The measured signed decomposition is:
read/context+1.073299s, plan+0.179648s, upstream serial replay+3.970314s,
duplicate+0.000953s, ordinary-kernel occupancy-0.453181s,
batch outside kernel occupancy+4.624605s, other residual+0.838057s.
The components reproduce the full delta without borrowing historical time.

Thus extra workers hardly shorten the occupied-kernel critical time in this
configuration, while joined-batch overhead and serialized costs increase.
Ordinary-kernel thread CPU539.589->901.407s(+67.05%)despite all observed
per-module allocation sums being unchanged:3,055ordinary modules,
237,863checks,3,283,925,639units. Batch nonkernel CPU9.427->19.589s.
More worker CPUdoes not mean proportionally more useful elapsed progress.
Physical per-core work/CPUtable is included; no within-check migration occurred
with these singleton bindings. Historic OSthread count is not active concurrency.

The+3.97sserial replay increase also cannot be assigned to work-sharing
coordination: no check workers are active there. Frequency, preceding thermal
state and other uncontrolled run conditions remain plausible. No host setting
was altered. The measured kernel CPUinflation motivates the user's perf
experiment; atomic reference counts and cache competition remain hypotheses.

## Scope

This is a new deliberately pinned/P-first profile-enabled experiment. It does
not retroactively explain every second of the old unpinned+34.985sregression,
nor replace its raw result with+10.234s. Profile-off and natural-placement
controls remain essential. All comparisons consume stored declarations:
Mathlib prefix timings measure validation of existing proof terms, not source
elaboration or tactic-search parallelism. The shared one-node NUMAtopology
does not imply absence of cache contention.

Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2 .
