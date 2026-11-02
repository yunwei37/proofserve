from pathlib import Path
import os,subprocess,json,gzip,re
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cpu-coverage-root-step.txt').read_text().strip());e=s/'experiment-001';rel=str(s.relative_to(r));suffix=s.name[len('step-'):]
a=json.loads((e/'reanalysis.json').read_text());t=(r/'docs/paper/main.tex').read_text()
old=r"""to this closure. Their summed native wall time is 22,077.770s.
A chain of 27 successful checker processes accepts the complete module set
in 2,043.585s (2,038.444 wait4 CPU-s), or 9.2563\% of source work."""
new=r"""to this closure. Their summed native source-compiler CPU is 32,292.604s.
A chain of 27 successful checker processes accepts the complete module set
using 2,038.444 CPU-s, or 6.31\% of source-compiler CPU.
Here and in the matched Mathlib control, CPU means summed native user plus
system time, with checking and source work charged over their respective
complete selected closures.
The separate native elapsed sums are 2,043.585s for checking and
22,077.770s for source compilation, yielding a wall-time ratio of 9.26\%."""
assert old in t;t=t.replace(old,new)
old=r"""Three mathematical-closure
observations. Falconer has 13,205 modules/27 processes; both Mathlib Nat.Basic"""
assert old in t;t=t.replace(old,r"""Three mathematical-closure
wall-time observations. Falconer has 13,205 modules/27 processes; both Mathlib Nat.Basic""")
begin=t.index(r'Table~\ref{tab:mathclosureratios} places')
end=t.index('\nEach segment exports',begin)
new=r"""\measured{\expref{STEP}{0268}; retained raw process costs, no new native run.}
Table~\ref{tab:mathclosurecpu} compares native CPU under the same checkpoint
adapter and 500-new-module quota: 6.31\% for Falconer and 8.95\% for Mathlib.
Both selected mathematical closures use substantially less CPU for checking
than for source production. Source CPU includes imports, elaboration, tactics,
initial checking and artifact emission; it is not an isolated kernel baseline.

\begin{table}[t]
\centering\small\setlength{\tabcolsep}{3pt}
\begin{tabular}{lrr}
\toprule
Closure & Check / source CPU (s) & Ratio\\
\midrule
Falconer & 2,038.44 / 32,292.60 & 6.31\%\\
Mathlib Nat.Basic & 91.15 / 1,018.22 & 8.95\%\\
\bottomrule
\end{tabular}
\caption{\measured{\expref{STEP}{0268}} Summed native user-plus-system CPU
for complete selected closures under the same checkpoint protocol.
This clock differs from the wall-time sums in Table~\ref{tab:mathclosureratios}.}
\label{tab:mathclosurecpu}
\end{table}

Table~\ref{tab:mathclosureratios} separately retains the wall-time observations:
9.26\% for Falconer, 10.56\% for the historical Mathlib stream and
14.67\% for checkpointed Mathlib (91.279s versus 622.379s).
CPU and wall ratios answer different questions and are not pooled.
Each closure has one ordered capture with retained page cache.
The older unsegmented Mathlib result uses another adapter;
it is not a causal control for the checkpoint protocol.
Neither the CPU comparison nor the wall comparison isolates AI authorship,
tactics, dependency composition or import cost, and neither estimates
population cost or production latency.
""".replace('STEP',suffix)
t=t[:begin]+new+t[end:]
needle=r"""\paragraph{System-design implication.}
\partialev{implication of scoped observations; general benefit unproven.}
Expose the cheap checking boundary"""
assert needle in t
p=r"""\paragraph{A bounded whole-source attempt remains partial.}
\partialev{\expref{STEP}{0268}; source coverage and compilation failures unresolved.}
A separate finite-window attempt accepts only 2,488 of the 163,097 source
modules, plus 10,744 dependency modules; 160,609 source modules remain
without accepted checking records. Its terminal state is incomplete.
The production ledger records 9,124 source-compilation returns of
\texttt{rc=1}, whose causes remain under investigation.
These returns are not classified as kernel or mathematical rejections.
The accepted prefix does not establish whole-library checking cost, validate
the RQ1 scenario ranges, or replace the complete selected Falconer closure.
No missing module is assigned zero cost.

""".replace('STEP',suffix)
t=t.replace(needle,p+needle)
(r/'docs/paper/main.tex').write_text(t)
# Verify inherited numerical tables and fixed scientific structure immediately.
before=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
tabs=lambda x:re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}',x,re.S)
assert len(tabs(before))==19 and len(tabs(t))==20 and all(v in tabs(t)for v in tabs(before))
for pat in [r'\\title\{.*?\}',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ[^\n]+',r'\\(?:sub)*section\{[^\n]+']:
 assert re.findall(pat,t,re.S)==re.findall(pat,before,re.S),pat
imp=lambda x:[v.split('\n\n',1)[0]for v in x.split(r'\paragraph{System-design implication.}')[1:]]
assert len(imp(t))==4 and imp(t)==imp(before)
record=f"""CPU and coverage update [0268]({rel.replace('docs/','',1)}/step-report.md): Falconer native check/source CPU2038.443942/32292.603807s=6.3124%; matching checkpoint Mathlib91.145172/1018.219383s=8.9514%. Separate native elapsed ratios9.26%/historical10.56%/checkpoint14.67% remain. Source/protocol/CPU units are not pooled. Whole-source bounded attempt accepts2488/163097source+10744dependencies;160609source missing,9124source-compilation rc1 unclassified, not mathematical rejection or measured full-library cost."""
for f in ['docs/research-status.md','docs/research-plan.md']:
 pth=r/f;v=pth.read_text()
 v=v.replace('root0267.','root0268.')
 v=re.sub(r'Paper root0267:[^\n]+','Paper root0268: CPU/coverage update; final PDF verification pending in this step.',v)
 v+='\n\n'+record+'\n';pth.write_text(v)
idx=r/'research/README.md';v=idx.read_text();v+='\n\nCPU/coverage scope [root0268](../'+rel+'/step-report.md): Falconer6.31% and matched-checkpoint Mathlib8.95% are native CPU ratios.9.26%/10.56%/14.67% are separate wall ratios. Whole-source accepted2488/163097;9124compilation rc1 unclassified, bounded incomplete attempt. Raw process reanalysis and small CPU table are linked in the root report.\n';idx.write_text(v)
n=r/'docs/novelty-20261101.md';v=n.read_text();v+='\n\n## 2026-11-02 — CPU versus elapsed and partial source coverage\n\n'+record+'\nNo new novelty search or stronger A/B/C mechanism claim. The new CPU reconciliation does not establish a full-library saving, AI-authorship causality, general context safety or venue acceptance.\n';n.write_text(v)
ev=r/'docs/evaluation.md';v=ev.read_text();v+='\n\n## 2026-11-02 — root0268 CPU and coverage reconciliation\n\n'+record+'\n\nIndependent root read of13205source raw results and30checkpoint native results retains the complete selected-closure qualification from0264. CPU is native user+system, sourcej8 and checkpoint protocols unchanged. No native rerun. Root small analysis on E22–23 only. The original two1500s failed attempts, O4GiB share deviation, trusted metadata, missing independent native-child birth/RSS sampling and all global evidence gaps remain. Whole-source .olean-only production does not replace W normal .olean/.ilean/C sample costs. The finite whole-source and Hodge attempts ended by their declared windows; no restart authorized or made.\n';ev.write_text(v)
cleanup=f"""
## 2026-11-02 UTC — root0268 audit of historical build caches, no cache deletion

User requested native427 recovery (~12.2GiB) and repository/artifacts (~22.3GiB) audit, never delete tracked files or unreferenced raw. Root audited both. Native427 has13untracked .lake/build directories (4,945,862,656 allocated B), stock SDKlib2,588,311,552B, and11untracked artifact ELF executables714,248,192B. The25candidates span102693unique inodes; nlink-adjusted reclaim estimate8,235,347,968B. This is a candidate estimate, **not released space**. Artifacts contains17429Git-tracked files, all protected. No cache/SDK/ELF/source/raw file was deleted.

References checked: native427 absolute paths appear in10970tracked build/analysis records; SDK at artifacts/linarith-oracle-2026-10-17/gpu-stage/corrected-wall-profile/build-attempt3-compiler.log:19 and large-lp-race/native-queue-control/build-final.log; mathlib at current-budget-gpu-20261023/admission-async-20261024/preflight-analysis.json. Artifact families have existing tracked analyses/reports: artifacts/lean-modern-native-compilation-2026-10-14/native-oracle-full-plan.md and plan-gc.md; docs/idea-story.md (lean-gpu-checking). Inventory records exact candidate paths/inodes/blocks under [{rel}/experiment-001/cleanup-candidate-inventory.json.gz]({rel.replace('docs/','',1)}/experiment-001/cleanup-candidate-inventory.json.gz). Reproducible build caches and ELF outputs could be rebuilt; original raw/source/report/CSV must remain. This is an audit, not a claim every historical artifact can be deleted.

Initial live used129011671040B of134951424000B (~95.6%). Other owners' concurrent cleanup brought used to111201239040B (82.40%), already below85%, before root considered candidate deletion. Fresh analysis snapshot used{a['disk']['used_bytes']}B ({a['disk']['used_percent']:.3f}%), available{a['disk']['available_bytes']}B. None of that concurrent release is attributed to root. Target met; root retains all candidate caches to avoid unnecessary deletion. Earlier root0267 only deleted its35fresh renderings22,131,383B after all-page review, already separately recorded and pushed61e6dfd. New root0268 rendering cleanup, if any, is recorded only after review.

Connection uses existing Cloudflare SSH jump ssh.yunwei37.com added only in the invoking PowerShell module process; no network/Tailscale/server configuration mutation. No native collection, Agent/session, CronJob, queue or owner implementation changed.
"""
(r/'docs/cleanup-20261101.md').write_text((r/'docs/cleanup-20261101.md').read_text()+'\n'+cleanup)
report=f"""# Root step0268 — CPU and source coverage reconciliation

**自审, not independent review or venue acceptance.** Existing BUILD_AND_EVALUATE phase, fixed title/abstract/four RQs/section hierarchy/four design implications. User's exact current words appended verbatim to docs/user-instruction.md.

## EXPERIMENT_GATE — retained native capture analysis
Entry: read current user instructions, questions, canonical status/plan/index and0267reports. No new native experiment admitted: user asks reconciliation of retained complete results and partial coverage. Existing W/M/O owners remain; no agent/queue/session/native calls. Raw collection and complete selected-closure graph/reference qualification remain0264, not claimed repeated.

Root recomputes13205source .result.json records joined to retained source CSV and30checkpoint results (27Falconer/3Mathlib). Every selected process returns0; args omit-M.1330Mathlib IDs come from original measured capture. CPU is user+system. Falconer2038.443942/32292.603807s=6.3124174%; Mathlib91.145172/1018.219383s=8.9514277%. Wall sums separately give9.2563%/14.6662%; historical Mathlib65.692644/622.379412s=10.5551%. One ordered capture each, not CI, causal authorship or global population cost.26exports/restores already included, never added twice.

Whole-source ledger independently counts9124production rc1,19production rc0 and32checker attempts (31rc0/1rc126). Published terminal scope is2488/163097source accepted +10744dependencies,160609source missing, completeFalse. The accepted source set includes reused input artifacts;19new production successes are not the source acceptance denominator. Failure cause pending O, not mathematical rejection. Hodge440/616/1700s and whole-window ends are user-reported normal finite stops; no root restart. Preserve Wsource32/42,target31/42,dynamic13missing and207.8–630.8/10.8–41.9CPUh assumption scenarios.

## Storage/transport work
Completed0267 first: commit61e6dfd and ordinary push confirmed;23pages217908B. Existing Cloudflare jump restores authorized management CLI without network changes. Native427/artifacts audit preserves17429tracked files and unreferenced raw. Candidate8.235GB was NOT deleted: other-line cleanup already reached82.4%, latest snapshot{a['disk']['used_percent']:.3f}%. See docs/cleanup-20261101.md and exact inventory. No other-owner cleanup credited.

## WRITE_GATE — targeted result slots
Paper foregrounds6.31%/8.95% CPU, adds one two-row CPU table and retains19prior table bodies. Existing three-row wall table caption now explicitly wall; its body unchanged. Adds bounded partial whole-source paragraph. Updates canonical/status/plan/index/novelty/evaluation and cleanup. No narrative restructure, new mechanism or external literature search. Exact edit/reducer scripts and before-gzips retained.
Fixed title/fullabstract/fourRQ/sections/fourdesignimplication and19table bodies compared and identical;20tables total.
Full compile/all-page review/link verification not yet completed at this report creation; final receipt must supply actual completion.

## REVIEW_GATE — root self-review and routing
Scientific contract unchanged. Accepted: CPU and wall denominators differ; whole-source partial must constrain claims. Deferred:9124failure attribution to O, Wnewcost/grain and global/causal/software/axiom/cluster/nativebaseline/Envelopepair gaps remain. No reviewer or owner title substitutes for raw qualification.
Efficiency: no duplicate native work or extra cache deletion; reuse0264qualification. Read-only anchor lookup errors preserved, no scientific effect. Self-review may catch local issues but is not independent audit or acceptance. Next integrate actual new terminal/attribution from existing owners, never rerun completed plans from stale status.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0268 — CPU and source coverage reconciliation','# Root step0268 outer audit — 自审')+'\n## Audit disposition\n\nRoot checks authority against exact direct user words, raw CPU denominator, distinct clocks and partial coverage. No independent reviewer was launched, per user prohibition on new agents. Direction preserved; publication requires actual compile/all-page checks and ordinary main push. Storage audit satisfied user target with current live evidence, without unnecessary candidate deletion. No O/W scientific conclusion promoted beyond inspected evidence.\n')
print('EDITED',s,'TABLES',len(tabs(t)))
print(subprocess.check_output(['git','diff','--stat','--','docs/paper/main.tex','docs/research-status.md','docs/cleanup-20261101.md'],cwd=r,text=True))
