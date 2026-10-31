# Evaluation: current evidence and open work

Updated 2026-10-30 UTC. Root owns paper/evidence integration; all root reviews
are **self-review (自审)**. The four frozen RQs remain open.
The current paper is [docs/paper](paper/).

The [verbatim previous frontier](tmp/build-and-evaluate/step-0212-20261030T173551+0000/experiment-001/evaluation-before-step0212.md) preserves all prior statements,
numbers and links. Its links retain the original docs/evaluation.md base;
the [historical Git view](https://github.com/yunwei37/proofserve/blob/b7a77f868b9ea844c6554fcc7b04e115d104f7e1/docs/evaluation.md)
preserves their navigation. Earlier archives and raw failures are unchanged.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>

## Authority and scientific scope

W/M/O retain their own workload/mechanism/open-source paths; root integrates
their evidence. The mainline awaits W/M results and user decision. Keep the
four continuing directions and Lean/SMT/OSDI objective, without a new deadline
or replacement cache-only/negative-paper thesis. CPU oracle remains frozen;
E038/narrow GPU routes stay closed. Preparation, ordinary scheduling, generic
caching and reflection alone are not new-contribution claims.
Authority: [user words](user-instruction.md), [initial narrative](idea-story.md),
[author decisions](questions-for-author.md).

| RQ | Frozen question | Current status |
|---|---|---|
| RQ1 | How much expensive native preparation can real verification candidate streams share across independent jobs? | unanswered:complete preparation-cost/context coverage remains missing |
| RQ2 | Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation? | unanswered:full native artifacts,history,cancellation and supported scopes remain incomplete |
| RQ3 | How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse? | unanswered:one full warm-resource pair is complete with limits;scaling/repetition promises remain open |
| RQ4 | After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? | unanswered:no useful extra full-flow GPU gain has been demonstrated |

<a id="resource-point-and-workloads"></a>
<a id="resource-point"></a>

## Resources and comparisons

Same gpu-smt-dev/phobos-vt/PVC. User shares:40GiB total, W16/M16/O4/root4,
each at most8cores. Root uses CPUs0–1 for small analysis/builds. Captures,
datasets and binaries remain on the existing PVC outside Git. Own signal
controls return errno13; no working external-signal watchdog is claimed.
Finite self-exit points charge retained processes. One-second RSS sampling
may overshoot and is not a hard quota. Historical lab48GiB/four-worker,
older two-worker24GiB-AS and G10 points keep their own resources and clocks.

<a id="resource-layer-diagnosis-and-missing-warm-comparison"></a>
<a id="complete-nativemathlib-derived-pair"></a>

## Strong warm-service and failed-candidate evidence

The [complete7808pair](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md)
takes warm25176.4873s/engine20323.0076s:1.238817×,19.2778%less elapsed,
with7808status aliases/3014accepted IDs equal. There are7682raw payload
differences and23rejected-source differences after env/empty-AST removal.
One ordered shared-host pair,affinity,retries and support work do not isolate
COW or prove a general gain. Old21693.76s two-worker and own-fresh1.24028×
are separate comparisons; the former also has six state differences.

[Fixed42solo](../artifacts/engine-resource-profile-2026-10-25/solo42-native-library-20261029/README.md):
41watchdog failures/1timeout/0restored accepts,complete;do not restart old queues.
[Resource reanalysis](tmp/build-and-evaluate/step-0183-20261030T112405+0000/step-report.md):
11of52concurrent resource failures become timeouts in solo retry. Global cap,
goal and tactic do not form a stable per-call failure certificate.
[480profiles](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md):
83timeouts/355ordinary/42resource;timeout-thread CPU55.19%interval_cases/
28.21%simp_all is not full-candidate wall.71prototypes establish no reliable
early-failure rule.
[Scheduling](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md):
21746.81s all/15385.39s first-original/15112.12s first-short,same142tasks,
old two-worker point. This is pass@k,not every-candidate RL rewards or novelty.
Held-out source-cost ordering did not beat FIFO; no repeat.

## Workload characterization

OpenAI/math4eaee875,Lean4.34.1/Mathlibd13f23b7:163097source files and
1354379lexical decide+kernel sites are not executions,cache misses or costs.
The [paper's native table](paper/main.tex) retains each separate point:
7baseline/7profile;82expanded50k;47incremental100k;109wider;Grid300sprofile/
634.280s unprofiled;14after-Grid;180.276s Amplitudes;109new-strata;two
authored-options sources;189original-options sample calls;11remaining calls.
Different budgets,prerequisites,workers and clocks are never pooled as a
homogeneous full build.491completed Grid-profile events plus unfinished work do not
partition wall; the intervals overlap. Seven-source1.13%profile difference is a single fixed-order
observation. Compilation is not full-service acceptance or full-axiom audit.

[Step0205](tmp/build-and-evaluate/step-0205-20261030T152520+0000/step-report.md):
new-strata109calls/106compile/2HB/1remainderwall,2984uninvoked.
Final call has8.030s,not300s;two unchanged sources later compile after removing
the100kCLIoverride,7.934/33.878s,not a same-budget gain.
[Step0210](tmp/build-and-evaluate/step-0210-20261030T170436+0000/step-report.md):
189calls/187compile/1missingRellich/1remainderwall,47blocked dependents;
1399.505203wall/2539.433437CPU s.16cached targets freshly remeasured,
171new dependencies. Last call11.734s,not600s.19of42probability endpoints
and6of21complete cells;23costs missing. .olean-only,not full Lake artifacts.

[Remaining23 point audit](tmp/build-and-evaluate/step-0212-20261030T173551+0000/step-report.md):
11calls/7compile/2memory diagnostics/2selfalarms;8blocked/10724never-started,
no new endpoint cost. Exact source,authored HB,j8/M8192,CPUs0–7.
Native wall1399.897144/CPU1894.702852s,capture1406.532695s.
Memory exceptions156.589663s/full600.120081s censor/remainder106.116280s
sum862.826024s,61.63%of this selected dependency-heavy point only.
Interpreter-tag memory exceptions exit-11;the tag is a check site,not tactic
CPU or an intrinsic invalid-goal claim. At that boundary19/42costs,23missing. No easy
replacement draws,missing-as-zero,successful-subset whole-library estimate
or finite population95%CI. Combined sample12.49GiB includes retained EPFL.

[Native363metadata](tmp/build-and-evaluate/step-0205-20261030T152520+0000/step-report.md):
89268theorems/47989auxiliaries/44528Exprkeys/44532level-private groups.
45661decision-shaped helper names in90modules form42610types;
933repeat/919cross-module.3051extras split1497within-module+1554cross-module
module/key extras. Actual hidden/export/cache state,misses,cost and full
axioms remain unknown.135-object45distinct pilot is not generalized.
[Source/native units](tmp/build-and-evaluate/step-0210-20261030T170436+0000/step-report.md):
42886source sites vs45661retained helpers;Jet50944/3938 and
Canonical240114/600,each helper type distinct. Branch syntax is observed,
event attribution is not. AuxiliaryGram0sites/1helper limits the predicate.
[Module exposure](tmp/build-and-evaluate/step-0206-20261030T155146+0000/step-report.md):
48of109calls containing cross-module types use454.207083/1399.655781s
(32.45%),including all module work;this is not duplicate-check CPU/time saved.

[Modern certificate pairs](tmp/build-and-evaluate/step-0208-20261030T164526+0000/step-report.md):
seven Int/list goals,all original/cert sources accepted,all pairs slower:
13.317706→23.936857s whole-source wall;extra theorem checks2.327609→5.757960s,
292checks,not exclusive CPU/first checking/warm service.
Wrong-raw-HB observers excluded;matched45typeprobe only16complete/1partial/
28unreached,60.181s selfalarm,not a completed census.

[EPFL prefix](tmp/build-and-evaluate/step-0185-20261030T113532+0000/step-report.md):
136returns53compile/71ordinary/12budget,623.799s;25.60%budget cost is prefix-only.
Later10k/j1/j2 points remain separate;original stuck source is censored.
[APRIL39pairs](tmp/build-and-evaluate/step-0188-20261030T115336+0000/step-report.md):
35reference passes/4HB;23mutation errors/16budget. Selected50.53%budget cost
vs11.05%inverse-inclusion ratio for released1835rows,not natural arrivals/CI.
[Training construction](tmp/build-and-evaluate/step-0202-20261030T144255+0000/step-report.md):
4836380publisher rows include250k synthetic/8457contract exclusions;stage
filters are not disjoint failure rates.12selected replays3compile/3ordinary/
6HB,55.04%selected budget cost. Six recursion controls in
[step0204](tmp/build-and-evaluate/step-0204-20261030T150458+0000/step-report.md)
do not identify the producer's original invalid-label cause.

## Mechanism evidence and semantic limits

[Retained200source diagnostic matrix](tmp/build-and-evaluate/step-0186-20261030T114011+0000/step-report.md):
flags/diagnostics/InfoTrees equal,rawHB differs63off/62on;838.670bodyCPU/
781.384eqRefl. Conditional indivisible-leaf1.0317× is not a full-flow bound.
[Original-budget50source/150returns](tmp/build-and-evaluate/step-0193-20261030T123624+0000/step-report.md):
19prior-clipped passes restored;rawHBdiff29/30.18forks/seven sources:
2/4/8core body models1.1847/1.2759/1.3404×,own-full-clock models
1.0986/1.1423/1.1713×;snapshot/merge/HB costs unmeasured,no actual parallel gain.

[Complete grid pipeline](tmp/build-and-evaluate/step-0201-20261030T141554+0000/step-report.md):
2004rows/16chunks represent4016016logical cells;2.290783s full collection
includes C compilation/emission/Lean/extra recheck.384additional checks show
overlapping1/2/4/8task lifetimes,median ratios1/1.775/3.102/5.002.
Pre-established declarations/fresh names/discarded environments and per-task
budgets do not implement first-check merging or globalHB parity.

[Complete64source repairs](tmp/build-and-evaluate/step-0207-20261030T161637+0000/step-report.md):
128native calls;original0accepted/13errors/51budget,repaired31/29/4.
Invocation-wall879.431413/285.778088s;separate builds23.010/2.571s.
[Third-family32source point](tmp/build-and-evaluate/step-0209-20261030T165602+0000/step-report.md):
original20errors/12budget,repair2accepted/29errors/1budget;
336.372899/208.961074s native wall,separate3.573/4.124s builds.
One of8historical opportunity sources recovers,not eight.
All33new proofs have standard-three axiom closures/no admissions.
Historical3014+33=3047IDs and142→145/244tasks,58.1967→59.4262%,
is a cross-experiment inventory,not a new7808run or unchanged-source verdict
parity. Old passes retained by union construction,not measured nonregression.

[Remaining four](tmp/build-and-evaluate/step-0211-20261030T172449+0000/step-report.md):
3683tactics return0.963s then an open declaration check at16s;
3703open eqRefl fallback at16s;3698prefix simp recursion (not HB);
3710bridge recursion plus prior omega error. Primary source/diagnostic parity
covers these four plus positive only. Seven changed-source interventions
identify sensitive paths,not equivalent successful acceleration.0.296ms
direct theorem application excludes first imported proof checking;no new
candidate recovery or exact reduction-node diagnosis.33/145inventory unchanged.

<a id="public-lean-code-verification"></a>


[Cross-corpus audit](tmp/build-and-evaluate/step-0213-20261030T184541+0000/step-report.md) checks all6185external source/mode observations,
113budget observations and3historical ProofNet ZIPs. ProofNet5952sources/
413reported-complete IDs identical across repetitions,28of186groups passing;
five unparsed-name groups retained. Rep0budget70=56recursion+14HB,
138.011222/1192.435110request seconds(11.57%);other reps remain separate.
Operational5879 is not an ordinary failure. Currentthree-family router hits0
across all6185source observations,not an exhaustive semantic classification.

Two fitted EPFL factorial/product expressions are checked,generated5215539
proof bytes regenerated exactly. Successful selected base/facts/method builds
3.475372/85.263874/3.772063s useM6144,separate fromM8192/j1/CPU8–15/self30s
whole-source pairs. Both originals and both final repairs exit1 with recursion
diagnostics;one leaf hit does not recover a complete source.0new tasks/
ProofNetinventory unchanged,not a newfull native run.22actual native
identities retired;samplepeak4773236736B. Controls' accepted AXclosures standard,
false-modulus control rejects by recursion,not a formal refutation proof.
No production mode,generic fallback or amortized E2E benefit.

MiniF2F's same-point126budget outcomes are85timeout+41resource,whose worker
attempts use38795.133452/52992.124106s(73.21%). This is not the old83/42point
or concurrent20323.0076s service wall;no cross-point phase/denominator reuse.

## Other retained results

[AutoVerus](tmp/build-and-evaluate/step-0179-20261030T095708+0000/step-report.md):
nonzero exits use~95%process time,top1.6%only3.3–3.4%;JSON/exit disagree,
generation unmeasured. Failure frequency is not heavy-tail concentration.
Verina189:46no-explicit-admission successes/139stubs/4missing-API errors;
simp elapsed slices are not exclusive CPU. LNSym/source checker counts are
not native timings. [Lean-mlir](../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md)
40.47/40.21s file/stdin vs94.04s profiled;overlapping LRAT traces do not
partition wall,prior LRAT work limits novelty.

[Final arithmetic screening](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md):
same3014accepted IDs,8.86%slower;34refuted intermediate goals/29ordinary-error
candidates,no timeout removed. Old25/0.2%used invalid wrappers,not final data.
Interrupted8031state/cost capture preserves2640archived returns/one derived
panic with elapsed unknown/at least1273unrecovered observations. Missing
records are not failures,zero hits or a complete run;old queues do not resume.

## Open evidence

Complete requested native workload/context coverage,artifact/history/cancellation
semantics,equal-resource scaling/repetition and useful extra heterogeneous
full-flow gain remain unresolved. No production failure cache,parallel verifier
or generic proof-repair mode is qualified by these selected points.
Paper builds,CI and self-review establish evidence/build health,not novelty
or venue acceptance. Mainline and user decision remain unchanged.

## Historical navigation aliases

<a id="own-load-aware-methods"></a>
<a id="frozen-evidence-and-full-history"></a>
<a id="complete-retry-tail-engagement-2026-10-29"></a>
<a id="elastic-branches-and-complete-state-tactic-caching-initial-opportunity"></a>
<a id="native-input-matching-and-completed-error-cost-actual-measurement"></a>
<a id="actual-population-interruption-2026-10-29"></a>
<a id="current-recovery-status-after-the-storage-eviction"></a>
<a id="g10-continuation-user-directed-separate-hardware-point"></a>
<a id="shared-node-guard-implementation-step0150"></a>
<a id="2026-10-30-resource-tail-and-exact-first-success-opportunity"></a>
<a id="latest-correction-runtime-only-and-cross-proof-call-granularity"></a>
<a id="2026-10-30-root-paper-integration-after-authorized-parallelization"></a>
<a id="2026-10-30-root-audit-of-completed-m1149a59-evidence"></a>
<a id="2026-10-30-root-cross-check-of-w002-and-native-reuse-baseline"></a>
<a id="2026-10-30-integrate-w003-and-m003-without-selecting-a-new-thesis"></a>
<a id="2026-10-30-retained-grid-checks-and-fixed-trace-memory-envelopes-step0178"></a>
<a id="2026-10-30-failure-frequency-versus-tail-concentration-step0179"></a>
<a id="2026-10-30-profiler-changes-diagnostic-execution-step0180"></a>
<a id="2026-10-30-first-released-module-native-costs-and-engaged-timing-hook-step0181"></a>
<a id="2026-10-30-native-failuredependency-cache-precedents-step0182"></a>
<a id="2026-10-30-full-coverage-memory-retries-and-native-outcome-transitions-step0183"></a>
<a id="2026-10-30-released-kernel-checker-fixture-units-step0184"></a>
<a id="2026-10-30-completed-prefixes-do-not-qualify-a-full-native-comparison-step0185"></a>
<a id="2026-10-30-complete200-native-diagnostic-differential-step0186"></a>

## Characterization reconstruction — current scientific contract
The direct 2026-10-31 user decision replaces the former branching/device
paper RQs. Current RQ1: artifact and build-domain coverage; RQ2: stage/system
CPU, imports and memory; RQ3: budget exposure and observer/outcome
reproducibility; RQ4: validated design implications and targeted repair limits.
Historical results below/above retain their original questions and units.

[Step0214](tmp/build-and-evaluate/step-0214-20261031T040106+0000/step-report.md) retains the previous full
manuscript and bibliography, independently audited452native dependency
compiles (five newly costed original probability targets, one purposeful
zero-weight target), and the superseding separate26/42standard-artifact
frontier.26targets/11complete cells are not a full-build estimate.
Recomputed completed-target user/systemCPU510.822757/201.186913s gives
28.2562%systemCPU. Grid52.41696%,45,375,721voluntary context switches,
1.32512average cores. Amplitudes29.53777%,not an assumed39–52%cohort.
Fastest sampled whole compiler1.11641s/2,598,928KiB is not import-only.
Default-root omitted451,008/1,354,379kernel tokens=33.30%lexical coverage.
AutoVerus3.4%slow-tail fraction remains separate from budget-error fractions.

Public software availability: inspected full Vero0a7325df tree does not
establish evaluated agent-output population; Vericoding387cd699 publicly
contains626Lean/962Rust/1754Dafny generated files; Lean Kernel Verify129e65bf
is public checker/fixture source, model-output provenance pending.
No native software capture or generated candidate is run by root.
Missing full native costs, software results, perf causes and import-only
attribution remain explicit manuscript RESULT placeholders.

## Import-floor and resident-page evidence — step0215
[Self-reviewed integration](tmp/build-and-evaluate/step-0215-20261031T050401+0000/step-report.md).
Primary O commits957feb9/e25fd64/fd348df: corrected startup phase actual
81returns (39build/39direct-import/3Mathlib), all zero/retired;13modules selected
by historical<5s among26completed random draws. Raw source/command/CPU/output/
sampledPSS joined independently, not a new root native run.
Instrumented warm-cache import median0.711834–3.195465s/median1.354781s;
median per-module import/build0.682098 and ratio of sums0.677724 differ.
Not a measured cache speedup or all-library import share.
39controls median3.113GiB high-waterRSS,92.88898%file-backed sampledPSS and
237.766MiB anonymousPSS; low Shared_Clean in serial runs does not show
non-shareability. Observer/phase CPU54.044838s is additional to205.945162native
CPU;194.168151native-wall sum remains uncorrected. Calibration/replay/perf
continuation is incomplete and its healthy queued work is not restarted.

Mcf49a93recomputed historical W26: top2systemCPU consumers84.11266%,top3
89.38815%; high-RSS EnvelopePsiB has3.8238%systemCPU. Correlation/source-level
getrusage/mimalloc hypotheses are not native causal attribution.
No fullCPUglobalCI, novel mechanism, new throughput or semantic fidelity result.

## Methodology, related work and W cost evidence — step0216
[Self-review](tmp/build-and-evaluate/step-0216-20261031T054013+0000/step-report.md) follows the explicit
author request, preserving the four characterization RQs and main title.
Native timing now explicitly separates P0–7/sharedlock from E8–23preparation,
old prelock observations, clocks, output facets, censoring and hypothetical
source/byte-rate/import/storage extrapolations.21strata/seed20261030/42draws,
HTandfinite-population equations, no easy-target substitution or missing=0.

We independently recheck e3301f9:14native returns/13compile/1group-remainder
censor,14byte matches/retired identities,3304.393144CPU/1700.017556nativewall,
1.94374mean cores. OnlyCoverageK14new original endpoint11.015661s:
27/42legacy-plus-locked native-setting inventory, strictlocked1,11complete
legacy cells; no fullCPU/globalCI. KernelValues20actualallowance92.929919s,
not a full600s failed opportunity. Part003fresh258.740709s has no known
old interrupted cost and no speedup ratio.
b2df330:actual261artifact sizes across87successful rows match raw records;
A26:1,418,376→77,581,124bytes=54.697149x; B61:9,780,494→420,157,676
=42.958738x. Success/selection-conditioned, not full-build/RAM/CPU estimates.
O import1.354781s/ratio0.677724/PSSfile92.88898% remains instrumented,
conditional13short-module matrix with54.044838observer/phaseCPU caveat.

Related work now distinguishes runtime/tactic/build engineering, Mathlib
cache/CI, official-kernel replay versus separately implemented checkers,
RLservices and multiversion proof engineering. Primary sources verified,
no upstream performance figures imported. Vero/LKV evaluated-model-output
provenance remains unconfirmed in inspected official artifacts; Vericoding
generated files are public. No model generation or root native capture.
Mcausal attribution is still a missing result, not filled by a queued run.

## Native source profiles, observer follow-up and unavailable replay — step0217
[Self-review](tmp/build-and-evaluate/step-0217-20261031T061359+0000/step-report.md) integrates published
W2996335/O4f0e90e initially, then published W31f32b1/4f89614 before completion.
Initial frozen tables remain; the manuscript uses committed private-anchor
revision2, not uncommitted worktree derivatives.
W20actualinvocations/5sources: sourcebytes/native diagnostics match4modes;
all20retired. Root independently streams decoded stacks:46,882native samples,
all5period/launcher totals match, zero lost; raw stat IPC/MPKI recomputed.
C++caller shares (unchanged under revision2)1.918/2.061/81.520/74.931/94.012%:
nativeusercycles, nearestrecognizedcaller includingcleanup, not purefinalcheck/
systemCPU/wall/population. Other/anchorless mass retained. Before/afterCPU
drift-9.905..+6.384%; no acceleration or perfectobserverparity inference.
Strictlockedcostcoverage now6/42/twocompletecells; legacy27/42/11distinct.

O21calibrationcalls allzero/retired/source-matched;7groups x3,
wallmedianrelative0.919882–1.087370, observer14.347585CPU/native49.964258CPU.
Not randomized or uninstrumented, and incomparable to81call54.044838CPUtotal.
5perfimportcontrols allzero/retired; eventscopes/samples/lost checked.
One Mathlib user+kernel579sample profile:markpersistent9.29%,nameeq5.69%
selfperiod, not a whole-source causal profile. Msystemcauses remain missing.

O28target+13emptychecker attempts all exit1 withCouldnotfindanyoleans.
Read-onlySDK4.34.1source/path audit: module discovery canonicalizes target
filenames, while41existing alias objects resolve outsideeveryrecordedsearch
root. This happens before replay; times/statuses excluded from nativechecking
cost or acceptance. No0/41proofvalidityclaim; no new native rerun or Ofileedit.
Allrawfailuresandpublishedblankratios preserved. Own root analysis/compile
usesE22–23,4GiB; no timednativequeue or infrastructure changed.

The final integration also recomputes W4f89614's ten before/after rusage rows
against the frozen20invocation matrix. First-baseline systemCPU45.33%/39.73%
in UMoments9/BarrierData41 versus4.12%EnvelopePsiB; switchrates115680/131232/572s-1.
These are own-mode denominators, not user-cycle fractions or syscall causality.
Two computational targets are outside default OAI root. Revision2 partition
sums and checker-subfamily periods rechecked: normalization71.43/65.71/80.61%,
cleanup9.30/8.87/13.34% native-user periods, not purefinalcheck.

## Conditional import scale and actionable design implications — step0218
[Self-review](tmp/build-and-evaluate/step-0218-20261031T063558+0000/step-report.md).
User-requested interpretation refinement, no new native capture.
Frozen O4f0e90e39successful import controls reconstruct13module medians:
min0.711834286s/median1.354780910s/max3.195464632s.
Hypothetical163000identical serial calls give32.230275/
61.341469/144.683537hours; rounded32–145,median61.
Warm-page-cache/short-successful/cohort/observer/parallelism limits explicit.
Not all-source native total, interval, cold-start estimate or removable work.

Five-source caller shares retain published revision2;75–94%/about2% are
native-user-cycle sample-period distributions, excluding systemCPU and
not full-flow wall fractions. No classification/data/source change.
28target replayrc1 plus13controlrc1 remain setup failures; successful
kernelreplay/matchedcost now explicit missing, no cheap-replay inference.

All six finding-specific implications now name the engineering choice and
evidence boundary: coverage-aware cache/build contract, allocator/memory
accounting/synchronization candidate tests, resident/warm environment,
consumer-specific cancellation/retry accounting, reproducible versioned
logical-work budget, targeted certified representation changes.
Existing allocationheartbeats not assumed observerinvariant; wall/RSS remain
separate operational protection. No new policy/engine/other-lane mutation.

## Qualified replay and trust-scope costs — step0219
[Self-review](tmp/build-and-evaluate/step-0219-20261031T071200+0000/step-report.md).
Supersedes missing qualified replay in step0218 with published O3f52f97,
without rewriting failed v2 capture.21rawnative rows verified against CSV/
stdout/stderr/budgets/PIDbirth; all identities and submission retired.
Shared-lock holder matches submitted flock; root newLeanstarts0.
15/15target replay successes,13earlier-short modules. Recomputed each
build denominator from O4f0e90e39buildrecords/13medians:
checkerprocessmedian3.510312727s,medianratio1.280504636.
Sequential earlier-observer denominators, not purekernelfraction/speedup.
Grid253.438516s/Amplitudes113.617746s compared separately to historical
634.280070s/180.275578s, ratios0.399569/0.630245, not newmatchedbuilds.

Scopecontrols Initdefault2.026039/fresh2.428217;Mathlib2.194992/73.134445,
ratio33.318773. NearPinDeletiondefault2.555695;freshwallcensor180.111180
at180s,rc-15; no completedfreshcost or ratioimputed. StockSDKsource
verified: defaultimports trusted;freshloadedconstantmap intoemptykernel.
Unsafe/partial skip upstream; neither independentimplementation/axiom audit.
No current repairedemptycontrols/exclusivekernelcost; missing retained.

## Public generated-software outputs and observation units — step0220
[Self-review](tmp/build-and-evaluate/step-0220-20261031T081029+0000/step-report.md), published W2ad366d.
Root independently reads1503original Lean snapshots, verifies1490byte strings,
2013398bytes and626original snapshot inclusion; not626+1503.
Streams published journal for exact lexicalcounts, with no compiler start.
Reads all45rawfinaltables and joins16025rows/14109nonempty final outputs;
emptyoutputs remainmissing, publisherlabels notnativeacceptance.
No result is interpreted as perattempttiming, CPU fraction or fulltrajectory.
Static snapshots deepmath/proceduralsoftware scope remain separate.
Vero43/640active scaffold files/maxinternaldepth35 are not evaluatedoutputs;
HTTP403 limits absenceclaim. LKV90fixtures/12Leanfiles/templatenative_decide
notLLMstream/observednativeexecution. Vericoding rootversion metadata not
historicalperrun environment. Software nativecosts still explicitmissing.
RootE22–23/<4GiB; only paper/bib/eval/step edited. No W/M/O change.

Root all45table audit finds0nonempty explicit error_message fields:
do not call these complete failurediagnostics. Leanlexicalflags axiom35/
sorry12files are not measured nativeaxioms or proofacceptance.

## Collected locked original cohort C — step0221
[Self-review](tmp/build-and-evaluate/step-0221-20261031T081546+0000/step-report.md), W9244ef3.
Root rechecks544sourcebytecopies vsimmutablepublicsource,543triplesofartifact
sizes,544retiredPIDbirthidentities, rawCPU/wall and allcompleted42frame
costledgerreferences.617planned/73neverstarted retained, no restart.
2neworiginalendpoints only;544nativecalls are not544sampledraws.
OwnCPU2077.369333/wall1699.464566,average1.222367cores.
LastKeys28actual0.335247s/allowance0.302875s,
not600s failure. Native-settingcoverage29/42/12completecells, strict8/42/3.
No globalCPUestimate/finitefullCI; no weightedpooling acrosshistoricalpoints.
RootE22–23/0native starts; M/Otimingqueue untouched, Wcancelledqueues notresumed.

## Separate cost-denominator visualization — step0222
[Self-review](tmp/build-and-evaluate/step-0222-20261031T091443+0000/step-report.md).
No new measurement/conclusion. Five published W4f89614sources rendered as
twoaligned panels: before-baseline native user/systemCPU vs separate
native-user-period nearestcaller classes. Frozen217evidence is input;
allseries sum100%within its own denominator. No cross-run multiplication.
Replaces numeric phase table with reproducible PGFPlots PDF/TeX/stdlibplot
generator; normalization/cleanup/source/counter caveats retained intext.
RootE22–23/noLean. Firstfigurecompile rejects unqualifiedbarwidthkey; error
retained and corrected to documented /pgf/bar width, separatev2output.
No engine/runtime/other-lane/capture change. Not new performance evidence.

## Grid memory-budget enforcement attribution — step0223
[Self-review](tmp/build-and-evaluate/step-0223-20261031T092521+0000/step-report.md), Md4768da.
Root checks12baseline result/native/command/logs/retirement and1noMcontrol,
recomputes triplet medians/overhead ratios, streams305417cached native samples
to independently sum resource-accounting kernel periods and PIDscope.
Kernel fractions74.9786/74.9197/75.2593%, median74.9786%; applicationguard
caller fullyresolvedfirst2, unresolvedthird notzero. SDKsource/disassembly
retained; primaryLeanruntime/getrusage documentation verified.
Reportedartifactparityreceipts retained; root checks sizes, not a new1GiB
binarycomparison. No independentreview/axiom audit claimed.

This Gridpoint is olean-only/j8/M8192/HB100000 withnative15GiBcgroup and
M16GiBtreeguard, separate from Wstandardartifactcostsample.
Plainn3median621.935656wall/385.525127user/436.150621sys,53.0655%sys.
Recordkernelaccounting75%notmultipliedinto plainwallfraction.
One noM320.611816wall/391.521471user/107.411798sys, exactcommand/env
except-M/outputpath,matchingreportedartifact/logs; changedresourcepolicy,
not final3repeatgain or candidatefailureequivalence.
Instrumentedstatwall+1.4667%/sys+33.0974%;record+1.5681/+11.4738%;
tracesys+18.2492%, fixedtriplets not randomizedCIs. Trace losses retained.
Othermodulecausality/globalcost/softwarecosts stillmissing.
RootE22–23/15180KiBpeak/12.964sanalysis/0native starts.

## Preliminary half-wall contrast and implications for W costs — step0224
[Self-review](tmp/build-and-evaluate/step-0224-20261031T093728+0000/step-report.md), explicit latest author request.
Reuses already-audited d4768da, no new native run or repeatedrawdecode.
Single noM320.611816 vsbaseline-n3median621.935656:48.449359%lesswall;
107.411798vs436.150621sys:75.372774%less. Labels preliminary/n1vsn3/
Gridonly/nonrandom, not finalspeedup or exactremovablephasefraction.
UMoments9/EnvelopePsiB counterfactuals stillmissing in frozen resultset.

Wcostpoint-M9216 remains actualguardedcost; projectedexternal-only costs
maybelowerbyunknownamount. NoUniformGridcorrection/fullcorpusclaim.
Designimplication explicitlyexternalcgrouporlower/coalescedqueryfrequency,
not implementedpolicy. Kernel docs memory.max/OOMboundary cited; distinct
accounting/errorsemantics retained. No cgroup/nativeM/runtime change.
Paperrootonly/E22–23, no P-lock/agent/otherlane mutation.

## Completed Grid no-M triplets from closed native cells — step0225
[Self-review](tmp/build-and-evaluate/step-0225-20261031T102209+0000/step-report.md).
No new rootnative run. Nine MnoMplain/stat/trace cells have actual result/
native receipts and retiredPIDbirths; source/explicitEnv/ARGV differ only-M/
output. Outer15GiBcgroup retained; rootchecks empty native logs and all
artifact sizes/retained parityreceipts. FullMprioritydriver/matrix notclaimed
complete and healthy remainingworker cells untouched.
n3plain wallmedian305.692852280s,
range303.202725–320.611816 vsguardedn3median621.935656,
ratio2.034511608/reduction50.848155%.
Sysmedian107.411798range101.353828–213.345772 vs436.150621,
75.372774%medianreduction. Notsinglefirstresult/fullcorpus/equalpolicygain.
NoMstatwall+7.248272%/sys+
126.981651% versusownplainmedians, notuniversal
observercorrection. Wcostguardbias/othermoduleeffect/failuresemanticsunknown.

## Retired 90-cell matrix and variable policy effects — step0226
[Self-review](tmp/build-and-evaluate/step-0226-20261031T180455+0000/step-report.md).
Actualterminal90/90/no stop,90uniqueplan keys/rawpaths/PIDbirths; main/
prioritycontrollerretired. Root90native/result/command/log/size checks pass;
allnative/observer0,alloleanparityreceipts true. No raw data or driver changed.
Failedinitialrootqualification is retained: it wrongly assumed allmodules
shareGridHB/artifacts/M8192. ActualGrid is olean-only/HB100000/M8192;
UMoments9/Envelope use3facets/authoreddefault/M9216. The first diagnostic
guess aboutobserverstatus was corrected; all90observers actuallyreturn0.
Per-modulefactorARGV/explicitEnv parityrecomputed andscope kept separate.

NoMplainmedians Grid305.692852vs621.935656;UM88.211287vs141.739139;
Envelope63.517679vs64.446537. One-worker710.291849/174.764628/64.967556,
higherthan8workerbaselines. Two128MiBglibcthreshold controls have no lower
wallmedians; effects<0.71%. No randomizedCI/equivalencetest/globalcorrection.
Fullnativewall22157.171566/CPU31763.322688/groupinclqueue26850.310155
seconds are matrixcosts, not one-source build or noqueue-throughput.
Rootrawaudit0.056s/16636KiB/0native calls; no heavy perf decoding.
