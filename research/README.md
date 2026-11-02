# Research result index

Current2026-11-02UTC, root0266. [Status](../docs/research-status.md) ·
[Plan](../docs/research-plan.md) · [Paper](../docs/paper/main.tex) ·
[Full history](../docs/evaluation.md).
[Exact previous index](../docs/tmp/build-and-evaluate/step-0266-20261102T083616+0000/experiment-001/before-research-README.md.gz).
Reports identify input, version, clock and trust boundary. Reviews are **自审**;
preparation, queues, controls and code are not performance or general acceptance.

## Latest complete results

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
