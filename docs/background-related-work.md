# Background And Related Work

Prior-map integration below retains its old scope. **Fresh 2026-11-01 primary-source novelty audit and root verdict:** [A/B/C audit](novelty-20261101.md). A/B generic ideas and C generic parallel/decomposition/composition overlap established work; application-specific evidence remains qualified. The paper now marks Measured/Partial/Unproven claims.
This frontier indexes the existing paper bibliography, historical primary-source
reports and recent native-source audits under the user-selected characterization
mainline. Original source-access dates remain in those records.
[Paper](paper/main.tex) · [Bibliography](paper/references.bib) ·
[Status](research-status.md) · [Plan](research-plan.md).
The prior map, dated source judgments and old serving/GPU/failure-cache
admissions remain verbatim in the [entry archive](tmp/build-and-evaluate/step-0249-20261101T151943+0000/experiment-001/background-before.md.gz).
Historical next-action paragraphs are not current experiment instructions.

## Search Log
| Existing record / date | Question covered | Present use |
|---|---|---|
| Paper bibliography, annotations through2026-10-31 | Build/runtime, independent checking, warm RL services | Existing evidence, not refreshed metadata |
| [Native module-task audit](tmp/build-and-evaluate/step-0247-20261101T131749+0000/step-report.md),2026-11-01 | Does the bundled checker wait for imported modules to finish verification? | Actual pinned source says independent task dispatch; matched performance still missing |
| [Failure-selection source review](tmp/build-and-evaluate/step-0163-20261030T032548+0000/literature/report.md),2026-10-30 | Algorithm selection, restarts, stopping | Historical overlap; no new reproduction |
| [Closest failure-memory follow-up](tmp/build-and-evaluate/step-0165-20261030T035108+0000/literature/report.md),2026-10-30 | Existing deterministic failure skipping and cost control | Retain prior-art limits, not the current paper mainline |
| This consolidation | Reconcile an old2026-10-16 header/accumulated map with the current fourRQ | Records-only update, no new novelty verdict |

## PDF Corpus
Existing PDFs retain their original provenance, not a fresh download.
| Work | Retained path | Role |
|---|---|---|
| Lean4 | [lean4-cade21.pdf](reference/lean4-cade21.pdf) | Frontend/runtime/kernel architecture |
| Kimina | [kimina-2504.21230.pdf](reference/kimina-2504.21230.pdf) | Persistent verification service precedent |
| Keep the Proof State Live | [lean-snapshot-2605.25556.pdf](reference/lean-snapshot-2605.25556.pdf) | Prepared proof-state reuse |
| Boogie fine-grained caching | [boogie-cache-krml245.pdf](reference/boogie-cache-krml245.pdf) | Existing dependency-aware result reuse |
| Verus / VeruSAGE | [Verus](reference/verus-oopsla2023.pdf), [VeruSAGE](reference/verusage-2512.18436.pdf) | Historical software-verification source boundaries |

## Claim-Oriented Novelty Map
No claim of firstness is added by this table. The user-selected empirical scope
is unchanged; overall novelty remains unestablished pending the missing evidence.
| Current claim/question | Existing closest work | Overlap and unresolved delta |
|---|---|---|
| Cost location across released AI formal artifacts | Lean runtime, Mathlib profiling/build CI, Isabelle/AFP build studies | Profiling/build costs are established. Current study joins selected native clocks with fixed-source coverage; global weights/software coverage remain incomplete. |
| Cheap independent checking versus source production | leanchecker, Lean4Lean, Lean Kernel Arena | Independent/kernel replay is established. Our comparison charges source compiler work and explicitly scopes complete closures/components; causal import attribution is not complete. |
| Original-kernel parallel cases | Bundled leanchecker tasks, Isabelle build parallelism | Parallel checking is prior art. Current mechanisms are design cases, with extra coordinator/Cadapter trust and missing native module-task comparison. |
| Meaning of verified | Kernel/checker semantics and project build/input boundaries | No universal soundness or complete axiom-closure result follows from accepted sets, source tokens or short controls. |
| Warm/COW/cache/failure reuse | Kimina, snapshots, fine-grained caching, SHRED and historical source map | Existing primitives, not the paper's novelty. No return to closed GPU/oracle routes or new competitor reproduction. |

## Closest Work
These links identify the already cited primary artifacts; the integration date
does not certify their current live state or transfer their performance numbers.
| Work | Existing evidence boundary | Role here |
|---|---|---|
| [Distributed Parallel Build for Isabelle AFP](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.22) | Build/session parallelism and dependency scheduling | Prior build engineering, not our measured native kernel costs |
| [Lean4Lean v3](https://arxiv.org/abs/2403.14064v3) | Reimplemented Lean checker and compiled-environment replay | Independent-checker precedent; not source compiler work |
| [lean4checker / bundled checker](https://github.com/leanprover/lean4checker) | Official-kernel replay, not a separate kernel implementation | Native checking family and trust boundary |
| [LeanChecker4.34.1 source](https://github.com/leanprover/lean4/blob/v4.34.1/src/LeanChecker.lean) | Independent module-local task dispatch and prefix-based CLI selection | Root0247 verified source; no matched throughput yet |
| [Lean Kernel Arena](https://github.com/leanprover/lean-kernel-arena) | Checker/corner-case comparison at exported-environment scope | Different boundary and metric from source build wall |
| [Kimina paper](https://arxiv.org/abs/2504.21230) / [server](https://github.com/project-numina/kimina-lean-server) | Concurrent persistent REPL/header reuse | Existing service mechanism, not a serial library-build speedup |
| [APE-Bench v3](https://arxiv.org/abs/2504.19110v3) | File/repository-level proof-engineering evaluation | Workload/infrastructure precedent; not new timing evidence here |

## Mandatory Baselines
This section indexes **existing comparison families**. It admits no new capture,
baseline implementation, budget, agent or competitor reproduction.
| Existing family | Current evidence | Fairness / remaining limit |
|---|---|---|
| Pinned original source compilation | Four selected Oclosures reconstructed, source work charged per module | Includes imports/tactics/output; serial work is not parallel Lake wall. O resource-share deviation retained. |
| Direct original-kernel serial replay | Matched closure and local-module references in root reports | Stronger than comparing only to a deliberately fragmented one-worker variant; exact clock/output scope retained. |
| Declaration-parallel versus chunked target | Envelope existing decl8/chunk8 sequence | Chunking compared to stronger declaration parallelism; complete chosen-configuration pairing/repeats remain missing. |
| Native module-local task path | Actual bundled source dispatch verified in root0247 | Throughput at matched closure/worker/resource/lifecycle remains missing; strict-import DAG does not bound it. |

Lean4Lean/Arena/Isabelle/Kimina are citation precedents here, not newly admitted
numerical main baselines. Existing user ban on new competitor reproduction holds.

## Experimental Precedents And External Assets
| Question | Existing public/source-native asset | Reused boundary / caveat |
|---|---|---|
| RQ1 population costs | Fixedopenai/math4eaee875 and same-mask Mathlibd13f | Allsource census complete; original42draw runtime population incomplete |
| RQ2 checking versus production | Officialkernel replay and matched constructed artifacts | Charge wholeclosure separately from module components; shared dependencies overlap |
| RQ3 parallel checking | Originalkernel APIs and bundledchecker module tasks | No new proof rules; implementation trust, preparation and fullcost still matter |
| RQ4 coverage and trust | Native headers/acceptance logs, pinned source/toolchain/project targets | Missing/timeout/unsafe-partial exclusions not hidden, source tokens not axiom closure |
| Public software | [Released-output audit](../workloads/ai-verification-software/README.md) | Reference solutions/checker fixtures do not substitute for model outputs |

## Baseline Candidates And Controls
Existing malformed-proof/context controls support only their tested transitions.
Positive-set parity is not a proof of universal context/budget/diagnostic
transparency. The oldv4counterexample and v10RSS/Envelope timeout remain intact.
No unexecuted control, source code or model bound fills a missing native result.

## Absorbable Ideas And Adjacent Communities
Proof engineering/build systems establish cached artifacts and dependency
scheduling; checker work establishes post-export trust/acceptance boundaries;
verification services establish persistent environments and feedback APIs.
These are established methods to account for, not new names or novelty claims.
The characterization preserves Lean-first/OSDI-level goals without claiming
that selected prototypes or a successful compilation establish acceptance.

## Venue Evaluation Patterns
Keep exact workload population, actual input/output/trust boundary, strong
existing baselines, complete cost accounting, original failed/partial results,
resource-policy deviations and uncertainty. Do not mix process, component,
threadCPU, sampled cycles, queue time or hardware points.
This is the existing evaluation promise, not a new review gate or enlarged scope.

## Must-Read List And Novelty Verdict
Read the current paper/status/plan, root0231/0238population boundaries,
root0245censored result, root0246component interpretation and root0247baseline
source audit. Older detailed source branches remain in the entry archive and
their original linked reports.
No new novelty confidence, fullpaper acceptance or scientific-contract revision
is asserted by this record cleanup. Remaining global/source-phase weights,
software native coverage, matched module-task comparison, causal decomposition,
axiom closure and cluster evidence remain missing.
Next action follows existing owners' real results or independent root analysis
with paper-decision value; never a historical next-action paragraph or stalePID.

[Current-map consolidation](tmp/build-and-evaluate/step-0249-20261101T151943+0000/step-report.md); the entry archive above
preserves every prior dated branch and source judgment.

Closest same-corpus overlap newly verified: [nealmcb pinned report](https://github.com/nealmcb/openai-math-lean-tooling/blob/c9570a82f79b78a1a969a6316ac0fdd69aabef55/REPORT.md), sections1b/3c/3f/4/5, public technical report. Existing intuition/cost/coverage work, not just a generic predictor precedent. Root audit withdraws priority implications; no foreign performance numbers pooled. [Current verdict](novelty-20261101.md).
