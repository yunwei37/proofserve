# Native CPU is not serial compilation elapsed time: the26-module cohorts

Question:in the existing26module historical pairing,how far do compiler elapsed
and native CPU differ? Values below are recomputed from each actual native
wait4result,not inferred from thread count.52historical raw observations were
cross-checked against the published paired CSV. No new native timing.

|Cohort|Native wall sum s|Native user+system CPU sum s|CPU/wall|
|---|---:|---:|---:|
|Historical26,-M arm|432.134416|650.293756|1.504841|
|Historical26,no-M arm|350.212707|555.744907|1.586878|
|Fresh no-M,exact same26module names|350.818085|557.564144|1.589326|

For the historical no-Marm CPU exceeds the wall sum by205.532200s,
58.6878%of wall. Equivalently,using wall as CPU would undercount this observed
work by36.9832%of CPU. The fresh same26point differs by206.746059s,
58.9326%of wall. These percentages have explicitly different denominators.

Per-module CPU/wall differs:historical no-Mmedian1.190377,range1.000367–
3.191490;freshmedian1.188183,range0.993743–3.239233. Ratio of sums is not the
unweighted median ratio. CPU/wall near or below1can reflect waiting/accounting;
parallel thread work can make it exceed1. The8thread setting is not8effective
cores or an8x speedup.

The same fresh26split by the fixed source marker proxy gives ordinary11:
59.697252wall/109.285174CPU s(1.830657);certificate15:
291.120833wall/448.278970CPU s(1.539838). These are unweighted observed
subsets,not population class shares or profile-derived kernel percentages.

## Which conclusions require which clock?

- **Population work/budget**:HTtotals of compiler/checker work and class CPU
  fractions must use native user+system CPU. Each sample uses its actual
  inclusion weight; prerequisites and purposeful cases have no such weight.
- **Build versus replay work**:report the paired CPUratio separately from the
  paired wallratio. Differing internal parallelism means they can support
  different conclusions. Replaying on one fresh process does not inherit a
  producer's effective core count or sampled C++fraction.
- **Latency/throughput/deadlines**:measure walltime for the stated execution
  policy. A native serial sum excludes lock queues/orchestration and is not
  parallel Lake makespan or service end-to-end latency. Extrapolated CPU/8is
  only an optimistic work-capacity lower bound,not a wall forecast.
- **Phase attribution**:user-cycle/instruction samples are their own
  denominators. They are not whole-process CPUseconds,system CPUseconds or
  wall fractions. No oldprofile fraction reweights a newrun denominator.
- **Failures/timeouts**:a wall deadline and consumed CPU are different facts.
  A32sremaining-group interruption is not a600snative timeout or a false goal.

-Mobservations and the historical M/no-Mexperiment remain methodology only.
The fresh no-Mcohort is a different run;its qualified original samples enter
the existing estimator individually,not as a duplicated26-case average.
No global CI,repeatability interval or full-library validity follows here.

Raw historical point:
captures/workloads/openai4341-memory-option-pairs-20261031/runs.
Fresh point:
captures/workloads/openai4341-noM-standard-a-20261031/results.jsonl.
The O-line startup/replay tables have different memberships and trust/time
scopes;they are not silently treated as this26pair. Current31target replay is
an independent matched-target measurement pending actual native completion.

## Same current14strata: changing the clock also changes the cost share

Using the same completed no-Moriginal draws and inclusion weights over the
14complete strata(103,468modules),the CPUestimates are24.146735certificate/
116.704826ordinary hours,certificate share17.1434%. Weighting the native serial
process elapsed times instead gives18.790827/108.086603hours,share14.8102%.
The point-share difference is2.3332percentage points. This is descriptive,
not a significant-difference test or whole-library estimate.

The weighted complete-stratum discrepancy is not the26cohort's1.589factor.
Neither a cohort-average correction nor a producer profile fraction converts
one clock into the other. Covered14-clock-choice.csv and per-stratum CSV
retain both measurements. Missing59,629modules still prevent a globalshare.
