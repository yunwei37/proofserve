# Source33 CPU cost staircase with latest complete serial anchors

E-core reanalysis only; no extra native job. Original33/42draws,16/21complete
strata cover144565/163097modules. Fixed original weights, source exact/noM/
P0-7/j8/olean+ilean+C construction costs. Five incomplete strata and9missing
draws remain; this is not measured full-library construction or checking.

## CPU anchors and their boundaries
- Segmented Falconer:2038.443942 /32292.603807 CPU s =6.3124174%.
  Complete13205closure includes2461AI source modules and10744external modules.
- Matched segmented Mathlib Nat.Basic:91.145172 /1018.219383 =8.9514277%.
  Complete1330module closure. Both include native startup/reload/checkpoint/exit.
  Neither is a per-regime population ratio or a causal AI-authorship effect.
- Computation retains complete older unsegmented Grid8.4671469% and
  Amplitudes8.4421495%; there is no matched segmented computational CPU anchor.
- Parallel ordinary factor:93.429579 /68.569794 =1.362547CPU, from M's three-repeat
  Nat.Basic medians; elapsed factor0.656656 (about1.52x wall).
  Parallel computation Grid CPU factor1.335617, elapsed0.531404 (about1.88x wall).
  Envelope uses its own measured leaf parallel/chunk factors, with only ten
  qualified large goals. These are older M protocols transferred onto O's new
  segmented serial costs, not measured matched parallel checkpoints.
All source/evidence paths are in calibration.csv. Historical default outputs are
preserved; --latest-serial opts into these new serial CPU and elapsed anchors.

## Whole-frame class-mean projection (assumption, CPU hours)

Assume unseen modules match their class's covered mean. Source238.7835CPUh is
not the alternative fixed-missing-draw point model below.

|Class|Build|Serial stream|Parallel stream|
|---|---:|---:|---:|
|Ordinary proxy|181.2371|11.4404–16.2233|15.5881–22.1050|
|Computational proxy|57.5464|4.8582–4.8725|6.5767–6.5961|
|All|238.7835|16.2986–21.0958|22.1648–28.7012|

Ranges choose the two stated closure-transfer settings, not confidence limits.
Parallel reduces modeled durations but raises CPU: never divide CPU by wall
speedup. Summed module durations are not a measured library makespan.

## Fixed42 missing-draw sensitivity (CPU hours)
Assume each missing draw has its observed class min/max CPU cost. All missing
draws here are ordinary, with1.204525–40.791652s. This differs from assigning all
unseen modules a covered class mean. Combine both transfer settings:

|Class|Build|Serial stream|Parallel stream|
|---|---:|---:|---:|
|Ordinary proxy|166.5836–369.8305|10.5155–33.1051|14.3278–45.1073|
|Computational proxy|57.5464|4.8582–4.8725|6.5767–6.5961|
|All|224.1300–427.3769|15.3736–37.9776|20.9045–51.7034|

Exact values in full-frame-scenario-envelope.csv take precedence over rounding.
These are assumption endpoints, not bounds on hard nonrespondents or95%CIs.
Without assumptions, no finite successful full-build upper is known. Confidence
columns in conditional-staircase.csv are fragile approximate source-sampling-only
t intervals with fixed calibration; missingness, selection and transfer uncertainty
are excluded, so they are not full-population uncertainty intervals.

## Computation share and chunk marginal
Covered16strata:57.546404 /217.424460 =26.4673% construction CPU.
Class-mean full-frame projection:24.0998%. Fixed missing-min/max scenarios:
13.4650–25.6755%. Earlier17.1434% described only the31cost/14complete-cell domain;
it is neither this new conditional share nor a full-library estimate.
Explicit static markers are cost-regime proxies, not dynamic ground truth.

Chunk applies only to qualified Envelope goals. It adds about0.02947–0.02955
CPUh versus parallel at this transfer point, rather than saving CPU. Its small
modeled reduction in summed module elapsed time is separate from resource-hours
and excludes untimed support/payload generation. No chunk benefit is assigned
to unprofiled modules or every computational proof.

Reproduce:
python3 workloads/openai-math/cost_staircase.py --frame workloads/openai-math/noM-hodge-source33/sample-costs.csv --latest-serial --out <new-output>

Self-review (自审): historical default four central CSVs byte-identical; numerical
chunk-sensitivity values match at1e-12 (prior explanatory text differs). Initial
regression exposed a new scenario assertion assuming every missing draw ordinary;
generalized to per-class min/max so the frozen31 snapshot with a missing marked
draw reproduces too. This analysis correction changed no native capture.
Whole-library O prefix remains incomplete and is not divided by this projection.
