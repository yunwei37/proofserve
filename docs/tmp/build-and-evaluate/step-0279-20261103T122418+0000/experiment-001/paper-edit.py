from pathlib import Path
import json,gzip,re
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
p=r/'docs/user-instruction.md';p.write_text(p.read_text()+'\n## 2026-11-03 UTC — verbatim cleanup and persistence correction request\n\n'+"【Claude 督促：磁盘归你的两块还没动】12:20 UTC 工作盘 83%（126 GiB 用了 104 GiB），近十小时约每小时涨 1 个百分点，几小时内就到 85%，各线都会停。昨天 18:50 UTC 我请你判断的两块还是原样：gpu-smt-native427-20261017-recovery 12.2 GiB，repository 26.5 GiB（其中 artifacts 约 22 GiB）。请这一轮就处理：\n1) 查这两块里哪些已被报告引用、哪些可再生、哪些是 Git 已跟踪的。已跟踪的不要动；没有引用也没入库的原始数据不要删，先写清楚再问我。可再生的、已被报告引用的中间产物直接清掉，记进 docs/cleanup 记录并推送。\n2) 目标是至少腾出 15 GiB，把使用率降到 75% 以下。\n另外，M 线已完成 24 次 plain 对照（7bdd161，3 次重复：8P CPU −14.13%、墙钟 −5.13%，1P CPU −2.02%）和第一组 PMU（16442dc，1P lock-load −98.30%）。写进论文时注意：这说明之前的额外 CPU 主要来自原型没标记持久对象，属于我们的方法修正，不是 Lean 或负载的性质；相关的旧并行数字（3.33×、1.52×、1.88×）要标明是未标记时的结果。"+'\n')
t=(r/'docs/paper/main.tex').read_text()
t=t.replace('seconds, 3.326-fold against the direct stock-API baseline','seconds, 3.326-fold for the historical unmarked prototype against the direct stock-API baseline')
t=t.replace('Eight workers reduce process-wall median 34.33\\%, or 1.523-fold, with','For the historical unmarked prototype, eight workers reduce process-wall\nmedian 34.33\\%, or 1.523-fold, with')
needle='Actual complete native-process pairs, one observation per arm.'
assert needle in t;t=t.replace(needle,'Historical unmarked prototype: actual complete native-process pairs, one observation per arm.')
# Qualify captions as well as prose, without altering numerical table bodies.
needle='BarrierData41 independent compiled-module replay, three ordered'
assert needle in t;t=t.replace(needle,'Historical unmarked prototype. BarrierData41 independent compiled-module replay, three ordered')
anchor='\\paragraph{Pooled certificates pass a broader native qualification.}'
assert t.count(anchor)==1
new=r"""
\paragraph{Persistent frontiers correct a prototype lifetime choice.}
\measured{\expref{"""+s.name.removeprefix('step-')+r"""}{0279}; complete 24-cell plain submatrix and first 1P counter pair.}
A matched intervention uses the same new executable with persistence disabled
or enabled, three ordered repetitions at each of 1/2/4/8 workers.
The enabled arm calls the official runtime persistence primitive on each
replay frontier before enqueueing workers, after joining the previous wave.
The original proof terms and mathematical kernel remain unchanged.
Each of the 24 complete processes accepts exactly the same 4,449 modules
and reproduces every module's check/allocation vector
(237,863 observed checks and 3,283,925,639 units).
The 13 qualification controls preserve positive outcomes and reject malformed
proofs or stale/duplicate coordination tokens.

At eight workers, median process CPU falls from 722.297 to 620.240 seconds
(14.13\%) and wall time from 314.839 to 298.675 seconds (5.13\%).
At one worker, median CPU falls from 640.427 to 627.502 seconds (2.02\%).
The three directly paired four-to-eight-worker contrasts remove a median
43.380 seconds, or 65.21\% of the extra process CPU
(range 61.80--71.76\%); positive residual growth remains.
These are observed repeats and ranges, not confidence intervals.
Most of this finite prototype's excess CPU therefore responds to correcting
its unmarked shared-object lifetime choice. The earlier negative scaling
must not be read as a property of Lean or of computational proofs.
Marking also touches the object graph and changes reclamation, so this
contrast is not an exact decomposition into reference-counting stall time.

The first one-worker whole-command PMU pair records retired lock-load
events falling from 5,800,924,030 to 98,707,245 (98.30\%), cycles falling
2.39\% and instructions increasing 1.195\%; all 14 event readings report
100\% running time. These are user-mode process-lifetime counters,
not hardware-gated checking intervals or three-repeat PMU estimates.
Locked-load events include runtime operations and do not directly measure
stall seconds. The one-worker coherence counts are near zero and do not
establish a multiworker contention effect.
The remaining planned counter cells are outside this admitted subset.

This is a method correction to our prototype. The historical 3.326-fold
Barrier pipeline, 1.523-fold mathematical closure and 1.882-fold Grid pair
remain measurements of their unmarked implementations and scopes.
The new Barrier ablation does not replace their different baselines or
provide corrected gains for those workloads.
Persistence retains objects by design; full-library retained-memory cost
and arbitrary extension-task safety remain unproved.
The new unsafe FFI call requires quiescence at its declared enqueue site;
the original mathematical kernel does not remove trust in the coordinator.
"""
t=t.replace(anchor,new+'\n'+anchor)
(r/'docs/paper/main.tex').write_text(t)
rel=str(s.relative_to(r));ref=rel.removeprefix('docs/')
entry=f'- [Persistence method correction and historical-cache reclamation](../{rel}/step-report.md): root0279 independently qualifies the complete24plain/first1Pstat subset and13controls; 8P CPU−14.13%/wall−5.13%, 1P CPU−2.02%, paired excessCPU reduction65.21%. Historical3.33×/1.52×/1.88× explicitly unmarked; overall32matrix remains separate. Exact cleanup manifests preserve tracked/raw data.\n\n'
p=r/'research/README.md';v=p.read_text().replace('root0278.','root0279.',1);v=v.replace('## Latest complete results\n\n','## Latest complete results\n\n'+entry);p.write_text(v)
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text().replace('root0278.','root0279.',1)
 note=f'\nRoot0279 user-directed correction: [complete24plain/first1Pstat qualification]({ref}/step-report.md). Same binary flag0/1, exact4449module graph/work; 8P CPU−14.13%/wall−5.13%, 1P CPU−2.02%; paired4→8 extraCPU reduced65.21% median, not an atomic-stall fraction. Prior scaling is an unmarked-prototype property; old3.33×/1.52×/1.88× labels retained. Full32stat/memory/stock-scope work not claimed complete. Historical-cache cleanup now executed with tracked paths protected and exact-byte retention; see [cleanup](cleanup-20261101.md).\n'
 v=v.replace('\n## ',note+'\n## ',1);p.write_text(v)
p=r/'docs/novelty-20261101.md';p.write_text(p.read_text()+f'\n## Root0279 — prototype method correction, not a Lean/novelty claim\n[Raw-qualified subset]({ref}/step-report.md): 24plain matched cells and first1Pcounter pair support a large prototype contribution from unmarked shared frontiers. Median paired4→8 extraCPU reduction65.21%; graph touches/reclamation also change. Old3.33×/1.52×/1.88× are explicitly historical unmarked implementations, not corrected gains or an intrinsic workload law. New unsafe quiescence obligation/retained-memory/generalization gaps remain.\n')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+f'\n## Root0279 — current user cleanup and persistence correction\n[Step]({ref}/step-report.md), [outer self-audit]({ref}/outer-audit.md). Independently read 24plain+2P1stat native raw,13controls, same4449module graph and per-module work;106actual emitted PID/birth identities retired. 8P medians722.297→620.240CPU-s/314.839→298.675wall-s;1P640.427→627.502CPU-s. Paired4→8 excessCPU removed43.380s/65.21% median; not exactRCstall time. P1lockloads5800924030→98707245,cycles−2.39%,instructions+1.195%,all14counters100%running. Full32not claimed. Old numeric table bodies unchanged; historical unmarked labels added. Cleanup manifests distinguish regenerated outputs, exact retained archive copies and byte-identical historical hardlinks; no tracked or unique raw deletion.\n')
base=f"""# Root step0279 — user-directed cache reclamation and prototype method correction
**自审; not independent review, research completion or venue acceptance.**

## EXPERIMENT_GATE
Existing BUILD_AND_EVALUATE. Current direct user request authorizes immediate cleanup of the two named historical roots and paper admission of the completed24plain/first1Pstat subset. No new native verifier/Agent/session/queue, no foreign implementation edits. Full32matrix is not claimed complete. Preserve fixed scientific contract and all previous failures.

### Node E1 — historical storage
Re-read prior0268 audit, current Git index (including nested source repositories), actual file types, process descriptors/maps/commands and block/link identities. Retired generated Lean caches, SDK4.27 libraries, ELF/Rust outputs are regenerable from retained sources/build logs. All tracked paths protected. Raw logs/sources/failed partial archives retained. Exact duplicate historical files preserve their paths by byte-equal hardlink consolidation; old mtimes and restoration instructions retained. Expanded intermediate copies may be removed only after streaming byte comparison to an existing retained ZIP/split-tar; malformed archives stay untouched. Exact per-path inventories/results linked below; actual totals added after completion. No root inference from concurrent df delta.

### Node E2 — actual independent qualification of the requested subset
Raw /workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103. All24plain cells plus only firstP1stat off/on pair; commands/results/stdout/stderr/memory/terminals read directly. Graph rebuilt against original v14 serial accept schema:4449exact module IDs/imports/constants;425463entries/3595unsafe-partial exclusions/0contextfallback. Per-module work matches original fixed reference,237863checks/3283925639units. All18990frontiers per process ST before mark, persistent only when enabled, otherwise activeMT after enqueue.
Same new executable botharms. Source persistence.c calls exact official one-argument lean_runtime_mark_persistent iff enabled; marker before enqueue/after prior-wave joins. Single-worker ready snapshot can overlap checking, not marking. Original mathematical Kernel.addDeclCore remains; unsafe quiescence/coordinator/FFI trusted, not arbitrary extension safety/TCB unchanged.
13separate finite controls:4positive exact650-module outcomes,4loose-bvar original-kernel rejects,4stale/duplicate coordination rejects,1official import probe. Not independent corpus coverage.
All39selected native attempts noM/P0–7/14GiBcharged+14GiB sampled ownRSS response/wait4complete/noOOM/noRSSstop/cgroupsabsent. 106actually emitted PID/birth identities checked retired; no fabricated checkingTID/launcher identities. Primary native1100s, outer1740afterblockinglock from frozen runner. Wall ends atwait4,before samplerjoin/cgroupdelete;queue excluded. Parent HWM/sample/charged maxima remain separate in CSVs; no hardRSS/whole16GiBlane-tree audit.
Root reduction20.701204s/54172KiB/E22–23,zero native reruns. Initial offline assert incorrectly equated off-arm post-no-op ST with post-enqueue MT: script/failure retained, then corrected by actual source chronology. Not a native failure or hidden work mismatch. Raw/source archive29520732B,5smallCSVs retained.

## WRITE_GATE
Actual RQ3 paragraph reports8P CPU−14.13%/wall−5.13%,1P CPU−2.02%;3paired4→8 excessCPU contrasts remove median43.380s/65.21%,range61.80–71.76%,residualpositive. This is our method correction/prototype contribution, not Lean/workload intrinsic limit. FirstP1PMU lockloads−98.30%,cycles−2.39%,instructions+1.195%;14readings100%running. Not gated kernel counters/PMUrepeats/atomic stall seconds. Mark changes graph touches and reclamation, retains objects; no full-library memory/service guarantee.
Historical3.326/1.523/1.882 numeric values preserved and explicitly labeled unmarked. No new table. Title/fullabstract/fourRQ/sectionhierarchy/fourdesignimplication bodies and all20oldtable bodies preserved. Canonical/status/plan/index/novelty/evaluation/userwords/cleanup synchronized. Source38/42 and existing RQ1/2/4 denominators unchanged.

## REVIEW_GATE — root self-review
Direction unchanged: characterize two cost regimes with explicit method/trust/coverage boundaries. Current user overrides prior wait-for-whole32 instruction only for named completed plain/P1subset. No cherry-picked incomplete plain group. Reject generic Lean law, exactRCstall fraction, corrected old gains, full32 completion and official mark primitive as arbitrary safety proof.
Storage decision uses verified retired/generated outputs or retained identical bytes; never deletes tracked or unique unreferenced raw data. No infrastructure/network/Tailscale/credential/UI/CronJob/runtime/resource/owner policy change. No false hot delivery/dispatch/consumption. A/Cgeneric novelty downgraded and globalphaseweights/software/axioms/cluster/nativebaseline/Envelopepair gaps remain.
"""
(s/'step-report.md').write_text(base)
(s/'outer-audit.md').write_text(base.replace('# Root step0279 — user-directed cache reclamation and prototype method correction','# Root step0279 outer audit — 自审')+'\n## Outer disposition\nAdmit only the independently qualified requested completed subset and its method correction. Existing owners continue their actual pending matrix/prerequisites/prefixes. Storage results require exact release accounting and final tracked-file check before persistence; compilation/all-page verification follows.\n')
print('EDITED',s)
