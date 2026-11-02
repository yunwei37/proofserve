from pathlib import Path
import os,subprocess,json,csv,gzip,tarfile,time,resource,math
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/('docs/tmp/build-and-evaluate/step-0265-'+stamp);e=s/'experiment-001';e.mkdir(parents=True);Path('/workspaces/.agent-state/gpu-smt-final-numbers-root-step.txt').write_text(str(s)+'\n')
for n in ['docs/user-instruction.md','docs/paper/main.tex','docs/paper/main.pdf','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md']:
 (e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
began=time.monotonic();m=r/'research/reproducible-verdict/census-results-v12';o=r/'research/decoupled-check'
targets=list(csv.DictReader((m/'target-heartbeats.csv').open()));assert len(targets)==2524 and len({(x['module'],x['target'])for x in targets})==2524
ranges=[]
for x in targets:
 assert int(x['observations'])==12
 counts=[int(x[k])for k in ['min_raw_HB','max_raw_HB','j1_min_raw_HB','j1_max_raw_HB','j2_min_raw_HB','j2_max_raw_HB','j4_min_raw_HB','j4_max_raw_HB','j8_min_raw_HB','j8_max_raw_HB']]
 assert len(set(counts))==1 and counts[0]>0
 v=100*(max(counts)-min(counts))/min(counts);assert v==float(x['relative_range_pct']);ranges.append(v)
assert all(v==0 for v in ranges)
p95=sorted(ranges)[math.ceil(.95*len(ranges))-1];assert p95==max(ranges)==0
distribution=list(csv.DictReader((m/'distribution.csv').open()));assert all(float(x['p95_relative_range_pct'])==float(x['max_relative_range_pct'])==0 for x in distribution)
table=list(csv.DictReader((o/'falconer-paper-table.csv').open()));assert len(table)==3
for x in table:assert abs(float(x['check_wall_sum_s'])/float(x['source_wall_sum_s'])-float(x['check_over_source']))<1e-12
raw=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101/checkpoint-recheck-v2')
terms=[json.loads(p.read_text())for p in sorted(raw.glob('segment-*-terminal.json'))];assert len(terms)==27
exports=sum(v['snapshot']is not None for v in terms);restores=sum(v['previous_snapshot']is not None for v in terms);assert exports==restores==26
# Freeze final owner reports/tables and link earlier raw-qualified captures; do not rerun native Lean.
files=[m/'results.md',m/'target-heartbeats.csv',m/'distribution.csv',m/'summary.json',o/'falconer-paper-result.md',o/'falconer-paper-table.csv',o/'falconer-paper-evidence.json']
with tarfile.open(e/'published-final-panels-and-comparison.tar.gz','w:gz')as tf:
 for p in files:tf.add(p,arcname=str(p.relative_to(r)))
j=dict(targets=len(targets),observations=sum(int(x['observations'])for x in targets),pairs=2524*3*3,p95_relative_range_pct=p95,max_relative_range_pct=max(ranges),zero_range_targets=sum(v==0 for v in ranges),three_ratio_rows=table,snapshot_exports=exports,snapshot_restores=restores,root_analysis_seconds=time.monotonic()-began,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,native_reruns=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
# Direct user words are appended verbatim, never rewritten.
userwords="【Claude 通知：两个关键数字定稿了，请写进论文】用户要求定时盯着、每条线结束立即派活，所以这轮直接给你可用的结果。\n1) M 线 a0a2916：2,524/2,524 个计算目标，1/2/4/8 线程 × 3 次重复 = 30,288 次检查，心跳波动**全部为 0%**，P95 和最大值都是 0；22,716 个配对判定和诊断全部一致。这基本坐实了\"计算区间的确定性是免费的\"。边界：仍是实测包络，不能保证未来运行；但没有一个反例。\n2) O 线 395a8b3（research/decoupled-check/falconer-paper-result.md）：Falconer 13,205 模块、27 段，检查 2,043.59 s vs 构建 22,077.77 s = **9.26%**，接受集合与逐模块复核一致，26 次快照导出和 26 次恢复已计入。同一文档还给了另两个对照：历史 Mathlib 10.56%、同检查点协议 14.67%。请把三个数字并列，并写清比较边界（不同闭包、不同协议，不能相乘或合成一个平均值）。\n请在论文里做三件事：\n- 把 RQ4 改成收窄后的确定性表述，用 2,524 个目标 0 波动这个证据，写\"计算区间的确定性不需要额外预算，数学区间的实测波动上限约 2.33%（模块级 0.03–0.14%）\"。\n- RQ2 用 9.26% / 10.56% / 14.67% 三个数，说明 AI 生成库和 Mathlib 在数学区间上量级一致，验证远低于构建。\n- 更新 research/README.md 索引，加上 Falconer 结果和 2,524 目标普查这两个条目（O 线给了可直接采用的条目文本，但没改共享索引）。\n改完 commit 并 push。"
p=r/'docs/user-instruction.md';u=p.read_text()
if userwords not in u:p.write_text(u+'\n\n## 2026-11-02 UTC — verbatim finalized numbers and paper request\n\n'+userwords+'\n')
ref=s.name.removeprefix('step-');p=r/'docs/paper/main.tex';t=p.read_text()
# Explicit parallel comparison with the already measured historical protocol.
anchor='The same checkpoint adapter and 500-new-module quota checks the 1,330-module'
a=t.index(anchor)
new=r"""\begin{table}[t]
\centering\small
\setlength{\tabcolsep}{2pt}
\begin{tabular}{lrr}
\toprule
Closure / checking protocol & Check / source (s) & Ratio\\
\midrule
Falconer, checkpoints & 2,043.59 / 22,077.77 & 9.26\%\\
Mathlib, historical stream & 65.69 / 622.38 & 10.56\%\\
Mathlib, checkpoints & 91.28 / 622.38 & 14.67\%\\
\bottomrule
\end{tabular}
\caption{\measured{\expref{STEPNAME}{0265}} Three mathematical-closure
observations. Falconer has13,205 modules/27 processes; both Mathlib Nat.Basic
rows have1,330 modules, with one and three processes respectively.
Each ratio uses its own complete checking/source wall sums.}
\label{tab:mathclosureratios}
\end{table}

Table~\ref{tab:mathclosureratios} places the three observed ratios side by side:
9.26\% for the selected AI-generated Falconer library,10.56\% for the
historical Mathlib stream and14.67\% for checkpointed Mathlib.
In these mathematical closures, checking is of the same order---roughly
one tenth of construction---and substantially below the source-compiler work.
The closures and protocols differ; these ratios are not multiplied or
averaged into one gain or a population estimate.
"""
t=t[:a]+new.replace('STEPNAME',ref)+t[a:]
t=t.replace('Startup, artifact reads, prefix restoration, snapshot writing and native exit\nare within the summed process clocks.','Startup, artifact reads, all26 snapshot exports and26 prefix restores,\nand native exit are within the2,043.59s summed process clock.\nSnapshot write-return costs follow normal page-cache semantics; isolated\nsnapshot seconds and physical-flush durability latency were not measured.')
# Make the no-extra-count claim prominent and explicitly scoped to observed units.
a=t.index(r'\paragraph{Reproducibility requirements differ across measured stages.}')
b=t.index(r'\partialev{observed count allowances; required budget margins remain unmeasured.}',a)
rq4=r"""\paragraph{Measured kernel recomputation needs no extra count allowance.}
\measured{\expref{STEPNAME}{0265}; the qualified three-module census.}
Across all2,524 eligible computational targets, allocation-heartbeat variation
is0\% for every target under1/2/4/8 workers and three repeats:
30,288 accepted checks, with P95=0\% and maximum=0\%.
All22,716 matched comparisons preserve counts, verdicts and diagnostics;
there is no nonzero case in this census.
For these measured computation-stage units, determinism therefore needs
no extra allocation-count budget to cover the observed worker/repeat envelope.
This is the bounded empirical meaning of determinism without an extra budget
here, not a guarantee for future runs, all computational proofs or zero runtime
overhead.

The mathematical source panels instead have an observed maximum span of
2.333868\% (about2.33\%) over the separate16-source concurrent-candidate panel,
with83/192 changed theorem-command counts (84/192 full command vectors)
and no acceptance changes.
The two full-source modules have spans0.036739\% and0.138453\%,
a coarse0.03--0.14\% module-level envelope, with identical judgments.
These different units and inputs are not pooled.
All percentages use the observed maximum relative to the observed minimum;
they bound only the measured runs, not future executions.

"""
t=t[:a]+rq4.replace('STEPNAME',ref)+t[b:]
t=t.replace("All22,716 worker-one versus higher-worker comparisons preserve allocation\ncounts, verdicts and diagnostics; each target's range across all12\nobservations is zero.","All22,716 worker-one versus higher-worker comparisons preserve allocation\ncounts, verdicts and diagnostics; each target's range across all12\nobservations is zero. Across targets, both the nearest-rank P95 and maximum\nrelative range are0\\%; all2,524/2,524 targets have zero observed variation.")
# Correct spacing only in the newly written local passages.
for x,y in {'has13,205':'has 13,205','have1,330':'have 1,330','library,10.56':'library, 10.56','and14.67':'and 14.67','all26':'all 26','and26':'and 26','the2,043.59s':'the 2,043.59s','all2,524':'all 2,524','is0\\%':'is 0\\%','under1/2/4/8':'under 1/2/4/8','All22,716':'All 22,716','about2.33':'about 2.33','separate16-source':'separate 16-source','with83/192':'with 83/192','spans0.036739':'spans 0.036739','a coarse0.03':'a coarse 0.03','are0\\%':'are 0\\%'}.items():t=t.replace(x,y)
p.write_text(t)
# Shared index: directly link both final owner results and remove the now-stale pending warning.
p=r/'research/README.md';idx=p.read_text()
idx=idx.replace('Current2026-11-02UTC, root0264.','Current2026-11-02UTC, root0265.',1)
idx=idx.replace('OwnerREADME pending text is stale.','',1)
idx=idx.replace('[v11](reproducible-verdict/module-results-v11/results.md),','[Completed2,524-target census](reproducible-verdict/census-results-v12/results.md), [v11](reproducible-verdict/module-results-v11/results.md),',1)
idx=idx.replace('[Falconer](decoupled-check/falconer-final-analysis.md)','[Falconer final paper result](decoupled-check/falconer-paper-result.md)',1)
marker='## Existing research directories'
latest="""## Latest complete results

- [Falconer mathematical closure](decoupled-check/falconer-paper-result.md):
  13,205accepted modules/27checkpointed processes;2,043.59/22,077.77s=9.26%.
  All26exports/26restores included; module-local acceptance set agrees.
  Historical Mathlib10.56% and same-checkpoint Mathlib14.67% are separate
  closure/protocol observations, never multiplied or averaged into one gain.
- [2,524-target computation census](reproducible-verdict/census-results-v12/results.md):
  1/2/4/8actual workers ×3repeats,30,288acceptedchecks/22,716stable pairs;
  every target has0%allocation variation, P95=maximum=0%.
  No extra count allowance covers these observed runs; future runs, maxHB
  threshold guarantees and zero runtime overhead are not established.

"""
idx=idx.replace(marker,latest+marker,1)
idx+=f'\n[Root0265](../docs/tmp/build-and-evaluate/{s.name}/step-report.md) implements the direct finalized-number request; prior raw qualifications remain0262/0264. No native rerun or generic mechanism firstness.\n';p.write_text(idx)
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;text=p.read_text();text=text.replace('root0264','root0265')
 text+=f'\nDirect finalized-number update [0265](tmp/build-and-evaluate/{s.name}/step-report.md): RQ2 now places9.26%/10.56%/14.67% side by side with distinct closure/protocol boundaries and26exports/26restores included. RQ4 foregrounds2,524/2,524 zero-range targets, P95=max=0%, observed no-extra-count allowance only; module-source envelope0.0367–0.1385% and separate candidate maximum2.3339% remain different units. No guaranteed maxHB margin/future/zero-runtime claim.\n';p.write_text(text)
note=f"""
## Root0265 — direct finalized-number wording and index update
[Step](tmp/build-and-evaluate/{s.name}/step-report.md). Owner commitsa0a2916/395a8b3
restate already raw-qualified results. Root rechecks all2524published count ranges,
12observations each, nearest-rankP95=max=0%,30288checks/22716pairs.
RQ4 says no extra allocation-count allowance for these observed prepared kernel
runs; it does not guarantee future execution or a sufficient native maxHB margin.
Math source modules0.036739/0.138453% (coarse0.03–0.14% envelope) and a separate
16-source panel maximum2.333868% are not pooled or causal tactic-path evidence.
RQ2adds a three-row9.26%/10.56%/14.67% comparison, differentclosures/protocols,
not multiplied/averaged;26exports/26restores already inside2043.59s.
Index directly links both final owner reports. No new native experiment, generic
determinism/checkpoint mechanism or globalcost guarantee.
"""
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+note)
report=f"""# Step0265: implement the direct finalized-number request
Date2026-11-02UTC. Review **自审**, not independent/venue acceptance.

## Entry and scientific contract
Latest direct user message is appended verbatim to docs/user-instruction.md.
Owner commitsa0a2916/395a8b3, both final reports/tables, prior qualified root0262/
0264records and current paper/index were read. The user requests three concrete
edits: RQ4scope/P95/max, RQ2three parallel ratios and direct result-index entries.
Title/fullabstract/fourRQ meanings/section hierarchy/four design implications
remain. The user authorizes the local result wording; genericmechanism firstness
and universal budget guarantees are not inferred. No newagent/native run/foreign
implementation/queue/infra change.

## EXPERIMENT_GATE — reuse completed evidence, no rerun
Native selection/preflight/execution skipped:36Mprocesses/30288checks and
27Falconer+3Mathlibprocesses were already root-qualified in0262/0264.
Re-running them adds no evidence to this writing request. Root reads the new
published2524targetCSV:12observations perunique target, all j1/j2/j4/j8 min/max
equal, allpositive; relative range formula recomputes0forall.
Nearest-rankP95=max=0%, distribution rows agree.2524×12=30288observations;
2524×3repeats×3higher-worker comparisons=22716pairs, verdict/diagnostic parity
remains the earlier complete raw qualification, not a new experiment.
ThreeCSVratios are recomputed from their own checking/source wall sums.
All27actualFalconerterminal records give26export snapshots and26non-null
predecessor restores. These are already inside nativeprocessclocks, not new
snapshot component timings. Published final panels/tables frozen gzip.
Root analysis{j['root_analysis_seconds']:.6f}s/maxRSS{j['root_analysis_maxrss_kib']}KiB.
Transition: targeted WRITE.

## WRITE_GATE — actual paper and index changes
RQ4foregrounds: in the measured prepared computation targets, no extra
allocation-count budget is needed to cover the observed worker/repeat variation;
all2524ranges/P95/max0. It is explicitly an empirical envelope, not future
acceptance or a wholecandidate/native maxHBthreshold guarantee. The observed
math-source maximum2.333868% and module-specific0.036739/0.138453% are stated
with the requested coarse0.03–0.14% envelope, without pooling their units.
Mathematical stored-proof stability and untraced search/shared-realization/
attribution alternatives remain. No claim that only mathematics needs padding,
or that0range establishes zero runtime overhead.

RQ2adds a separate three-row table9.26/10.56/14.67%, names the historical
unsegmented and matched checkpoint protocols and different module counts.
All are roughly one tenth of sourcework in these selected mathematical closures,
substantially belowconstruction, not a population law or AI-authorship cause.
No multiplication or averaged gain.26exports/restores included; physical-flush
durability/component seconds unknown. Prior17table bodies remain unchanged,
one new comparison table added. ExistingOshare/identity/RSS/trust/failure limits
remain; earliertimeouts not discarded.

Sharedresearch/README links the finalFalconer report and completed2,524census,
with two direct current entries. MownerREADMEpending warning is now removed
becausea0a2916corrected it. Root canonical/evaluation/novelty entries synchronized.
No source32/paired31/dynamic13gap or scenario calibration changes.
Transition: full compile/visualverification and REVIEW.

## REVIEW_GATE — self-review and routing
Root checks requestalignment/numerators/denominators/rounding against owner
documents and prior raw audits.0extraallocationcount allowance is supported only
for observed counted units; required maxHBmargins remain unmeasured because its
scope differs and no thresholdladderwas run. This qualification is not a denial
of the measured0% result.2.33% is not futurebound;0.03–0.14% is a coarse envelope
around exactmodule values, not nearest-hundredth rounding of0.0367.
RQ2same-order conclusion is descriptive across threefinite observations, not
controlled causal proof or a combined speedup. Priorresource/trust gaps remain.
Independent/fresh-agentreview skipped under user's no-newagentrule; both reports
are explicitlyself-review. No ideaskill/fullwriting/milestoneacceptance.
Ranked remaining gaps unchanged:source10/paired11/dynamic13, fullphaseweights,
causality/repeats/crossmachine,software/axioms/cluster,matchednative taskbaseline
and completeEnvelope singleconfigpair. They do not block these authorized edits.
Git persists onecoherentstep onmain,ownedpathsonly,ordinarypush; no foreignstash/
reset/forcepush. Actual build/all-page verification follows.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(f"""# Step0265 outer audit — 自审
Date2026-11-02UTC. Root has an execution role; this is not independent review.

The direct user request is faithfully implemented in RQ2,RQ4 and the sharedindex.
The raw-qualified0262M/0264Ocaptures are reused, never rerun or relabeled as
new independent data. Published per-target ranges/P95/max and threewallratios
are independently reduced from compact source-native tables;26exports/restores
are cross-checked against actual terminalchain fields.
The strong finite statement is retained: all2524targets have0observedrange,
so no extra count allowance was needed for those observations. Nativekernelpoll
limits/wholecandidate budgets, future acceptance and runtime overhead differ;
retaining those boundaries prevents an unsupported generic 'free' guarantee.
Mathfull-source spans and16-sourcecandidate maximum have distinct units/inputsets.
Math storedproof stability and unmeasured causality are not hidden.

The three ratios9.26/10.56/14.67% are displayed together, distinct closures and
protocols. They support comparable small checking fractions for the selected
mathematical closures, not population cost, an averaged/multiplied speedup or
causalAIauthorship benefit.26snapshotwrites/restores are charged; isolatedI/O/
physicalflush latency remainsunknown. O4share deviation/twofailedfullattempts/
trustedcheckpointmetadata/unknownnativechildidentities remain disclosed.
Index links bothownerfinalreports and removes stalependingwording; historical
rootrecords remain untouched. No title/abstract/RQmeaning/section/fourdesign-
implication change, no newnative/agent/foreigncode/runtime/entity.
Fullpaperverification and owned-path Gitpersistence remain required.
""")
print('EDITED',s,json.dumps(j))
