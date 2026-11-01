# Idea story

## Initial Narrative — 2026-10-07

This section records the initial scientific disposition of the expanded research effort and remains intact. It is a hypothesis and evaluation contract under BOOTSTRAP, not a claim that the intended system already exists or achieves its performance goals.

**Problem and stakes.** Verification is increasingly performed on related candidate programs and proofs. Independent candidates require isolation, but preparing their verifier state repeatedly can consume CPU, memory and latency. The project studies real Lean proof checking and SMT-backed systems verification, preserving accepted, rejected, incomplete and resource-limited outcomes. The human requests acceleration, meaningful benchmarks, GPU exploration and an OSDI-level complete paper effort.

**Challenged belief.** A warm mutable session or result cache captures all useful cross-job reuse. The competing position is credible: established Lean REPL environments already remove cold imports, and the retained VeruSAGE sample has sparse exact duplicates and modest ordered-prefix bytes. The central question is whether preserving preparation while separating candidate execution histories changes the attainable latency/throughput/memory frontier beyond competent warm services.

**Central insight and thesis.** Reusable verification state is a native execution prefix, not merely a set of logically equivalent assertions. Reconstructing an assertion-equivalent incremental context can alter solver mode, heuristic history or resource accounting. Immutable prepared states with disposable native branches separate preparation reuse from candidate interference. The thesis is that this separation enables consequential parallel verification under bounded memory, with correctness defined by native verifier behavior rather than accepted-job counts.

**System and method.** The intended system prepares exact ordered native prefixes at supported quiescent boundaries, preserves configuration and solver resource state, and creates independent branches for candidate suffixes. Copy-on-write sharing reduces replicated preparation where feasible; bounded placement and branch lifetimes control memory and cancellation. Unsupported runtime or protocol cases execute on the native baseline. A stock library or frontend hook is distinguished from an unmodified executable. No arbitrary multithreaded fork is assumed safe. GPU work is selected from measured remaining checker costs and evaluated with preparation, transfers, fallback and the best CPU method included.

**Intended contributions.** A source-grounded characterization of preparation sharing in real candidate streams; a native-state isolation mechanism and its observable-behavior argument; a bounded service implementation with useful latency/throughput/memory tradeoffs against established reuse; and a causal assessment of heterogeneous checking after warm preparation. Fork/COW, REPL backtracking, result caching, integer-ID arrays and cached metadata computation are prior mechanisms, not individual novelty claims. Novelty must survive closest-work comparisons without a coined name.

**Scope.** Lean/Mathlib and Verus/SMT verification remain in scope. The initial backend anchors are the official Lean kernel/community REPL and version-aligned Verus with stock Z3. Public source-native proof/candidate streams supply actual work, including failures. Published proofs with mutations are correctness controls, not real generated candidate traffic. Arbitrary backend transparency, semantic canonicalization, full GPU Lean checking and universal acceleration are not assumed. RTX 5090 is the only GPU family used. Final data are produced from a frozen evaluated version; prior inspected measurements remain preliminary evidence.

**Paper research questions.**

- RQ1: How much expensive native preparation can real verification candidate streams share across independent jobs?
- RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?
- RQ3: How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?
- RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

**Evaluation promise.** Use actual ordered proof/program attempts from public Lean and SMT-backed systems-verification workloads; retain all outcomes, context availability and stage boundaries. Cover multiple contexts/projects in both families and unrelated-work controls. Compare the strongest runnable established warm services with result caching, matched native fresh execution as a control, and branch execution; baseline families remain subject to bootstrap literature pressure. Include candidate parsing/elaboration/construction, verifier checks, shared preparation, process/device setup, transport, queueing, replacement and teardown in end-to-end measurements. Report latency distributions, throughput, memory/PSS, CPU work, concurrency and offered-load scaling, and uncertainty across whole-run repetitions. Explain causal effects through preparation depth, COW mutation, state placement and lifecycle ablations. Test exact per-input decisions, requested models/cores/proofs where applicable, incomplete proof handling, timeout/cancellation and scope/history regressions. Evaluate GPU opportunities by measured expensive dynamic work and equal boundaries against tuned CPU checkers, allowing a useful negative GPU conclusion. All four RQs remain unanswered by final evidence.

## Current frontier

The user directs four continuing areas: reliable early failure/timeout
determination, first-success multi-candidate scheduling, Lean code-verification
workloads, and the layered Rust engine. There is no project deadline or
performance-based closure rule. Resource primitives remain prior techniques;
prospective novelty must come from workload-level methods. The external CPU
oracle is frozen, with no new oracle experiments or contribution claim.

The complete own arithmetic counterexample pair retains all7,808originals,
exact accepted/status parity and8.86%more native elapsed. It removes no
timeouts and remains a small component:
[full result](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md).

The480source failure profile is complete:
[actual tactic/phase ranking](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md).
Its source-memory diagnostic distinguishes sampled process occupancy, old
address-space failures, missing observations and new-RSS-point uncertainty:
[memory evidence](../artifacts/source-memory-attribution-2026-10-25/result-review.md).
Neither thread-CPU fractions nor sampled RSS maxima are whole-flow removable
fractions or a justified failure predictor.

The [Rust architecture](architecture.md) now includes typed backend/policy/
resource interfaces, dynamic admission, retirement, prepared import parents
and task-aware ordering. Pinned native contracts and whole-input policy checks
are implementation evidence; actual Mathlib/new-resource/full population
throughput and a useful systems contribution remain unproven.
[Task-aware implementation/model scopes](../artifacts/task-aware-engine-2026-10-25/result-review.md).

For current runtime/terminal state and the next inner work item, inspect the
latest timestamped reports under docs/tmp/build-and-evaluate and the owning
capture's actual terminal files. A narrative checkpoint is not a live-process
health record. Existing captures, raw failures and historical resources remain;
do not restart or change an active capture to match a newer resource point.

The complete Initial Narrative, all four RQs, Lean/SMT scope and OSDI-quality
objective remain intact and open. This thread performs implementation,
experiments, writing and self-review; no independent audit is claimed.
The current manuscript remains [docs/paper](paper/main.tex).

## Narrative evolution

### 2026-10-07: established native branching enters the competing position

The Initial Narrative challenged warm mutable sessions/result caching as the competing answer. The immediately preceding narrative was that initial disposition. Root now rejects the exclusive mutable-session framing: Kimina reuses immutable roots with candidate pruning, stock Lean supports serialized incremental snapshots, and Snapshot-DSP shares prepared state across independent parallel tactics. The chosen comparison explicitly includes native logical/serialized branching and bounded warm/cache services. RQ meanings and Lean/SMT/GPU scope remain intact. This is stronger and more faithful than both initial and previous framing because acceleration must survive current native reuse, rather than a cold or accumulating worker strawman. Evidence: [complete literature report](tmp/bootstrap/step-0001-20261007T212930+0000/literature-20261007T213700+0000/report.md), primary code/papers in its canonical map, and root E5 disposition in the [step audit record](tmp/bootstrap/step-0001-20261007T212930+0000/step-report.md). No process-cloning novelty claim is accepted. Revisit before freeze if no behavior/resource advantage survives these strong alternatives or a safe native boundary fails. This evolution preserves the complete Initial Narrative above.

Current E100 evidence bounds the current GPU fragment and finite-retirement gains; it does not alter the Initial Narrative or RQs. Complete CPU acquisition continues, useful GPU implementation and full service/SMT evidence remain open. No WRITE, final result review, outer audit, publication or acceptance has completed.


E101 isolated explicit-continuation/closure implementation now has compiled CPU/PTX identities and complete373retained real-graph CPU error analysis:5330/14591exports,57wholegraphs,73/399exact matchednative locals. Oldeager analysis remains168exports/0wholegraphs/2locals. AllareCPU controls, notGPUperformance/coverage orfullkernelproof. PublicWHNF ispartial; nativeMeta bridge remains absent. OfficialCPU fallback/trustedmetadata remainrequired. Rootimplementsresidentactualdevicepathseparatelywithouttouchingfrozenacquisition orresettingE021'sthreeattempts. Mainformal/fullservice/SMT/fourRQ/paperambition remainsopen. [Implementation limits](../artifacts/lean-gpu-checking-2026-10-13/closure-development-20261013/report.md) and E101completecommands/raw preserveprovenance.


E103 whole ProofNet WHNF diagnostic completed all5952 original sources, normalexit0/basic0differences,585.2256s. Raw and reconstruction are experiment015/whnf-full1/whole-counter-analysis.json. Four of five worker sessions have terminal counter dumps; the original operational worker is censored. Observed exclusiveCPU281.3783s in the cache-inadmissible/level-mvar union versus2.5654s cache-admissible cannot be whole CPU shares or GPU bounds: preparation inheritance, missing failed work, profiling overhead and duplicate rechecks remain. Native source proves cache-disabled modes can still be deterministic, so that union does not identify GPU support. E104/E105 classified repair completes all5952 original inputs/basic0differences,5951matched frontend intervals and one censored original5879, fresh whnf-classified-full1/reanalysis. Closed/no-custom scopes contribute97.5767s observed exclusiveCPU; the instances/cache-disabled/no-variable mask alone contributes82.9134s. This resolves the old overconservative cache-derived grouping, not actual GPU coverage or a whole CPU/GPU speedup bound. Native preparation inheritance, instrumentation/non-atomic deltas and failed/open work remain limits. A substantive native reduction/readback/provider integration is underway separately; its current compiled CPU/PTX controls are not device execution. Original queue41070/E015mini full5 child57992 on4–7, E01813440 and E0085450 remain protected. All8 E021 ProofNet CPU cells are complete; the original24 whole heterogeneous matrix remains incomplete. Native reduction/readback bridge implementation is isolated CPU control only until actual complete device integration and measurements.


E107 implementation/evidence update changes noInitialNarrative/RQ/acceptedconcept. Native3's realGPUpreflight1 completes44basic-matched outcomes,16usefulnativeoperationreturns onincompleteProof2913, minizero. Wholeformal32conditioncomparison againststrongwarm/snapshot-cache isadmitted; all16ProofNetcellsrequested, mini16afterheavydependency, nofulldataorGPUgainyet. Complete373graphactualcomponentcost isnegative, retainedratherthanhidden. Offlineprimarymeans/resources are notofferedload/service evidence; theoriginalRQ3promise drivesactualstreaming-interfacequalification. Fullservice/SMT/fourRQ/novelty/paperambition stayslargerthannarrowbeta orCOWprimitive; fullwriting/auditsremainrequired.


E110–E111 implementation/evidence update changes no Initial Narrative or accepted scientific concept. E022 full-cohort native3 CPU/GPU failures invalidate its performance comparisons; actual kernel-rejection exception ABI conflict is repaired in native4, all37 repair rows basic-match, old invalid/partial and valid stock data retained. Fresh matched final16 ProofNet request is ready. RQ3 implementation now separates real disposable candidate branches from unlimited warm sharing; full60-cell offered-load plan is independently reviewed and its first actual preflight started. No new performance/RQ/novelty conclusion follows. Complete main formal/service/SMT/GPU/writing/audits remain the target.


E113 accepts AXLE as additional same-claim pressure for generic isolated preloaded Lean serving, with SOCK/SEUSS/native snapshots already covering reuse mechanisms. This changes the literature/evidence frontier, not the Initial Narrative, RQ meanings or ambitious full verification goal. Complete source-native resource/history/service evidence must establish any surviving distinction; the active E023 full capture and ready repaired E022 request have not yet done so. Current node and literature report preserve limitations and root disposition; no first-isolated-service or OSDI acceptance claim is introduced.


E114 real complete5952-source service observations at one low-load pair show worse branch arrival latency than shared warm while whole time follows offered arrivals; strongest snapshot comparison and complete60-cell scope remain pending. Figures are staged raw-derived evidence, not final contribution/RQ results. This is an implementation/evidence boundary update, not a change to the Initial Narrative or full Lean/SMT/GPU service promise.

E038native runtime branching is now closed by explicit user instruction after no stable stock-relative gain in the final finite diagnostic. The known-slow eager-v1 capture is operator-stopped with all partial data retained. No full matrix may restart without a beneficial real matched preflight and complete-cost rationale. This closes an implementation constructor, not the original thesis or four RQs. [Disposition, GPU boundaries and next mainline](tmp/bootstrap/step-0010-20261014T133154+0000/route-closure-20261017T0127/result.md).

The [new primary-source admission](tmp/bootstrap/step-0010-20261014T133154+0000/literature-20261017T0212/report.md) verifies that plain expensive closing-proof/tactic-prefix reuse is already implemented by SHRED, while learned GPU feedback changes exact-verdict semantics. No new mechanism/preflight/full matrix is admitted; source pins, upstream-only arithmetic and released-data exclusions remain explicit. This adds prior-art pressure without changing the Initial Narrative or four RQs.


### 2026-10-17T22:16:14.732716+00:00 — CPU result does not resolve the GPU decision

The user explicitly requires evaluating the better CPU/GPU arithmetic oracle
before applying the >1.5x continuation criterion. The CPU stage is 1.34668x; GPU
attribution/evaluation remains open. The premature CPU-only closure is corrected
forward and the original hourly task restored. The [all-call GPU-stage plan](../artifacts/linarith-oracle-2026-10-17/gpu-stage/plan.md) and actual 1000-source
diagnostic now advance RQ4; they do not change the Initial Narrative, four RQs,
prior negative constructors or novelty requirements. Root self-review only.

### 2026-10-18 latest arithmetic evidence

The fresh full1,000native/positive-onlyCPU/two-sidedCPU clocks are
681.24/472.09/453.51seconds. The best CPU observation is1.50216x, only
0.653candidate seconds beyond1.5x. Native verdict/non-message parity holds
for all1,000, with104message-onlychanges. This motivates an unchanged
reversed-order replication rather than a stable performance or GPU claim.
The original system narrative and four RQs remain open: numerical certificate
primitives and one-block-per-LP batching already exist. A meaningful system
must still outperform competent warm/service/cache alternatives at matched
resources and demonstrate the broader workload and lifecycle claims.

### 2026-10-18 — reversed CPU pair and rejected async-device candidate

The unchanged reversedpaircloses: native687.263046932/two-sided447.309270379s
=1.536438193x,all1000verdict/non-messageparity,992/8/0,104messagechanges.
Bothprimaryordersnowabove1.5x;two-pairaggregate1.519180302x is descriptive.
Theoriginalthree-pairprotocolisnotcomplete: thirdnative-firstpairrunning.
RootimplementedindependentGPUgroup/streamprogress,but48GiBqualification
returns31allocationOOM/zeroactualGPUkernels. Failed65.444552sclockisnotGPU
performance. Noallocatorgrid/addressspacerelaxation/sourcepromotion/fullGPUrun.
[Reversedresult](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/two-sided-oracle/full1000-reversed-result-review.md);
[asyncfailure](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/async-device-progress/result-review.md).
StrongCPUbaselineapplicability/broaderworkload/novelty/serviceandfourRQcoverage
remainopen. Allreviewisrootself-review;goal/hourlynotclosed.

### 2026-10-18 — complete component result and full-workload admission

SameblocknativeFast/hybrid691.359191s,ASTdual464.579050s,nativefrontend/
dualbackend518.504231s. All1000verdict/non-messageparity,992/8/0;native-dual
has62message-onlychanges/88observerreaderrors. Nativebackendcomponent1.33337x,
ASTadditional1.11607x(10.40%lesselapsed),not1.5x. ChangedLPinputs/proofs/
fallbackmeanthisisnotapureproof-constructiontimer. Donotattributealltotal
speedup todeferredproofs orclaimglobalsystemsnovelty.

Nextfull29,750original-sourceblock isadmittedwiththeexistingnativehybrid,
nativefrontend+dualbackend,andAST+dualbackend,ononeCPU0–3/width8/48GiBblock.
First24realoriginal-sourcetransport/loggingqualificationmustactuallycomplete.
SupportJSONlogginguseslosslessstreaminggziptostaywithintheactual2.8GiBfree
projectvolume;allnormalcompression/flushoverheadcharged,no newquota/helper.
NoGPUclaimedintheCPUgeneralityexperiment.

TheoneGPUdiscovered-capacitypoolrepairalsoreturns31OOMs,nowpinnedto
cudaMemPoolCreatebeforeLPbuffers;zeroactualkernels. Nofurtherallocator
parametergridorfullGPUcapturefromthiscandidate;oldlegacybackendpreserved,
overallGPUroute/hourlygoalnotclosed.


### 2026-10-23 local — user-directed false-arithmetic-goal screening
The user stops further external-method reproductions/integrations and directs
our method toward exact-checked counterexamples before costly arithmetic
search. Retain all existing comparisons. GPU proposes points; CPU rational/
integer checks must satisfy the complete supported context and refute the
actualgoal. No witness/unsupported cases follow native. This is a new RQ4
mechanism experiment, not a claim that failedproofs are falsestatements or
that priorCPU/GPU results prove thisdirection. CurrentfullminiF2Fcensus
identifies87.66%of accumulatedrequestenvelopes on non-complete sources,
with51arithmetic-mentioned300stimeouts; actualfalse-goalcoverage isunknown.
The completeInitialNarrative/all4RQs and Lean+SMT/OSDIgoal stayintact, with
futureeffort focused on our method rather than expanding competitors.
[Plan and evidence](../artifacts/arithmetic-counterexample-2026-10-23/plan.md).

### 2026-10-25 — user freezes the arithmetic oracle and bounds further research

After reading the complete Initial Narrative and evolution, root accepts the
explicit user decision: external certificate search, floatingLP/exact repair
and the retained arithmetic CPU composition are established techniques and
remain frozen baselines, not our contribution. No further oracle variant or
experiment is admitted. This supersedes the earlier selected1,000/better-oracle
1.5x continuation rule; numbers and raw results remain unchanged.
The sole480failure profile must finish and its actual ranking be committed
first. Continuing requires a dominant actual tactic/phase and a new method
with defensible >1.3x end-to-end over native on all7,808or29,750originals,
excluding oracle gains; completion deadline2026-11-01UTC. Otherwise new
experiments end and the user authorizes a measurement/negative-results short
paper. This is more faithful to the user's latest scope than presenting a
known certificate interface as novelty or repeatedly narrowing GPU kernels.
It preserves the Initial Narrative as history and does not pretend its four
systems RQs were answered. Pending480evidence determines the conditional
disposition. [Root decision/self-audit](tmp/bootstrap/step-0011-20261023T195335-0700/step-report.md#cpu-oracle-frozen-and-new-conditional-continuation).

### 2026-10-25 — user replaces the conditional closure with three continuing directions

The latest explicit user instruction supersedes the immediately previous
1.3x condition, one-week deadline and short-paper closure. CPUoracle freeze
is unchanged. Continue reliable earlyfailure/timeout detection, first-success
candidate scheduling, and actual Lean code-verification workloads. This
preserves the ambitious Initial Narrative and is more faithful to current
user intent than a forced closure or oracle novelty claim. Candidate
scheduling changes the consumer contract to pass@k/best-of-n, not full
candidate rewards; report that boundary rather than claiming identical
per-candidate RL semantics. A provable local simplifier cycle or branch count
must still account for backtracking and complete-request acceptance.
The full480profile remains active; offline scheduling analysis/workload
preparation proceeds concurrently without a second collection or agent.
No new proof of benefit or contribution is implied by this direction change.

### 2026-10-25 — user prioritizes layered Rust engine and dynamic memory

The complete Initial Narrative/evolution were read. The user adds the Rust engine as a fourth continuing direction and makes extensible OSS organization the immediate priority. Resource/workload/semantic layers preserve the original verification-service ambition more faithfully than isolated arithmetic primitives. Only workload-level methods may support novelty. The next resource point removes fixed24GiB process caps, retains48GiB total actual RSS, measures CPU demand for concurrency, and retries preempted candidates alone. Healthy existing capture stays unchanged; historical outcomes remain. Safe COW, native parity and throughput are unproven. CPU oracle remains frozen; no gate/deadline/closure. [Design and root disposition](architecture.md).

## 2026-10-31 — user-authorized characterization reconstruction
The user explicitly replaces the independent-branching paper with a
characterization of the cost of verifying AI-generated formal artifacts.
The complete Initial Narrative above and all historical experiments remain.
Current primary workload: pinned openai/math research mathematics.
Second workload class: public model-generated verified software; admit only
existing public outputs, never generate replacements. Vero scaffolds do not
establish evaluated-output release; Vericoding generated sources are public;
Lean Kernel Verify is a distinct checker/fixture boundary with output
provenance still open. miniF2F, ProofNet and AutoVerus are contrasts.

Current claim: cost depends on build scope, stage/runtime boundary, outcome
policy and measurement method. RQ1 covers artifact/build-domain coverage;
RQ2 stage/CPU/memory costs; RQ3 failure/observation/reproducibility; RQ4
validated design implications and their limits. These explicitly replace the
previous four branching/device RQs by the user's scientific decision.
Six finding sections carry evidence, limits and a design implication.
Certificate repair and the Rust service are supporting cases, not core
contributions. System-CPU causes/import-only/software/full-build results
remain missing until qualified lane data arrive. No novelty or venue
acceptance is inferred from counters or compilation.
[Reconstruction and self-review](tmp/build-and-evaluate/step-0214-20261031T040106+0000/step-report.md).

## 2026-10-31 — user withdraws the memory-guard finding
Explicit user decision: completely omit -M, memory protection outside Lean.
The previous configuration-attribution finding is removed, not promoted as a
workload property. Five finding sections remain; four characterization RQs
and the original narrative/history above stay preserved. One methodology
paragraph gives the three within-module guard/noM ratios and observed parity.
All affected compilation/import/profile costs and projections are superseded,
replaced by missing noM results rather than scaled. Legacy systemCPU/core-use
claims withdrawn. Source/build-domain counts and separate noM checker scopes
remain evidence; certificate/service cases retain original historic boundaries.
This is more faithful to the user's workload-cost question than attributing
our nondefault setting to the workload. Revisit numerical findings only when
W's matching noM results arrive. [Self-review](tmp/build-and-evaluate/step-0229-20261031T235441+0000/outer-audit.md).
