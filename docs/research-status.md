# Research status

Snapshot2026-11-02UTC (root0263). Current frontier, not a new experiment or live-process
inventory. [Paper](paper/main.tex) · [Plan](research-plan.md) ·
[Results](../research/README.md) · [Related work](background-related-work.md) ·
[Detailed history](evaluation.md) · [Novelty verdict](novelty-20261101.md) · [Root cleanup](cleanup-20261101.md).

## Scientific contract
**Checking or Recomputing? Two Cost Regimes in Verifying AI-Generated Formal
Artifacts** is the user-selected mainline. Four questions concern cost location
and population weights; independent-checking preparation/coupling; original-
kernel parallelism/trust; and build, outcome and axiom boundaries.
Mechanisms are characterization cases, not a general accelerator or novelty
claim for caching, warm contexts or parallel checking.
Missing values remain explicit. Tests, self-review and activity are not acceptance.

## Ownership and policy
| Owner | Paths / responsibility |
|---|---|
| W | workloads/: fixed-frame native costs, released outputs, population weights |
| M | research/chunked-kernel-check/, research/parallel-stream-check/, research/reproducible-verdict/ |
| O | research/decoupled-check/, assigned research/cost-prediction/, engine/service/open-source paths |
| Root | docs/paper/, root reports, status/plan/index; other lines read-only |

Existing gpu-smt-dev/phobos-vt/128GiB PVC; W16/M16/O4/root4GiB within40.
At most8cores/line; root E22–23 small analysis/builds, no heavy native captures.
Native timing uses shared P0–7 and existing pcore.lock. Data/builds stay on PVC
outside Git. No new agent, queue, infrastructure or schedule.
Current Lean commands omit -M, including -M0; protection is external cgroup.
Charged memory, RSS and sampling overshoot differ. The old-M CPU profiles and
1.28replay/build ratio are historical, not current phase fractions or gains.
[Guard calibration](../research/profile-2026-10-31/systime/final/README.md):
three selected passing cases give guard/noM ratios2.03/1.61/1.01 and matching
outputs, without proving failure-budget equivalence.

## Current evidence
| Evidence | Result and actual boundary | Root audit |
|---|---|---|
| Fixed lexical census | Mathlib8529files/7masked sites; OAI163097/1354379sites in5848files,10668.32xsites/MB. Not runtime or exhaustive regime classification. Default root misses33.30%sites. | [0231](tmp/build-and-evaluate/step-0231-20261101T001556+0000/step-report.md) |
| W probability frame |32/42 source draws,15/21 complete strata/104632 modules. Conditional marked-source CPU share33.025%;10 ordinary draws/58465 modules in incomplete strata. Target-only paired replay remains31/42/14strata. No finite full-library CPU/global share estimate. | [0263](tmp/build-and-evaluate/step-0263-20261102T040256+0000/step-report.md) |
| Four O closures | Nat1330/NearPin3333/Grid3793/Amplitudes5083; check/source-work10.56/6.76/14.52/14.55%. One5085-node source union/161oracle chunks, overlapping warm observations. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) |
| Target components | Nat/NearPin/Grid/Amplitudes read-map-replay/source ratios6.54/0.46/80.28/82.35%. Excludes shared startup/base, not standalone latency or CPU shares. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) |
| Source provenance | Grid4OAI nodes9.76%compiler work/52.70%replay-call wall; Amplitudes8nodes8.69%/46.93%. NearPin2nodes0.569%replay/source work. Not global semantic weights. | [0246](tmp/build-and-evaluate/step-0246-20261101T121151+0000/step-report.md) |
| Native grain |31artifacts/34units;12decision-shaped calls >=1CPUsecond use10.09%callCPU. Weighted available29case28.23%,13draws missing. Not source/closure costs. | [0234](tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |
| Small Grid partitions |Both variants have no whole-path gain; some kernel subclocks improve. Old sampled14GiB guard lacks dedicated charged-cap receipt. | [0234](tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |
| Barrier fragment pipeline |15cells/99native stages,3425typedconstants;46.992→14.127s at8workers,3.326x/CPU+27.8%. One compiled-module lifecycle, not source/service gain. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) |
| Envelope small helper |15cells, kernel6.292x but prepared-runtime1.096x/CPU+53.6%, one pairedrepeat slower. Imports/assembly/lifecycle charged separately. | [0236](tmp/build-and-evaluate/step-0236-20261101T051231+0000/step-report.md) |
| Repaired v14 Mathlib stream |18cells/1330same module IDs,3fixed-order repeats:68.605→45.050s at8workers,1.523x/CPU+36.25%. Extra coordinator/Cadapter trust remains. | [0241](tmp/build-and-evaluate/step-0241-20261101T080929+0000/step-report.md) |
| Complete computational pairs |Barrier4449modules474.851→304.862s/uniform4=1.558x; Grid3793modules557.568→296.293s=1.882x. CPU+24.63/+33.56%, one ordered pair each; Grid repair gap disclosed. | [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md) |
| Incremental v14 targets |Grid8=4.024x/CPU+97.76%; Barrier8=5.297x/CPU+48.62%. Prefix/all-variant totals are not complete single-mode costs; old v12Grid underfill remains historical. | [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md), [0242](tmp/build-and-evaluate/step-0242-20261101T081822+0000/step-report.md) |
| Envelope full-prefix sequence |10752modules/nine target paths; chunk8vsstrongdecl8=1.319x/CPU+5.19%. Whole1665.530s includes all9/prefix, not one configuration. Sample13.971GiB vswait4peak14.019GiB. | [0243](tmp/build-and-evaluate/step-0243-20261101T091434+0000/step-report.md) |
| Existing module-task baseline |Bundledchecker dispatches module-local tasks independently; a strict checked-import DAG is not its upper bound. Matched native task comparison remains unmeasured. | [0247](tmp/build-and-evaluate/step-0247-20261101T131749+0000/step-report.md) |

O resource deviation remains explicit: nativecap11.875GiB and sourcepeak7.57GiB
exceeded the listed O4GiB share. It is not a qualified4GiB comparison or a
retroactive budget authorization. Whole-source totals are serial native compiler
work, not parallel Lake wall or model generation. Unsafe/partial exclusions and
axiom semantics remain in all checking scopes.

## Failures and unresolved trust
- [Context mismatch](tmp/build-and-evaluate/step-0237-20261101T060743+0000/step-report.md): defectivev4 accepts cyclicTrue-proof data
  after an undeclared sibling; samebinary module-localpath rejects. Repaired
  finite controls reject, but positive-set parity is not universal context proof.
- [v10Envelope interruption](tmp/build-and-evaluate/step-0239-20261101T062456+0000/step-report.md): return-9/RSSsample15.698GB.
  Raw cleanup-pending receipt retained; later retirement verified. Total child
  CPU unknown, not zero; no full curve or mathematical rejection.
- [Original Envelope full-reference timeout](tmp/build-and-evaluate/step-0245-20261101T111249+0000/step-report.md):
  rc124/1680.158s,10744complete accepts plus222byte fragment of10752expected.
  No completion/RSSstop/OOM. Missing records are unknown, not8proof failures.
  Full serial parity and single-configuration speedup remain missing.
- Full axiom closure, general corrupted-input/budget/backtracking transparency,
  multi-machine validation and broad public-software native costs remain open.
  [Released software audit](../workloads/ai-verification-software/README.md):
  Vericoding snapshots are model outputs; Vero agent-output availability is
  unestablished, and LKVfixtures are not an identified LLM candidate stream.

## Retained history and next action
Completed finite captures stay completed: especially W48, O's four-closure
matrix and the published M curves/pairs. Future execution requires the owner's
actual new plan/PID/birth/terminal, never an old running/prepared field.
No automatic retry, queue restoration or resource extension.
[Warm7808](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md):
19.28%less elapsed with matching statuses/3014accepted IDs, but order/retry/
support work differ; not isolatedCOW or general superiority.
[Held-out source-cost scheduling](../artifacts/candidate-scheduling-2026-10-25/source-cost-crossfit-20261026/README.md)
did not beatFIFO. GPU screening was negative at its measured point.
CPU oracle stays frozen; closed narrowGPU paths stay closed.
The42resource reruns and interrupted state-reuse data remain in
[evaluation](evaluation.md); missing records never become failures or zero hits.
Root integrates actual new evidence and independent in-scope analysis.
All reviews are **自审**, not independent or venue acceptance.
Unavailable complete cross-chat history is not claimed recovered.

[Current-record consolidation](tmp/build-and-evaluate/step-0248-20261101T141922+0000/step-report.md); exact prior text
is retained in [its entry archive](tmp/build-and-evaluate/step-0248-20261101T141922+0000/experiment-001/before-docs-research-status.md.gz).

## Direct novelty decision, 2026-11-01
[Primary-source verdict](novelty-20261101.md) and actual M/W/O handoffs are now integrated.
A's generic mechanism is precedented and its strong prediction/admission benefit unsupported:
[0254](tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md) recomputes31completed source costs and45native outcomes;
FIFO/predicted/upper complete15/15/13 at60CPU-s. Upper cuts0 rather than1 but completes fewer.
No per-request bound, global population guarantee or production gain follows.
Same-corpus prior work also limits broad characterization priority.

[B v1/root0253](tmp/build-and-evaluate/step-0253-20261101T185439+0000/step-report.md)
retains its parser-adapter defect and768row history; do not pool into correctedv2.
[Root0255](tmp/build-and-evaluate/step-0255-20261101T200059+0000/step-report.md) qualifies v2's1536rows/16selected inputs,10qualification rows and8task controls:
17rc0native phases,35PID/birth identities and all cgroups retired.
At budget1000 off/trace8/256acceptance-flag changes all repeat one input on the synchronous path;
stock has no observed acceptance loss. Frontend8/384at1000,0at3000; no thread-count acceptance change.
This refutes observer-independent accounting for the tested synchronous adapter, not Lean soundness
or stock-frontend acceptance stability. B global/cross-machine guarantees remain unproven;
C remains a measured finite engineering application with incomplete general/fullcost evidence.

Paper now root0255:17pages/177246bytes, full compile/all-page static self-review,
12prior numeric table bodies unchanged plus2distinct prediction/policy tables.
No new rootnative/agent, no old capture restart; prepared v3/v4 or ongoing Falconer work is not a result.

## Regime label and checker routing: new finite evidence
[Root0256](tmp/build-and-evaluate/step-0256-20261101T205729+0000/step-report.md) independently reconstructs31retained trace call sums:
among29original dynamic draws, fixed marker label givesTP14/TN13/FP1/FN1,
27/29conditional accuracy;13dynamic draws remain missing. Operational reference
is decision-helper>=50%kernel-callCPU, not all computational proof forms or production cost.
Both errors shareCatalanproject.0.482%kernelCPU exposure is not a causal wrong-route penalty.

New separate compiled-artifact120CPU-s point:9batches/12native calls;5completeMathlib
roots exactly1330reference IDs and7SIGXCPU interruptions. FIFO/type/upper mean complete
roots0.333/0.333/1, interrupts1/1.333/0,unused0.649/0.610/54.049CPU-s.
Known-root upper admission helps this panel, leaving45.04%idle; class envelope fails
retained NearPin transfer172.726>71.744CPU-s. Routing faster wall does not increase
completion count under CPU work budget. Same-root historical bounds are not
unseen-input safety, novel classification or a production scheduler.
Recorded sample1,389,350,912B/charged322,310,144B differ;Ochildcap11.5GiB+driver512MiB
still exceedslistedO4, driverpeakunknown. No retroactive share compliance.

M v3's160ladder rows yield0violations in100lower-pass/larger-budget comparisons;
8unsupported adapter controls excluded.48cache pairs preserve verdict/diagnostics,
but only7requestJSONpages treated, notcoldSDK/Mathlib. GeneralBstillunproven.
Both completed matrices'34PID/birth identities/cgroups retired. Real Falconerholder
and M/W kernel-lock waiters protected; no newrootnative/agent or queue restart.
Paper integration of this evidence is root0256, final compile/static review recorded there.

Current paper root0256:18pages184684bytes, full compile/all-page static self-review;14oldtable bodies+1new policy table, no newrootnative/agent. General/global/cluster/software/axiom gaps remain.

## Private-input cache and cost estimand: root0257
[Root0257](tmp/build-and-evaluate/step-0257-20261101T215746+0000/step-report.md) qualifies actual Mv8 complete9rc0phases:
512rows/256cache pairs,0verdict/diagnostic/axiom-policy differences,
128sync count vectors same;42stock parent counts vary, nottotalcandidatework.
101743private runtime files/8846348681bytes have different inodes from original
inputs;2238400selectedpages cold0/warmallresident. Cold native66.18–72.51s versus
warm8.83–15.04s is harness/import/frontendwall, notpurekernel/cache speedup.
Same-machine finite stability only; generalBremains unproven.
Retainedv6failure rc1/12.079s/0candidate rows precedes correctedinputclosure,
notLean rejection or a completed cache comparison.

Root recomputes Wsame14strata CPUmarkedshare17.1434% versus summed-native-elapsed14.8102%.
7incompletecells/59629modules and11missingdraws remain. Known165.187936HTterm hours
are a subtotal, not lowerconfidencebound; uniform+1CPU-s/missingdraw sensitivity10.842083h
is not imputedcost/globalCPU. Original31/42 and grain29random+2purposeful/13missing unchanged.
Mcache controller292324 retired; next matched-regime301735 is a real kernel-lockwaiter,
W301743 also waits behind healthy O301572. No restart or hot modification.

Paper root0257:19pages188474bytes, full compile/all-page static self-review;all15prior table bodies/title/fullabstract/4RQ/sections/four implications unchanged. Root0newnative/agent. GeneralB/globalweights/software/axiom/cluster gaps remain.

Root audit metadata correction:0256count34covered Mparents/controllers but not memory-process arrays;0257now checks all16sampledMv3processes retired as well. No clock/verdict changes or backdated audit; original report/raw retained.

## Matched co-execution attempt is partial, not still running
[Root0258](tmp/build-and-evaluate/step-0258-20261101T225830+0000/step-report.md) audits actual M5terminal:15nativephases,
14rc0/1rc1,all31PIDbirth/controller301735/cgroups retired,noOOM/RSSstop.
Completedmath8cells256rows:192worker1-versus-higher comparisons show0verdict
andacceptancechanges,84commandcounter-vector differences;actualworkerTIDs1/2/4/8.
These are finite configuration observations,not exactunit/globalbudget guarantees.
Grid4first-repeat cells32accepted rows retained;Envelope first import rc1/0.916s
has no REGIONrows because configuredLEAN_PATH lacks targetartifact.
Targetname matches qualifiedv14;existingoverlay-complete-v2has2268344Bobject.
This is inputavailability,notkernel rejection,notcompletecross-regimecurve.
Rootonlyread/freeze/diagnosis,noMsource edit or native restart.
HealthyFalconerholder332933/birth762601598 andW332936/birth762601628waiter
observed/protected;W31replaypartial10rows andFalconer11066sourceprefix are not
complete31sample/13205closure results.

Paper now root0258:19pages189874bytes,complete compile/all-page static self-review;15prior tables/title/fullabstract/4RQ/sections/four implications unchanged. No completecross-regimecomparison or generalB/Cguarantee follows.0rootnative/agent.


## Original-module stage qualification: root0259
[Root0259](tmp/build-and-evaluate/step-0259-20261102T000306+0000/step-report.md) reconstructs Mv10 actual complete terminal:58rc0nativephases,
56stagecells/336rows/252workercomparisons;117PID/birth identities and all cgroups retired.
Stored proofs: computational192rows/144pairs, mathematical16rows/12pairs,
0allocation/verdict/diagnostic differences. Mathematical kernel has only one eligible
proof per module and one active thread regardless of requested pool: no matched
concurrent-kernel treatment. Two mathematical source programs, eight clones percell:
128rows/96pairs/49allocation-vector differences,0verdict/diagnostic changes.
Syncbudget2000000/recursion20000/asyncfalse, not stock-budget equivalence.
Stage boundary, not math-only determinism, nativepollcount or completecandidate budget.
Full target imports trusted; computational source arm absent. Bgeneric guarantee remains unproven.
Old Mv5 partial remains partial: same192comparisons have83theorem/26opening/0terminal
count differences (overlap) and3timeout-text differences,0outcome changes.
No newrootnative/agent; old v5/v9/inventory/link/eligibility failures preserved.

Paper now root0259:19pages193486bytes,complete compile/all-page static self-review;15prior tables plus1stage table/title/fullabstract/4RQ/sections/four implications unchanged. Completed narrowstagepanel does not establish concurrentmathkernel/computationalsource or generalB/Cguarantees.0rootnative/agent.


## Completed target panel and repeated stages: root0260
[Root0260](tmp/build-and-evaluate/step-0260-20261102T020415+0000/step-report.md) independently reconstructs W31target-only replays:
31accepted/exact target-part matches; sourceCPU632.590445/replay272.695065s
(ratio0.431077), nativeelapsed393.895780/274.208513s(0.696145).
Queue-inclusive14768.395s is separate. Same14strata conditional source140.851561/
target-replay54.905548CPUh, ratio0.389811/nominal95%[0,0.940135],2draws/cell,
fragile effectiveDF1.185. Trustedimports/fulltransitiveidentity not established;
not empty-environment closure checking, full-library cost or source/service gain.
Original source31/42,11missing source/paired and13dynamic missing remain.

M v11 separately complete86rc0phases/84cells/504rows/378comparisons:
storedproof312rows/234pairs0allocation/verdict/diagnostic differences;
mathsource192rows/144pairs78allocationchanges/0verdict/diagnostic changes.
Only2actualprograms; kernelmath1activeproof/module, computational8selectedhelpers.
Pooled observed source count ranges0.036739%/0.138453%, not certified budget padding.
All205M/W recorded PIDbirth identities/controllers/cgroups retired; no rootnative/agent.
Prepared/queued Mv12full2524helper census is not this sampled result.

Falconer source summary reports13205constructed, but original fullcheck rc124/
1500.210998s,8942completeaccepts/8943headers plus75bytecutfragment.
CollectorJSONerror is operational, not math rejection or finalacceptsetmismatch.
Nativecgroup absent/noOOM; nativePIDbirth absent in receipt, not invented.
11.75GiBcharged cap deviates from listedO4; no retroactive authorization.
Recovery checks are separate actual owner paths; fullparity/ratio remainmissing.

Paper now root0260:20pages198939bytes,complete compile/all-page static self-review;16prior tables plus1target table/title/fullabstract/4RQ/sections/four implications unchanged. FullFalconerparity/ratio and generalB/globalcost remainmissing; target-only and repeated-stage scopes preserved.0rootnative/agent.


## Direct B boundary and missing-cost scenario revision: root0261
[Root0261](tmp/build-and-evaluate/step-0261-20261102T023802+0000/step-report.md) implements the user's narrowed empirical argument in the
Bcontribution/RQ4 and adds Wwhole-frame scenario ranges inRQ1.
Prepared24computationtargets:0%observed allocation spread across12checks each;
two mathsource spans0.036739%/0.138453%; concurrentminiF2F theoremcommand
83/192changes (fullvector84/192), max2.333868%,0acceptancechanges.
Cache256verdict/diagnostic and128syncvectors stable;100ladderpairs no counterexample.
No newbudgetmechanism or inference that onlymath/tacticsearch needs margins.
Percentages are observed count allowances, not required/sufficient maxHBpadding:
Corebudgetscope differs and threshold/causal-search evidence is absent.
M12census has an actualcomplete receipt now, not stillrunning; this revision
does not silently adopt its unreviewed2524-target outcomes or generalize v11.

Wsource178.225696–627.348203CPUh (outward-rounded178.2–627.4),
modeledstream8.322086–41.555143h (8.3–41.6) under explicit missing-cost
support and Oclosure CPU-ratio transfer. Not confidence/guaranteed bounds
or measured wholelibrary costs; no-assumptionupper unbounded.
Missingchecks2xsource reverses gap935.534vs627.348h; no tautological generalgain.
MeasuredW31targetreplay medianCPUratio0.451(range0.087–0.885) remains
target-only/trustedimports, separate from modeledemptyenvstream.
14stratum140.852/54.906CPUh are retained as conditionalmeasured-estimator
quantities, not relabeled wholelibrary or replaced by a differentestimand.
Original31/42source/11missing,13dynamicmissing remain.0newrootnative/agent.

Paper now root0261:21pages204566bytes,complete compile/all-page static self-review;17prior tables/title/fullabstract/4RQ/sections/four implications unchanged. Bobserved count allowances are not guaranteed maxHBmargins; Wwholeframe ranges are scenarios, not confidence/measured cost bounds.0rootnative/agent.


## Qualified computation-helper census: root0262
[Root0262](tmp/build-and-evaluate/step-0262-20261102T030442+0000/step-report.md) now independently qualifies actual Mv12 terminal/raw/source:
36rc0processes/30288accepted checks of2524unique local helpers
(UMoments91164/BarrierData411320/Envelope40),each12observations at1/2/4/8workers
and3fixed-order repeats.22716j1-versus-higher pairs0allocation/verdict/diagnostic
differences; all2524per-target observedranges0%. ActualTID counts match requested.
73PIDbirth identities/controller366671 and36cgroups retired;noOOM/RSSstop,
noM/P0–7/14GiBcharged.3target.olean byte-match retained originalWproducers.
OriginalnoinlineIOkernel-check/timing code matches prior qualifiedprobe;
selection expands8→all eligiblelocal of_decide_eq_true-headed theorems,
freshnames/proofbodies preserved, importtargetcontext stilltrusted.
This is all eligiblehelpers in3modules, not allcomputationalproofs/globalcandidate
work/nativekernelpoll counts or threshold/crossmachine budget guarantee.
UnitCPUvaries despite fixedallocations;UMj1→j8median73.957600→95.415988s,
notzero-overhead or isolatedconcurrencycausality.
wait4RSS12727196KiB/sample13028470784B/charged6533206016B distinct.
Wholecontroller1283.999848s includesall36cells,not singleconfiggain.
ActualBintro/RQ4 nowuses qualifiedcensus, keeps v11math/24target panel separate;
prior0261receipt-only caution was accurate then, this step supplies missingaudit.
Wsource31/42/scenarioassumptions and13dynamicmissing unchanged;O/Whealthy
partial/reference/checkpoint requests protected.0newrootnative/agent/foreignedit.

Paper now root0262:21pages206438bytes,complete compile/all-page static self-review;17prior tables/title/fullabstract/4RQ/sections/four implications unchanged. B2524helper census is qualified within3modules; general maxHB/crossmachine/global guarantees remainmissing. Wscenario assumptions unchanged.0rootnative/agent.


## New source draw and terminal source19: root0263
[Root0263](tmp/build-and-evaluate/step-0263-20261102T040256+0000/step-report.md) independently qualifies source19 actual complete terminal:
13nativecalls/12rc0compiles/1SIGALRMwallcensor/6dependency-uninvoked.
Successes are11dependencies+1original LowBlock15_1; DihedralIntervals original
notinvoked. All14recordednative/controllerPIDbirth identities and13cgroups retired.
noM/P0–7/j8/authoreddefaultHB/olean-ilean-C/15GiBcharged+separateRSS/noOOM.
13sourcefiles byte-match pinned4eaee875. NewLowBlock184.589081CPU-s/
124.512017648nativewall, outputs7246016/985771/47699B,notnewkernel/replay evidence.
IntegralPairings dependencyrc-14/600.197701524s/633.525530CPU-s:
resourcecensor,notmathematicalreject/targetfalse.6uninvoked areunknown,not6failures.
Native1456.905625wall/1560.934089CPU separate from8019.708321queue-inclusive.
No oldqueue resume/retry/budgetextension.

Rootoriginal42frame +1verifiedcost now32/42source,10missing/allordinary,
15complete strata/104632modules.9marked strata coverall5848marked files;
sourceCPUestimate57.546404h marked/116.704826ordinary, conditionalshare33.024963%;
summednativeelapsedshare27.020391%. Old14stratum17.1434/14.8102% remains
historicalcoverage,notfixed-populationtime trend. Full-libraryCPU/globalshare
unknown; proxy!=semanticphase. KnownHTsubtotal195.029837h/notconfidencebound;
uniform+1CPU-s/missingdraw sensitivity10.680417h.32observedCPU817.179526/
nativeelapsed518.407798s. Target-onlypaired replay remains31/42/14strata,
dynamicgrain29random+2purposeful/13missing unchanged.

NewLowBlockcost exceeds previousmarkedclassmax163.845944,showing oldsupport
was anassumption.Updated32cost/10ordinarymissing supportminmax scenarios:
source207.894666–630.701677h→outward207.8–630.8;modeledstream10.826785–
41.839086h→10.8–41.9 with OclosureCPUtransfer. NotCI/guaranteedbounds/
measuredfullstream. Old178.2–627.4/8.3–41.6retainedasdated31snapshot;
unknownchecks2xsource reversesgap885.083vs630.702h. No-assumptionupperunbounded.
ActualpaperMethods/RQ1 and pairedscope updated,notonlylogs. Bcensus/otherRQ
evidence unchanged;0rootnewnative/agent/foreignedit.

Paper now root0263:22pages/207423bytes, complete compile/all-page static self-review;17prior table bodies/title/fullabstract/4RQ/sections/four implications unchanged. Source32/42/15strata differs from paired target replay31/42/14strata and dynamic panel13missing. Updated scenarios207.8–630.8source/10.8–41.9modeledstream CPUh retain explicit assumptions.0rootnative/agent.
