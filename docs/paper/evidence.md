# Six-page paper: evidence and completion map

This map records admitted measurements, versions and protocol boundaries. The latest decision makes a possible full run conditional on a usability gate; it has not started and supplies no new result. Historical reviews and raw qualifications remain linked below. Root runs no new native measurement.

## Protocol appendix: census transition and evidence handoff

**The full run has not started.** W first validates that its full-corpus numbers will be directly usable. A passing validation permits the run; a failed validation means do not run. The earlier description of W already building the full corpus is superseded.

This is an internal readiness record, not census methods or results added to the paper. The manuscript, numerical values, figure inputs and PDF remain unchanged. Any possible later handoff is conditional on W passing its gate and subsequently returning usable completed data; the [plan](../research-plan.md) owns that decision.

**Every root operation inside the Workspace uses CPUs 8–9, including reads, analysis, Git and PDF compilation.** Remote entry uses `taskset -c 8,9`; child affinity has been checked as 8–9. The former 22–23 setting must not be reused. Historical build checks below retain the CPUs actually used in those past runs.

The conditional target remains the 163,097-source-module OpenAI corpus at revision 4eaee875, in the existing phobos-vt / gpu-smt-dev Workspace. The earlier all-resource permission and 384 GiB expansion do not bypass the usability gate. W chooses the technical validation approach; root does not introduce a numeric threshold or another approval round, start a second collector, or infer that an old unsuccessful pilot is the final decision on the new gate.

The retained preparation records under `/workspaces/.agent-state/gpu-smt-captures/workloads/census-pilot-20261104/` include a completed source-acquisition receipt at 01:15:41 UTC and an earlier unsuccessful six-target pilot with `full_census_started=false`. These establish preparation only, not a passing gate, full-run start or whole-corpus CPU cost. Later status must be read afresh rather than resuming a PID from these observations.

The original42 and independent precision panel stay separate and preserved. Current M timing runs are previews, excluded from Table 1 and final system performance even if complete. Final system timing follows the resolved gate/full-run path on an otherwise idle machine. Existing external installed checks and CI remain versioned functional observations; no same-obligation speedup is inferred.

The nealmcb distinction is unchanged: 13.8 hours on 32 vCPUs is measured cloud wall time, while approximately 330 compilation CPU-hours is extrapolated from 26 modules with estimated ±30% uncertainty. No new full-corpus measurement content is added to the manuscript.

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

The complete **804-line / 74,061-byte** [REPORT at c9570a82](https://github.com/nealmcb/openai-math-lean-tooling/blob/c9570a82f79b78a1a969a6316ac0fdd69aabef55/REPORT.md) was fetched and read in full during the 3 November review. The retained copy is outside Git on the existing PVC. Relevant exact distinctions:

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

## Installed external checking and package qualification (4 November integration)

The paper now replaces the functional Pending table with three measured external cases. The scaling matrix remains Pending. Only O's published tool-form observations are admitted here; M's ongoing matrix is preview-only and excluded from final paper performance.

[measurements.csv](../../data/external-projects/measurements.csv) and [acceptance.json](../../data/external-projects/acceptance.json) were published at **d0c41e24d1800b69427d692de5f6bcafdf94bb48**. [results.md](../../data/external-projects/results.md) incorporates the package/container closeout at **b3e28f4d8a1a726e51d68cc172c4b0e1a8a7a3b5**. Timed bundle **703055a11b749013d7251d93bb7127bd5222a447**, checker **c8e7c615413819bee0931dde09450b8222c6d62a**, Lean **4.34.1 / 5045d005**, four native workers.

| Project source pin | Native closure / common local roots | ProofServe CPU / wall seconds | Completed official CPU / wall seconds |
|---|---:|---:|---:|
| Newspeak e2232d8f | 754 / 105 | 70.555511 / 35.713940 | 63.663383 / 32.914940 |
| Solar f4f5c9a1 | 2368 / 12 | 135.214714 / 76.077903 | 10.965787 / 7.115533 |
| CrocSwap 7c49fe32 | 3166 / 64 | 211.260760 / 114.782636 | 103.858315 / 105.221068, one runtime worker |

Root read the retained result JSON, native stdout, complete receipts, audit JSON and official stdout; all **10 public measurement rows** match their raw clocks and complete/unknown accounting fields. The three native accepted arrays have exactly 754/2368/3166 unique IDs, no rejected modules, and contain every requested local root. Official verbose replay sets equal the respective 105/12/64 local-root sets. This does **not** assert official verification of every imported dependency: default official checks trust imports, while ProofServe checks the compiled closure. No speed ratios are computed.

The frozen evaluator records P0–7 placement, shared lock, four workers, fresh checkpoints, 1740-second outer command limit, no -M, 11.75 GiB charged cap and a one-second 12 GiB process-tree RSS response. Clock starts before Popen and stops immediately after wait4, before sampler join and cgroup deletion; input compilation and queue wait are excluded. Sampled RSS, charged peak and wait4 HWM remain separate. The evaluator's roughly 12 GiB resource policy exceeds the listed O 4 GiB share; this integration records the actual setting and does not retroactively certify that share as respected. These result records do not supply a complete historical child PID/birth ledger, so root does not manufacture one.

CrocSwap's original official batch stopped at **75.043040 wall seconds**, sampled tree RSS **13,782,695,936 bytes**. The separate default-prefix MultitapeToolkit diagnostic stopped at **9.014836 seconds**, **13,882,531,840 bytes**. Neither is proof rejection. Timeout-parent CPU of 0.001787/0.001578 seconds omits killed descendants; total failed CPU stays unknown. The completed stock official fallback uses **one process, one runtime pool worker, all 64 roots**; its successful cost is additional to both failures. Raw per-attempt JSON is used for prefix controls; the current prefix-controls.csv encodes literal newline separators and is not used as a parsed CSV input to this integration. No foreign file was edited.

CrocSwap's [setup repair](../../data/external-projects/croc-setup-patch.json) changes one upstream Lake manifest Name field. The source/dependency revisions remain the declared input; this is a disclosed repair, not unmodified-input acceptance. Root read the retained pinned subproject README, which explicitly discloses substantial OpenAI Codex assistance. That supports **AI-assisted**, rather than wholly AI-generated, provenance.

Installed audit finds default scope 105/105, 12/32 and 64/64 source files. Solar's 20 omitted files are explicit inputs of a custom EVM flow; this experiment did not execute it. Newspeak's receipt includes a project native_decide axiom; all three list closure-declared axioms including sorryAx/Lean.trustCompiler. These are **declared inventories**, not minimal per-theorem dependency sets or proof that a particular target uses every listed axiom. Current-source binding remains unavailable.

[Portable CI qualification](../../packaging/qualification-ci.json): latest run **41740681358**, source **adf816ae0661ded8a2fc4d528ca78618e04e8209**, actual relocated install, project check/audit, official default/fresh controls, and three malformed-proof rejections. Root read retained ZIP log output and the qualifier source. Retained local raw controls separately show original-kernel rejection for loose bound variables, an unknown constant, and a wrong sort; CLI usage errors are excluded.

[Container qualification](../../packaging/qualification-container.json): run **41740685837**, same adf816ae source, successful image build with an actual **network-disabled** self-test. Retained log confirms full-Mathlib service controls, a two-module installed project check/audit, and explicit unsupported-version rejection. These are CI correctness observations, not timed paper performance or the three-project external benchmark.

Remaining decision: W's full-run usability gate. The full run is not started; only a pass permits it, and a failed gate means do not run. Final quiet-machine scaling/ablation/official measurements and interruption overhead remain separate dependencies. Completion of the current M preview does not fill this dependency. Do not pool its ba316991 executable with the external c8e7c615 timing rows. The original42 estimate stays unchanged; the separate precision panel has six of twelve costs and is not pooled. No new native run, publication or replacement collector was started.

## Manuscript checks

Six pages including references, existing 10pt two-column format, at most four displays, no missing/evidence-grade macros. The title is unchanged; RQs now match answered scopes and omit cluster scaling under the latest explicit authorization. The old long paper stays in Git history. Only paper/docs/index paths are changed, with one forward commit; visual review is self-review, not independent or venue acceptance.

Previous 3 November revision check: **6 pages / 101,497 bytes**, four displays, 14 resolved references, no overfull boxes or result-grade macros. All six final pages were visually inspected; compilation succeeded in 2.599 seconds on E22–23. This is self-review. Earlier layout versions and logs remain outside Git on the existing PVC; no native result was rerun or modified.

4 November integration check: **6 pages / 103,788 bytes**, four displays and 14 resolved references; no overfull boxes or evidence-grade macros. All six final pages visually reviewed; compile rc0 in 2.554 seconds on E22–23. This is self-review. The new external table comes only from committed installed-tool measurements; original42 and historical Figure 1 are unchanged. Root ran no new native measurement, changed no owner implementation, and started no replacement collector.
