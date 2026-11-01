from pathlib import Path
import re,json,gzip,subprocess,datetime
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-two-cost-regimes-paper-step.txt').read_text().strip());e=s/'experiment-001'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
assert not subprocess.check_output(['git','status','--porcelain','--','docs/paper','docs/idea-story.md','docs/evaluation.md','docs/user-instruction.md'],cwd=r,text=True).strip()
# Two complete scans overlapped after the full download naturally finished.
# Preserve both actual receipts; neither is a second population sample.
def receipt_from_log(name):
 lines=(e/name).read_text().splitlines()
 return json.loads(next(x[len('COMPLETE '):] for x in reversed(lines) if x.startswith('COMPLETE ')))
full=receipt_from_log('source-scan.stdout');prefix=receipt_from_log('prefix-scan.stdout')
assert full['complete'] and prefix['complete'] and full['corpora']==prefix['corpora']
(e/'full-archive-reanalysis.json').write_text(json.dumps(full,indent=2)+'\n')
(e/'received-prefix-reanalysis.json').write_text(json.dumps(prefix,indent=2)+'\n')
(e/'reanalysis.json').write_text(json.dumps(full,indent=2)+'\n')
m,o=full['corpora'];assert m['masked_occurrences']==7 and m['masked_positive_files']==4
assert o['masked_occurrences']==1354379 and o['masked_positive_files']==5848
text=gzip.decompress((e/'paper-front.template.tex.gz').read_bytes()).decode()+gzip.decompress((e/'paper-body.template.tex.gz').read_bytes()).decode()
before=(e/'entry-main.tex').read_text()
related=before[before.index('\\section{Related work}'):before.index('\\section{Conclusion}')]
related=related.replace("The certificate case study tests a specific consequence of a measured\nreduction bottleneck; external search with native checking is prior art.",
"The streaming and chunking prototypes test different regime-specific\nimplications; external search with native checking is prior art.")
related=related.replace("The gap addressed here is a boundary-consistent characterization of released",
"The gap addressed here is a boundary-consistent, two-regime characterization of released")
fill={
'@@O_OCC@@':f"{o['masked_occurrences']:,}",'@@O_FILES@@':f"{o['source_files']:,}",
'@@M_OCC@@':str(m['masked_occurrences']),'@@M_FILES@@':f"{m['source_files']:,}",
'@@O_POS@@':f"{o['masked_positive_files']:,}",'@@M_POS@@':str(m['masked_positive_files']),
'@@O_FRAC@@':f"{o['positive_file_fraction']*100:.4f}",'@@DENSITY@@':f"{full['density_ratio']:,.1f}",
'@@M_MB@@':f"{m['source_bytes']/1e6:.3f}",'@@O_MB@@':f"{o['source_bytes']/1e6:.3f}",
'@@M_DENSITY@@':f"{m['occurrences_per_decimal_MB']:.4f}",
'@@O_DENSITY@@':f"{o['occurrences_per_decimal_MB']:.3f}",
'@@SCAN_PROVENANCE@@':r"""The reference source tree is checked at its exact Git revision.
All 163,097 primary source members are independently rescanned from the
pinned official archive and matched by path/byte size to the complete
inventory; decoding and lexical checks succeed.
The local extracted cache is partial and is not used as the population.
A complete received-archive-prefix scan and full-archive scan agree exactly;
they are repeated validation, not additional corpus observations.""",
'@@NO_M_COVERAGE@@':r"""The newly checked no-\texttt{-M} point has 31 successful native calls:
29 original random draws and two purposeful modules.
All original sources, no-\texttt{-M} arguments, PID/birth retirement and
matching native clock sums are checked.
The random-frame coverage is 29/42 with 12 complete strata; 13 draws remain
missing. The two purposeful modules receive no sampling weight.""",
'@@M_RAW_CORRECTION@@':r"""Unmasked Mathlib text contains eight sites in five files.
One is a documentation comment in \texttt{Mathlib/Tactic/Echelon/Cert.lean}.
Removing comments gives seven in four files; the table uses this common
masked boundary, not eight unmasked sites against masked generated code.""",
'@@NATIVE_COST_OBSERVATION@@':r"""The 29 completed no-\texttt{-M} random targets sum to 367.024 seconds
of native wall intervals and 602.628 user-plus-system CPU seconds.
This is not a full-build makespan or population expansion.
The separate purposeful Grid and Amplitudes points differ in output/heartbeat
scope and do not fill missing strata.""",
'@@RELATED_WORK@@':related}
for key,value in fill.items():assert key in text,key;text=text.replace(key,value)
assert '@@' not in text
assert text.count('\\item[RQ')==4 and text.count('\\paragraph{System-design implication.}')==4
(r/'docs/paper/main.tex').write_text(text)
bib=r/'docs/paper/references.bib'
(e/'entry-references.bib.gz').write_bytes(gzip.compress(bib.read_bytes(),mtime=0))
if 'mathlibD13fSource2026' not in bib.read_text():
 with bib.open('a') as f:f.write(r"""
@misc{mathlibD13fSource2026,
 author = {{Lean community}},
 title = {{Mathlib4 reference source at d13f23b7}},
 year = {2026},
 howpublished = {\url{https://github.com/leanprover-community/mathlib4/tree/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib}},
 note = {Pinned Mathlib subtree; local Git revision and unchanged source checked 1 November 2026. Lexical census excludes comments and strings}
}
""")
# Append the actual current request, not a rewritten summary of user intent.
request=r"""【Claude 通知：论文主线定为"两种成本区间"】用户原话：「按这个主线推进」。请按这条主线改论文的标题、摘要、RQ 和结构：
- 核心观察：AI 生成的数学把验证从"检查"变成了"重算"。同版本 Mathlib（d13f，8,529 个文件，98 MB）里 decide +kernel 只出现 8 次（5 个文件）；openai/math（163,097 个文件，1.785 GB）里是 1,354,379 次（5,848 个文件），每 MB 密度约高 9,000 倍，集中在约 3.6% 的计算证书文件里。数字请用你们自己的扫描脚本复核后再写进去。
- 两种区间：计算模块里 C++ 内核占用户态周期的 75–94%，独立验证就等于重做计算；数学模块里内核只占约 2%，验证理论上只需生产成本的零头，但现有流程的重放却是构建的 1.28 倍，原因是逐模块导入，以及验证和 elaboration 绑在一起。
- RQ 建议：(1) AI 生成的形式化产物的验证成本落在哪里，两种区间在全库各占多少（等 W 线的无 -M 新口径数据）；(2) 为什么现有独立验证兑现不了数学区间的低成本（导入、流程耦合；O 线在做单进程流式检查）；(3) 计算区间能否在不扩大可信基础的前提下扩展到多核或集群（M 线在做自动分块并行检查）；(4) "已验证"的含义缺口：默认构建范围漏掉 33% 的 decide +kernel、判定随设置和观测手段变化、公理闭包不明。
- 机制部分写成由刻画推出的设计含义，配原型。数据没出来的地方一律 \missing，不预填。-M 只作为方法学说明。
改完 commit 并 push。

【同一轮还要做：记录和整理】用户问：「过去的完整的对话和变更和文档都记录了吗? 都整理了吗」。我核对了一遍，发现三处缺口：
1) docs/user-instruction.md 只收了我转给你的通知，用户直接对我说的原话很多没有收进去。我把 10-30 到 10-31 的原话逐字整理在这个文件里（在本机，你可以直接读）：C:\Users\10678\AppData\Local\Temp\claude\C--Users-10678-OneDrive----spark-manage\cef933b4-529c-40c9-a25a-327925dfe25f\scratchpad\proofserve-user-words-1030-1031.md。请原样追加到 docs/user-instruction.md，按日期排好，和已有条目去重，不改写原话。
2) docs/research-status.md 和 docs/research-plan.md 最后更新是 10-30 09:27，已经过时。请更新到当前状态：刻画论文；完全不用 -M；"两种成本区间"主线；各线分工和目录（W：workloads/；M：research/chunked-kernel-check/；O：research/decoupled-check/；之前的 research/mechanisms-2026-10-30/ 和 research/profile-2026-10-31/）；已有结果和负结果，各自链接到对应的报告。
3) 新建一个结果索引 research/README.md，列出每个研究目录：做了什么、关键数字、报告链接、原始数据在 PVC 上的位置。
分步 commit 并 push。"""
with (r/'docs/user-instruction.md').open('a') as f:f.write('\n\n## 2026-11-01 UTC — verbatim two-regime and records request\n\n'+request+'\n')
with (r/'docs/idea-story.md').open('a') as f:f.write(f"""
## 2026-11-01 — user selects two verification-cost regimes
Explicit user instruction replaces the prior five-finding organization with
checking mathematical witnesses versus replaying proof-embedded computation.
Newtitle/abstract/fourRQmeaning/structure are authorized, notagentstorydrift.
RQ1nativecost/location andcost-weightedprevalence; RQ2independentverification/
import/elaborationcoupling; RQ3original-kernel multi-core/cluster scaling;
RQ4build/outcome/axiomcoverage. Primarymath/publicsoftware/RLcontrasts remain.
Commonmaskedscanner independentlyfinds Mathlib7sites/4files versus
openai1354379/5848; rawMathlib8/5includesonedoccomment. Density10668.3188x,
positivegeneratedfiles3.585596%, neitherisCPUshare. Old-M75–94/~2/1.28
remain methodologymotivation, notfreshanswers. NoM31rawrecordschecked,
random29/42/12cells; fullweights/streaming/chunked/cluster slotsmissing.
Ostreaming andMchunking are implicationprototypes; stockkernel/APIcalls do
not themselves prove fullsoundnessor speed. OriginalInitialNarrative/evolution
above retained; current framing is morefaithful to explicituserregimequestion
than a general resource/accelerator story.
[Evidence and self-review]({s.relative_to(r/'docs')}/step-report.md).
""")
ev=r/'docs/evaluation.md';t=ev.read_text()
a=t.index('| RQ |');b=t.index('\n## ',a)
t=t[:a]+"""| RQ | Two-regime characterization question | Current frontier |
|---|---|---|
| RQ1 | Cost locations and runtime-weighted regime prevalence | matchedlexicalcensus complete; noM29/42costs, fullphaseweights missing |
| RQ2 | Why cheap mathematical checking isn't cheap independent verification | samekernel replay scopes known; matchedstreaming/import/coupling costs missing |
| RQ3 | Original-kernel computation across cores/cluster | M18leafprototype inspected, complete performance/differential/cluster results missing |
| RQ4 | Build/outcome/axiom meaning of verified | defaultroot33.30%siteomission, historicalsetting/observer sensitivity; axiomclosure missing |
"""+t[b:]
t+=f"""
## Two-regime source census and noM31 — step0231
[Report]({s.relative_to(r/'docs')}/step-report.md), self-review.
Mathlibd13f subtree8529files/98449500bytes,7masked sites/4files; raw8/5 has
one documentationcomment. Completeopenai4eaee875 source163097files/
1785499363bytes/1354379sites/5848files. Density10668.3188x and3.585596%
positivefiles are lexical, not timeweights. ExistingWmask reused; fullarchive
andreceivedprefix scans agree, nottwoobservations. Partiallocal13952cache
wasrejected beforepaperedit. Whole896084751byte officialarchive retainedonPVC.
Fullsource download/scan1037.986s; prefixscan58.759s, bothsamecounts;
max253020KiB perprocess, concurrentrootanalysesbelow4GiB/E22–23/noLean.
Duplicate scan overlapped naturaldownloadcompletion; no extra sample/draw.

All31newWnoMargv/source/retirement/logs/scopedclockschecked,29randomtargets
CPU602.627562s/nativewall367.023781s. PurposefulGrid/Amplitudes notweighted.
This supersedes earliercurrentmissing coverage at229, notthe old-Mclocks.
Runtimephaseweights, matchedstreaming andparallel/cluster results remainmissing.
Source/prototypecode inspected/frozen withouteditingownerimplementations.
"""
ev.write_text(t)
status=r/'docs/research-status.md';t=status.read_text().replace('Same-scanner Mathlib density comparison is being rechecked.','Same-scanner Mathlib masked7sites/4files versus openai1354379/5848;\\n  density10668.32x, positivegeneratedfiles3.5856%, not CPUweights.')
t=t.replace('Matched Mathlib density comparison is being independently rescanned.','The matched maskedcomparison is7/4versus1354379/5848,10668.32x perMB.')
t=t.replace('Root paper integration must recheck raw records.','Rootstep0231 has rechecked nativeargv/source/identity/scopedclocks.')
status.write_text(t)
idx=r/'research/README.md'
with idx.open('a') as f:f.write(f"""
## Root source comparison and paper integration
[Step0231]({Path('../docs')/s.relative_to(r/'docs')}/step-report.md):
freshsame-maskMathlib/openaicomparison7/4vs1354379/5848,10668.32xsites/MB;
3.5856%positivegeneratedfiles, notCPUshare. Rawfixedarchive andsourcecensus:
{full['raw_archive']}. Two scans agree; no-M31results independentlyaudited.
Old8/5Mathlibfigureincludesadocumentationcomment. Nativeweights remainopen.
""")
(s/'step-report.md').write_text("""# Step0231 — user-authorized two-cost-regime paper reconstruction
Phase: authorized reconstruction, then BUILD_AND_EVALUATE.
All review 自审, not independent.
## EXPERIMENT node
RQ1 commonlexicalboundary. Same Wmaskfunction scanned Mathlibd13f8529files/
98449500bytes and completeofficialopenai4eaee875163097files/1785499363bytes.
Matchedallprimaryinventorypaths/sizes; no decoding/lexicalfailure.
RawMathlib8/5 includesEchelonCertdoccomment; commonmasked7/4.
Openai1354379/5848 unchanged. Density10668.3188x;3.585596%files, notCPU.
Initialextractedcache13952 wasincomplete andassertedout beforepaper mutation.
Fullofficialarchive896084751bytes downloaded; full/prefixscansagree exactly.
Prefixanalysis overlapped fullcompletion; duplicatedvalidation, notsamples.
NoLean/native/ownerqueue/infrachange; rootE22–23, <=4GiB.
NewWnoM31records independentlychecked: argvomit-M/source/PIDbirth/logs/
scopedclock totals;29originalrandom+2purposeful. Coverage29/42/12cells;
no globalruntime/costweight estimate. M/Oprototype sources inspected,
smallfrozen snapshots only, notexecuted or edited.
## WRITE node
Userexplicitlyselectstwo regimes: title/abstract/fourRQmeanings/organization
rebuilt. RQ1concentration+costweights;RQ2imports/productioncoupling and
Ostreamprototype;RQ3M18leafassembly andoriginalkernelparallel/cluster
boundary;RQ4build/settings/observer/axiommeaning. Mechanisms are implications,
not claimednewTCB/freeparallelism. Allpendingnativeweights/ratios/soundness/
cluster results literal missing. Old-M75–94/~2/1.28 methodologymotivation only.
Priorpapers/evaluation/idea preserved, userpromptverbatim appended;
currentstatus/index getsverifiedsourcecomparison/currentnoMcoverage.
## REVIEW node
Self-review userintent andsource/costdenominators. Correct baseline7not8,
neversites=>time; sourcepositivefiles aren'texhaustivecomputationclasses.
Independentchecker/fullbuild/freshtrust aren'tequivalentclocks. NoM31
unweightedsubset doesn'tfillmissingstrata. StockkernelAPIs/codepresence
notfullcorrectnessor performance. OriginalregimeRQsnewbyuser, notsilentdrift.
Formalcompile/visualself-review and ownmaincommit/push follow.
""")
(s/'outer-audit.md').write_text("""# Outer audit step0231
Review 自审, no independent acceptance.
## Direction
Newtwo-regime scientificcontract isexplicitlyuserauthorized. CurrentRQs
retain primaryresearchmath/publicsoftware/RLcontrasts and noMdecision.
Sourcecomparison supportslexicalshift/concentration; runtimeweightsopen.
Do notpromote old-Msamplesor1.28ratio backtocurrent evidence.
## Validity
Original8/5rawMathlib isn'tsameboundary asmaskedopenai; mainuses7/4.
Freshfullsource/prefix scansagree, samepin/filemembership/bytes, no sampling.
Initialpartialcache failure preserved. Fullarchive ended naturally; prefix
doesn'tcreateanotherpopulationdraw. Rootduplicatedsomework, nothidden.
NoM31rawaudited butphaseweightsmissing. M/Ocodecountsasimplementation
description, notnativecompletion or expandedTCBsoundnessproof.
## Ownership and efficiency
First9b76244alreadycontains51newquotes/2exactduplicates skipped andindex.
No inaccessiblecompleteconversationclaim. Allfourresearchrootsindexed.
Thisstepreuses currentpublishedprimarydata/prototypes; no newnative run,
agent, queue orownerfileedit. Rootinputs/oldpaper/failures retained.
Compilecitations/refs, fourRQstructure, missingvalues, visualinspection and
own-path Git publication remain required. No venueacceptance implied.
""")
print('PAPER_REWRITTEN',len(text),'density',full['density_ratio'],'step',s)
