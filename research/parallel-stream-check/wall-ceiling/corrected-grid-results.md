# Corrected Grid3793 closure —3 repeats per arm
自审,2026-11-03. Raw parallel-stream-wall-20261103, frozen sourcea62a4ba.
Exactly12/12 Grid cells and all21 Mathlib/Grid timing cells complete; all
native/cgroups retired, no stops. Every Grid arm/repeat has identical ordered
3793 accepted IDs. Input artifact/closure family matches full-grid-results.md.
Original serial O reader retained as denominator, not slower prototype1worker.

| Arm | Wall median[range]s | CPU median[range]s | PeakRSS medianGiB |
|---|---:|---:|---:|
| original serial |561.213[555.326,571.886]|558.456[555.200,561.173]|2.165|
| default persistent1worker |581.429[579.775,582.426]|579.927[578.167,580.909]|2.440|
| default persistent4workers |264.097[263.030,265.476]|630.129[626.753,634.774]|2.682|
| default persistent8workers |221.614[217.716,223.332]|662.182[661.572,668.115]|2.958|

Strong serial/4=2.125020869; strong serial/8=2.532391496.
8workers use18.575% more CPU than strong serial.4→8 improves wall16.085%
while CPU rises5.087%; added cores still not free.
Native P0–7 affinity, configured pools1/4/8, no per-worker pin. Plain means
no C profile or dependency trace. Each fresh native command includes startup,
reads/imports/planning/checking/commit/output; external lease wait and analysis
excluded.1100s/14GiB outer guards, no Lean-M. Shared host and order noted.

## Which old value can be replaced?
Old full-grid-results.md has one ordered reference/4worker pair557.567719s /
296.293453s=1.881809. The matched corrected4worker figure is2.125x, with these
three-repeat ranges. New8worker2.532x is an additional configuration, NOT a
relabeled4worker replacement. Old raw results and scope remain unchanged.
Neither is the separately measured Grid leaf/chunk curve.

New observations use kernel7.0.0-42 after host reboot; old same-binary causal
marking experiment and historical curves are not normalized across that boundary.
The new plain within-point ratios are valid scoped retimings, not estimates
attributing every old/new difference to marking. No whole-library or service
throughput claim. Original kernel and declaration content retained; trusted
reader/token-commit adapter and unsafe/partial exclusions remain explicit.
