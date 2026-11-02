# Completed 31 native target replays (W075,2026-11-02)

**31/31 accepted**, exact matched target parts; zero native errors/timeouts/
resource failures or upstream unsafe/partial exclusions. Native processes,
controller and owned cgroups are retired. Actual terminal:01:00:09UTC.
Raw PVC: openai4341-noM-original31-kernel-replay-namespace-v2-20261101.
No repeat was needed: the previous one-return checkpoint was stale.

## Matched observed distribution

Seconds;31original random draws with qualified source costs, not42complete
draws or the whole source population. Source versus fresh target-only replay:

| Clock | Source median [min,max] | Replay median [min,max] | Ratio of sums | Median module ratio [min,max] |
|---|---:|---:|---:|---:|
| Native CPU |5.105 [1.070,163.846]|2.328 [0.680,81.575]|0.43108|0.45088 [0.08726,0.88498]|
| Native elapsed |4.245 [1.076,90.283]|2.376 [0.693,81.634]|0.69614|0.56799 [0.25497,0.90419]|

All31per-module ratios are below one, on these ordered source/replay observations.
CPU sums632.590445 vs272.695065s; elapsed sums393.895780 vs274.208513s.
A ratio of sums is not the median module ratio, and neither is a population
ratio or parallel makespan. Ordinary14 CPU sums154.348592/29.619979(ratio0.19190);
marked17 CPU sums478.241853/243.075086(ratio0.50827). Full distributions by
source proxy and clock are in paired-distribution.csv.

## Conditional original-stratum estimates

Only14of21paired strata complete, covering103468modules:
- Source140.851561CPUh vs target-only fresh replay54.905548CPUh;
  ratio0.389811, nominal paired95%[0,0.940135].
- Ordinary116.704826vs41.406001CPUh; ratio0.354793,[0,1.052021].
- Marked24.146735vs13.499547CPUh; ratio0.559063,[0.108241,1.009885].

Original inverse probabilities and two-draw finite-population variance are
unchanged. Covariance is retained in ratio residuals. Intervals are fragile
nominal t/delta approximations, exclude selection/nonresponse/machine drift
and scope changes, and are not confidence intervals for observed31speedups.
Still11missing source/paired draws and59629modules in incomplete strata.
Full-frame cost and confidence fields remain blank.

## Boundary: fresh targets are not an empty-environment stream

Each invocation loads trusted compiled imports, then stock-kernel replays only
the matched target declarations.31leaf artifact parts match their measured
producer copies byte-for-byte. The1713provider namespace fixes the earlier
partial-namespace setup error; full transitive producer artifact-byte identity
was not established. The two original setup failures remain retained in the
old point, not rewritten as proof rejection or successful replay.

O's decoupled-check instead checks a full dependency closure in one empty
checked kernel environment and amortizes imports/reads across the stream.
Its selected-closure ratios cannot be substituted for this54.91CPUh subtotal,
and this subtotal is not a measured independent whole-library stream cost.
No ratio is a speedup of proof search/production or a production service.

No Lean -M; P0–7, j8requested, one native at a time, per-case shared flock,
15GiB charged-memory cgroup plus1s16GiB native+controller RSS response.
Native wait4 CPU excludes coordinator/lock waiting. Total controller elapsed
14768.395s includes contention;274.209s is actual native elapsed sum.
Peak native HWM7235552KiB; sampled native7409205248bytes; largest cgroup
charge1375137792bytes. These are different accounting measures, not a hard
RSS quota or proof that1s samples capture every transient peak.

## Reproduction

The source/replay snapshots and31raw results remain on PVC; small exact
derived paired-modules.csv, domain-costs.csv, paired-distribution.csv and
observed-pairs.csv are here. Collection-verification checks every native
PID/birth retirement, cgroup cleanup, event contract and target artifact parts.
Estimator: ../estimate_paired_replay_costs.py with original42frame/strata and
../noM-original-c-suffix48/sample-costs.csv. Review: this thread's自审.

After real retirement, W launched only the prepared hard-two-suffix19 group
at01:37:11UTC(controller364584/birth763601470):17dependencies+2originaldraws.
It releases the shared lock between native tasks; no second W capture.
