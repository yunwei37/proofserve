from pathlib import Path
import os,json,gzip,re,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-falconer-root-step.txt').read_text().strip());e=s/'experiment-001';j=json.loads((e/'reanalysis.json').read_text());ref=s.name.removeprefix('step-');root=f'tmp/build-and-evaluate/{s.name}/step-report.md'
p=r/'docs/paper/main.tex';t=p.read_text()
a=t.index(r'\partialev{\expref{0260-20261102T020415+0000}{0260}; source construction completed, first full check interrupted.}')
b=t.index(r'\paragraph{System-design implication.}',a)
new=r"""\paragraph{A large project completes through checked-prefix recovery.}
\measured{\expref{STEPNAME}{0264}; one complete segmented capture.}
The Falconer extension contains 13,205 modules: 2,461 generated modules and
10,744 dependencies. All have successful source-compiler records, including
5,077 exact common artifacts reused from the same capture and charged once
to this closure. Their summed native wall time is22,077.770s.
A chain of27 successful checker processes accepts the complete module set
in2,043.585s (2,038.444 wait4 CPU-s), or9.2563\% of source work.
All native module names and import edges match the planned closure.
The final event records800,218 input entries,4,451 upstream unsafe/partial
exclusions and19 module-local fallbacks.
Sixteen new module-local reference chunks cover8,128 modules; the remaining
5,077 retain exact-artifact qualification from the original capture.
The resulting reference and segmented acceptance sets both contain13,205 IDs.
This is finite positive-set agreement, not universal context or axiom closure.

The same checkpoint adapter and500-new-module quota checks the1,330-module
Mathlib control in three processes:91.279s versus622.379s of retained source
work, or14.6662\%. Each closure has one ordered capture with retained page
cache. The older unsegmented10.5551\% Mathlib result uses another adapter;
it is not a causal control for the new protocol. A smaller Falconer ratio
does not isolate AI authorship, tactics, dependency composition or import cost.

Each segment exports original-kernel-accepted declarations and audit metadata;
the next stock importer trusts that certified delta before checking new terms.
Startup, artifact reads, prefix restoration, snapshot writing and native exit
are within the summed process clocks. Queue wait, driver reduction, reference
qualification and producer/tool preparation are excluded.
The clock ends immediately after wait4, before collector/cgroup cleanup.
Five finite checkpoint cases span18 native processes, including two bad-proof
rejections in restore sequences. Serialized audit metadata and the adapter
remain trusted implementation code; arbitrary supplied snapshots are outside
this protocol. Frozen-input continuation is not a cross-candidate cache or
an uninterrupted single-process check.

\partialev{resource and generalization boundaries remain.}
The earlier full attempts both end at their1,500s limits:8,942 and9,040 complete
accept records, with unterminated output fragments. Their3,000.416s of failed
native work stay separate from the successful segmented cost.
Neither timeout is a mathematical rejection or a complete-set mismatch.
The source cells use11.875GiB (reused) or11.75GiB (new) charged caps;
the new checker uses11.75GiB and reaches10.368GiB wait4 RSS.
These exceed the listed O4GiB share and are not a qualified4GiB comparison.
Independent sampled RSS and exact native-child PID/birth records were not
emitted by this collector; absent cgroups and retired recorded controllers
do not establish a complete process-tree audit.
\missing{Repeated complete-project captures, causal component attribution
and whole axiom/context qualification.}

"""
new=new.replace('STEPNAME',ref);t=t[:a]+new+t[b:];p.write_text(t)
# Canonical summaries retain exact entry archives rather than repeated historical prose.
status=f"""# Research status

Snapshot2026-11-02UTC, root0264. [Paper](paper/main.tex) · [Plan](research-plan.md) ·
[Results](../research/README.md) · [Full history](evaluation.md) ·
[Novelty audit](novelty-20261101.md) · [Related work](background-related-work.md).
[Exact previous status]({root.replace('step-report.md','experiment-001/before-docs-research-status.md.gz')}).

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
| Large Falconer closure |13205source records;27checkpoint processes2043.585s/source22077.770s=9.2563%; complete graph/accept set and module-local reference union agree. Same-protocol Mathlib3segments91.279/622.379s=14.6662%. One capture each, trusted certified deltas, not uninterrupted/service/4GiB gain. | [0264]({root}) |
| Provenance composition |Grid4OAI nodes9.76%compiler work/52.70%replay-call wall; Amplitudes8nodes8.69/46.93%. Target components6.54/0.46/80.28/82.35% for Nat/NearPin/Grid/Amplitudes. Not CPU, global weights or causal import shares. | [0246](tmp/build-and-evaluate/step-0246-20261101T121151+0000/step-report.md) |
| Small Grid partitions |Both finite variants have no whole-path gain, despite some smaller kernel subclocks. Older sampled guard lacks independent charged-cap qualification. | [0234](tmp/build-and-evaluate/step-0234-20261101T030854+0000/step-report.md) |
| Barrier/Envelope helper cases |Barrier fragment pipeline3.326x/CPU+27.8%; small Envelope kernel6.292x but whole prepared-runtime1.096x/CPU+53.6%, one slower repeat. Different boundaries, not multiplicative. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md), [0236](tmp/build-and-evaluate/step-0236-20261101T051231+0000/step-report.md) |
| Repaired parallel stream |v14 Mathlib18cells/3fixed repeats:68.605→45.050s/8workers=1.523x, CPU+36.25%. Added coordinator/Cadapter trust remains. | [0241](tmp/build-and-evaluate/step-0241-20261101T080929+0000/step-report.md) |
| Complete computational pairs |Barrier4449modules1.558x/CPU+24.63%; Grid3793modules1.882x/+33.56% at uniform4. One ordered pair each; Grid controller repair gap preserved. | [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md) |
| Incremental targets |Finalv14 Grid8=4.024x/CPU+97.76%, Barrier8=5.297x/+48.62%; Envelope chunk8/strongdecl8=1.319x/+5.19%. Prefix/all-mode totals are not cold single-mode costs. | [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md), [0243](tmp/build-and-evaluate/step-0243-20261101T091434+0000/step-report.md) |
| B measured stages |2524local eligible helpers in3pinned modules,30288checks/22716thread comparisons:0allocation/verdict/diagnostic differences. Math source ranges0.0367/0.1385%, separate16-source panel max2.3339%/0pass changes. Not free runtime, sufficient maxHB padding or global/cross-machine guarantee. | [0262](tmp/build-and-evaluate/step-0262-20261102T030442+0000/step-report.md), [0261](tmp/build-and-evaluate/step-0261-20261102T023802+0000/step-report.md) |
| B cache/budgets |Private-input cache256verdict/diagnostic pairs stable,128sync vectors stable;100valid budget-monotonicity pairs no counterexample. Limited treatments, not universal semantics. Sync trace acceptance loss repeats one input; observer transparency not established. | [0257](tmp/build-and-evaluate/step-0257-20261101T215746+0000/step-report.md), [0255](tmp/build-and-evaluate/step-0255-20261101T200059+0000/step-report.md) |
| A prediction/admission |Grouped source forecast error and native CPU-budget policies do not establish bounded prediction or route benefit.29/42dynamic labels agree27/29conditionally; known-root upper admission has finite availability tradeoffs, not general service gain. | [0254](tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md), [0256](tmp/build-and-evaluate/step-0256-20261101T205729+0000/step-report.md) |

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
"""
(r/'docs/research-status.md').write_text(status)
plan=f"""# Research plan: two verification-cost regimes

Current frontier2026-11-02UTC, root0264. [Status](research-status.md) ·
[Evidence](evaluation.md) · [Results](../research/README.md) ·
[User words](user-instruction.md) · [Novelty](novelty-20261101.md).
[Exact previous plan]({root.replace('step-report.md','experiment-001/before-docs-research-plan.md.gz')}).

## Fixed questions and ownership

The user-selected characterization title/four RQ meanings/section hierarchy remain:
1. Where does checking work fall, and what are population-weighted costs?
2. Which preparation/import/production boundaries obstruct cheap checking?
3. Which original-kernel parallelism survives complete costs and trust boundaries?
4. What does verified establish about build, outcome and axiom/declaration closure?

User novelty and narrowed-B decisions authorize evidence-based claim strength,
not generic mechanism firstness. Missing results stay explicit. A/B/C are measured
cases/limits, not a replacement framing or venue acceptance.

W owns workloads/ and fixed-frame population costs; M owns chunked-kernel-check/,
parallel-stream-check/ and reproducible-verdict/; O owns decoupled-check/,
cost-prediction/ and engine/service paths. Root owns docs/paper and root records,
reads foreign implementation only, and starts no additional agent or queue.
Same gpu-smt-dev/phobos-vt/128GiB PVC; W16/M16/O4/root4GiB within40,
at most8cores/line, root E22–23 small work. Native P0–7/existing pcore.lock;
no Lean -M option. Data/toolchains/builds remain outside Git. Charged caps,
sampled RSS and wait4HWM are distinct. Historical O share deviations stay explicit.
Preserve live identities and real lock waiters; never infer a resume from old status.

## Completed branches: integrate, do not repeat

| Branch | Current completion boundary | Record |
|---|---|---|
| Fixed source census |163097OAI files and8529Mathlib files already scanned with common masking; default-root lexical gap retained. No repeat download/census. | [0231](tmp/build-and-evaluate/step-0231-20261101T001556+0000/step-report.md) |
| W source continuations |48job suffix complete; later19job attempt adds only LowBlock original. Source32/42/15strata,10missing. Dependencies/censors never receive original-draw weights. | [0263](tmp/build-and-evaluate/step-0263-20261102T040256+0000/step-report.md) |
| W target replay |31/31accepted,14paired strata; trusted imports. Keep its source denominator separate from source32coverage. | [0260](tmp/build-and-evaluate/step-0260-20261102T020415+0000/step-report.md) |
| Original O closures |Four complete overlapping closures/5085source union/161module-local reference blocks. | [0235](tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) |
| Falconer recovery |13205source/27successfulsegments, complete graph and reference union. Same-protocol Mathlib3segments also complete. Two full-check timeouts remain failures. No old checkpoint/reference queue restart. | [0264]({root}) |
| M parallel cases |Small-helper negatives, Barrier fragments, repairedMathlib18cells, full Barrier/Grid pairs and incremental targets completed with version-specific boundaries. | [0241](tmp/build-and-evaluate/step-0241-20261101T080929+0000/step-report.md), [0244](tmp/build-and-evaluate/step-0244-20261101T101651+0000/step-report.md) |
| B stage/cache/budget panels |v12census2524local helpers/30288checks complete; earlier24target/math-source/observer/cache/budget panels stay separate. Counts are not kernel polls/global candidate work. | [0262](tmp/build-and-evaluate/step-0262-20261102T030442+0000/step-report.md), [0261](tmp/build-and-evaluate/step-0261-20261102T023802+0000/step-report.md) |
| A limited policies |Native forecast/policy studies and grouped prediction errors complete; limited negative/tradeoff evidence, no bounded general predictor or route benefit. | [0254](tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md), [0256](tmp/build-and-evaluate/step-0256-20261101T205729+0000/step-report.md) |

## Evidence still needed within the four questions

| RQ | Unresolved evidence | Existing owner/integration boundary |
|---|---|---|
| RQ1 |10original source costs,11paired source/replay draws,13dynamic draws; native phase weights and uncertainty. | W/M; no -M/purposeful/dependency/zero-imputed substitute |
| RQ2 |Repeated/broader mathematics and released-software cases; causal preparation/production decomposition; arbitrary context and axiom qualification. | O/W; Falconer fills its selected closure only, not these global gaps |
| RQ3 |Matched native module-task comparison; complete selected-config Envelope baseline/pairs/repeats; general failure/budget/object-transfer and cluster evidence. | M; follow actual new plans/terminals, no root heavy native run |
| RQ4 |Whole declaration/axiom closure, observer/settings and cross-machine replication, released model-output software native evidence. | Existing W/M/O; no new generated candidates |

Same source32data preserve conditional marked CPU33.025% over15complete strata,
not a semantic phase/global fraction. Whole-frame207.8–630.8source/
10.8–41.9modeledstream CPUh retain missing-cost/selected-closure transfer
assumptions. The new point exceeded the old marked support maximum; scenarios
are neither CI nor guaranteed bounds. No-assumption upper remains unbounded.
Forecast/classification historical31-input panels do not become32-input experiments.

Kernel-helper allocation stability does not imply zero runtime overhead or a
sufficient maxHB margin. Math stored proofs are also stable in limited panels;
math kernel cells with only one eligible theorem do not establish8way concurrent
math checking. Source-count variation does not identify changed search paths.
The actual boundary is the measured stage/treatment, not universal regime law.

A checked-prefix chain starts empty and continues from its own certified deltas,
but stock loading trusts those deltas and private metadata. Whole acceptance
parity does not prove arbitrary snapshot safety, context transparency or axiom policy.
Do not merge segmented/uninterrupted ratios or treat unchanged mathematical kernel
rules as unchanged implementation TCB. Repaired M coordination has separate trust.

Bundled LeanChecker launches module-local tasks without a checked-import barrier.
A strict dependency-DAG span is a diagnostic, not its upper bound.
[Source audit](tmp/build-and-evaluate/step-0247-20261101T131749+0000/step-report.md).
Incremental and complete-configuration ratios have different clocks; never multiply
them, pool protocol versions or impute a full Envelope pair from a timeout.

## Next root action and review routing

Integrate real new owner terminals, or choose independent in-scope analysis only
when it can change a paper decision. Protect healthy work and genuine waiters.
No minute polling, duplicate controls, CPU-oracle extension, oldqueue restoration,
new runtime budget, agent or schedule. Completed Falconer/source19/v12points
are not pending despite stale owner README text.
The paper remains an unfinished characterization with explicit missing evidence;
self-review is not independent audit or submission acceptance.
"""
(r/'docs/research-plan.md').write_text(plan)
idx=f"""# Research result index

Current2026-11-02UTC, root0264. [Status](../docs/research-status.md) ·
[Plan](../docs/research-plan.md) · [Paper](../docs/paper/main.tex) ·
[Full history](../docs/evaluation.md).
[Exact previous index](../docs/{root.replace('step-report.md','experiment-001/before-research-README.md.gz')}).
Reports identify input, version, clock and trust boundary. Reviews are **自审**;
preparation, queues, controls and code are not performance or general acceptance.

## Existing research directories

| Directory | Qualified work/boundary | Reports/raw location |
|---|---|---|
| [mechanisms-2026-10-30](mechanisms-2026-10-30/README.md) |Historical tactic/profile/resource studies. Old-M diagnostic data are not current noMcost/acceptance evidence. |[Prior work](mechanisms-2026-10-30/prior-work.md); PVC captures/mechanisms-2026-10-30/ |
| [profile-2026-10-31](profile-2026-10-31/systime/final/README.md) |90guard-calibration cells/3modules; guard/noM ratios2.03/1.61/1.01, matching outputs at passing points, not failure equivalence. |[Startup/replay](profile-2026-10-31/startup-replay/README.md); PVC captures/profile-2026-10-31/ |
| [decoupled-check](decoupled-check/README.md) |Four original overlapping closures/5085source union. New Falconer13205-module segmented chain9.2563%source wall, Mathlib same protocol14.6662%, complete module-local reference union. Added snapshot/metadata trust, Oshare deviations, two prior timeouts retained. |[Original results](decoupled-check/results.md), [Falconer](decoupled-check/falconer-final-analysis.md); PVC captures/decoupled-check-20261031/scale-study/falconer-project-20261101/ |
| [chunked-kernel-check](chunked-kernel-check/README.md) |31artifact grain panel/13randommissing; small Grid whole-path negatives. Barrier fragment pipeline3.326x and small Envelope prepared-runtime1.096x are different scopes. |[Grain](chunked-kernel-check/step-006-report.md), [Barrier](chunked-kernel-check/parallel-result.md), [Envelope](chunked-kernel-check/envelope-result.md); PVC captures/chunked-kernel-check/ |
| [parallel-stream-check](parallel-stream-check/README.md) |Defectivev4context mismatch preserved. Repairedv14Mathlib1.523x/8workers; full Barrier/Grid4worker pairs1.558/1.882x. Envelope full original reference times out. |[Mathlib](parallel-stream-check/v14-math-results.md), [Full Barrier](parallel-stream-check/full-barrier-results.md), [Full Grid](parallel-stream-check/full-grid-results.md); PVC captures/parallel-stream-check-v4,v10,v12,v14/ |
| [reproducible-verdict](reproducible-verdict/README.md) |Observer-sensitive sync adapter, source counters and private-cache/budget controls. Root-qualifiedv12census2524local helpers,30288checks/22716stable thread pairs; no globalbudget/crossmachine guarantee. OwnerREADME pending text is stale. |[v11](reproducible-verdict/module-results-v11/results.md), [cache/coexecution](reproducible-verdict/cache-and-coexecution-results.md); PVC captures/reproducible-verdict-v*/ |
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
| [0264](../docs/{root}) |Full Falconer source/segmented/refset audit and same-protocol Mathlib; raw source/protocol/failures frozen, no root native run or new scientific contract. |

[Novelty audit](../docs/novelty-20261101.md) covers prior Isabelle/Coq/Lean checking,
Mathlib, services, SATzilla and the closest same-corpus technical report.
A/Bgeneric mechanisms and Cgeneral decomposition/composition have precedents;
finite controlled boundaries and limits are the current empirical increment.
"""
(r/'research/README.md').write_text(idx)
f=j['falconer'];m=j['mathlib'];ids=len(j['recorded_PID_birth_retired']);pidonly=len(j['PID_only_records_not_birth_audited'])
record=f"""
## Root0264 — selected large-project recovery completed, not a new general mechanism

[Root report]({root}).27successful Falconer segments accept13205unique modules
with complete native import graph;16new original module-local reference chunks
plus5077exact previously qualified common artifacts cover the same set.
Source13205records/8128new+5077reused:22077.770248wall/
32292.603807CPU-s. Falconer2043.585476wall/2038.443942CPU-s, ratio9.2563%.
Same checkpoint protocol/quota500 Mathlib3segments91.279127/622.379412sourcewall
=14.6662%, one ordered capture each; older unsegmented10.5551% is another adapter.
Two full-check timeouts remain3000.415754failedwall, excluded from successful
protocol cost, not hidden or mathematical rejections. Queue/control/qualification
and collector cleanup are separate from timed native intervals.
Base starts empty; later stock imports trust this run's own certified deltas and
unsafe-cast private metadata. Not arbitrary-snapshot safety, general context/
axiomclosure, service performance or a first checkpoint mechanism.
Oshare deviation remains:sourcecaps11.875/11.75GiB/check11.75,wait4checkRSS10.368GiB.
IndependentRSS sampling/native-child PIDbirth not emitted;{ids}recorded controller
identities retire,{pidonly}PID-only submission records are not birth-audited.
Source32/paired31/dynamic13missing and B2524scope remain unchanged.
"""
for n in ['docs/novelty-20261101.md','docs/evaluation.md']:
 p=r/n;p.write_text(p.read_text()+record)
report=f"""# Step0264: complete selected Falconer recovery and source-cost comparison
Date2026-11-02UTC. All reviews are **自审**, not independent audit or venue acceptance.

## Scientific contract and gate entry
User words, current novelty/status/plan/index, root0263step+outer reports and
questions-for-author were read. The newest direct B/W decision remains implemented.
Chosen parent is RQ2's missing complete Falconer closure/reference/ratio.
It changes a load-bearing missing result, not framing/title/abstract/RQ meaning.
Central position remains: unchanged certificates range from cheap witness checks
to replayed computation; full costs depend on the checked scope and trust boundary.
No new agent/native Lean session/owner implementation/queue/limits/infra/schedule.
User no-agent policy overrides the skill's fresh-review delegation; outer review
here is explicitly root self-review. No iter-refine-ideas/full writing/milestone review.

## EXPERIMENT_GATE — collect an actual completed owner run
New plan/preflight/native execution skipped: the existing O finite protocol has
real terminal data; recreating it would duplicate completed work. Root performs
offline result review on E22–23, preserving native artifacts and original failures.
Inputs: O fa295de, [final report](../../../.. /research/decoupled-check/falconer-final-analysis.md)
and raw /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/
scale-study/falconer-project-20261101, especially checkpoint-recheck-v2/
and bounded-recheck-v1/. Source/native/protocol/failed raw frozen in
[experiment-001](experiment-001/), no build trees/Lean objects copied into Git.

### Node: complete source and graph qualification
Re-read all13205successful native source records/commands/stdout/stderr:
8128new,5077same-capture reused; noM/j8/P0–7 and absentcgroups, no kernelOOM.
Source wall{j['source_wall_s']:.9f}s/CPU{j['source_cpu_s']:.6f}s;
maxwait4RSS{j['source_maxRSS_KiB']}KiB/charged{j['source_charged_peak_B']}B.
Same-capture common artifacts are checked by25377actual same-device/inode/size
links. All13205current inputoleans exist. Current5077reused ilean/C companions
are absent, while8128new counterparts exist; root neither infers when they
disappeared nor claims all old outputs are still retained. Native successful
source clocks/flags and typed replay inputs remain; no foreign cleanup/regeneration.
2461selected AI sources/9279240bytes match the existing4eaee875full archive
byte-for-byte,17.403s selected comparison. The familiar13952-file extraction is
partial and is not a source-availability oracle. No download/whole lexical census.

All27segment rawstdout accept IDs form exactly13205unique planned modules.
Native imports match every planned edge; root recomputes reachability from roots.
Final totals800218entries/4451unsafe-partial exclusions/19module-local fallbacks.
Prepared declaration counts were null for2461AI modules and differed from native
outputs in3dependencies (27→28,251→253,279→281). These metadata do not claim
unchanged cached declaration identity; current raw counts are used instead.
The graph qualification concerns module IDs/import edges, not that stale count field.

### Node: checkpoint chain and reference comparison
Each of26prefix snapshots follows the exact prior terminal/snapshot name, quota500,
with disjoint newaccepts; final27th has205 andcomplete. Required snapshots exist.
Falconer wall{f['wall_s']:.9f}/wait4CPU{f['cpu_s']:.6f}s.
Ratio to successful sourcewall{j['falconer_ratio']*100:.9f}%.
Mathlib1330same-protocol3segments wall{m['wall_s']:.9f}/CPU{m['cpu_s']:.6f}s,
sourcewall{j['math_source_wall_s']:.9f},ratio{j['math_ratio']*100:.9f}%.
One ordered capture/closure, retained cache; not independent repeats or CIs.
OldunsegmentedMathlib10.5551% is not pooled or treated as a causal control.

Reference8,128new modules from16fullrc0one-mode chunks plus5,077exact common IDs
reconstructed from all161original successful raw reference blocks gives13205.
Complete sets agree; no timeout prefix or malformed fragment is accepted.
The common reference is reused same-capture evidence, not13205fresh oracle calls.

CheckpointAudit source uses originalKernel.Environment.replay, original
saveModuleData/importModules, structural typed comparisons and module-local
fallbacks. It begins empty but restored certified deltas and unsafeCast audit
metadata are trusted inputs. This is not standalone hostile-snapshot checking,
unchanged implementationTCB, arbitrary context transparency or whole axioms.
Five cases/18nativecontrol parts include16rc0+2intentionalbadproof rc1.
Oldercontrolterminalschema omits previous_snapshot/per-call environment;
do not invent those fields. Snapshot sequences/source protocol and actual
bad-proof rejection remain finite control evidence, not a general proof.

### Node: failure, clock and resource limits
Fullattempts remain rc124/1500.210998416s with8942fullaccepts+75bytefragment,
and1500.204755224s with9040fullaccepts+167bytefragment.
Failed nativewall3000.415753640s; successful+failedwall5044.001229439s,
not the successful protocol cost or a service latency metric.
One recoveredsourcefault0.053097s/startupcompiler failures are separately frozen.
No mathematical rejection or accepted-set mismatch follows from these timeouts.

native_project.py starts the timer immediately before Popen and ends afterwait4.
Includes startup/reads/kernel/native JSON/restore/snapshot/output/normal exit;
excludes queuewait, preparation, controls/reference qualification, driver reduction,
sampler-free collector bookkeeping/cgroup removal afterwait4.
Sourceclocks includeimports/elaboration/tactics/kernel/emission, not Lake makespan
or toolchain bootstrap. No isolated import/tactic causal share is inferred.

Sourcecaps:5077at12750684160B(11.875GiB),8128at12616466432B(11.75GiB);
newcheckercap11.75GiB. Falconer wait4HWM{f['maxRSS_KiB']}KiB,
chargedpeak{f['charged_peak_B']}B; no independentRSS samples/native-childPIDbirth
were emitted. ListedOshare is4GiB: deviation remains, not retroactive compliance.
All selected performance cgroups absent. {ids}actually recorded PID/birth pairs
retired;{pidonly}PID-only submit records are preserved without birth audit.
No fake missing child identity or complete process-tree audit.

### Invalid/offline re-entry history
Root first asserted prepared counts equal native counts; retained failure and
corrected the criterion to the declared ID/import graph while recording counts.
Next required all current ilean/C paths, then used an incomplete source extraction,
then indexed an older absent control field. Each read-only failure is retained;
no data modified, fabricated, or Lean rerun. Final reducer and exact source-byte
comparison scripts are preserved. Root analysis{j['root_analysis_seconds']:.3f}s,
maxRSS{j['root_analysis_maxrss_kib']}KiB. Main rawfreeze{j['raw_freeze_bytes']}B.
Transition: accept the finite complete cost/set result with above limits; WRITE.

## WRITE_GATE — targeted RQ2 update
Replace only the stale Falconer pending paragraph with complete segmented result,
same-protocolMathlib comparison, native clock, trust/resource/failure limits.
Title/fullabstract/fourRQ/sections/four design implications/17table bodies unchanged.
No new table, generic mechanism, source32denominator change or Bscope upgrade.
Full compile/all-page visual review follow. Prior/current documents are losslessly
archived; status/plan/index are compressed to current-frontier summaries, while
evaluation/novelty preserve detailed history. No orphan old pending queue remains.
Transition: REVIEW after complete paper verification.

## REVIEW_GATE — contract audit, meta-review and routing
Root self-review checks raw IDs, graph,sourceclocks/referencecoverage and scopes.
Direction: result fills selected RQ2case, no contract/story/novelty change.
Waste: no native rerun/restarts; source lookup failures corrected offline and kept.
Maintenance: canonical histories outgrew gate-entry summaries; exact parents
archived, concise current summaries retain ownership, resource deviations, failures,
missing denominators and all result links. No new rule/skill/runtime layer.
Ranked open objections: globalphaseweights/source10+paired11+dynamic13nonresponse;
causal/repeated/crossmachine scopes; whole axioms/software coverage; native
module-task competing baseline; full Envelope single-mode pair; cluster/failure
semantics. They do not invalidate this explicitly scoped capture.
Next action follows actual new owner plans/terminals or paper-value offline
analysis, never automatic restoration of completed Falconer/source19/v12queues.
"""
# Fix relative link directly; no opaque path substitutions.
report=report.replace('../../../.. /research/','../../../../research/')
(s/'step-report.md').write_text(report)
outer=f"""# Step0264 outer audit — 自审
Date2026-11-02UTC. Root performed implementation-source inspection and offline
result reduction, so this is not a fresh independent reviewer or venue decision.

## EXPERIMENT audit
Question is the existing missing full Falconer RQ2case. Exact13205IDs/import
edges,27successful chain terminals and complete module-local reference union
support the limited result. Source denominator uses13205actualrc0records,
including5077same-capture common nodes; it is summed compiler work, not a
parallel build or new independently resampled workload.
Root byte-compared2461selected sources to the fixed archive; incomplete local
extraction and prepared counts did not replace native evidence.
Prepared2461null/3different counts are disclosed rather than silently enforced
as byteidentity. Typed inputoleans persist; oldilean/Cavailability gap is recorded.

## Cost/trust/failure audit
Native source{j['source_wall_s']:.9f}s/check{f['wall_s']:.9f}s
supports9.2563%only for the segmented protocol. Mathlib14.6662%uses the
same adapter/quota but old same-capture source costs and one ordered observation.
Neither gives causality, a CI, service throughput, global cost or a new mechanism.
Two full1500s timeouts retain completeaccept prefixes and fragments; they do not
fill missing IDs or vanish from recovery accounting.
Restored deltas/unsafeCastmetadata remain trusted glue. Positive-set parity and
finite restored bad-proof rejections do not prove arbitrary context/object safety.
O4share was exceeded; absent independentRSS/native-childidentities prohibit
clean aggregate-resource/fullidentity claims despite retired recorded controllers
and empty cgroups. Existing maximum caps do not authorize a changed lane budget.

## WRITE/REVIEW audit and scientific authority
The new direct user B/Wdecisions remain: counted stage limits, not free general
determinism or proven budgetpadding; Wsource32/replay31/dynamicpanel differ.
Actual RQ2text is updated, title/abstract/RQ meanings/section hierarchy/17tables/
fourimplications stay fixed. Full paper compilation/staticreview must complete.
Old canonical text is losslessly archived, not history rewritten or raw removed.
Only root paths change. No new native/agent, foreign edit, infrastructure or
scheduler. Skill-required independent/fresh delegation is not performed because
the user expressly prohibits new agents; both reports mark self-review.
Outer decision: finite result admitted with stated protocol/resource/trust limits.
The paper as a whole is not complete; ranked global/causal/software/axiom/cluster/
baseline gaps remain. No genericA/B/C novelty or OSDI acceptance is promoted.
"""
(s/'outer-audit.md').write_text(outer)
print('EDITED',s,'canonical_lines',{n:len((r/n).read_text().splitlines())for n in ['docs/research-status.md','docs/research-plan.md','research/README.md']})
