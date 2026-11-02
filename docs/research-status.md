# Research status

Snapshot2026-11-02UTC, root0267. [Paper](paper/main.tex) · [Plan](research-plan.md) ·
[Results](../research/README.md) · [Full history](evaluation.md) ·
[Novelty audit](novelty-20261101.md) · [Related work](background-related-work.md).
[Exact previous status](tmp/build-and-evaluate/step-0267-20261102T092013+0000/experiment-001/before-docs-research-status.md.gz).

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
| Source probability frame |32/42 draws;15/21 complete strata/104632modules. All9marked strata cover5848marked files. Conditional marked compiler CPU57.546/174.251h=33.025%; summed-elapsed share27.020%.10ordinary draws/58465modules in incomplete strata remain. No full-library CPU/global semantic weight. | [0263](tmp/build-and-evaluate/step-0263-20261102T040256+0000/step-report.md) |
| Whole-frame scenarios |32known+10ordinary missing assumed within observed support:207.8–630.8source/10.8–41.9modeledstream CPUh. O selected-closure CPU fractions transferred, not measured full checks, CI or guaranteed bounds. No-assumption upper unbounded. New LowBlock184.589CPU-s exceeds old marked max163.846. | [0263](tmp/build-and-evaluate/step-0263-20261102T040256+0000/step-report.md) |
| Target-only replay |31/31 accepted, trusted compiled imports, source632.590/replay272.695CPU-s; median per-module ratio0.451 (0.087–0.885).14paired strata140.852/54.906CPUh, nominal weak interval[0,0.9401], effectiveDF1.19. Separate from source32coverage/full closure. | [0260](tmp/build-and-evaluate/step-0260-20261102T020415+0000/step-report.md) |
| Native checking grain |29available random+2purposeful artifacts/34units;13original draws missing.12decision-shaped calls>=1CPU-s use10.09%total call CPU; available-case weights are conditional, not global. | [0234](tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |
| Four original O closures |Nat1330/NearPin3333/Grid3793/Amplitudes5083: complete check/source-work10.56/6.76/14.52/14.55%. Same5085-node source union/161reference blocks, overlapping dependencies and warm observations. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) |
| Large Falconer closure |13205source records;27checkpoint processes2043.585s/source22077.770s=9.2563%; complete graph/accept set and module-local reference union agree. Same-protocol Mathlib3segments91.279/622.379s=14.6662%. One capture each, trusted certified deltas, not uninterrupted/service/4GiB gain. | [0264](tmp/build-and-evaluate/step-0264-20261102T061224+0000/step-report.md) |
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

Source10/paired11/dynamic13 gaps differ; do not change one denominator with another.
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

Paper root0267:23pages/217908B,19oldtables/title/fullabstract/4RQ/sections/fourimplications unchanged;fullcompile/all-page self-review completed,0newrootnative/agent.

Direct finalized-number update [0265](tmp/build-and-evaluate/step-0265-20261102T065555+0000/step-report.md): RQ2 now places9.26%/10.56%/14.67% side by side with distinct closure/protocol boundaries and26exports/26restores included. RQ4 foregrounds2,524/2,524 zero-range targets, P95=max=0%, observed no-extra-count allowance only; module-source envelope0.0367–0.1385% and separate candidate maximum2.3339% remain different units. No guaranteed maxHB margin/future/zero-runtime claim.
