# Source compilation CPU distribution and concentration

2026-11-02UTC; self-review. These are exact authored-source module compiler
processCPU measurements, no-M/P0–7/j8, olean+ilean+C and externalcgroup.
They include that invocation's imports/elaboration/tactics/check/output work,
not isolatedkernelCPU, projectmakespan or end-to-endservice latency.

## Requested32-module description

32of42original draws completed: total817.179526CPU s, median6.770575s,
P90(R7)63.553991s, maximum184.589081s(LowBlock15_1).
The largest3originalcosts are184.589081,163.845944,113.882318s.
Four observed expensive files(12.5%of32) consume64.661493% of this observed
CPU. This selected panel contains18explicit-computational draws(56.25%),
versus3.5856%ofwhole-sourcefiles: it is deliberately stratified and incomplete,
not a uniform full-library distribution.

|Top module fraction by CPU|Selected32cost share|Complete15strata weighted cost share|
|---|---:|---:|
|1%|7.228339%|24.566862%|
|5%|34.618666%|35.011670%|
|10%|58.192105%|42.048801%|

These fractional-boundary curve points linearly interpolate the last ranked
atom. A32module panel has integer resolution3.125%; it does not observe a
literal0.32module top1%. The CSValso givesactual integer counts:
top1file(3.125%)22.588559%, top2(6.25%)42.638737%, top4(12.5%)64.661493%.
Do not present interpolated1% as a directly observed population percentile.

The weighted column uses30draws in15complete originalstrata, N_h/2weights,
representing104632modules. Weighted median4.435118s/P90 8.435903s are
left-inverse weightedCDF values, not the raw32R7statistics.
Total174.251230CPU h matches the originalHTcomplete-cell total.
Tail ratios and quantiles are nonlinear plug-in quantities, not unbiased
population totals; no confidence interval has been established for them.
The two other returned draws sit in incompletecells and remain in raw32,
but cannot turn the missing35.8468%ofpopulation into completecoverage.

Thus the observed panel has substantialcostheterogeneity, but these data
do **not** establish that the whole AI library's top10%consume a majority.
Even on completed15cells the corresponding weighted estimate is42.05%.
The current full-frame hypothetical min/max missing-cost scenarios give
top10%shares42.03%/34.21%; those assumptions are neither confidencebounds
nor bounds on arbitrary unobserved heavycosts. Sourcebytes and actualcost
also differ: largest-by-bytes10%consume43.19%inraw32 /38.81%inweighted15.
Expensivefileoracleordering does not demonstrate a source-size scheduler win.
The prior negative held-outsourcecost prediction is not refitted here.

## Curves and reproducibility

concentration-curve.csv gives exact ranked cumulativeCPU/count coordinates
for raw32, conditional15cells and the two explicitly hypothetical missingcost
completions. top-cost-shares.csv gives1/5/10/20/50%points and integercounts.
source-size-cost-curve.csv gives the separate source-bytes-order curve.
distribution-summary.csv states quantile definitions, denominators and limits.
Run cost_concentration.py --out /workspaces/.agent-state/gpu-smt-captures/workloads/NEW-UNUSED-DIRECTORY on E8–15; no newnativeprocess. Arithmetic checks
match817.179526observedCPU s and174.251230weightedCPUh; everycurve ends(1,1).
Unknownoriginaldrawcosts are never silently imputed for the primaryresults.

## Reconciliation with O's native checking CPU

The complete result currently available for cross-check is Falconer's
13205-module closure, not all163097source modules. Its IDset contains2461
W-frame modules and10744external-to-W-frame dependencies.
W independently reread13205successful rawcompiler cells and27successful
streamsegment cost records. O reports whole-closure graph/referenceparity;
W did not run another mathematical referencecheck.

|Same Falconer closure|Construction|Checkpointed streamcheck|Check/build|
|---|---:|---:|---:|
|NativeCPU h|8.970168|0.566234|6.312417%|
|Sum native elapsed h|6.132714|0.567663|9.256304%|

The6.3124%CPUfraction lies inside W's old ordinaryclosure anchor envelope
3.9699–6.4497%. This is consistent for this selected completeclosure, not
validation of the full-libraryprojection. It overlaps the NearPin project's
family and uses a checkpointedadapter, so it is not independentcross-project
confirmation or a causal adapteroverhead result.

When O's whole-library run returns, reconcile **module IDs before totals**:
163097internal-sourceframe versus actualtargetset plus externalclosure;
same source/SDK/Mathlib revisions; missing/import/failure/unsafe/partial policy;
successful originalchecked-module set; once-onlyexternalkernel work; repeated
per-sourcecompileimports; and stream checkpoint/restore/contextfallbackCPU.
Use native user+systemCPU on both sides. Queue wait, parentCPU, setup/reference
qualification and failedrecovery are separate costs, not silently borrowed
denominators. A completed Falconer subset cannot supply the wholeframe numerator.
A discrepancy beyond assumptions should first be reduced on the same exact
closure and measuredsource costs, then attributed to mix, sharedbase,
checkpoint/context or missingcosts; do not retune a ratio merely to fit.

The207.9–630.7sourceCPUh /10.8–41.8streamCPUh values remain missing-draw /
fixed-anchor scenarios, not full-library confidence intervals. A new full
Omeasurement may challenge that transfer; it must not be relabeled as a
measurement of these old scenarios.

Recompute the Ocost cells with reconcile_stream_costs.py --out followed by a
fresh analysis directory on thePVC. This analysis does not start O controllers
or rewrite Oresults. Complete parity stays Oreported evidence.
