from pathlib import Path
import os,json,re,gzip,shutil,subprocess
os.sched_setaffinity(0,{22,23})
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-pmu-uncertainty-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text())
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');tag=r'\expref{'+s.name.removeprefix('step-')+r'}{0277}'
p=r/'docs/paper/main.tex';t=p.read_text();old=t
rq1=r"""\paragraph{Narrow missing-cost scenarios do not imply precise sampling.}
\partialev{TAG; nominal sampling uncertainty for the 19 complete strata.}
Recomputing the finite-population stratified variance from the same two
original draws per stratum gives an approximate 95\% Student-$t$ interval
of 43.99--449.74 CPU-hours around the covered-domain estimate of 246.863 hours,
with Satterthwaite effective degrees of freedom 2.13.
Two strata contribute 62.41\% and 27.61\% of the estimated variance.
This nominal interval is fragile with two observations per cell; it omits
the two incomplete strata, nonresponse, runtime drift and protocol-transfer
uncertainty. It is neither a full-frame confidence interval nor a guaranteed
bound. The narrower missing-cost scenarios below address a different
uncertainty and do not establish population-estimate precision.

""".replace('TAG',tag)
anchor=r'\paragraph{Whole-frame costs require explicit missing-cost scenarios.}'
assert t.count(anchor)==1;t=t.replace(anchor,rq1+anchor)
rq3=r"""\paragraph{Whole-command counters narrow the CPU-growth hypotheses.}
\measured{TAG; a separate complete 16-process Barrier matrix.}
Each of four worker settings (4, 8, 1, 2, in that order) has ordinary
before/after, counter and sampled-recording processes.
All 16 accept the same 4,449-module closure with identical per-module
check and allocation-count vectors: 237,863 checks and 3,283,925,639 units.
Across the four ordinary 4-to-8-worker before/after pairings,
91.70--99.15\% of extra native CPU lies inside the observer brackets
around original kernel calls. As above, these include heartbeat and timing
reads and are not pure C++ kernel cycles.
The earlier 95.95\% observation belongs to its separate capture.

In the whole-command user-mode counter runs, 4-to-8-worker instructions
increase only 0.0396\%, while cycles increase 8.31\% and aggregate IPC falls
from 1.834 to 1.694. Retired locked loads change 0.117\%, L3-miss loads
increase 11.98\%, modified-line forwarding 46.41\%, and demand-RFO
snoop-HITM responses 49.76\%.
These counts cover startup, coordination and checking together; they are
not gated to the observer brackets. Locked-load counts are operations,
and forwarding/RFO events do not identify reference counting uniquely.
The observations support investigating coherence, ownership and cache
costs under nearly fixed instruction work, without isolating one cause
or a removable stall fraction.
Fixed order, retained page caches and one counter run per setting leave
order, frequency and instrumentation effects unresolved.
Original sampled-worker READ metadata is incomplete for some settings;
later counting-only repair points have separate denominators and are not
used here to fill missing original attribution.

""".replace('TAG',tag)
anchor=r'\paragraph{Pooled certificates pass a broader native qualification.}'
assert t.count(anchor)==1;t=t.replace(anchor,rq3+anchor)
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
p.write_text(t)
entry=f"""[Root0277]({drel}/step-report.md) independently qualifies the original16 completed PMU matrix processes: each4449unique accepted modules,425463entries/3595upstream exclusions/0contextfallback; per-module237863checks/3283925639allocation units unchanged. Four ordinary4→8 pairings place91.70–99.15% extra nativeCPU in observer brackets including HB/timing reads, not pure C++cycles. Separate whole-command user PMUs: instructions+0.0396%,cycles+8.3107%,lockedloads+0.1171%,L3missloads+11.9794%,modified-line forwarding+46.4111%,RFOsnoopHITM+49.7555%,IPC1.833725→1.693693. Whole-command scope/fixedorder/pagecache/one counter cell preclude a unique RC/cache/frequency cause or removable stall share. Original sampled-worker metadata and separate owner counting-only repairs are not root-qualified causal attribution. Old0273's95.95% bracket observation remains separate.
Same38original source costs,19complete strata/161034domain: independent finite-population stratified variance32376792892.27296CPU-s², nominal95%t/Satterthwaite43.987706–449.738374CPUh around246.863040h,df2.130943. Two cells contribute62.4086%/27.6065% variance. n2/cell fragile, excludes incomplete strata/nonresponse/transfer/drift, notfullframeCI/bound. Missing-cost scenarios247.5–270.3source/16.8–24.0mixedtransfer unchanged, distinct uncertainties;4source/11paired/13dynamic gaps unchanged."""
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text().replace('root0276.','root0277.',1)
 v=re.sub(r'Paper root0276:[^\n]+','Paper root0277: fixed-work PMU and covered-domain uncertainty; final compile/all-page verification pending.',v)
 if n.endswith('status.md'):
  marker='## Terminal failures and trust that remain visible'
  newrow='| Fixed-work PMU and uncertainty |16full Barrier processes share graph/count work; extra4→8 CPU91.70–99.15% in observer brackets, whole-command cycles+8.31% at instructions+0.0396%. No unique RC cause.19complete source strata nominal95% interval43.99–449.74CPUh/df2.13; not full-frame CI. | [0277]('+drel+'/step-report.md) |\n\n'
  v=v.replace('\n'+marker,'\n'+newrow+marker)
  v=v.replace('Separate from current source37coverage/full closure.','Separate from current source38coverage/full closure.')
 else:
  v=re.sub(r'Current owner snapshot at root0275:[^\n]+','Current owner snapshot at root0277: original M16/16matrix is complete, not pending P2. Supplemental P8 count-only and P4 external-parent/drain points are owner-complete with separate metadata qualifications; root qualifies original16 graph/clocks/whole-command counters here, not new worker-level causal claims. Ramsey production remains stopped190/444 and20-file sample complete. W38 costs unchanged; existing Allocated preparation is owner work. SubexponentialSAT remains a source prefix, not a complete closure ratio or root dispatch. Refresh actual terminals.',v)
  v=v.replace('| RQ1 |5original source costs','| RQ1 |4original source costs')
  st=v.index('Current source37data preserve');en=v.index('\nKernel-helper allocation stability',st)
  v=v[:st]+'Current source38data preserve conditional marked CPU23.311% over19complete strata/161034modules, not semantic phase/global weights. Nominal sampling uncertainty43.99–449.74CPUh/df2.13 is fragile and conditional on covered strata; missing-cost scenarios247.5–270.3source/16.8–24.0modeled checking CPUh answer a separate question. No-assumption upper remains unbounded. Historical31-input forecasts remain31-input experiments.\n'+v[en:]
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';v=p.read_text().replace('root0276.','root0277.',1)
v=v.replace('## Latest complete results\n','## Latest complete results\n\n- [Fixed-work whole-command PMU and sampling uncertainty](../'+rel+'/step-report.md): original16full cells qualified; instructions nearly fixed while cycles/coherence events rise. No unique RC cause. Covered19source strata nominal95% interval43.99–449.74CPUh/df2.13, distinct from missing-cost scenario247.5–270.3CPUh. [Owner PMU](parallel-stream-check/perf/full-matrix-report.md); later worker-count repairs remain separate.\n',1)
v=v.replace('source coverage32/42/15strata differs from31target-replay pairs/14strata.','source coverage38/42/19strata differs from31target-replay pairs/14strata.')
p.write_text(v)
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0277 fixed work, hardware counters and sampling uncertainty\n\n'+entry+'\nNo new native run or mechanism claim; all20table bodies and scientific contract frozen. Resource clocks, nativePID/birth and source ledger qualifications are recorded in the root step. General causal/replication/global/axiom/software/cluster/baseline gaps remain.\n')
report=f"""# Root step0277 — fixed-work PMU counters and covered-domain uncertainty
**自审; not independent review, research completion or venue acceptance.**

## EXPERIMENT_GATE
Existing BUILD_AND_EVALUATE collection of completed owner work plus offline arithmetic. Entry rereads direct decisions, canonical0276/0275 and both root reports, actual original16terminal and source38frame. No native experiment/Agent/session/queue/restart. No new research question or mechanism; complete-idea/full-writing/milestone-review triggers absent.

### Node E1 — independent original16 native qualification
Raw /workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103. Foreground terminal completes06:34:59UTC; stale analysis-status10/16 is not actual completion. Each worker4/8/1/2 has plain-before/stat/record/plain-after,16actual rc0/native processes. All4449unique header/accept/profile sets, imports/constants,425463entries/3595unsafe-partialexclusions/0contextfallback/rootreachability independently rebuilt; matches original v14 serial accept-event schema and graph. All per-module check/allocation vectors equal,237863checks/3283925639units. Not a new corpus or theorem count.
Frozen ParallelCore/ParallelStream/placement_profile/checked_commit and runners read. Original mathematical Kernel.addDeclCore preserved; trusted coordinator/CABI/observer remain. C CLOCK_THREAD_CPUTIME_ID brackets surround original call plus HB/timing reads, not pure C++clock. Native wall ends after wait4 before samplerjoin/cgroupcleanup; queue excluded. Configuration from frozen runner/terminal, not invented per-open execution trace.
All16 actual command/result/stdout/stderr/memory read: noM(omit-M0),P0–7,1100native/1740outer-afterlock,14GiBcharged+14GiBsampledownRSSresponse.16cgroups absent/noOOM/noRSSstop/wait4complete.58unique emitted PIDbirth identities retired, no inventedlauncher. HWM3439628KiB/sample3539369984B/charged1277435904B distinct, not hardRSS or complete16GiBlane-tree qualification.
Four ordinary4→8pairings: extraCPU63.315947–76.268142s, bracketfractions0.9170082663–0.9914779057. Historical0273's95.95% is another capture and retained unchanged.
Raw7 whole-command user-mode stat selectors each100%running: instructions+0.0396073%,cycles+8.3107477%,referencecycles+9.7405937%,lockloads+0.1170975%,L3missloads+11.9794397%,XSNPmodifiedlineforwarding+46.4110502%,demandRFOsnoopHITM+49.7554849%; aggregateIPC1.833724943→1.693692703. Cycles/referencecycle ratio decreases1.3029%, not fixed effective frequency. Events are user whole-command, not bracket-gated; locked loads are operations not stalls, HITM/forwarding not RC-specific. Frozen primary Intel event semantics distinguish XSNP_HITM aliasXSNP_FWD. Support investigating coherence/ownership/cache participation, not unique RC cause or removed-stall fraction.
Original sample READ metadata incomplete for P8 and P4coverageunknown. Original perf.data for somepoints owner-cleaned after published analysis; raw clocks/events/stat preserved. Root does not claim new unwind/sample-family causal qualification. Later owner P8count-only/P4drain counts complete according latest supplemental report, separate points/parentage, not used to impute originalmatrix or root worker-counter causal conclusion. FailedREADattempt retained, no hot edit/restart by root.

### Node E2 — independent source38 sampling uncertainty
No new original draw, weight or source/native run. All38 fixed-frame raw cost/result links checked against qualified source38; same19complete strata/161034modules with2draws each. Variance independently N²(1-n/N)s²/n percell, sum32376792892.27296CPU-s²; point246.8630397965CPUh. Satterthwaite df2.130942986, inverse Student-t numerical Simpson integration/bisection critical4.058960595 independently gives43.987705740–449.738373853CPUh. Matches ownerW105 without importing owner numerical implementation. Two cells contribute62.4085782%/27.6065191% variance; source19-variance.csv preserves every cell.
Nominal approximate95%, n2/cell fragile; not distribution-free bound/fullframeCI; excludes2incompletecells/nonresponse/runtime drift/transfer assumptions. Four ordinaryoriginalcosts/2063domain remain missing. Existing247.5–270.3source/16.8–24.0mixedprotocol scenarios unchanged; narrow support scenario not precision. Paired31/42/14cells/11missing,dynamic13missing,RQ2CPU/wall,B2524/30288/22716 and overlapping M100/50 panels unchanged.

## WRITE_GATE
Actual local RQ1 paragraph distinguishes sampling and missing-cost uncertainty. Actual local RQ3 paragraph adds independent16 matrix/fixed work/ordinary CPU bracket range/whole-command event semantics and limits. Old0273 paragraph unchanged.20oldtable bodies/title/fullabstract/fourRQ/sectionhierarchy/fourdesignimplications byte-preserved. No new table/firstness or generic mechanism claim. Canonicalstatus/plan/index/novelty/evaluation synchronized, stalecurrent13/16 and source37 plan text corrected without rewriting dated historical reports.
Rawarchive15192357B retains16commands/results/stdout/stderr/memory/terminals/frozen source and owneroriginal16 outputs/source38 evidence. FourCSV,reanalysis/source/entrygzips retained; noSDK/buildtree/nativeELF/perfdata copied intoGit. Root analysis10.744780s/31312KiB/E22–23. No new native or Agent. Fullcompile/visual/linkcheck completion appended after actual work.

## REVIEW_GATE — self-review
Accept identical finite work, observed extraCPU brackets and scoped whole-command PMU covariance. Reject purekernelcycles/RCuniquecause/operationstallshare/causalfrequency/independentrepeatedCI or new workerrepair qualification. Accept nominal conditional sampling uncertainty, reject fullframeCI/guaranteedbound/zeroimputation or support-scenario precision. Own raw/results/failed/partial histories retained.
M owner-count repair complete is not original16 missingdata fill. Wexistingmaster/Eprep preserved. O Ramsey cancelled190/444/samplecomplete; otherdirectoryprefixes not fullratios. No hotdelivery/dispatch/consumption claimed. No new Agent/session/queue/UI/network/Tailscale/server/credentials/CronJob/target/frequency/resources/foreign implementation edits.
A/Cnoveltydowngraded;Bglobalbudget/globalphaseweights/causalrepeats/software/axioms/cluster/nativebaseline/Envelope complete single-configpair remainmissing. Self-review/ordinarypush notOSDIacceptance.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0277 — fixed-work PMU counters and covered-domain uncertainty','# Root step0277 outer audit — 自审')+'\n## Outer disposition\nBoth nodes change interpretation within existing RQs. Whole-command counters narrow hypotheses without unique attribution. Conditional sampling uncertainty remains broad despite narrower missing-cost scenarios. No mechanism promotion or completed/cancelled queue restoration. Actual build and complete-page review follow below.\n')
shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0277-recompute.py',e/'step0277-recompute.py')
print('EDIT277',str(s),len(t)-len(old))
