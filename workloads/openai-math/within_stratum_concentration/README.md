# Within-stratum concentration and absolute half-cost counts

2026-11-02UTC. Self-review. No newnative measurements: originalsource32 plus
O's complete2461-module Falconer AI subtree. No-M/P0–7 native captures;
offline reduction onE8–15. AllCPU is sourcecompiler user+system, including
per-fileimports/tactics/checking/artifactoutput, not isolatedkernelCPU.

## Requested within-stratum calculation

For complete stratum h with population N_h and two observed costs a_h,b_h:

- Estimated stratum cost T_h=N_h(a_h+b_h)/2.
- Fractional empirical top10% share q_h=0.2 max(a_h,b_h)/(a_h+b_h).
- Share of totalCPU in the union of all strata's top10%:
  sum(T_h q_h)/sum(T_h)=15.62999956%.
- The different module-weighted average sum(N_h q_h)/sum(N_h)=15.47236027%
  is an average of within-layer fractions, not totalCPUshare.

These numbers use15complete strata/30draws/104632representedmodules.
Six incomplete strata remain unavailable, not assigned a zero or uniformtail.
stratum-tail.csv includes everyoriginalstratum, observedpair, censusflag,
N/2weight andmissing-data status. One stratum is a genuine N=2census;
the other14complete strata are not censuses.

**This is not an unbiased measurement of population top10%concentration.**
With only two observations, the interpolation formula necessarily yields
10%<=q_h<=20%, even for arbitrarily extreme pairs. Its smallest observed
integerfraction is50%, so rounding onefileup and calling ittop10% is wrong.
The low15.63% cannot establish that real within-stratum tails are light.

Analytic identifiability controls, not workload data: the same observed pair
(1,10) gives18.18%sampleinterpolation. A compatible1000module population
can have true top10%share10.08% or nearly100%. No actualsourcecost or
benchmark outcome is generated/changed by this demonstration.

Also the selection rule changes: globalmost-expensive10% can take morethan10%
of expensive layers, whereas within-layer10%forces quotas even incheaplayers.
Thus global42.05% versus within15.63% is not a pure sampling-bias correction.
It does not byitself separate actualheterogeneity from sampleillusion.
KnownN/2weights correct originalallocation, not informative noncompletion
or unknown within-layer distribution. Completing42draws would stillbe sampling,
not an exhaustive full-library costranking.

## A complete AI project without within-project sampling tilt

Reused O's COMPLETE Falconer AI subtree:2461exactmoduleIDs, allsuccessful
originalsource captures individuallychecked. EightglobalWstrata appear,
all ordinarysourceproxy. Its6918.855422CPU s exclude10744externaldependency
source files; the completeclosure CPU32292.603807s is a different denominator.
No2461census row is added to the original42randomdraws or samplingweights.

|Measured complete Falconer subtree|Result|
|---|---:|
|Global fractional top1%CPU share|3.621121%|
|Global fractional top5%CPU share|11.215067%|
|Global fractional top10%CPU share|18.475795%|
|Union of within-stratum fractional top10%CPU share|17.339559%|
|Union of integer ceil(10%N_h),250actualmodules|17.644438%|
|Actual modules needed for halfCPU|906|
|CPU covered by those906modules|50.038005%|

This census avoids sampling/response tilt WITHIN this project and gives actual
IDs, not duplicatedweightedpseudo-files. It is onepurposefullyselected ordinary
mathematical project, not a representative census of163097AI source modules.
Singlecapturedconstruction/machinevariation is not removed.
Here concentration is substantially weaker than raw32; a universal
AI-library top10%-majority statement is contradicted by this completeproject.
It does not refute such concentration in othercomputational projects.

falconer-census-strata.csv records exactprojectcounts andCPUweights.
falconer-census-tails.csv separates fractional and literalinteger subsets.
falconer-actual-half-cost-modules.csv lists the actual906moduleIDs/costs.

## Absolute counts for50%CPU: observed versus estimated

|Population/assumption|Module count forhalfCPU|Status|
|---|---:|---|
|Observed32originalsamples|3|Actualselected IDs|
|Complete Falconer AI subtree2461|906|Actualfullproject IDs|
|104632-module covered15strata HTdistribution|16376|Conditional model-equivalent count|
|Whole163097frame, alltenmissingdraws assignedobservedordinaryminimum|23381|Assumedcostcompletion|
|Whole163097frame, alltenmissingdraws assignedobservedordinarymaximum|25100|Differentassumedcostcompletion|

The lasttwo are **two scenarios, not lower/upper bounds on the count**:
cost-cover counts are nonlinear; mixed/interior missingcost assignments may
differ. The ordinarymin/max sourcecosttotal endpoints207.9/630.7CPUh are not
automatically countbounds. Neither16376nor23381/25100identifies that many
actualmodules for allocation. Actual whole-library count/identities areunknown.

Using only nonnegative costs and N=163097 gives a universal nonsharp count
bound1..81549; it is not a statisticalconfidenceinterval or useful measured
allocation policy. Theactual32half-cost files are LowBlock15_1,UMoments9,
BarrierData41; their complete IDs/CPUs are in actual-half-cost-modules.csv.
The906projectIDs are actionable historical observations withinFalconer;
prospective source-only cost prediction has notbeen established here.

## Reproduction and checks

Run within_stratum_concentration.py --out with a NEW directory on thePVC.
An explicit --frame allows future originaldrawsnapshots without rewritingold.
CPUweight equation checked two ways; originalconditional174.251230CPUh
agrees W077; observed32 andhalf-cost cutoffs checked.
2461rawsuccessful/no-M/P0–7source resultcells andexactIDmembership verified.
Constructed resolution controls are separateCSV, clearly not empiricaldata.
Rootpaper remains owned byroot; onlyworkloads changed.
