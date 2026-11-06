# Six-page paper: evidence and completion map

This map records admitted measurements, versions and protocol boundaries. The total-instruction gate failed. The latest instruction authorizes W to proceed with the frozen 22-core census; no corpus total is available yet. Historical reviews and raw qualifications remain linked below. Root runs no new native measurement.

## Protocol appendix: census transition and evidence handoff

**The gate completed and failed. The latest instruction supersedes stop-and-wait: proceed with option A, W's frozen 22-core census.** W's [published result](../../data/openai-math-4eaee875/measurement/census-gate/README.md) is committed as f97e6fbdc4d8ef167d43a32944cbabb7cad1db19; the measurement source is 2c901ec4f0bbf73b75b534bbc255fcc973aebe6f. The terminal record is dated 2026-11-04 05:15:28 UTC.

This internal protocol record supports the manuscript's disclosure of the current measurement decision. The existing sample numbers and figure inputs remain unchanged. The manuscript now discloses the protocol decision; full-corpus numbers await actual completed records. The [plan](../research-plan.md) records the authorized execution.

**Every root operation inside the Workspace uses CPUs 8–9, including reads, analysis, Git and PDF compilation.** Remote entry uses `taskset -c 8,9`; child affinity has been checked as 8–9. The former 22–23 setting must not be reused. Historical build checks below retain the CPUs actually used in those past runs.

The target remains the 163,097-source-module OpenAI corpus at revision 4eaee875 in the existing phobos-vt / gpu-smt-dev Workspace. The latest decision authorizes the unchanged eight-P-core plus fourteen-E-core protocol despite the failed gate. Cross-module comparisons use user-mode instructions; this criterion was selected after seeing the gate results and is not a pre-registered passing gate. P/E CPU seconds remain separate without conversion. Wall time is an observation of this machine and configuration. Root adds no threshold or approval round and starts no duplicate collector.

The retained preparation records under `/workspaces/.agent-state/gpu-smt-captures/workloads/census-pilot-20261104/` include a completed source-acquisition receipt at 01:15:41 UTC and an earlier unsuccessful six-target pilot with `full_census_started=false`. These establish preparation only, not a passing gate, full-run start or whole-corpus CPU cost. Later status must be read afresh rather than resuming a PID from these observations.

The complete gate contains 240 foreground, 240 enabled/disabled-counter controls and 1,413 background compiler attempts. All returned successfully. For each of 20 modules, take the median total retired instructions in each of four conditions, then compute max/min minus one. Across modules the median is **1.331198%** and the linearly interpolated P95 is **3.149811%**, exceeding the frozen **1%/3%** criteria. The alternative pooled deviations relative to P-quiet are a different statistic and do not replace this failed comparison.

Root independently parsed the retained raw records and recomputed the instruction spreads and counter overhead. CPU-overhead medians are **0.527371% P / 0.280388% E**; wall-overhead medians are **0.127603% P / 0.249686% E**. These pass the aggregate overhead criterion, without establishing a uniform per-module bound. Recorded active PMU coverage is complete. Root checked recorded product-digest parity; W additionally publishes direct byte-comparison results. Root checked all 1,893 recorded native PID/birth identities retired and their cgroups absent, with no recorded OOM events. This is a bounded protocol failure, not a proof rejection or a claim that all ways of measuring a census are impossible. Raw records remain at /workspaces/.agent-state/gpu-smt-captures/workloads/census-gate-20261104/run-1/.

The original42 and independent precision panel stay separate and preserved. Current M timing runs are previews, excluded from Table 1 and final system performance even if complete. Final system timing follows the resolved gate/full-run path on an otherwise idle machine. Existing external installed checks and CI remain versioned functional observations; no same-obligation speedup is inferred.

The nealmcb distinction is unchanged: 13.8 hours on 32 vCPUs is measured cloud wall time, while approximately 330 compilation CPU-hours is extrapolated from 26 modules with estimated ±30% uncertainty. Only the protocol disclosure is added to the manuscript; no full-corpus numerical result is added.

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

Historical 4 November integration placed three external observations in the paper. Under the latest preparation instruction those preview costs are removed from the current manuscript and retained here only as historical evidence. The scaling matrix remains Pending. Only O's published tool-form observations are admitted here; M's ongoing matrix is preview-only and excluded from final paper performance.

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

Current decision: W proceeds with the frozen 22-core option A under the latest instruction, retaining the failed total-instruction gate. No further user decision is awaited. Final quiet-machine scaling/ablation/official measurements and interruption overhead remain separate dependencies. M's preview does not fill them. Do not pool its ba316991 executable with the external c8e7c615 timing rows. The original42 estimate stays unchanged; W's superseded precision panel retains seven of twelve costs separately.

## AI-generated external case: functional preview (4 November)

Root read the raw installed-tool receipt, result and official verbose output for samuelburbulla/proofs at source commit **3042904c5f7e96732c1ff4ac01745a8be9ae91ff**. The retained upstream repository metadata describes it as “AI generated proofs of open math problems”; model, per-proof authorship and human editing are undisclosed. This collection-level attribution is stronger than the older CrocSwap AI-assistance disclosure, without proving autonomous authorship.

The receipt is complete, with **10,753 unique accepted modules**, an empty rejected array and **22 successful segments**. Its nine local roots exactly equal the nine official-default verbose replay names and are all in the accepted closure. Installed audit reports **9/9** source files in the static defaults. Official default still trusts imported proofs, so this establishes common-root parity rather than equal full-closure obligations. The source pin in the receipt is recorded provenance, not binding of the current source bytes.

This is a **functional preview, not a frozen release or final timing**. The archive records source 6618e734 with a dirty O worktree and checker 3a56405f; the receipt records one worker. Two caller invocations timed out before continuation completed in a third invocation. Full-request CPU accounting is incomplete; successful-segment cumulative CPU and the last invocation clock are not fresh end-to-end costs. No new speed ratio or paper number is admitted. Historical CrocSwap results remain; the prepared external set now uses Newspeak, Solar and this AI-labelled collection.

Raw evidence: /workspaces/.agent-state/proofserve-o-line/freeze-preparation-20261104/freeze-preview-v3/external-2/, including checkpoint/receipt.json, official-default.stdout, result.json and separate attempt results. O's new small preview summaries were still uncommitted at the root read, so this record cites the retained raw evidence and does not claim a clean frozen artifact. The paper source, PDF and figure data remain unchanged. This review is self-review; no root native collection or foreign-file change was made.

## Retained-closure checker qualification (4 November)

**The old acceptance qualification remains superseded.** The 14,721-module run below used defective certificate logic in checker **2df1d9d7**, despite unchanged inputs. A separate fresh repaired-binary run has now returned, as recorded below; it does not validate the old certificate implementation. The O-run, coordinator-written Workspace summary at packaging/checker-review-2df1d9d7.md reports false acceptance after adding a bad-proof module part following certification, and after copying an authentic certificate from another project; both no-certificate and official paths reject those inputs. That review remains open, is not a pass, and the checker must not be frozen before the coordinator verifies the fix. M owns the repair. Root reads returned evidence and does not execute checker reruns or promote a release freeze.

M's committed development result **b0b87445** records the retained SubexponentialSAT run using source **2df1d9d70259d2630edda2aa1a4a8663753e5f9d**; its following counts are historical tool outputs, not currently admitted acceptance evidence, full-corpus results or final performance. Root read the actual final receipt and continuation result: **14,721 unique accepted modules**, no rejected entries, **9 batches**, **14,720 first-check entries** and **86,150 reconstructed import entries**. The defective reuse path intended to trust local successful receipts and matching compiled-artifact hashes; the review shows that its input binding is insufficient. M identifies one accepted module with no own declarations and no replay entry. M reports equality with the retained O stream and no acceptance difference against **14,401 available module-local references**; **320 remain unreferenced**, so full official parity is incomplete. Root did not repeat M's reference reduction.

The completed continuation used two kernel workers on E17–23 under the separately recorded 40 GiB policy, resuming prior successful certificates. Root confirmed controller 444252/birth6815158 and native 444253/birth6815162 absent, the recorded cgroup absent, native rc0 and no guard stop. M reports sampled tree RSS **26.062 GiB**, distinct from single-process wait4 HWM and charged memory. Earlier 16 GiB stops remain separate; this is not a fresh timing or memory-saving comparison. Raw: /workspaces/.agent-state/gpu-smt-captures/checker-full-feasibility-20261104/, especially relaxed40/runs/subexp-cache-6/stdout and result.json. [Qualification](../../checker/results/full-feasibility-qualification.json) also records a tiny clean-source workflow control; its fixture routes are not workload benchmarks.

The separate repaired-source run is committed as **5155ad9f**, using **e0c92d51ab0faf24f1c7ac64323d5ea2f2e4575d**. Root read its actual stdout, on-disk receipt, native result and controller terminal: **14,721 unique accepted modules**, no rejected entries, and **nine new batches with no reused batch certificates**. Stdout and the saved receipt are identical. Native exit is 0; the recorded controller 483671/birth7557600 and native 483672 have retired and the recorded cgroup is absent, with no guard stop. The run used a new checkpoint directory, two workers on E17–23 and the separately authorized 40 GiB policy. M reports the same 36,209 recorded input identities, old receipt axiom list and retained-stream accepted set; the available module-local references still leave 320 modules unreferenced. Raw: /workspaces/.agent-state/gpu-smt-captures/checker-subexp-fixed-e0c92d51-20261104/. See the [fixed-run summary](../../checker/results/certificate-reuse-fix/subexp-fresh-e0c92d51/summary.json).

This fresh retained-case result is development evidence, not an independent review of the repaired implementation. M replayed the regression fixtures and the coordinator read the repair direction; neither supplies independent repaired-source test evidence. The checker remains unfrozen, and no repaired-source acceptance or E-core timing is added to the paper. The old flawed run is not relabelled as valid.

A subsequent independent **code-only** review of e0c92d51 is now recorded in the Workspace at packaging/checker-review-e0c92d51.md. A fresh reviewer read the implementation without M's or the coordinator's conclusions, but built and ran nothing. Its status is **open**, not passed. Findings include omitted axiom names for segregated modules, checkpoint-directory search precedence that can differ from the hashed input resolution, and child completion events overriding a nonzero child exit; other findings concern importer parity and receipt coverage. The coordinator spot-checked the cited code for the first, second and stdout/exit findings. That code-only report supplied no native reproductions. M subsequently ran baseline fixtures against the immutable e0 executable. Root read baseline-final-probes.json under /workspaces/.agent-state/gpu-smt-captures/checker-review-e0-fix-20261104/: 2-state-shadow reports exit 0 and complete, whereas 2-state-shadow-official returns exit 1 with a loose-bound-variable kernel rejection; 1-segregated-axioms reports complete with an empty axiom list. M's fixture report identifies the omitted declared axiom. These are implementation-lane reproductions, not independent execution review. M also distinguishes a saved-complete/nonzero-exit coordinator control from the proposed project-IR route, which was rejected rather than reproduced; the proposed Quot counterexample was not confirmed. Repair and regression work is still in progress, so no repaired-release pass or freeze is inferred. The earlier 15-name axiom-list equality is equality between tool outputs, not an independently established complete axiom inventory.

Whole-corpus import capacity, the full official reference ledger and quiet-machine final evaluation remain incomplete. The W total-instruction gate remains failed; the latest instruction authorizes option A without another user decision. No result from this development qualification changes the paper, launches the full corpus or fills its final performance table.

## Manuscript checks

Six pages including references, existing 10pt two-column format, at most four displays, no missing/evidence-grade macros. The title is unchanged; RQs now match answered scopes and omit cluster scaling under the latest explicit authorization. The old long paper stays in Git history. Only paper/docs/index paths are changed, with one forward commit; visual review is self-review, not independent or venue acceptance.

Previous 3 November revision check: **6 pages / 101,497 bytes**, four displays, 14 resolved references, no overfull boxes or result-grade macros. All six final pages were visually inspected; compilation succeeded in 2.599 seconds on E22–23. This is self-review. Earlier layout versions and logs remain outside Git on the existing PVC; no native result was rerun or modified.

4 November integration check: **6 pages / 103,788 bytes**, four displays and 14 resolved references; no overfull boxes or evidence-grade macros. All six final pages visually reviewed; compile rc0 in 2.554 seconds on E22–23. This is self-review. The new external table comes only from committed installed-tool measurements; original42 and historical Figure 1 are unchanged. Root ran no new native measurement, changed no owner implementation, and started no replacement collector.

Latest option-A disclosure check (4 November): six pages / 104,284 bytes, two figures and two tables, 14 resolved references, no overfull boxes. Compilation returned 0 in 2.288 seconds on CPUs 8–9; all six pages were visually self-reviewed. The only manuscript edit is the census-protocol disclosure and timing-scope clarification. Original42 numerical results, figure inputs, title and RQs are unchanged. Build/log/render outputs remain under /workspaces/.agent-state/gpu-smt-paper-recovery-20261030/six-page-census-A-20261104/. This is self-review, not independent acceptance or a full-census result.


## Prepared result integration (4 November)

The committed generate_census.py and generate_system.py read the published W/M/O
schemas and output final TeX/CSV/provenance artifacts. Real five-module records
validate census structure and absent-cost handling; real unreplicated gate rows
validate separate P/E numerical aggregation. M loaded previews and O freeze
previews validate grouping, interrupted accounting and TeX output. None of these
preview values is included by main.tex: preview filenames differ and no ready
marker is produced. README.md gives the one-command handoffs.

Section 3.2 now reserves observed census totals and distributions, retaining
original42 only for calibration. Figure 2 replaces the generic workflow diagram;
the paper still has two figures and two tables. Both system tables are pending
final frozen data, and the old external timing numbers are no longer in the
current paper. This layout compiled with rc0 on CPUs 8–9, six pages / 98,443 bytes,
14 citations and no overfull boxes; all pages were visually self-reviewed.


## Review facts now in the six-page system section

The manuscript distinguishes O's original execution review of 2df1d9d7,
the independent code-only review of e0c92d51, and M's later baseline
reproductions/3fe83c5a repair. It names authentic-certificate reuse, optional
module parts, artifact shadowing, sibling/import-context errors and omitted
axiom declarations, with their input-resolution, publication and event/exit
repairs. Saved-result controls are not described as demonstrated project-IR
injection; IR/Quot proposals that were not reproduced remain unconfirmed.
Explicit native-IR refusal, default/fresh differences on supplied incomplete
parts, editable checkpoint trust and incomplete independent reference coverage
remain visible. No repaired-checker large-case acceptance or preview clock is
used as final evaluation evidence.

Final PDF verification: six pages / 100,848 bytes, two figures and two tables,
14 resolved citations, zero missing/evidence-grade macros, no overfull boxes.
Tectonic returned 0 in 2.413 seconds on CPUs 8–9. All six latest pages were
visually self-reviewed; pages 2–5 were byte-identical renderings after the final
wording adjustment, and pages 1/6 were inspected again. This is self-review.
Build/render/logs remain under six-page-review-facts-20261104/build-final on
the existing paper-recovery PVC directory. No extra native measurement ran.

The original W controller was observed live at PID 528400/birth10465017,
using its frozen census-22core-9389daff-20261104 source and run directory.
This establishes actual launch, not completion or a numerical corpus result.


## Two-day closure and cutoff reporting (4 November)

The user's exact instruction, “确保 2 天内收尾这个项目.”, is recorded in
[user-instruction.md](../user-instruction.md). The project deadline is
6 November 2026, 20:00 UTC; the complete schedule is in
[research-plan.md](../research-plan.md). Root finishes prose/scripts by
5 November, 12:00 and numerical integration by 6 November, 16:00.
The compilation cutoff is 6 November, 04:00; final matrix and external
timing then have six-hour and two-hour budgets in sequence, followed by
library checking with a hard stop at 14:00. No separate PlanarPacking
comparison is retained in the manuscript or planned evaluation.

Section 3.2 and Figure 2 admit either a complete ledger or an explicitly
partial cutoff ledger. generate_census.py --partial reports completed native
coverage, configuration units and units without completed native costs;
summed CPU and curves refer only to successful observed modules, split by P/E.
It never imputes missing costs, extrapolates a cutoff subset, or reclassifies
the failed gate. Partial-mode reduction and plot compilation were verified
with the retained numerical validation input and explicitly synthetic coverage
metadata outside Git; those counts are not corpus results. Preview mode still
cannot create publication markers.

The system evaluation reserves library-check-summary.tex for the actual
returned count and scope. The text distinguishes unique accepted modules,
attempted roots, proof rejection, operational interruption, remaining scope
and available official-reference coverage. A stopped run is reported as the
scope reached, without whole-library completion or parity. No current count
has been invented or copied from the retained-case preview.

The cutoff-ready manuscript compiled successfully on CPUs 8–9 in 2.339 seconds: six pages including references, 101,657 bytes, two figures, two tables and 14 citation keys. All six rendered pages were visually self-reviewed; no overfull boxes, undefined references or missing/measured/partialev/unproven macros remain. The initial seven-page build is retained outside Git; prose was shortened, without reducing the 10pt type size or changing existing measurement numbers. This is layout/self-review, not independent acceptance or a completed final evaluation.


## Later review: context and quotient failures reproduced (5 November)

Committed review [checker-review-2628d727.md](../../packaging/checker-review-2628d727.md)
is independent code-only inspection, not execution. M's implementation-line
controls and repairs are committed in 981d544d; the validation-region ownership
follow-up is e1557c77. See [review-2628-repair](../../checker/results/review-2628-repair/README.md).
Root read both the committed report and raw fixture records, including
quot-before2-fixtures/results.json, old-context-focused6-fixtures/results.json
and final-review6-fixtures/results.json under
/workspaces/.agent-state/gpu-smt-captures/checker-review-2628-fix-20261104.

The old checkpoint-restored axiom-tagged Quot fixture returned complete/0 with
ASeed and ZFake accepted, while both official modes returned 1. Plain old native
also rejected it; the restored context is material. This later actual fixture
supersedes any current blanket description of Quot as unconfirmed. Earlier
genuine-Quot controls remain historical non-reproductions of their own inputs.
Swapped WellFounded/Acc bodies similarly yielded old native 0 versus both
official modes 1; repaired native returned 1. The honest body-sensitive case
was an old false rejection. Unsafe duplicate names, missing/corrupt IR and
accepted/rejected overlap are separately retained outcomes. The project-IR
stdout-forgery proposal remains unconfirmed and is not merged with these
demonstrated failures.

The repaired quotient paths refuse malformed declarations operationally (2),
where official rejects (1). Direct open primitive mentions are now supported,
while closed/higher-order evaluation remains conservatively unsupported.
ABI 5 / independent-closures v7 invalidates old state; the old 14,721-module
ABI-4 acceptance output does not qualify the repaired source. No new large
replay, full-library result or final timing was run for these controls.

Root also read the final-contract8 raw result/stdout and the committed
ir-lifetime-followup.json: native rc0, complete wait4 usage, no stop/OOM,
90 legacy plus 109 new command records and a successful core contract.
These are command counts, not independent bugs or proofs. The report compares
198 common command outcomes, and the separate ownership controls distinguish
discarded validation data from another owner's live regions. That comparison
and mapping interpretation are M's analysis; root did not rerun native tests.
Initial 981d544d automatic CI passed; e1557c77 follow-up CI was pending in the
committed record. All are self-review/mechanical evidence, not repaired-source
independent execution review, release freeze or paper performance.

Root directly checked final-contract8 PID 997606/birth11906385 and its recorded cgroup are absent. Updated paper: six pages / 101,584 bytes, 2.398-second rc0 compilation on CPUs 8–9, no overfull or undefined-reference warning, two figures/two tables/14 citation keys/zero evidence macros. Changed pages 3–4 were visually reviewed; pages 1–2 and 5–6 are byte-identical renderings to the previously reviewed cutoff manuscript. The first seven-page layout attempt is retained on PVC. This root integration adds no native experiment or final system number.


### Follow-up CI terminal observed (5 November, 01:05:14 UTC)

GitHub's live API now reports the e1557c77 [engine run](https://github.com/yunwei37/proofserve/actions/runs/41938525300)
and [benchmark-smoke run](https://github.com/yunwei37/proofserve/actions/runs/41938525076)
completed successfully. The engine jobs endpoint confirms checker-contract
success; this observation resolves the automatic-CI pending status at the
repair commit. Root retained the reduced API snapshot beside its ABI-5 paper
build on PVC. This is mechanical execution status, not a new independent
execution review, large-closure replay, freeze or final performance result.
The manuscript's scientific scope and numbers are unchanged by this observation.


## Census completion instruction supersedes cutoff publication (5 November)

The latest exact user words are recorded in [user-instruction.md](../user-instruction.md).
The first half quotes the coordinator's discarded cutoff proposal; the user's
decision is “不要这样. 让它跑完”. The census now has no time cutoff and will
not close with a deadline-selected subset. Earlier cutoff-mode validation and
deadline entries above are historical, superseded dispositions; their original
data and receipts remain preserved.

The manuscript and generate_census.py now wait for the full campaign's natural
terminal. The partial-publication option is removed. W's actual controller
schema distinguishes all-native-success (complete) from an exhausted campaign
with genuine failures: full_census/cost_measurement, successful, failed,
blocked, configuration_units, total_source_units and stop are retained.
Publication accounts for disjoint outcome identities across the entire frame;
stop or not_attempted outcomes cannot qualify an early subset as complete.
All failed/blocked modules are exported individually in census-outcomes.csv,
alongside configuration/success identities and supplied dependency reasons.
Successful costs remain separate from absent costs of failures/blockers.

Root read the frozen controller: its six-hour deadline applies only when
validate_subset is set, not the actual full-census invocation. Root changed
neither W's running collector nor its implementation. Other stated delivery
deadlines are unchanged and do not authorize truncating the census. Matrix,
external timing, optional full-library checking and numerical integration
follow full-campaign completion. Library checking alone retains partial or
not-attempted reporting and is not required for the paper.

Completion-mode generator validation used retained numerical rows with explicitly synthetic exhaustive terminal categories outside Git. Successful CPU sums remained equal by P/E; every failed/blocked identity was exported. Early-stop and not-attempted input and the removed option were refused; preview still produced no ready marker. The figure compiled. None of these validation numbers entered the manuscript. Updated manuscript compilation returned 0 in 3.225 seconds on CPUs 8–9: six pages, 101,503 bytes, two figures/two tables/14 references/zero evidence macros, no overfull/undefined warnings, all six pages visually self-reviewed. Root directly reconfirmed W controller528400/birth10465017 in full --execute mode without validate_subset or functional flags; no collector was stopped or replaced.


## e155 real-closure regression and superseding preparation (5 November)

M's committed [06d8e81d pre-freeze record](../../checker/results/pre-freeze-e1557c77/README.md)
records an e1557c77 / ABI-5 native freeze under a correctness-first exception:
the performance-growth criterion failed, and paper_eligible/performance_qualified
are false. This is not an independent execution review or final timing.

Root read the raw e155 and same-root 3fe receipt pairs under
/workspaces/.agent-state/gpu-smt-captures/checker-freeze-e1557c77-20261105.
Nat.Basic has 1,330 unique accepts and Grid 3,793, each with no rejection and
15 declared axiom names, equal to the corresponding 3fe accepted/axiom sets.
This establishes that retained comparison, not official full-ledger parity.
The seven-name earlier ba316991 lists omitted eight names already present in
the unchanged inputs, according to M's input/axiom reduction; these are not
newly introduced target assumptions.

Root independently counted module_verifications classified module_local:
Nat.Basic 49 on 3fe versus 1,016 on e155; Grid 157 versus 3,465.
The Grid e155 receipt includes 2,673 checkpoint_reuse/module_local and 792
kernel_replay/module_local records. These counts classify unique committed
module records, not fresh kernel calls in the resumed invocation.
The old 3fe binary has known correctness defects and is a diagnostic reference,
not a release competitor. These background E8–9 controls and different P/E
historical rows do not establish final speedup or an isolated causal effect.

Root read all five guarded terminal records and directly verified their
recorded PIDs and cgroups absent: Nat e155 and both 3fe controls returned 0;
the first Grid e155 window returned 124, then its same-state continuation
returned 0. No memory/reserve stop or OOM is reported. The two Grid clocks
are separate operational attempts, not one fresh uninterrupted measurement.
M discloses that the initial uncommitted partial Grid event file was not
archived before resume; complete checkpoint/receipt outputs survive.
Root does not claim every partial event was preserved.

At root observation, M's dirty worktree explicitly supersedes this freeze
with preparation of a shared-checked default and strict mode; that replacement
was not yet committed or qualified by root. The authoritative final handoff
must identify the actual policy/source, its review and returned controls.
No final freeze, release acceptance or new performance number is inferred
from the historical e155 freeze declaration. Root changed no foreign source,
started no native run and left the manuscript's performance slots untouched.


## Frozen shared-checked policy: e000ed62 (5 November)

The coordinator confirms e000ed62 as the native freeze, replacing e1557c77.
Root read [theorem-body-policy](../../checker/results/theorem-body-policy/README.md),
its freeze/qualification/oracle records and the committed 26-row official
comparison table. Git's introducing commit resolves to e000ed62; all seven
native/build Git blobs match its freeze record. No independent runtime review
is inferred from this source binding or the implementation-line controls.

Default shared-checked retains a kernel-checked same-interface theorem body.
A crafted artifact whose proof succeeds only by depending on another module's
body can be accepted while official replay rejects it in its own import
context. The proposition remains derived from kernel-checked proofs relative
to the checked shared closure and its reported axioms, under the documented
kernel/reader/coordinator/checkpoint trust assumptions. This is checked-closure
derivability, not original serialized-proof/context equivalence.
--strict-theorem-bodies selects isolation for matching theorem-body-context
behavior; other documented IR/artifact/operational differences remain.

Root directly read contract3-2628/results.json in
/workspaces/.agent-state/gpu-smt-captures/checker-body-policy-20261105:
the supplied swapped-body native row is complete/0 under shared-checked,
strict rejects/1 and both official modes return 1. This is the declared policy
difference, not a claim that the fixture's serialized proof now passes official.
The 26-row table has exactly that supplied new default-accept/official-reject
case; it is a finite fixture scope, not universal parity. Two read-only reviews
have regression repairs; the repair has no independent runtime review.
Original old-certificate execution findings remain historical facts.

The frozen tool explicitly checks duplicate bodies that upstream replay may
skip, without putting temporary checking names into the frontier or adding an
axiom. Receipts and state identities bind the selected policy; ABI 6 /
independent-closures v8 invalidates older state. Root read the two real new
receipts: shared-checked, ABI 6, 1,330/3,793 unique accepts and no rejection.
Their timing values remain background-load previews, not final paper numbers.

The rejected e155 isolation policy raised Grid module-local classifications
from 157 to 3,465. The coordinator's approximate 2.27 CPU factor corresponds
to its complete-segment accounting (3370.427492 / 1485.572441); whole-attempt
accounting includes interruption and repeated work. Neither is a measured
cost of the new strict executable, which also adds explicit duplicate-body
checks. Strict CPU/wall cost in the paper must come from returned final matrix
rows of the same tool/input/worker configuration.

generate_system.py now keeps theorem-body policies separate in native and
external summaries, labels default/strict table rows D/S, and exports matched
strict/default CPU and wall ratios of medians when actual paired groups exist.
Missing strict points produce no invented costs. Existing preview rows plus
explicitly synthetic policy labels tested separation, no cross-commit pairing,
preview isolation and TeX compilation; they are adapter tests, not strict
measurements, and their numbers do not enter the manuscript.

W's 5 November 17:00–18:00 UTC finish is the coordinator's estimate, not an
observed terminal, a cutoff, or an added time limit. Root's prose/scripts are
ready before its 12:00 milestone; actual census and final performance figures
remain pending.

The completed policy update compiles to six pages / 101,629 bytes in 2.595 seconds on CPUs 8–9, with two figures/two tables/14 citation keys, zero missing/measured/partialev/unproven macros and no overfull/undefined-reference warning. Pages 1–2 are unchanged renderings; pages 3–6 were visually self-reviewed, including the final removal of an orphaned artifact line. The default/strict table adapters compiled without overfull boxes; explicit receipt metadata takes precedence over command-key aliases, and repeated generation clears stale strict-cost files when no such points are supplied. All adapter validation numbers remain outside the manuscript. No new native experiment, independent runtime review or final performance result is claimed.


## Final driver schema and finite matrix preparation (5 November)

M's 5367aea9 prepares the post-census phases; 456f340f repairs selection of the
actual interrupted retry directory. Neither changes the e000ed62 native inputs.
The current six-hour plan retains Nat.Basic/Grid workers 1/2/4/8, three repeats,
8-worker ablations and strict points, but only Barrier workers 1/8. Its two
middle worker counts are deliberately unmeasured. The 71 planned attempts
and budget projections in [post-census-preparation](../../checker/results/post-census-preparation/README.md)
are not final performance. In particular, planning-only P/E conversions and
kernel-fraction assumptions do not enter the paper's measured costs.

Root read the actual new fixture exports in
checker/results/post-census-qualification/matrix/. Dataset labels select
Base/Fixture/All workflow routes, not real Nat.Basic/Grid/Barrier workloads.
The acceptance sidecar explicitly sets paper_eligible=false; the row CSV has
no corresponding column. The generator now checks that actual sidecar
designation, so fixture results cannot qualify merely by having the expected
filename or number of repeats. Its archived fixed-failed-attempts.csv is
preserved separately from the current successful-point table and never enters
successful medians. Native and driver commits remain separate provenance.

No matrix or corpus phase is launched by root; W remains running and retains
the P-core lease. The prepared driver only runs those phases after the actual
full-census terminal and retirement; corpus checking remains optional after
external timing. The retry fix is a harness regression, not another native
checking result, independent review or final timing.

Root preview-adapted the actual new fixture schema: 18 matrix groups, two strict-policy groups, the archived 126 failure retained outside one-observation medians, and explicit refusal of paper_eligible=false in final mode. These are fixture adapter counts, not performance results. The aligned manuscript remains six pages / 101,625 bytes, with two figures/two tables/14 references/zero evidence macros; CPU8–9 compile rc0 in 2.121 seconds, no overfull/undefined warnings. Page 4 was visually reviewed; the other five page renderings are byte-identical to the previously reviewed policy manuscript. No new native run was started and no fixture/model number enters the paper.


## e000 preview package and container completion (5 November)

Root read the real completed controller/freeze manifests under
/workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105.
Both identify preview=true and final_system_timing_eligible=false; native
source is e000ed62 / ABI 6, but CLI/packaging runtime paths were dirty.
This is a completed functional preview, not a clean release freeze, final
quiet-machine timing or an independent adversarial runtime review.

The relocated archive qualification reports all three malformed-proof classes
rejected, closure batching/resumption, root-file forwarding, strict flag
forwarding and receipt policy fields. Root read the actual --network none
container command and its successful self-test log: installed-project check,
audit, unsupported-version refusal, shared-checked/strict policy forwarding
and the three kernel mutation controls passed. The invocation has no Workspace
bind mount. Controller/freeze/temporary-Docker exits are all 0, and their
recorded identities 1586361/birth13860331, 1586463/birth13861254 and
1586400/birth13861018 were directly observed absent. This does not claim a
birth audit of every descendant or hard RSS enforcement.

For Newspeak, Solar and samuelburbulla-proofs, root parsed the actual final
native stdout receipts and official verbose output. There are respectively
754 / 2,368 / 10,753 unique accepts, no rejected modules, shared-checked policy
and ABI 6. The requested local-root sets are exactly the official replayed sets:
105 / 12 / 9 names, all included in the native accepted closure.
Audit calls returned 0. These are common local-root observations; official
default trusts imports, so they do not establish full-closure official parity
or equal-obligation speedups.

Newspeak and Solar each used one invocation. The AI collection used two
1740-second caller windows returning 124, then a third continuation returning
0. Its complete_native_cost_available flag is false. The final continuation
cost cannot stand for a fresh whole request; full CPU remains unknown.
Its upstream AI attribution is collection-level, with model/human contribution
undisclosed. Axiom lists remain declaration inventories rather than minimal
theorem dependencies; receipt-to-current-source binding remains unestablished.

The small e000 preview exports were still O-owned uncommitted files when read;
root did not stage them. No preview cost or acceptance table was inserted into
the manuscript. The existing system generator preview-adapted the actual new
external CSV with the nonfinal M fixture input: all nine external groups
remain scoped previews, AI whole CPU stays blank and no system-ready marker
is produced. Raw data, both timeouts and earlier archived cases remain retained.
Clean packaging-source provenance, final portable acceptance and the post-census
timing run remain pending.


### O result publication and manuscript update

O committed the preview source changes and small results as 420dc9d6.
The earlier statement that they were uncommitted describes root's initial
observation; the test-time dirty-input provenance remains true and is not
rewritten as a clean immutable release. The package report explicitly says
no new adversarial case was constructed. Its existing valid-fixture strict
checks are functional forwarding controls, not a new independent soundness
review.

The manuscript now describes this e000-native portable archive/container
functional qualification instead of only the earlier adf816ae CI.
It includes no preview timing or new performance-table value; fresh-state
quiet-machine evaluation remains pending. The AI preview's whole CPU stays
unknown despite the successful final continuation.

The updated manuscript was compiled on root CPUs 8–9 with Tectonic:
exit 0, 2.313 seconds, six pages / 101,636 bytes, two figures / two tables /
14 references, with no overfull boxes, undefined citations/references or
missing/measured/partialev/unproven macros. Root visually inspected the
changed page 5. The other five rendered pages are byte-identical to the
previous visually checked version. This is root layout self-review, not an
independent paper review or completion of the pending final measurements.
The initial expanded wording produced seven pages and was shortened before
publication without changing the qualification boundaries or measured values.


## Two-phase census admission decision (5 November)

The coordinator authorizes phase 2 after reporting repeated concurrent-memory
interruptions in PadicHodge and related families from 16:00 UTC, following
the earlier Ramsey behavior. The notice reports 128,329 of 163,096 executable
modules completed and 65 unsuccessful attempts at 20:25 UTC. These are
coordinator-supplied progress observations, not root's recomputed final ledger,
and are not inserted into the manuscript as census results.

Phase 1 retains its fixed 22-slot admission with memory-reserve drains and
exclusive retry. Phase 2 uses memory admission and family concurrency caps;
compiler argv, -j8 and P/E pools remain fixed. At root's initial read the old
controller was still active and its execution-phases.jsonl contained only the
original lease event. The actual switch time and new implementation are not
invented from this notice. Final reporting must bind each successful module
to its phase, retain unsuccessful attempts separately, and report measured
phase wall and phase/P-E CPU. Total campaign wall sums the measured phase
intervals, with any gap separate; module wall sums are not makespan.

The failed total-instruction gate and post-result user-mode-instruction choice
remain disclosed; the admission change is not a new invariance result.
The laptop sleep interval is a coordinator-reported monitoring outage, not
evidence of a remote census interruption. No native run, controller mutation,
owner affinity change or replacement queue was started by root.

The two-phase prose compiles on CPUs 8–9: exit 0 in 2.061 seconds,
six pages / 101,369 bytes, two figures / two tables / 14 references, no
overfull or undefined warnings and no missing/measured/partialev/unproven
macros. Root visually reviewed all six rendered pages. No census progress,
new CPU/wall result or admission-policy benefit was inserted. The actual
switch timestamp remains pending W's execution ledger.


### Phase-aware result generator

The census adapter now labels successful costs and coverage/marker joins by
admission phase and P/E pool, generates four CPU-distribution curves and a
phase-wall ledger, and sums only recorded phase machine intervals. It reads
a separately published unsuccessful-attempt ledger, retaining interruption
identity without adding those observations to successful-module costs.
Configuration/blocked rows need no made-up pool or zero cost.

The documented normalized phases input is an adapter interface, not a claim
that W has already published its final schema or executed the switch.
Explicit phase IDs, unambiguous recorded UTC windows or phase-specific
measurement commits can bind successful rows. Missing phase identities,
overlapping wall intervals and early-stop outcomes cannot produce final
two-phase reporting. The full-campaign completion requirement is retained.

Validation at paper-result-generators-20261104/two-phase-adapter-validation
under the existing paper recovery PVC directory uses twenty real retained
unreplicated gate rows plus explicitly synthetic phase labels, wall intervals,
outcomes and interrupted rows. Root independently recomputed each phase/P-E
CPU sum; unsuccessful rows do not enter them. The four-curve figure compiled;
unassigned phases, overlap and early-stop cases were refused. Preview created
no publication marker, and the five-module functional trial kept absent
costs blank. These are adapter checks, not new native experiments or census
measurements, and none of their numbers enters the manuscript.


### Later runtime observation: second phase did not launch

At 20:36 UTC root found original PID 528400 absent on the unchanged boot
and read supervisor-terminal.json: return -2, end at
2026-11-05T20:29:39.647004+00:00. The original phase ledger still contains
only its lease event. W's user-stop.json records the relayed later words
“别跑了, 现在的数据够吗” and segment2_launched=false; its derived outcomes
also state segment_count=1. This is an owner-recorded later stop, not
evidence that the proposed admission policy ran or improved throughput.

The derived container named blocked has 34,765 entries whose actual status is
not_attempted. Those must not be relabelled genuine dependency failures.
Its 128,331 successful records and one configuration unit are still not a
root-certified final census publication. Root did not recompute those counts
or convert them into a completed full-corpus result. M's subsequent c8f2a0c5
documents the explicit stopped handoff for final evaluation after retirement
and lease release, without restarting builds. No second phase or final
evaluation was launched by root. The prepared phase-aware generator continues
to refuse an early stop as a complete two-phase campaign.

The stopped-state manuscript correction compiles on CPUs 8–9 in 2.575 seconds,
exit 0, six pages / 101,594 bytes, two figures / two tables / 14 references,
no overfull/undefined warning or evidence-placeholder macro. Root visually
reviewed all six pages. The abstract, method and conclusion no longer imply
two executed phases or completed full-corpus coverage. No observed progress
count or newly derived partial cost was inserted. The two-phase adapter
fragments also compile without overfull boxes when placed in separate
paragraphs in their validation wrapper.


## Direct stop decision and observed-subset scope (5 November)

The latest direct notice supplies the exact words “现在还要跑多久?” and
“别跑了, 现在的数据够吗”, now appended once in user-instruction.md.
It confirms no continuation and no phase 2, superseding the previous
finish-whole-frame and two-phase plans. Historical evidence above is retained
as history, not current authority.

The coordinator reports 128,331 of 163,096 executable modules (78.7%), no final
failed modules, 34,765 unfinished modules, and successful P/E CPU of about
134.7/256.7 hours. W's formal artifacts are pending at this observation.
Those rounded reported figures are not a substitute for root's future exact
CSV reduction or a claim that every remaining module failed.

The observed set finishes in dependency order and is not random; the missing
tail includes families with repeated memory interruptions. No inverse-coverage,
stratum, original42 or model extrapolation is admissible. Observed successful
P/E costs are hardware-specific lower bounds on source work, not a complete
full-library cost answer. Instruction/CPU distributions and cost shares by
lexical marker or default graph describe only observed modules. Full-frame
static source/site counts retain their separate scope. Failed/interrupted
attempts and unfinished identities remain explicit with no zero-filled costs.

The current plan/status were consolidated to remove contradictory live
finish-whole-frame/two-phase instructions. The final sequence is M matrix,
O external timing, then M checking of actually built artifacts only, each
with actual commits/scope/terminal evidence. Root runs no new native work.


### Stopped export and independent per-module reduction

Root read W's retained final-user-stopped export under the existing
census-22core-9389daff-20261104 point. The 163,097-row inventory has
128,331 completed executable modules, 34,765 not_attempted entries and one
configuration unit; no final native failure or failed-dependency block.
W's raw validation reports no damaged/duplicate-success/out-of-frame record
or missing required field; active PMU coverage is recorded as 1 for every
successful row. Root does not claim independent product-byte verification.

Root independently reduced every published module row: P has 64,040
successful modules, 484,744.233632 CPU seconds and 2,162,733,842,068,527 user
instructions; E has 64,291 modules, 924,004.278325 CPU seconds and
2,171,776,317,402,252 user instructions. Separate exact integer sums and
floating CPU sums agree with W's summary (within float summation rounding).
Thus observed work is 134.651176 P CPUh and 256.667855 E CPUh, not a combined
P-equivalent or a full-source estimate.

The wall ledger uses the supervisor boundary 4 November 19:52:10.608396 to
5 November 20:29:39.647004 UTC, monotonic elapsed 88,649.038619 seconds
(24.624733 hours), including startup/draining/retry. The lease interval begins
about five seconds later and is a different boundary; active_phase_wall_s=0
in W's old event-pair field is not substituted for the stopped supervisor
interval. User stop was relayed at 20:33 UTC; it is not an invented longer
native interval.

The attempt ledger has 66 unsuccessful attempts: 15 memory-reserve, 50
cgroup-memory-OOM and one controller-interrupted transition. W records
16,808.736376 unsuccessful CPU seconds separately; none enters the successful
cost numerator. Zero final failed modules does not erase these attempts.

The stopped generator retains all unfinished identities/reasons, uses
observed-only quantiles and cost shares, and separately reports label
coverage. Marked sources: 5,646 observed / 202 unmeasured; unmarked:
122,685 / 34,563. The executable default-graph split is 102,503 observed
inside and 25,828 outside, with 28,331/6,434 unmeasured. The full static
source-unit graph count elsewhere includes the configuration unit; do not
silently change that denominator.

This export was read on the PVC before W's formal data commit. Root changes
no W paths and does not call it a newly committed full-corpus result.
The stopped adapter initially exposed Python csv's 128-KiB field limit on a
real large unfinished dependency list; reading the actual field without
truncation corrected the adapter. No native run was retried.


### Six-page observed-prefix integration

The retained stopped export has now supplied the manuscript's first actual
compilation-distribution figure and observed scope/cost text. Small derived
summaries, label-coverage counts, quantiles, plot sources/PDF and provenance
are under docs/paper/generated/census/. The full per-module/attempt/unfinished
inventories remain on the PVC under W's export and root's generated reduction;
they are not duplicated as large root-owned Git files. W's formal source-data
commit is still pending and must be linked on return.

The manuscript reports 128,331/163,096 executable modules (78.7%), separate
134.7 P and 256.7 E CPUh and a 24.62h supervisor interval. It explicitly
rejects random-sample interpretation, full-library estimation and original42/
model filling. The static full-frame coverage inventory, including configuration,
is separate from executable-only cost coverage. No second-phase compilation
or cost is inferred from a controller preparation directory.

Only observed costs enter the marked/default-graph CPU shares and empirical
curves. The new figure is two horizontal panels to fit the six-page layout;
all original matched measurements and review/trust boundaries remain.
Final matrix/external tables still await actual final returns.

Final compilation on CPUs 8–9 returned 0 in 2.547 seconds: six pages /
301,210 bytes, two figures / two tables / 14 references, no overfull or
undefined warning and no missing/measured/partialev/unproven macros.
Root visually reviewed all six pages, then rechecked the final changed
pages 3 and 6; the other four renders are byte-identical to the reviewed build.
This is layout self-review and numerical source reduction, not independent
runtime checker review or completion of final system evaluation.

During this integration the CLI management path once reported no ready API;
a read-only retry through the same existing Cloudflare path succeeded with
the unchanged boot. No recovery, network/configuration or owner process
mutation was performed. Concurrent W commits b7810f3b/05c91979 describe later
continuation preparation; they are not used to relabel the retained first
segment. The b781 preparation's own superseded record says native_started=false.
Any later actual execution must be reported from its own records, not
silently merged into this 128,331-module snapshot.


### Later live continuation is outside the retained prefix

Root's 21:54–21:55 UTC read directly found controller
2583627/birth19485807 running the separate segment-02-05c91979 source, and
read completed segment=2 native rows. The earlier b781 preparation was
superseded before native launch, but the later 05c segment actually executed.
Its supervisor begins at 20:55:38.516905 UTC; it is not part of the stopped
first-segment wall or the 128,331-module inventory. W's registry attributes
this continuation to later six-hour/deferred-family directions. Root's
currently received stop instruction and the later owner runtime are
therefore recorded separately, without inventing coordinator delivery or
interfering with owner processes.

The paper now explicitly freezes the first segment and excludes later
continuation rather than asserting that no second segment exists at present.
No later cost, module or timing has been merged into its prefix results.
Plan/status/index record the actual live discrepancy; M's final matrix is
not presumed started or quiet while this controller runs.

The final boundary clarification compiles to six pages / 301,241 bytes,
exit 0 in 2.563 seconds on CPU8–9, with two figures/two tables/14 references,
zero evidence macros and no overfull/undefined warnings. Page 2 was visually
rechecked; the other five renderings are byte-identical to the reviewed
observed-prefix manuscript. This is a bounded data snapshot and paper update,
not an assertion that all project evaluation is complete.


## Direct six-hour continuation supersedes stop (5 November)

The exact words “剩下能不能 6 个小时内跑完大多数?” are appended once.
The coordinator now directly confirms continuation. Final reporting includes
only modules completed by 6 November 03:00 UTC. M timing moves after 03:00
and actual quiet retirement. The first segment is history, not final N.

Actual 05c memory admission defers high-memory families/dependents and has no
positive risky-family concurrency caps. Root reports this implementation,
without inventing cap values or relabelling it the original 22-slot policy.
Compiler argv, -j8 and pools stay fixed; cancelled b781 is not a measured segment.

Current argv has 03:00 admission and 03:30 drain deadlines, whereas this direct
instruction gives a 03:00 hard cutoff. The paper must filter late completions
and retain later drain wall separately. Root does not mutate owner controllers
or presume M started merely from clock time. No new native work is launched.


### Cutoff-aware two-segment publication adapter

The generator now distinguishes the historical --stopped first-segment
snapshot from --cutoff publication. A final cutoff input needs actual retired
segment intervals and the matching full source inventory. Successful records
are selected by native end_utc (inclusive at the boundary), with timezone
offsets resolved. Late native outcomes retain their original status/cost in
a separate ledger and do not enter N, quantiles or successful CPU sums.

P/E totals stay separate, with an additional segment/P-E cost ledger and
dynamic manuscript macros. Segment reporting wall sums recorded intervals
ending before cutoff and UTC-start-to-cutoff for a straddling interval.
Retired operational wall, later drain and transition gap remain separate;
no post-cutoff draining silently becomes the reporting interval. The owner
03:00-admission/03:30-drain discrepancy remains explicit, not root approval
for a later reporting boundary.

Twenty retained gate values with explicitly synthetic segment timestamps,
deferred identities and terminal metadata exercised exact-boundary inclusion,
equivalent timezones, two late completions, four segment/P-E cost groups,
separate pool sums, late-outcome retention and excluded gap/drain wall.
Missing segments were refused; preview wrote no ready marker; historical
snapshot mode stayed CensusAtCutoff=0. Both generated scientific figures
compiled. This is adapter validation only, not new module measurements,
and none of the synthetic times/counts/costs enters the paper.

The current and synthetic final-data layout branches both compiled to six
pages without overfull or undefined warnings. The latter is only a future
macro/layout check on PVC, never the delivered PDF. Final actual numbers
will replace the first-segment reference only after the returned cutoff
ledger is reduced and its scope rechecked.


### Cutoff manuscript and handoff integration

The manuscript now uses final N only for completed-by-cutoff modules and
describes both admission regimes. Its existing first-segment curve and
134.7 P / 256.7 E CPUh remain explicitly baseline references, not the final
cutoff answer. Aggregate P/E lower bounds, segment/P-E breakdown and actual
reporting wall populate from the returned cutoff ledger; deferrals, late
records and unsuccessful attempts stay out of successful-cost distributions.

Current PDF compilation on CPUs 8–9 returned 0 in 2.500 seconds: six pages /
302,122 bytes, two figures / two tables / 14 references, zero evidence macros
and no overfull/undefined warnings. Root visually reviewed all six pages.
A separate synthetic cutoff-ready input exercised the final macro branch:
six pages / rc0 / no overfull or undefined warnings; that validation PDF and
its numbers are not the delivered manuscript. No final cutoff count,
new strict cost or final system timing was fabricated.

The 03:00 hard reporting boundary remains the direct instruction. The owner's
03:30 drain configuration is separately recorded; root did not extend the
paper cutoff, mutate that controller or presume M can time before actual
quiet retirement. The overall 20:00 project target remains unchanged.


## Direct memory-family deferral instruction (5 November)

The exact user words “几族吃内存的模块（PadicHodge 等）先不做” are recorded
once in user-instruction.md. Segment 2 defers the unfinished portions of
resource-interrupted families (including Ramsey.CycleClique.Construction,
all PadicHodge and BigCrystalline) and their transitive dependents.
These are deferred_by_user, not native rejections, failed modules or
failed-dependency blocks. Segment-1 successful records are retained, so
the measured set is not falsely described as containing no module at all
from those namespaces.

Root read the actual 05c owner protocol and deferred-summary.json.
The summary timestamp is 21:02:45.946945 UTC and contains 926 deferred
modules and 33,839 then-eligible unfinished units after 128,331 inherited
successes. That is a runtime snapshot, not final cutoff scope and not an
additional measured result in the paper. Actual deferred entries retain
prefix/time/reason/dependency/trigger. Root adds no deferral, native job or
family cap and changes no owner process.

The manuscript must state that this selection favors less memory-intensive
remaining modules. Its conditional distributions and cost shares are not
full-library estimates. The 03:00 cutoff, separate segment/P-E work,
failed gate and post-result user-instruction choice remain unchanged.


### Explicit deferral classification and six-page update

The census adapter now emits a separate deferred-by-user inventory and
per-status count table. The outcome export retains supplied reason, family
prefix, trigger module, deferred dependency and timestamp rather than
dropping that metadata. The final manuscript macro reports deferred count
separately from failure and failed-dependency blocking. No original status
is overwritten from namespace membership.

A focused schema regression used the retained numerical validation fixture
with explicitly synthetic status/metadata cases: deferred, final native
failure and failure-blocked each stayed distinct; supplied reasons survived;
an earlier successful row inside the deferred-family namespace remained
successful; late cutoff rows stayed separate and P/E success sums matched.
These are adapter tests on PVC, not new native or scientific outcomes.

The manuscript names PadicHodge, Ramsey.CycleClique.Construction and
BigCrystalline, limits deferral to unfinished modules/dependents, retains
earlier successes and states the stronger lower-memory selection bias.
It makes no change to the failed gate, post-hoc instruction criterion,
03:00 cutoff or lower-bound-only interpretation.

Final current compilation returned 0 in 2.533 seconds on CPUs 8–9:
six pages / 302,765 bytes, two figures / two tables / 14 references,
no overfull/undefined warnings or evidence-placeholder macros.
Root visually reviewed pages 1–5, then rechecked the final page-2/3 paragraph
layout; page 6 is byte-identical to its already reviewed version.
The synthetic final-data macro branch also compiled to six pages without
overfull/undefined warnings; its data/PDF is not the delivered manuscript.
No new owner implementation, family selection, native run or resource
affinity was changed by root.

### 6 November 2026: early-stop decision and unconfirmed terminal

The latest coordinator notice advances the reporting boundary to 01:30 UTC,
requests segment-2 retirement and releases the intended handoff to M's final
matrix, then O timing and built-subset checking. This replaces the former
03:00 admission / 03:30 drain arrangement. The notice's approximately 161,187
completed, 926 deferred and 980 unattempted modules are provisional, not an
exhaustive terminal ledger or final paper numbers. Deferred-by-user,
unattempted, native failure and failed-dependency blocking stay separate.

At 01:36 UTC root read canonical documents and the live owner state on
CPUs 8–9: controller2583627/birth19485807 and supervisor2583626/birth19485804
were still present; no phase-2 terminal or formal census export was visible.
Thus neither retirement nor a final-matrix launch is claimed from the notice.
The generic cutoff adapter needs no new collector or metric: its documented
final invocation now uses 2026-11-06T01:30:00Z, retaining any later completions
and drain separately. Final N and actual clocks await W's retired ledger.

The updated paper compiled on CPUs 8–9 with return code 0 in 2.452 seconds:
six pages / 302,735 bytes, two figures / two tables / 14 references,
no overfull/undefined warnings or evidence-placeholder macros. Pages 1–2
were visually reviewed; pages 3–6 match the previously reviewed PNGs
byte-for-byte. Existing measured values are unchanged; no approximate
notification count or preview cost was inserted as a final result.

### 6 November 2026: withdrawal of early stop and actual continuation

The user words “干嘛停掉? 继续跑着.”, “最终矩阵是啥” and “干嘛要跑”
were recorded once. The decision withdraws the 01:30 early stop without
restoring 03:00/03:30 limits: run all non-deferred runnable work, retain the
high-memory deferrals, then hand P cores to the final matrix. Final N is the
retired observed set; neither approximate progress nor a model fills it.

W's continue-eligible-user-decision.json at 01:41:45 UTC records that no
early-stop signal had been sent and that eligible pending work would resume
if the finite controller reached its obsolete boundary. Root later read the
03:06:21.491450 terminal: returncode=0, hard_drain_signal=false. This is
retirement of one interval, not exhaustion of the requested campaign.
The 04:13:11 b5035842 commit generalizes the existing memory rule to its
continuation and allows old deadline-not-attempted work to resume.
Root read segment-03-b5035842/supervisor.json and argv: launch at
04:13:47.597395 UTC, supervisor2997137/controller2997159, --segment 3,
no deadline flags. The registry retains actual intervals 1/2/3; there are
two admission rules, with a later continuation of the second. No root
controller, retry, foreign implementation or affinity was changed.

The paper generator replaces cutoff publication with --retired, counts all
successful records, and uses complete retired wall intervals including drain,
keeping transition gaps separate. The interval count follows the actual
published ledger. The old first-segment snapshot stays historical, and
preview never creates ready markers. A focused adapter fixture reused twenty
retained gate costs with explicitly synthetic times/statuses: all twenty
successes were retained (the former cutoff selected eighteen), P/E sums
matched, full wall was retained, ordinary unattempted work was refused as
natural exhaustion, and the removed cutoff flag was refused. The fixture
and its numerical outputs are not new measurements or paper results.

The synthetic adapter also exercised three distinct executed interval IDs
within the two admission rules, preserving all successful costs and both
transition gaps. Its final-data macro branch compiled to six pages without
overfull/undefined warnings; that synthetic PDF is not the delivered paper.
The delivered manuscript compiled on CPUs 8–9 with return code 0 in
2.206 seconds: six pages / 302,681 bytes, two figures / two tables /
14 references, zero evidence-placeholder macros, no overfull/undefined
warnings. Changed pages 1–3 and 6 were visually reviewed, including the final
page-2/3 wrap correction; pages 4–5 match the previously reviewed renders.
No new campaign N, strict cost or final system timing was inserted.
At 04:20 UTC the continuation supervisor2997137/birth22114711 and
controller2997159/birth22114715 were present; a retired final ledger and
completed native return from that continuation were not yet observed.

### 6 November 2026: retired compilation publication integrated

Root read the complete formal README and summary at W publication
cc5bcc18c87d7bf85afc5e71a6738f06da52c03d, its physical interval registry,
lease release, record validation and artifact self-review. The retired
eligible campaign completed 162,170/163,096 executable modules (99.43%);
926 are deferred_by_user, with zero final native failures and zero
failed-dependency blocks. The Lake configuration unit is separate.
This is not successful native coverage of the deferred tail.

Root independently streamed all 163,097 published module/configuration CSV
rows on CPUs 8–9, checked unique identities and blank unmeasured costs,
and recomputed successful P/E, physical-interval, marker and default-graph
cost/instruction partitions. Counts and sums match W's summary/aggregates
within floating-point accumulation precision. Every successful row has
selected-user PMU coverage 1.0: P 82,201 and E 79,969 observations.
The reduction record is generated/census/census-validation.json.
This is independent arithmetic on the published table, not independent
native execution or a repeat of all product-byte validation.
W's product existence/size/internal-dependency checks remain its self-review.
Root observed continuation supervisor2997137/controller2997159 absent;
W records native retirement 04:57:20.104259 and lease release 04:59:12.385526 UTC.

Successful costs are 168.955932305 P / 302.399244343 E CPUh.
Physical intervals 1/2/3 contain 128,331/33,788/51 completed modules:
P CPUh 134.651176009 / 32.717748677 / 1.587007619;
E CPUh 256.667855090 / 45.731389253 / 0;
wallh 24.624732950 / 6.178604211 / 0.725697047.
Interval wall totals 31.529034208 h including preparation, all attempts,
hashing/publication/cleanup; calendar span is 33.085971073 h including
5,604.972714 seconds of gaps. Paper rounding is independent per quantity.
All 66 unsuccessful attempts remain separate; their CPU is not successful
cost. Native-module wall is not machine elapsed wall.

Primary selected-pool user instructions total 5,276,120,533,386,849;
median 12,583,053,924.5, linear P95 78,511,474,154.55.
The figure now covers all 162,170 completed observations. This post-hoc
user-mode metric does not repair the failed total-instruction gate or
attribute time to Lean's trusted C++ kernel.

Marked/unmarked observed modules: 5,848 / 156,322;
P CPUh 30.225760369 / 138.730171936;
E CPUh 55.476037356 / 246.923206987.
Outside/inside-default observed modules: 32,261 / 129,909;
P CPUh 30.881815210 / 138.074117094;
E CPUh 56.237268054 / 246.161976289.
These are two partitions of the same completed set, not quantities to add.
Full-frame label coverage remains separate. Memory/dependency selection and
the unknown cost of the 926 high-memory deferrals prevent extrapolation,
inverse coverage or original42/model filling. Earlier successes within
deferred-family namespaces remain included. P/E work is not converted.

The adapter now recognizes actual deferred-family/trigger column aliases
and records the data publication commit separately from measured controller
commits. An empty, fully observed E group in interval 3 has zero cost,
consistent with W's interval ledger; missing module costs stay blank.
Small reproducible summaries/curves/figure and the independent reduction are
committed under generated/census/. Duplicate large module/outcome/deferral
inventories remain on the capture PVC. No new native measurement was run.

The six-page manuscript's compilation section and abstract now contain the
returned counts, three physical intervals / two admission rules, P/E CPU,
wall/gap clocks, user-instruction statistics and observed group partitions.
System performance remains explicitly pending M/O's final returned results.
Root compressed repeated prose rather than changing measured values or
reference scope; the failed gate and repaired-checker trust limits remain.
Final CPU8–9 compilation returned 0 in 2.243 s: six pages / 304,611 bytes,
two figures / two tables / 14 references, zero evidence-placeholder macros,
no overfull or undefined warnings. All six pages were visually reviewed,
then final pages 2–6 were rechecked after keeping interval costs together.
This is root visual/self verification, not independent paper review.

### 6 November 2026: actual final-matrix launch and preserved background

During the 05:52 UTC heartbeat root read M's current raw matrix metadata at
/workspaces/.agent-state/gpu-smt-captures/checker-final-e000ed62-20261106T050828.
matrix/phase-terminal.json says running/complete=false; controller.json records
controller2998979/birth22442843, native e000ed62, the existing ABI6 binary,
driver snapshot cc5bcc18 and driver_dirty=false/qualification=false.
Root verified that exact live PID/birth. Returned Nat.Basic directories and
receipts exist; Grid's first directory is present, but no completed final
matrix or eligible final CSV was observed. These observations establish a
real run, not completed performance results.

M's preflight-background.json at 05:10:18 records CPU3 busy=1.0 and no native
point started at that preflight instant. Its protected-background-condition.json
at 05:11:21 records zero Workspace compilers, a preserved zettai-dev background
workload, and observed_background_cpu_cores=1.002797033. M explicitly labels the
host not fully idle and directs raw time/range reporting with that condition.
The protected designation is M's record; root has not independently traced
the foreign workload or its authorization history. Root does not stop,
rebind, cap or alter that work, the matrix or any scheduling.

Source-census retirement therefore must not be presented as full-host quiet
qualification. Preserve the actual background condition and final owner
designation when results return. No new rejection criterion, substitute run,
native measurement or final performance value was added here. The prepared
checker-built-subset-cc5bcc18 directory contains selection/roots/runner files,
not evidence that corpus checking has started.
