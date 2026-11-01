# Research status

Snapshot2026-11-01UTC. Current frontier, not a new experiment or live-process
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
| W probability frame |31/42draws,14/21complete strata/103468modules. Conditional marked-source CPU share17.1434%;11draws/59629modules still missing. No informative global share/totalCPU estimate. | [0238](tmp/build-and-evaluate/step-0238-20261101T061522+0000/step-report.md) |
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
[Root primary-source A/B/C verdict](novelty-20261101.md) and the actual M/W
handoffs downgrade generic mechanisms/methods; the paper now marks evidence
near principal claims and links experiments. A/B benefit remains unproven;
C is a measured finite engineering case with partial general/fullcost evidence.
M's six qualification controls do not complete stability claims. O's specific
cost-prediction report remains unavailable; its context/Falconer work is distinct.
No old capture is restarted or prepared result promoted.

[M v1 bounded matrix/root0253](tmp/build-and-evaluate/step-0253-20261101T185439+0000/step-report.md):768rows/16selected sources,0acceptance mismatches;16/256trace operational-label differences and128/128sync count changes.48/384frontend labels reflect the v1parser adapter defect. Not universal stability or novel deterministic budget. Correctedv2 is separate/in progress; paper remains0252.

## O prediction audit now complete
[Root0254](tmp/build-and-evaluate/step-0254-20261101T195608+0000/step-report.md) integrates O A audit/results: strong bounded-error/admission-benefit claim unsupported; native60s completes15/15/13, no sorting gain, upper trades coverage for fewer cuts. Same-corpus prior report overlaps the core cost/coverage intuition; no priority claim. Existing controlled characterization stays scoped. M v2 actual terminal is complete17phases; row audit pending, no restart. Paper still0252 until separate integration.
