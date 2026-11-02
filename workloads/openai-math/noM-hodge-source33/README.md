# Hodge finished: original source33 snapshot

Self-review (自审),2026-11-02UTC. Original public source4eaee875,
Lean4.34.1, pinned Mathlibd13f23b7, authored/native HB and autoImplicit=false.
No -M; P0–7/j8/per-task shared flock; outer15GiB charged cgroup and16GiB
sampled RSS response. Standard olean+ilean+C output; not full Lake driver/linking.

## Actual recovery
The remaining176 native tasks all returned compile_ok at19:06:39UTC.
Native elapsed598.409963s, CPU724.102854s; queue-inclusive665.541616s.
All source bytes and native/controller/cgroup retirement checked.
The original IndexedInverseMultiplier draw completed **3.929919elapsed /
4.131784CPU s**, no OOM; actual wall allowance1095.52s. It did not need that
full allowance. Successful producers from prior Hodge windows were reused.

The four Hodge windows produced1719 successful source modules, including the
endpoint;15 initially cached modules had no new cost here. Hodge-producer-phases.csv
lists these measured producers only. Do not count all dependency work as the
single endpoint's HT cost or pretend their sum is a complete1734-module cold
build. Previous group allowance exhaustion was not a native failure or an
endpoint censor. Historical IntegralPairings600s censors remain unchanged.

## Original fixed sample and remaining gap

|Snapshot|Original costs|Complete strata|Uncovered module domain|Source scenario CPUh|High/low|
|---|---:|---:|---:|---:|---:|
|source32|32/42|15/21|58465(35.8468%)|207.8947–630.7017|3.0338|
|source33|33/42|16/21|18532(11.3626%)|224.1300–427.3769|1.9068|

These are assumption scenarios: all nine missing ordinary draws are assigned
the observed ordinary min1.204525s or max40.791652CPU s. Neither is a guaranteed
bound on hard nonrespondents. The width shrank422.8070→203.2469CPUh; this is
**not a95% CI**, even now that its ratio is below2. No finite completion-cost
upper bound follows without assumptions. Ten-times-max missing costs instead
give2312.2571CPUh. Full successful-build CPU and confidence interval remain unknown.

The complete16-stratum conditional construction estimate is217.424460CPUh
over144565modules. Ordinary source domain contributes159.878056CPUh; the complete
5848 marker-positive domain57.546404CPUh (26.4673% of covered CPU). Fixed original
N/2 weights and source labels unchanged. The new Hodge cellN39933 contributes
43.173230CPUh; no population weight is given to its dependencies.

## Build versus check, with O's latest complete ratios

Ordinary complete segmented closure CPU ratios: Falconer6.3124%, Mathlib8.9514%.
Computation anchors remain older unsegmented Grid/Amplitudes8.4421–8.4671%.
Do not call their mixture a measured matched protocol or full-library experiment.

|Domain|Scenario source CPUh|Transferred check CPUh across anchors/scenarios|
|---|---:|---:|
|Ordinary proxy|166.5836–369.8305|10.5155–33.1051|
|Explicit computation proxy|57.5464|4.8582–4.8725|
|All|224.1300–427.3769|15.3736–37.9776|

These transfer-model sensitivities are in latest-O-transfer-scenarios.csv.
The prior frozen O-anchor model is retained separately in missing-cost-scenarios,
rather than overwritten. Neither table is O's actual full-library verification
time. O accepted2488/163097source IDs in its finite incomplete window; its
0.694505CPUh observed check prefix is not a whole-library numerator.
The completed31 target-only fresh replays remain31pairs, a different trusted-
import protocol; no Hodge replay is invented.

## Half-cost quota and censor audit update

Applying the same per-stratum quota formula to16 complete cells gives **52,780**
rounded model-equivalent modules (fractional52772.41) in the larger144565 domain.
It is not a change from33971 on the same domain and not actual global hot IDs.
Exact n2 bootstrap reference53663–71403 again excludes the point and is not a
population CI. Entire-frame half-cost quota remains unknown. All33 original
costs are complete raw compile_ok observations, with no timeout substitution.
Nine original endpoints remain missing; dependency failures remain separate.

Reproduce estimate_native_build.py with the retained chronological result files
in sample-costs.csv and noM/authored_or_native_default/olean_ilean_c/locked-only;
missing_draw_stress.py and half_cost_quota.py accept --frame and --out. The latter
was parameterized and reproduced every frozen source32 CSV/JSON byte-for-byte.
No source or original42 sampling frame was changed. Raw results stay on PVC;
Hodge working artifacts remain intact.
