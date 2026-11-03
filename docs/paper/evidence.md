# Six-page paper: evidence and completion map

The 3 November review authorizes revised RQ wording, a data figure, a direct comparison with the complete nealmcb report, and replacement of the 41/42 snapshot. This map is provenance, not a second paper or independent review. Root ran no new Lean measurement.

## Admitted measurement snapshot

Original data-package revision: **1cc14067722a724c7d0eda6df52d81595c731d9f**. All **42/42** original draws and **21 strata / 163,097 modules** are complete. The fixed independent precision draws remain separate.

- [Final estimates](../../data/openai-math-4eaee875/final-estimates.csv), [sample costs](../../data/openai-math-4eaee875/sample-costs.csv): original stratified compiler total **279.1200782928 CPUh**, nominal 95% **95.1776075142–463.0625490713**, effective df **2.6086207962**. Marked-file compiler estimate **57.5464042772 CPUh**, share **20.617078%**. Two draws per stratum and heavy tails make the nominal approximation fragile. This is native per-module compiler work, not measured Lake makespan or dynamic kernel phase weight.
- The old 41-cost missing-value scenario is historical and has been removed from current prose. Completing the fixed sample does not eliminate sampling uncertainty.
- [Selected complete closures](../../data/openai-math-4eaee875/closure-ratios.csv): Falconer CPU **6.3124%**, wall **9.2563%**; matched checkpoint Mathlib CPU **8.9514%**, wall **14.6662%**. Overlapping closures and protocol differences remain explicit.

## Figure 1: clocks, source labels and reproducibility

[CPU plot inputs](figures/cost-regimes-cpu.csv) reproduce all 31 completed pairs from [paired-modules.csv](../../workloads/openai-math/native-replay31/paired-modules.csv). Median replay/compiler CPU is **0.4508809990**; unmarked 14 have median **0.3905818925**, marked 17 **0.4978783179**. These are source proxies, not a semantic two-class classifier. Whole target-replay processes trust imports. [Root0260 qualification](../tmp/build-and-evaluate/step-0260-20261102T020415+0000/step-report.md) records their no-M commands, completed identities and equal input artifacts.

[Target-wall inputs](figures/cost-regimes-target-wall.csv) come from [root-components.csv](../../research/decoupled-check/root-components.csv):
Mathlib Nat.Basic **0.026843838 / 0.410717749 = 6.53584%**;
NearPin **0.004472574 / 0.962273934 = 0.464792%**;
Grid **255.488732184 / 318.230851566 = 80.28409%**;
Amplitudes **110.026430792 / 133.615322179 = 82.34567%**.
The numerator is target read/map/replay after dependency preparation; the denominator is the target source compiler process. These are **wall intervals, not CPU phase shares**. Existing root0246 independently qualified the original no-M source costs, timer boundaries and matching closure graphs. The kernel-call subintervals are 0.026772106 / 0.004415718 / 255.486529166 / 110.024965725 seconds, respectively.

The figure is standard PGFPlots and reads both small CSVs directly. Rebuild with `tectonic cost-regimes.tex` in [figures/](figures/), then compile main.tex. Colors and shapes distinguish proxies; panel (b) identifies ordinary controls versus finite computational certificates. The overlapping scatter does not establish bimodality.

The old **75–94% versus ~2%** phase claim came from memory-guarded experiments and is excluded. Figure 1 makes no such claim.

Additional selected cases in the prose:

| Case | CPU evidence | Scope |
|---|---|---|
| Ramsey K10 | 356.442522 / 1725.133882 = **20.661731%** | Single module-local check, imports trusted; unmarked source can still compute |
| Ramsey 20-module panel | 815.679164 / 2271.356756 = **35.911539%** | Selected within the 190 built targets out of 444; retained prefix only |
| SubexponentialSAT | 3399.302946 / 46905.836649 = **7.2471%** | Primary full 14,721-module accounting; independent controls pending |
| Same SubexponentialSAT numerator | / 21532.088264 = **15.7871%** | Denominator contains only 3,977 new target compiles; not a matched target-only check ratio |

K10 and Ramsey were qualified in root0275. SubexponentialSAT comes from [primary-costs.md](../../research/decoupled-check/subexponential-primary-costs.md) at **6bdce8db17396f74b16412c2211e3248fb3eed38**. Its primary accounting is not final independent qualification or a release-tool system result.

## Coverage and repeatability

- [Masked lexical census](../tmp/build-and-evaluate/step-0231-20261101T001556+0000/experiment-001/reanalysis.json): AI **1,354,379 sites / 5,848 files / 1,785,499,363 bytes**; Mathlib subtree **7 sites / 4 files / 98,449,500 bytes / 8,529 files**. Decimal-MB density ratio **10,668.3188327**. Raw 8/5 includes a documentation comment and is not used.
- [Default scope](../../workloads/openai-math/default-build-scope/scope-comparison.csv): **32,263 / 163,097 = 19.7815% source modules** outside the OAI default closure; **451,008 / 1,354,379 = 33.3000% decision sites** outside. The review's proposed “33.30% of modules” would use the wrong denominator and was corrected.
- [Stored-proof panel root0262](../tmp/build-and-evaluate/step-0262-20261102T030442+0000/experiment-001/reanalysis.json): **2,524** eligible helpers from three modules, workers 1/2/4/8 and three repeats, **30,288** accepts / **22,716** one-worker versus higher-worker pairs. Zero verdict, diagnostic or allocation-count differences. Contexts/imports are trusted; this is historical fixed-panel evidence, not final release CI or future-budget assurance.
- [Installed external static audit](../../data/external-projects/audit-before-build.csv), result commit **1754aada94337233c636dd1a1a2ef7718696b106**, installed bundle **703055a11b749013d7251d93bb7127bd5222a447**: CrocSwap **64/64** default-covered, Newspeak **105/105**, Solar **12/32**, leaving **20** outside. Project commits are in that CSV. Solar's custom checker may consume omitted modules separately. AI assistance is disclosed for the CrocSwap subproject; do not convert that into a blanket wholly-AI-generated provenance claim.

## Direct comparison with the earlier same-corpus report

The complete **804-line / 74,061-byte** [REPORT at c9570a82](https://github.com/nealmcb/openai-math-lean-tooling/blob/c9570a82f79b78a1a969a6316ac0fdd69aabef55/REPORT.md) was fetched and read in full this turn. The retained copy is outside Git on the existing PVC. Relevant exact distinctions:

- Sections 1b and 3g: build revision **fd4aeeb2**, **122,458 modules**, **32 vCPUs / 13.8 wall-hours**. Approximately **330 compile CPUh** is extrapolated from a quiet **26-module sample**, with estimated ±30% uncertainty. Approximately **410 CPUh** includes roughly **80 Comparator hours**. It is not 410 hours of compilation alone.
- The report also measures a kernel-skipping ablation on 26 modules and profiles roughly 30,900 cloud-built modules. These are prior build-side phase measurements; our narrower increment is matched target replay/source windows with explicit boundaries.
- Section 3c: kernel-computation explanation is explicitly a hypothesis from three source samples and export-size evidence. We quantify expensive original-kernel replay in selected matching windows; we do not claim a universal semantic classifier or first recognition of that mechanism.
- Section 3b: **416 Comparator configurations**, **80.1 active hours**, longest PlanarPacking approximately **10.9 hours**.
- Section 3f: median nanoda/Lean **0.21** in the paired sweep, **four versus one threads**, excluding export. Pinned nanoda setup, with enlarged checker-stack configuration, **401/416** accepted; operational failures and subsequent revision/stack-dependent recoveries remain in the report. We neither transfer those timings nor claim ProofServe beats nanoda. Its separately implemented kernel is a different trust base.
- Section 4: **30,697** outside-default source files, about **25%** of **122,459** inventory nodes including the root. Different revision and count conventions preclude treating this as the same population as our **19.78% modules / 33.30% sites**.
- Section 8 already proposes standardized times, axioms and hashes in receipts. We claim usable integration and its evaluation, not invention of generic receipts.

Our 279.12 compiler CPUh is most comparable to the report's approximately 330 compile CPUh; both 330 and its broader 410 total fall within our 95.18–463.06 nominal interval. Different hardware, revisions, source populations and boundaries prevent calibrated agreement. Sampling measures the new pin under fixed per-module boundaries and provides explicit statistical uncertainty; it does not improve on the report's complete build coverage.

## System causes and release obligations

Persistence correction: [root0279](../tmp/build-and-evaluate/step-0279-20261103T122418+0000/step-report.md), same executable eight-worker CPU −14.13%, wall −5.13%. Split fallback: [root0285](../tmp/build-and-evaluate/step-0285-20261103T182451+0000/step-report.md), wall medians 257.658745→196.669275 seconds, CPU +0.10565%. These are prototype causal explanations only.

The context-visibility counterexample in the design section is recorded in [root0237](../tmp/build-and-evaluate/step-0237-20261101T060743+0000/step-report.md). It is an earlier prototype defect, not acceptance of a false proposition or a Lean kernel vulnerability.

The paper retains two Pending release tables. M's final matrix/ablations, official ledger comparisons, three bad-proof CI classes and real interruption/resume pair must return under [checker/results](../../checker/results/README.md). O's three external native timings/parity and clean-start package acceptance must return under [external-projects](../../data/external-projects/README.md). No prototype or superseded one-point executable fills these cells.

Current submission gap: release performance and full functional/external acceptance. Static audit success is admitted at its actual scope. No extra measurement, competitor experiment, publication or replacement collector was started.

## Manuscript checks

Six pages including references, existing 10pt two-column format, at most four displays, no missing/evidence-grade macros. The title is unchanged; RQs now match answered scopes and omit cluster scaling under the latest explicit authorization. The old long paper stays in Git history. Only paper/docs/index paths are changed, with one forward commit; visual review is self-review, not independent or venue acceptance.

Final 3 November check: **6 pages / 101,497 bytes**, four displays, 14 resolved references, no overfull boxes or result-grade macros. All six final pages were visually inspected; compilation succeeded in 2.599 seconds on E22–23. This is self-review. Earlier layout versions and logs remain outside Git on the existing PVC; no native result was rerun or modified.
