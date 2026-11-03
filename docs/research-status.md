# Research status

Snapshot2026-11-03UTC, root0281. [Paper](paper/main.tex) · [Plan](research-plan.md) ·
[Results](../research/README.md) · [Full history](evaluation.md) ·
[Novelty audit](novelty-20261101.md) · [Related work](background-related-work.md).
[Exact previous status](tmp/build-and-evaluate/step-0267-20261102T092013+0000/experiment-001/before-docs-research-status.md.gz).

Root0281 independently qualifies [three official checker scopes and two real-root rejects](tmp/build-and-evaluate/step-0281-20261103T141838+0000/step-report.md). Stock default65.423s checks one root with trusted imports; fresh1/8 take534.698/580.090s, approximately1CPU occupancy and sequential replay of final imported map, not equivalent to4449 per-module ledger. No stock speedup/isolated thread effect. Both flags reject the same corrupted real-root theorem after identical4448accepted prefix, native rc1/noOOM or resource stop. Finite correctness controls, not arbitrary unsafe-FFI safety; native matched module-task baseline remains missing. Prior0279/0280 primary, memory and storage conclusions retain their denominators.

## Scientific contract and operating scope

**Checking or Recomputing? Two Cost Regimes in Verifying AI-Generated Formal Artifacts**
is the user-selected characterization mainline. Four RQs concern cost location
and population weights; preparation/production coupling; original-kernel
parallelism and trust; and build coverage, outcome reproduction and axiom closure.
Mechanisms illustrate implications. Generic caching, scheduling, parallel checking
and deterministic budget units have prior art; no first same-corpus characterization
or OSDI acceptance is claimed. Missing values remain explicit; reviews are **自审**.

Existing gpu-smt-dev/phobos-vt/128GiB PVC; no new agent, queue, Workspace or schedule.
W owns workloads/, M owns chunked-kernel-check/, parallel-stream-check/ and
reproducible-verdict/, O owns decoupled-check/, cost-prediction/ and engine/service paths.
Root owns docs/paper and root records; foreign implementation remains read-only.
Shares W16/M16/O4/root4GiB within40; at most8cores/line. Root E22–23 small work.
Native timing uses P0–7/existing pcore.lock. Data/builds remain outside Git on PVC.
Lean commands omit -M, including -M0; external charged caps and RSS differ.
Historical -M profiles/1.28ratio are not current workload fractions.
O's observed share deviations remain disclosed, never retroactively authorized.

## Current evidence and boundaries

| Evidence | Qualified result | Root record |
|---|---|---|
| Lexical census | Mathlib8529files/7masked sites; OAI163097files/1354379sites in5848files. 10668.32xsites/MB; default root misses33.30%sites. Not runtime or exhaustive semantic classes. | [0231](tmp/build-and-evaluate/step-0231-20261101T001556+0000/step-report.md) |
| Source probability frame |38/42originals;19/21complete strata/161034modules.9marked cells/5848files complete; markedCPU57.546/246.863h=23.311%, nativeelapsed18.5945%.4ordinary costs missing/2063module domain incomplete. | [0276](tmp/build-and-evaluate/step-0276-20261103T062502+0000/step-report.md) |
| Whole-frame scenarios |38known+4ordinary missing within observed support:247.5–270.3sourceCPUh; mixed-protocol check transfer16.8–24.0CPUh. Assumptions, not CI/guarantee/measured full checking; no-assumption upper unbounded. | [0276](tmp/build-and-evaluate/step-0276-20261103T062502+0000/step-report.md) |
| Target-only replay |31/31 accepted, trusted compiled imports, source632.590/replay272.695CPU-s; median per-module ratio0.451 (0.087–0.885).14paired strata140.852/54.906CPUh, nominal weak interval[0,0.9401], effectiveDF1.19. Separate from current source38coverage/full closure. | [0260](tmp/build-and-evaluate/step-0260-20261102T020415+0000/step-report.md) |
| Native checking grain |29available random+2purposeful artifacts/34units;13original draws missing.12decision-shaped calls>=1CPU-s use10.09%total call CPU; available-case weights are conditional, not global. | [0234](tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |
| Four original O closures |Nat1330/NearPin3333/Grid3793/Amplitudes5083: complete check/source-work10.56/6.76/14.52/14.55%. Same5085-node source union/161reference blocks, overlapping dependencies and warm observations. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) |
| Large Falconer closure |13205source/27segments; native CPU2038.444/32292.604s=6.31%; matched checkpoint Mathlib91.145/1018.219s=8.95%. Separate wall9.26%/historicalMathlib10.56%/checkpoint14.67%. Selected closures, one capture each, trusted metadata and Oshare deviation retained. | [0268](tmp/build-and-evaluate/step-0268-20261102T190628+0000/step-report.md) |
| Provenance composition |Grid4OAI nodes9.76%compiler work/52.70%replay-call wall; Amplitudes8nodes8.69/46.93%. Target components6.54/0.46/80.28/82.35% for Nat/NearPin/Grid/Amplitudes. Not CPU, global weights or causal import shares. | [0246](tmp/build-and-evaluate/step-0246-20261101T121151+0000/step-report.md) |
| Small Grid partitions |Both finite variants have no whole-path gain, despite some smaller kernel subclocks. Older sampled guard lacks independent charged-cap qualification. | [0234](tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |
| Barrier/Envelope helper cases |Barrier fragment pipeline3.326x/CPU+27.8%; small Envelope kernel6.292x but whole prepared-runtime1.096x/CPU+53.6%, one slower repeat. Different boundaries, not multiplicative. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md), [0236](tmp/build-and-evaluate/step-0236-20261101T051231+0000/step-report.md) |
| Repaired parallel stream |v14 Mathlib18cells/3fixed repeats:68.605→45.050s/8workers=1.523x, CPU+36.25%. Added coordinator/Cadapter trust remains. | [0241](tmp/build-and-evaluate/step-0241-20261101T080929+0000/step-report.md) |
| Complete computational pairs |Barrier4449modules1.558x/CPU+24.63%; Grid3793modules1.882x/+33.56% at uniform4. One ordered pair each; Grid controller repair gap preserved. | [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md) |
| Incremental targets |Finalv14 Grid8=4.024x/CPU+97.76%, Barrier8=5.297x/+48.62%; Envelope chunk8/strongdecl8=1.319x/+5.19%. Prefix/all-mode totals are not cold single-mode costs. | [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md), [0243](tmp/build-and-evaluate/step-0243-20261101T091434+0000/step-report.md) |
| B measured stages |2524local eligible helpers in3pinned modules,30288checks/22716thread comparisons:0allocation/verdict/diagnostic differences. Math source ranges0.0367/0.1385%, separate16-source panel max2.3339%/0pass changes. Not free runtime, sufficient maxHB padding or global/cross-machine guarantee. | [0262](tmp/build-and-evaluate/step-0262-20261102T030442+0000/step-report.md), [0261](tmp/build-and-evaluate/step-0261-20261102T023802+0000/step-report.md) |
| B cache/budgets |Private-input cache256verdict/diagnostic pairs stable,128sync vectors stable;100valid budget-monotonicity pairs no counterexample. Limited treatments, not universal semantics. Sync trace acceptance loss repeats one input; observer transparency not established. | [0257](tmp/build-and-evaluate/step-0257-20261101T215746+0000/step-report.md), [0255](tmp/build-and-evaluate/step-0255-20261101T200059+0000/step-report.md) |
| A prediction/admission |Grouped source forecast error and native CPU-budget policies do not establish bounded prediction or route benefit.29/42dynamic labels agree27/29conditionally; known-root upper admission has finite availability tradeoffs, not general service gain. | [0254](tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md), [0256](tmp/build-and-evaluate/step-0256-20261101T205729+0000/step-report.md) |
| Heterogeneous full closure |Barrier4449modules,8P/8P+4E/8P+8E/8P+16E:284.720/299.807/310.591/319.705s;24versus8 wall+12.29%,nativeCPU+75.31%. One fixed-order capture/settings,not homogeneous scaling or a cross-version speed ratio. | [0266](tmp/build-and-evaluate/step-0266-20261102T083616+0000/step-report.md) |
| Streaming count/bytes |100overlapping Barrier helpers×12observations at1/4/8/16caps,1200accepted,allcount ranges0%.12actual9,160,440B.oleanfiles equal each other/original;3425checkedpayloads substituted,extensionmetadata trusted. UnitCPU3.575→9.941s;not zero runtime or globalbudget. | [0267](tmp/build-and-evaluate/step-0267-20261102T092013+0000/step-report.md) |
| Corrected full attribution |12full Barrier cells+compoundleaf complete; P4→P8 extraCPU95.95%in observed kernel-call brackets, natural mixedwall+6.36%on/+5.53%off. Fixedcount work with CPUinflation; causes notisolated. | [0273](tmp/build-and-evaluate/step-0273-20261103T031343+0000/step-report.md) |
| Whole-source producer diagnostics |9124rc1:9118unavailable interpreter/native declarations,4module-data,2IR/codegen.4finitecontrols pass;139declaration diagnostics notline1. Whole-source2488/163097stillpartial, no proof rejection/yield/globalcost conclusion. | [0271](tmp/build-and-evaluate/step-0271-20261103T004041+0000/step-report.md) |
| Ramsey retained-prefix sample | Production stopped190/444; no full stream.20/20 module-local references accept, pooled CPU35.91%; prefix-only weighted34.99%, resampling29.41–40.41% omits selection/missing-target uncertainty. Trusted imports, not a comparable full-closure ratio. | [0275](tmp/build-and-evaluate/step-0275-20261103T061615+0000/step-report.md) |

| Fixed-work PMU and uncertainty |16full Barrier processes share graph/count work; extra4→8 CPU91.70–99.15% in observer brackets, whole-command cycles+8.31% at instructions+0.0396%. No unique RC cause.19complete source strata nominal95% interval43.99–449.74CPUh/df2.13; not full-frame CI. | [0277](tmp/build-and-evaluate/step-0277-20261103T071354+0000/step-report.md) |

| Supplemental checking-thread PMU |Two valid counting-only points have14historical checkingTIDs/complete7×8READsets. Instructions+0.037%,cycles+10.60%,L3missloads+36.46%,IPC1.834→1.659. Thread-lifetime scope, not pure kernel/uniqueRC cause. FailedP4r2retained. | [0278](tmp/build-and-evaluate/step-0278-20261103T081624+0000/step-report.md) |

## Terminal failures and trust that remain visible

- Defective Mv4 accepted a cyclicTrue proof after an undeclared sibling; same-binary
  module-local replay rejected. Repaired finite controls do not prove general context
  transparency. [0237](tmp/build-and-evaluate/step-0237-20261101T060743+0000/step-report.md).
- v10Envelope sampled-RSS stop and original serial Envelope1680s timeout retain
  partials; unknown accepts/total childCPU are not failures/zero.
  [0239](tmp/build-and-evaluate/step-0239-20261101T062456+0000/step-report.md),
  [0245](tmp/build-and-evaluate/step-0245-20261101T111249+0000/step-report.md).
- Mv5math subset completes but Envelope import input is absent; v6cache missing IR,
  v9namespace and early v10qualification failures remain. Later versions do not
  retroactively complete them. [0258](tmp/build-and-evaluate/step-0258-20261101T225830+0000/step-report.md).
- W19continuation ends12compile successes=11deps+LowBlock original; IntegralPairings
  wall-censored,6uninvoked including DihedralIntervals. It is complete as an attempt,
  not a reason to restart or fill source10missing.
- Falconer's two unsegmented1500s timeouts retain8942/9040full accepts and fragments;
 3000.416s failed native work is separate from the successful chain.
  Snapshot metadata and restoration are trusted glue. Independent RSS samples and
  native-child PID/birth were not emitted; no full resource/identity qualification.
- Released AI software requires actual published model outputs. Vericoding snapshot
  sets overlap, Vero agent-output availability is unestablished, LKV fixtures are not
  identified LLM candidate streams. No replacement generation.

## Open evidence and next action

Source4/paired11/dynamic13 gaps differ; do not change one denominator with another.
Full-library phase weights, causality/repeats, whole axioms/declaration closure,
released-software native coverage and cluster behavior remain unresolved.
Bundled LeanChecker already dispatches module-local tasks independently:
a strict checked-import DAG is not its upper bound. The matched same-ID/resource/
full-clock native competing path remains unmeasured, not a root-launched queue.
Complete cold single-config Envelope parity/pairs and broad failure semantics
also remain missing. [Native baseline audit](tmp/build-and-evaluate/step-0247-20261101T131749+0000/step-report.md).

Root integrates only actual new qualified terminal evidence. Existing healthy
captures and real lock waiters are protected; no old completed queue resumes.
No schedule, model, resource, security or infrastructure change is implied.

Paper root0281:27pages/242735B,20oldtables/title/fullabstract/4RQ/sections/fourimplications unchanged;fullcompile/all-page self-review completed,0newrootnative/agent.

Historical finalized-number update [0265](tmp/build-and-evaluate/step-0265-20261102T065555+0000/step-report.md): RQ2 now places9.26%/10.56%/14.67% side by side with distinct closure/protocol boundaries and26exports/26restores included. RQ4 foregrounds2,524/2,524 zero-range targets, P95=max=0%, observed no-extra-count allowance only; module-source envelope0.0367–0.1385% and separate candidate maximum2.3339% remain different units. No guaranteed maxHB margin/future/zero-runtime claim.


CPU and coverage update [0268](tmp/build-and-evaluate/step-0268-20261102T190628+0000/step-report.md): Falconer native check/source CPU2038.443942/32292.603807s=6.3124%; matching checkpoint Mathlib91.145172/1018.219383s=8.9514%. Separate native elapsed ratios9.26%/historical10.56%/checkpoint14.67% remain. Source/protocol/CPU units are not pooled. Whole-source bounded attempt accepts2488/163097source+10744dependencies;160609source missing,9124source-compilation rc1 unclassified, not mathematical rejection or measured full-library cost.

Historical0268scope audited rc1count only. Root0271now independently classifies the retained9124diagnostics and qualifies finitecontrols, without asserting uniform phase/singlefacet/all-source repair.


[Root0269](tmp/build-and-evaluate/step-0269-20261102T191745+0000/step-report.md) independently qualifies W28d21e0 Hodge176 terminal:176rc0=175dependencies+1original IndexedInverseMultiplier (3.929919wall/4.131784CPU-s). Source33/42,16/21complete strata/144565modules;9ordinary original costs missing/18532module domain incomplete. Conditional source217.424460CPUh, marked57.546404h=26.4673%; summed-elapsed marked21.1985%. KnownHTsubtotal217.945744h is not population estimate/CI; each missing+1CPU-s adds5.134167h. Source support scenarios224.1–427.4CPUh; separate mixed-protocol transfer15.3–38.0CPUh uses current checkpoint ordinary6.31–8.95% with historical unsegmented computation8.4421–8.4671%. Neither is actual full checking/CI/guarantee. Wpaired31/42/14strata/dynamic13missing unchanged.


[Root0270](tmp/build-and-evaluate/step-0270-20261102T233639+0000/step-report.md) qualifies the actual84/84rc0terminal (19:44:26UTC), advancing the earlier Wsource34/77prefix:82dependencies+Intrinsic9.734671CPU/9.698324wall andDihedral20.154170CPU/8.784143wall. Original35/42,17/21complete strata/144663modules;7ordinary original costs missing/18434module domain incomplete. Conditional source218.220065CPUh, marked57.546404h=26.3708%; nativeelapsed marked21.1685%. KnownHTsubtotal227.988537h only; each missing+1CPU-s adds4.117083h. Source support scenarios232.9–396.0CPUh; separate mixed-protocol check transfer15.9–35.2CPUh, not actual full checking/CI/guarantees. Wpaired31/42/14strata/dynamic13missing unchanged.


[Root0271](tmp/build-and-evaluate/step-0271-20261103T004041+0000/step-report.md) reads all9124retained rc1source records/stdout/stderr:4697unknowninterpreterdecl+4421missingnativeexternal=9118unavailabledecldiagnostics,4missingmoduledata,1compilerIRmissingcode,1LakeinterpreterIR.139of9118are not atsource line1, so no uniform import/phase claim.4successful qualification controls=3pinned sourcefiles+1Init import control, plus preserved failedmetadata-copy retry. Current3source bytes11197match fixed full archive; old duplicate failure-input source copies are absent, so no direct historical-byte recheck. Old600s/11.5GiB/olean-only versuscontrols300s/11.75GiB/3facets and unlogged per-open env trace prevent isolatedfacet/cost causal claims.9124do not become proofrejection or repairedpasses. Historical2488/163097source+10744dependencies remains partial; currentRamsey is a separate unfinished closure, not its denominator.


[Root0272](tmp/build-and-evaluate/step-0272-20261103T025723+0000/step-report.md) independently qualifies the actual NativeCodeAssembly original terminal01:09:45UTC:4.981634wall/7.020013CPU-s, not E-core prerequisite timing. Exact42frame gains only that ID, prior35costs unchanged. Current36/42,18/21complete strata/151888modules;6ordinary original costs missing/11209module domain incomplete. Conditional source235.032925CPUh, marked57.546404h=24.4844%; nativeelapsed203.778943h/marked19.6382%. KnownHTsubtotal235.032925h equals complete-stratum subtotal here because incompletecells have0observations, not whole-frame point/CI. Missing+1CPU-s each adds3.113611h. Source support scenarios238.7–362.1CPUh; mixed-protocol checking transfer16.2–32.2CPUh, not actual full checking/CI/guarantees. Source35scenarios retained ashistory. Paired31/42/14strata/11missing and dynamic13missing remain distinct.


[Root0273](tmp/build-and-evaluate/step-0273-20261103T031343+0000/step-report.md) independently qualifies corrected-v2 twelve full Barrier cells+one compound leaf process and3finite controls. Every fullclosure has4449unique accepts/identicalimports/counts/referenceIDset,425463entries/3595unsafe-partialexclusions/0contextfallback.8observedcohorts preserve237863ordinarychecks/3283925639allocationunitsandper-modulesums. P4→P8nativeCPU+74.986s,observer-bracketCPU+71.953s=95.9549%; brackets includeheartbeat/timingreads,notpurecycles. NaturalP8→mixed24wall+19.230s/CPU+458.725s,phasewindows4.629serial+7.410occupancy+3.386batchoutside+3.805other;notinstructioncausality. Naturalwall+6.36%on/+5.53%off; P-first+3.25%on/-0.37%off,1orderedobservation/cell,notCI/isolatedcausalA-B.50overlappinghelpers×9=450accepted/zeroobservedcountranges;9actual9160440Boleansidenticaltooriginal,extensionmetadata trusted. Mixedchecks/same-targetsolo-typemedianCPUratiosP2.301/E2.834,notcontrolledphysicalcore/frequencyorRC/cachecause. Old2524census/100helperpaneldenominatorsunchanged.


[Root0274](tmp/build-and-evaluate/step-0274-20261103T040607+0000/step-report.md) independently qualifies PhysicalFieldPopulationLimit actual03:32:26UTC original return3.805640wall/3.900684CPU-s. Fixed42frame adds onlythisID;prior36costs match.37/42originals,18/21complete strata/151888coveredmodules unchanged becauseTrackedTestBoundsstillmissing in9146cell.5ordinary costs missing/11209module domain incomplete. Conditional235.032925CPUh/marked24.4844%/elapsed19.6382% unchanged;KnownHTsubtotal239.987877hincludesoneincomplete-celloriginal,notfullestimate/CI. Eachmissing+1CPU-sadds1.843333h. Sourceobservedsupportscenarios242.2–315.2CPUh; separate mixed-protocolchecktransfer16.5–28.0CPUh,notmeasuredfullchecking/CI/guarantees. Stressmissingcheck3xnow242.0hdoesnotexceedsource315.2;explicit4x317.1hdoes. Paired31/42/14strata/11missing,dynamic13missingnotfilledbysource37.

[Root0275](tmp/build-and-evaluate/step-0275-20261103T061615+0000/step-report.md) independently qualifies the completed20-file Ramsey sample and the190-source stopped prefix. Source CPU22146.098430s is separate from815.679164sample checkerCPU-s; sampled source2271.356756s gives35.9115% pooled, individual P10/median/P90=35.5103/40.6179/48.8260%. Five38-file size strata,4uniform without-replacement samples each, seed20261103 exactly reproduced. Independent module-local prefix estimate7748.952058CPU-s/22146.098430=34.9901%;10000within-stratum percentile resamples29.4130–40.4104%, not an interval for dependency-order bias,254missing targets or whole streaming.190Construction files median4457B versus81652.5B in254unbuilt;24/180marked built. K10supplement excluded:356.442522/1725.133882CPU-s=20.6617%, no+kernel marker but finite ordinary-decide certificates. Imports trusted; process/import floor not kernel dominance. Historical whole-source2488/163097 and completeFalconer/Mathlib fractions unchanged. No newrootnative/Agent/queue or foreign edit.


[Root0276](tmp/build-and-evaluate/step-0276-20261103T062502+0000/step-report.md) independently qualifies TrackedTestBounds actual06:22:07UTC original return5.198824wall/5.412330CPU-s. Fixed42frame adds onlythisID;prior37rawcosts match W38publishedrows.38/42originals,19/21complete strata/161034coveredmodules;4ordinarycostsmissing/2063module domain(1.26489%)in2cells. Conditional246.863040CPUh/marked57.546404h=23.311065%, summednativeelapsed215.217114h/marked40.018606h=18.594528%. Differentcovered domain than18-cell24.4844%,notpopulationtimetrend/semanticphaseweight. KnownHTsubtotal246.863040h equalsthecomplete-stratumsubtotalonlybecausemissing2cellshave0observations;notfullpoint/CI. Missing+1CPU-s eachadds0.573056h. Sourceobservedsupportscenarios247.5–270.3CPUh; separatemixed-protocolchecktransfer16.8–24.0CPUh,notmeasuredfullchecking/CI/guarantees.10xordinarymaxsource480.621868h;missingcheck1x40.184493/2x63.560375/4x110.312141/12x297.319203h. Fourtimesno longer exceedsactualmaxsource270.238923;explicit12xstressdoes,notmeasurement. Paired31/42/14strata/11missing,dynamic13missingunchanged.


[Root0277](tmp/build-and-evaluate/step-0277-20261103T071354+0000/step-report.md) independently qualifies the original16 completed PMU matrix processes: each4449unique accepted modules,425463entries/3595upstream exclusions/0contextfallback; per-module237863checks/3283925639allocation units unchanged. Four ordinary4→8 pairings place91.70–99.15% extra nativeCPU in observer brackets including HB/timing reads, not pure C++cycles. Separate whole-command user PMUs: instructions+0.0396%,cycles+8.3107%,lockedloads+0.1171%,L3missloads+11.9794%,modified-line forwarding+46.4111%,RFOsnoopHITM+49.7555%,IPC1.833725→1.693693. Whole-command scope/fixedorder/pagecache/one counter cell preclude a unique RC/cache/frequency cause or removable stall share. Original sampled-worker metadata and separate owner counting-only repairs are not root-qualified causal attribution. Old0273's95.95% bracket observation remains separate.
Same38original source costs,19complete strata/161034domain: independent finite-population stratified variance32376792892.27296CPU-s², nominal95%t/Satterthwaite43.987706–449.738374CPUh around246.863040h,df2.130943. Two cells contribute62.4086%/27.6065% variance. n2/cell fragile, excludes incomplete strata/nonresponse/transfer/drift, notfullframeCI/bound. Missing-cost scenarios247.5–270.3source/16.8–24.0mixedtransfer unchanged, distinct uncertainties;4source/11paired/13dynamic gaps unchanged.


[Root0278](tmp/build-and-evaluate/step-0278-20261103T081624+0000/step-report.md) independently qualifies three supplemental counting-only attempts, not original16 missing-counter imputation. All3rc0/full4449same graph/425463entries/3595upstream exclusions/0fallback; per-module237863checks/3283925639units equal. Direct perf binary headers/READ records independently parsed and compared to fresh perf report-D plus existing CSV:1019/672/800READs,zero samples. P8r2 has9complete historical checkingTIDs, P4r3drain5has5complete, each7events×8expectedIDs unique. P4r2only1/5complete remains excluded. Valid checking-thread lifetime sums P4→P8:instructions+0.0372775%,cycles+10.5976603%,lockedloads+0.1082902%,L3missloads+36.4636325%,modifiedlineforwarding+43.0077816%,RFOsnoopHITM+42.1119891%,IPC1.833853090→1.658748204;observerCPU474.358940→537.001279s(+13.2056832%). PMUthreadlifetime notbracketgated; historicalTIDs notsimultaneousworkers. No uniqueRC/coherencecause/removablestallshare. P4parent+5.000239286s drain changes ancestry andtailtiming; no universalmetadatafix/ordinaryspeedup/CI. Original16/0273clock scopes unchanged.
Threecgroupsabsent/noOOM/stop,16emittedPIDbirthidentitiesretired;noM/P0–7/sharedlock/1100native/1740outer-afterlock/14GiBcharged+14GiBsampleRSSresponse. HWM3391748KiB/sample3465015296B/charged1196441600B separate, nothardRSS/fullMtreeclaim. Root3.106923s/56352KiB/E22–23/0native/Agent. Source38/42/19cells/4missing, nominal43.99–449.74CPUhdf2.13 and247.5–270.3source/16.8–24.0mixedtransfer assumptions unchanged;paired11/dynamic13/B/RQ2denominators unchanged.
