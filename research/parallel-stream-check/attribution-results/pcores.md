# Matched full-closure P1/P2/P4/P8 model — complete P-core portion

All four observations use corrected fd1e9be source, the same frozen binary and
the same4,449-module Barrier closure, no-M, exact per-frontier distinct P-core
maps. All4,449accepted IDs match the original serial reference. All native and
cgroups retired, no guard interruption; peak RSS<=3348.372MiB. One fixed-order
observation per full point, not three repeats or a confidence interval.
Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2 .

| Workers / pins | Wall s | Total CPU s | Speed relative to P1 |
|---|---:|---:|---:|
|1 / CPU0 |655.448|647.069|1.000|
|2 / CPU0–1 |433.980|625.008|1.510|
|4 / CPU0–3 |346.351|648.965|1.892|
|8 / CPU0–7 |315.062|723.951|2.080|

## Direct attribution

| Workers | Implementation-serialized s | Original-kernel wall occupancy s | Other/coordination residual s | Original-kernel thread CPU s |
|---|---:|---:|---:|---:|
|1|161.843|474.500|19.106|468.392|
|2|161.619|251.671|20.691|445.155|
|4|159.545|164.808|21.998|467.636|
|8|158.166|133.737|23.159|539.589|

Serialized windows include read/context, graph plan, upstream complex/cycle
checking and duplicate checking. They are properties of this implementation,
not a proof that these tasks are inherently serial. The residual contains
batch cooperation, reporting, startup and uncovered code. Only5.989s at P8is
joined-batch wall outside original-kernel occupancy;17.170sis other residual.

P4->P8saves31.289s(9.03%)but consumes74.986smore CPU(11.55%).
Of that CPUincrease,71.953s(95.96%)falls inside the measured original-kernel
call intervals. Batch nonkernel CPUincreases only3.677s. Stable allocations
therefore do not imply fixed CPUcost: all3,055observed ordinary modules have
matching per-module sums,237,863checks and3,283,925,639allocation units in every
point, but ordinary-kernel CPUincreases15.39%from P4toP8.
This happens using P cores only; E-core speed is not the sole possible source
of CPUinflation. It does not by itself distinguish reference-count contention,
shared-cache effects, DVFS or observation cost. Profile-off controls are pending.

## Effective two-term fit

OLS over these four actual native wall points gives
T(n)=252.282819+395.579274/n seconds, effective serial fraction38.9408%,
RMSE11.3748s. P8observed315.062svspredicted301.730s(residual+13.332s).
The maximum absolute residual is16.092s at P2. This is a descriptive fit;
its asymptote is not a proven best possible runtime.

The fitted intercept decomposes linearly into158.457sserialized windows,
70.525sordinary-kernel occupancy,6.158sbatch nonkernel work and17.143sother
residual. Thus38.94%is not an inherent dependency fraction. The batch overhead
component has a negative fitted1/ncoefficient because its measured cost grows
with workers; no physical serial fraction is assigned to that component.
The raw JSON retains all residuals and unclipped parameters.

## Where the wave-span limit sits

P1ordinary-check work468.392CPU s divided by summed frontier maxima93.433s
gives5.013parallelism proxy. Wave barriers and module order are part of this
proxy; it is not the inherent declaration DAGspan. The source-level graph
may admit a different schedule.

| Namespace in this closure | Modules | Ordinary kernel CPU s at P1 | Frontier-span proxy s | Share of proxy span |
|---|---:|---:|---:|---:|
|Mathlib|2620|238.778|80.083|85.71%|
|OAI|20|156.130|1.542|1.65%|

The OAI computational declarations are highly parallel within this prototype
(work/span proxy~101.2), while its Mathlib dependency prefix has proxy~2.98.
At P4->P8, OAI ordinary-kernel occupancy43.545->27.892simproves, but its
CPU171.461->215.135srises. Mathlib occupancy97.338->87.593shas much less
headroom. Leaf parallelism cannot be substituted for whole-closure scaling.

## Boundary of the conclusion

The current evidence establishes saturation plus per-work CPUinflation before
adding E cores. It does not yet assign the historical unpinned34.985sextra
wall to a particular cause. Pure E16/mixed24, profile-off, and natural-placement
controls are still running/prepared. The existing sequence misses profile-on
natural-placement attribution; a final pair is prepared to complete the
placement x observation control, using the same frozen binary only after that
sequence retires. It is not yet submitted or measured.
