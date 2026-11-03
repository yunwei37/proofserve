# Research result index

Current2026-11-03UTC, root0275. [Status](../docs/research-status.md) ·
[Plan](../docs/research-plan.md) · [Paper](../docs/paper/main.tex) ·
[Full history](../docs/evaluation.md).
[Exact previous index](../docs/tmp/build-and-evaluate/step-0267-20261102T092013+0000/experiment-001/before-research-README.md.gz).
Reports identify input, version, clock and trust boundary. Reviews are **自审**;
preparation, queues, controls and code are not performance or general acceptance.

## Latest complete results

- [Ramsey completed sample](decoupled-check/ramsey-sampled-result.md), [root0275](../docs/tmp/build-and-evaluate/step-0275-20261103T061615+0000/step-report.md):20/20 retained-prefix module-local references accept, pooledCPU35.91%; weighted190-file estimate34.99% is prefix-only. Production stopped190/444, stream0/444; trusted imports and selection bias remain. Raw/source frozen in rootstep and original PVC size-sample directory.

- [Falconer mathematical closure](decoupled-check/falconer-paper-result.md):
  13,205accepted modules/27checkpointed processes;2,043.59/22,077.77s=9.26%.
  All26exports/26restores included; module-local acceptance set agrees.
  Historical Mathlib10.56% and same-checkpoint Mathlib14.67% are separate
  closure/protocol observations, never multiplied or averaged into one gain.
- [2,524-target computation census](reproducible-verdict/census-results-v12/results.md):
  1/2/4/8actual workers ×3repeats,30,288acceptedchecks/22,716stable pairs;
  every target has0%allocation variation, P95=maximum=0%.
  No extra allocation-count headroom was needed for these observed runs; future runs, maxHB
  threshold guarantees and zero runtime overhead are not established.

- [Heterogeneous Barrier closure](parallel-stream-check/extended-results/heterogeneous-scaling.md):4,449modules at8/12/16/24workers,284.720→319.705s and668.786→1172.473nativeCPU-s.8P→8P+16E is12.29%slower/75.31%more CPU in one ordered capture; neither homogeneous scaling nor a cluster result. [Root0266](../docs/tmp/build-and-evaluate/step-0266-20261102T083616+0000/step-report.md).

- [Parallel count and byte comparison](parallel-stream-check/extended-results/parallel-determinism.md):100overlapping Barrier helpers/1200acceptedchecks at1/4/8/16caps×3,allcount ranges0%;12actual9,160,440Boleanoutputs equal one another/original. Checked3425constantpayloads,retainedmetadata trust;CPU still varies. [Root0267](../docs/tmp/build-and-evaluate/step-0267-20261102T092013+0000/step-report.md).

## Existing research directories

| Directory | Qualified work/boundary | Reports/raw location |
|---|---|---|
| [mechanisms-2026-10-30](mechanisms-2026-10-30/README.md) |Historical tactic/profile/resource studies. Old-M diagnostic data are not current noMcost/acceptance evidence. |[Prior work](mechanisms-2026-10-30/prior-work.md); PVC captures/mechanisms-2026-10-30/ |
| [profile-2026-10-31](profile-2026-10-31/systime/final/README.md) |90guard-calibration cells/3modules; guard/noM ratios2.03/1.61/1.01, matching outputs at passing points, not failure equivalence. |[Startup/replay](profile-2026-10-31/startup-replay/README.md); PVC captures/profile-2026-10-31/ |
| [decoupled-check](decoupled-check/README.md) |Four original overlapping closures/5085source union. New Falconer13205-module segmented chain9.2563%source wall, Mathlib same protocol14.6662%, complete module-local reference union. Added snapshot/metadata trust, Oshare deviations, two prior timeouts retained. |[Original results](decoupled-check/results.md), [Falconer final paper result](decoupled-check/falconer-paper-result.md); PVC captures/decoupled-check-20261031/scale-study/falconer-project-20261101/ |
| [chunked-kernel-check](chunked-kernel-check/README.md) |31artifact grain panel/13randommissing; small Grid whole-path negatives. Barrier fragment pipeline3.326x and small Envelope prepared-runtime1.096x are different scopes. |[Grain](chunked-kernel-check/step-006-report.md), [Barrier](chunked-kernel-check/parallel-result.md), [Envelope](chunked-kernel-check/envelope-result.md); PVC captures/chunked-kernel-check/ |
| [parallel-stream-check](parallel-stream-check/README.md) |Defectivev4context mismatch preserved. Repairedv14Mathlib1.523x/8workers; full Barrier/Grid4worker pairs1.558/1.882x. Envelope full original reference times out. |[Mathlib](parallel-stream-check/v14-math-results.md), [Full Barrier](parallel-stream-check/full-barrier-results.md), [Full Grid](parallel-stream-check/full-grid-results.md); PVC captures/parallel-stream-check-v4,v10,v12,v14/ |
| [reproducible-verdict](reproducible-verdict/README.md) |Observer-sensitive sync adapter, source counters and private-cache/budget controls. Root-qualifiedv12census2524local helpers,30288checks/22716stable thread pairs; no globalbudget/crossmachine guarantee.  |[Completed2,524-target census](reproducible-verdict/census-results-v12/results.md), [v11](reproducible-verdict/module-results-v11/results.md), [cache/coexecution](reproducible-verdict/cache-and-coexecution-results.md); PVC captures/reproducible-verdict-v*/ |
| [cost-prediction](cost-prediction/README.md) |Finite grouped forecast/native policy work; no general deterministic bounds or causal service gain. Simulated mechanism combinations are not native throughput. |[Root0254](../docs/tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md), [0256](../docs/tmp/build-and-evaluate/step-0256-20261101T205729+0000/step-report.md) |

PVC capture root is /workspaces/.agent-state/gpu-smt-captures/.
Pinned sources/SDKs/builds stay under /workspaces/.agent-state/gpu-smt-workloads/
and owning raw capture directories, outside Git. Historical failed, partial and
superseded captures remain; no static README authorizes restarting them.

## Workloads and distinct denominators

- [W records](../workloads/W-status.md) retain historical timestamps; current root
  source coverage32/42/15strata differs from31target-replay pairs/14strata.
- [Fixed openai/math frame](../workloads/openai-math/README.md):163097source modules.
  [Source costs](../workloads/openai-math/noM-standard-artifacts-a/README.md) and
  [stratified analysis](../workloads/openai-math/cost-regimes-noM/README.md)
  retain old snapshots. Root0263adds LowBlock15_1 only: source10missing,
  paired11missing and dynamic13missing are different gaps.
- [Released software](../workloads/ai-verification-software/README.md): published
  model outputs differ from reference solutions/checker fixtures. Vericoding
  snapshots overlap; Vero agent-output availability remains unestablished.
- Full-library phase weights, axioms/context closure, repetitions, released-software
  native evidence and cluster behavior remain missing.

## Root-qualified evidence map

| Root | Evidence and limitation |
|---|---|
| [0231](../docs/tmp/build-and-evaluate/step-0231-20261101T001556+0000/step-report.md) |Fixed whole-source lexical census. Full source archive at captures/step-0231-20261101T001556+0000-static/source.tar.gz; the13952file extraction is partial. No repeated census/download. |
| [0234](../docs/tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |Grain-call threadCPU and small Grid whole-path negatives; sourceproxy is not a runtime class. |
| [0235](../docs/tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md), [0236](../docs/tmp/build-and-evaluate/step-0236-20261101T051231+0000/step-report.md) |Barrier fragments and Envelope small-helper curves, different clocks/trust/proof transformations. |
| [0237](../docs/tmp/build-and-evaluate/step-0237-20261101T060743+0000/step-report.md), [0239](../docs/tmp/build-and-evaluate/step-0239-20261101T062456+0000/step-report.md) |Context counterexample and later RSS interruption retained; neither is acceptance of False or zero total cost. |
| [0241](../docs/tmp/build-and-evaluate/step-0241-20261101T080929+0000/step-report.md), [0242](../docs/tmp/build-and-evaluate/step-0242-20261101T081822+0000/step-report.md), [0243](../docs/tmp/build-and-evaluate/step-0243-20261101T091434+0000/step-report.md), [0244](../docs/tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md) |Version-qualified repairedMathlib, incremental targets and complete Barrier/Grid pairs. No cross-version pooling or multiplied ratios. |
| [0245](../docs/tmp/build-and-evaluate/step-0245-20261101T111249+0000/step-report.md) |Original Envelope full-reference timeout:10744completeaccepts+fragment, missing IDs unknown. |
| [0246](../docs/tmp/build-and-evaluate/step-0246-20261101T121151+0000/step-report.md), [0247](../docs/tmp/build-and-evaluate/step-0247-20261101T131749+0000/step-report.md) |Closure-provenance composition; official native module-task baseline differs from strict checked-import DAG. Matched native comparison stillmissing. |
| [0254](../docs/tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md), [0255](../docs/tmp/build-and-evaluate/step-0255-20261101T200059+0000/step-report.md), [0256](../docs/tmp/build-and-evaluate/step-0256-20261101T205729+0000/step-report.md) |Anegative/tradeoff policies, Bobserver counterexample, narrowed novelty/closest same-corpus overlap. No generic mechanism firstness. |
| [0257](../docs/tmp/build-and-evaluate/step-0257-20261101T215746+0000/step-report.md), [0258](../docs/tmp/build-and-evaluate/step-0258-20261101T225830+0000/step-report.md), [0259](../docs/tmp/build-and-evaluate/step-0259-20261102T000306+0000/step-report.md) |Private-input cache finite positives; failed Mv5partial and completed stage panel remain separate protocols. |
| [0260](../docs/tmp/build-and-evaluate/step-0260-20261102T020415+0000/step-report.md), [0261](../docs/tmp/build-and-evaluate/step-0261-20261102T023802+0000/step-report.md), [0262](../docs/tmp/build-and-evaluate/step-0262-20261102T030442+0000/step-report.md) |31targetpairs; Bcount spans0/0.0367/0.1385/2.3339%, not budget-padding guarantees; v12census qualified within3modules. |
| [0263](../docs/tmp/build-and-evaluate/step-0263-20261102T040256+0000/step-report.md) |Source32increment,10missing; current207.8–630.8source/10.8–41.9modeledstream CPUh scenarios, notCI or full checks. Old31ranges retained as history. |
| [0264](../docs/tmp/build-and-evaluate/step-0264-20261102T061224+0000/step-report.md) |Full Falconer source/segmented/refset audit and same-protocol Mathlib; raw source/protocol/failures frozen, no root native run or new scientific contract. |

[Novelty audit](../docs/novelty-20261101.md) covers prior Isabelle/Coq/Lean checking,
Mathlib, services, SATzilla and the closest same-corpus technical report.
A/Bgeneric mechanisms and Cgeneral decomposition/composition have precedents;
finite controlled boundaries and limits are the current empirical increment.

[Root0265](../docs/tmp/build-and-evaluate/step-0265-20261102T065555+0000/step-report.md) implements the direct finalized-number request; prior raw qualifications remain0262/0264. No native rerun or generic mechanism firstness.


CPU/coverage scope [root0268](../docs/tmp/build-and-evaluate/step-0268-20261102T190628+0000/step-report.md): Falconer6.31% and matched-checkpoint Mathlib8.95% are native CPU ratios.9.26%/10.56%/14.67% are separate wall ratios. Whole-source accepted2488/163097;9124compilation rc1 unclassified, bounded incomplete attempt. Raw process reanalysis and small CPU table are linked in the root report.


Hodge/source33 [root0269](../docs/tmp/build-and-evaluate/step-0269-20261102T191745+0000/step-report.md), [Wresult](../workloads/openai-math/noM-hodge-source33/README.md): original33/42/16strata; source224.1–427.4CPUh and separate mixed-protocol15.3–38.0modeledcheckCPUh are assumptions, notCI or whole checks. No Hodge target replay/grain measurement follows.


Actual84terminal/source35 [root0270](../docs/tmp/build-and-evaluate/step-0270-20261102T233639+0000/step-report.md):35/42originals,17complete strata; source232.9–396.0CPUh/mixed transfer15.9–35.2CPUh are assumptions. Wpublished34is an earlierprefix, fullterminal includesDihedral. Raw input/source35frame and originalcosts are in root record; no new replay/grain denominator.


Producer diagnostics [root0271](../docs/tmp/build-and-evaluate/step-0271-20261103T004041+0000/step-report.md), [Oreport](decoupled-check/whole-library-source-errors.md), [finitecontrols](decoupled-check/ramsey-qualification.md): all9124rc1logs classified;4controls do not prove all-source repair, uniformphase or isolatedruntimefacet.2488/163097historicalsource acceptance unchanged; Ramsey is separate/pending. No new native run byroot.


Source36 [root0272](../docs/tmp/build-and-evaluate/step-0272-20261103T025723+0000/step-report.md), [Wresult](../workloads/openai-math/final-seven-20261102/source36-NativeCodeAssembly/README.md): NativeCodeAssembly actualP0–7 compiler endpoint,36/42originals/18complete strata.238.7–362.1sourceCPUh/16.2–32.2mixed checking transferCPUh are assumptions, not measured full-library cost/CI.6source/11paired/13dynamic costs missing remain separate.


Corrected full attribution [root0273](../docs/tmp/build-and-evaluate/step-0273-20261103T031343+0000/step-report.md), [Mfinal](parallel-stream-check/attribution-results/final.md):12fullclosurecells+separatecompoundleaf. CPUgrowthinsideobservedordinarykernelbracketsdespitefixedcounts; phase/placement/observercomparisonsand50helpercount/bytequalification,notPMUcausality/generalbudget. Rawfrozeninrootstep;originalcaptureonPVC.


Physical/source37 [root0274](../docs/tmp/build-and-evaluate/step-0274-20261103T040607+0000/step-report.md), [Wresult](../workloads/openai-math/final-seven-20261102/collection-remaining-six-20261103T0325/source37-PhysicalFieldPopulationLimit/README.md):37/42originals/18complete strata; source242.2–315.2CPUh/mixed checktransfer16.5–28.0CPUh scenarios, notCI/wholelibrarymeasurement.5source/11paired/13dynamicmissingremainseparate; no completednewcelluntilTracked.
