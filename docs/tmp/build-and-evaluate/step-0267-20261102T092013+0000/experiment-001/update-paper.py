from pathlib import Path
import os,json,re,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-stream-bytes-root-step.txt').read_text().strip());e=s/'experiment-001'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
user=(r/'docs/user-instruction.md').read_text();questions=(r/'docs/questions-for-author.md').read_text()
t=(r/'docs/paper/main.tex').read_text()
old='The separate resident-leaf determinism experiment is not a result of this curve.'
new='The separately instrumented resident-leaf observation in Section~\\ref{sec:meaning}\nuses different output and timing boundaries; its counts and leaf costs cannot\nreplace these complete-process observations.'
assert t.count(old)==1;t=t.replace(old,new)
insert=r'''\paragraph{Parallel checking preserves observed counts and serialized payloads.}
\measured{\expref{0267-20261102T092013+0000}{0267}; finite streaming and serialization comparison.}
A separate v16 process checks Barrier's 4,448-module dependency prefix,
then repeats its entire 3,425-declaration leaf in six waves at per-wave
worker caps 1, 4, 8 and 16, three times each, reversing order in the middle
repeat.
The 100 observed helpers are evenly spaced in the sorted eligible list
and overlap the earlier Barrier census; they are not additional independent
targets or a new population sample.
All 1,200 observed checks accept, and every target has zero allocation-count
range across its 12 observations: both P95 and maximum are 0\%.
All leaf constants structurally match the one-worker reference.
Each trial substitutes all 3,425 checked constants into the module metadata
and actually serializes an output: all twelve 9,160,440-byte
\texttt{.olean} files match one another and the original input byte for byte.
Only that one artifact part exists for this input; no absent companion is
counted as equal.
Extension metadata retains the input policy and is not independently
revalidated. This establishes neither whole elaborator/axiom equivalence nor
byte identity of every transitive artifact.

These observer-enabled trials share a resident checked prefix and the
allowed 8P+8E mask; workers may migrate within it.
Median leaf wall decreases from 50.358 to 9.033 seconds at caps one and 16,
while leaf process CPU rises from 50.334 to 139.099 seconds.
Those windows include leaf planning/checking/structural audit and observer
work, but exclude the following serialization; they are not unprofiled
complete-process throughput.
CPU summed inside the same 100 executing-worker call windows rises from
3.575 to 9.941 seconds despite fixed allocation counts.
The clocks include counter reads around the original-kernel call and
precede per-row logging; no cause among placement, frequency, contention
and other runtime effects is isolated.
Distinct TIDs accumulated over six waves are unions over time, not
simultaneous concurrency counts.
The complete native process takes 556.858 seconds and 1,651.508 CPU seconds,
including prefix checking, all twelve trials and all serialization.
This finite result strengthens the prepared-stage count and output boundary,
without establishing zero observer/runtime cost, native kernel poll counts,
a near-threshold budget guarantee or a future-machine property.
It is separate from both the earlier 2,524-target protocol and the
negative heterogeneous complete-closure curve.

'''
idx=t.rfind(r'\paragraph{System-design implication.}');assert idx>t.index(r'\paragraph{RQ4:')
t=t[:idx]+insert+t[idx:];(r/'docs/paper/main.tex').write_text(t)
rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');link='[0267]('+drel+'/step-report.md)'
for n in ['docs/research-status.md','docs/research-plan.md','research/README.md']:
 p=r/n;x=p.read_text().replace('root0266','root0267')
 label={'docs/research-status.md':'Exact previous status','docs/research-plan.md':'Exact previous plan','research/README.md':'Exact previous index'}[n]
 target=drel+'/experiment-001/before-'+n.replace('/','-')+'.gz'
 if n.startswith('research/'):target='../docs/'+target
 x=re.sub(r'\['+label+r'\]\([^)]+\)','['+label+']('+target+')',x,count=1)
 if n=='docs/research-status.md':
  row=f'| Streaming count/bytes |100overlapping Barrier helpers×12observations at1/4/8/16caps,1200accepted,allcount ranges0%.12actual9,160,440B.oleanfiles equal each other/original;3425checkedpayloads substituted,extensionmetadata trusted. UnitCPU3.575→9.941s;not zero runtime or globalbudget. | {link} |\n'
  x=x.replace('\n\n## Terminal failures and trust that remain visible','\n'+row+'\n## Terminal failures and trust that remain visible')
 elif n=='docs/research-plan.md':
  x+=f'\nStreaming leaf count/byte capture now independently qualified by {link}:100targets overlap oldBarriercensus;12full-leaftrials/1200acceptedobservations/12exactoleanoutputs complete. Do not wait/restart17c4989; no globalmaxHB/TCB/property upgrade or poolingwith2524census. Existing ownerroutes handle further work.\n'
 else:
  row=f'- [Parallel count and byte comparison](parallel-stream-check/extended-results/parallel-determinism.md):100overlapping Barrier helpers/1200acceptedchecks at1/4/8/16caps×3,allcount ranges0%;12actual9,160,440Boleanoutputs equal one another/original. Checked3425constantpayloads,retainedmetadata trust;CPU still varies. [Root0267](../{rel}/step-report.md).\n'
  x=x.replace('## Existing research directories',row+'\n## Existing research directories')
 p.write_text(x.rstrip()+'\n')
p=r/'docs/novelty-20261101.md';p.write_text(p.read_text()+f'\n## Root0267 — streaming count and mathematical-output stability\n{link}. A newly checked4448-moduleprefix and12complete3425-declaration leaf\ntrials yield100overlapping targets×12=1200acceptedobservations with0range,\nP95/max0%,and12serialized9,160,440Boleanfiles byte-equal to each other/original.\nOriginal-kernel checked constants substitute into retainedmetadata; extension\nentries are not revalidated. Only1actualartifactpart,not alloutputs/bootstrap.\nCall-windowCPU3.575→9.941s while counts stayfixed; no free runtime/observer,\nnativekernelpoll/globalcandidate/near-threshold/future guarantee.100targets\nare selected from oldBarrier1320,not100newindependentcomputationalworkloads.\nPrepared-stage evidence strengthens within the existing characterization,\nwithout newdeterministicbudget/parallelchecking mechanism firstness.\n')
step=f'''# Root0267 — streaming counts and serialized mathematical payloads (自审)
2026-11-02UTC; BUILD_AND_EVALUATE; parent0266/8e5c2e3.
Exactly2rootMarkdownreports,self-review not independent audit or venue acceptance.
User words/questions/current canonicaldocs and prior0266reports read.
No newuser instruction/scientificcontract/agent/nativequeue/foreignedit.

## EXPERIMENT_GATE — qualify completed owner handoff
RQ4 concerns which observed checking/outcome/artifact boundaries are established.
M17c4989 [step](../../../../research/parallel-stream-check/step018.md),
[audit](../../../../research/parallel-stream-check/step018-audit.md),
[result](../../../../research/parallel-stream-check/extended-results/parallel-determinism.md)
report the actual complete frozenv16capture. New experiment/skill/agent/full-run
loops skip because root must not duplicate already completed native work.
Root independently re-parses original stdout/command/memory/terminal/source,
compares the12actual9,160,440Bfiles against the original WnoM input and eachother,
and checks graph/set against retained fullserialreference.

Native rc0;4449unique moduleheaders/accepts, exact imports/counts and root
reachability;425463entries/3595unsafe-partial exclusions/0contextfallback.
4448prefix independently checked before12full-leaftrials,3425jobs/6waves each.
Exactly100fixed targets×12(worker,repeat)combinations=1200acceptedobservations.
Sorted1320oldBarriercensus helpernames reproduce the100rank-spaced selector
including endpoints. No new independent targets/families are added to2524.
Allper-target countspositive/equal,P95=maxrange0%;900same-repeat1-vs-higher
countpairs equal. Per-unit diagnostic vectors were not emitted,so no new
900diagnostic-equivalence claim is fabricated.

Actual all3425checkedConstantInfo substitutions plus structural one-worker
reference match precede native serialization.12actual.oleanfiles equaloriginal
and one another by byte comparison; snapshots say parts1, extension_entries_
revalidated=false. No private/server/IR/ilean/C or arbitrary metadata validation.
Native originalCheck usesforced noinlineIO original addDeclCore with actual
declaration/type/proof; heartbeat and CLOCK_THREAD_CPUTIME_ID reads bracketit.
Per-rowlogging follows these clocks. TIDunions2and17 in one/16captrials are
not concurrency counts. Processallowmask0–15(8P+8E) applies to alltrials,
prefix8workers; no static workerpinning or P/Ecausality.

Leafmedianwall50.358481430/16.003184325/10.320512182/9.032978400s;
leafmedianprocessCPU50.333893215/63.645761021/81.332565347/139.099353271s.
Serialization follows leafclocks. Sum100callCPU medians3.575259697/
4.471970042/5.829826470/9.940651023s:2.7804xone-to16 despite fixedcounts.
Whole native556.858207521wall/1651.508190CPU includes prefix+all12+serialization,
controller556.955056594s separate; not a singlemodeperformancegain.
All3actuallyrecorded PIDbirthidentities/controller406976/766076160 and
native406987/766076342 plus sampledLean child retire; cgroupabsent.
Wait4HWM3507392KiB/sample3591426048B/charged1282400256B separate;
noOOM or sampledstop, noM/14GiBexternalcharged. Not hardRSS/entireMlaneaudit.
Observed16CPUfootprint differs from old8-core summary; root doesnot change
runtimepolicy or retroactively authorize the extension.

Raw/source/command/stdio/memory/terminal andownerreports
[archive](experiment-001/stream-raw-source-and-owner-reports.tar.gz);
[units](experiment-001/units.csv), [targetranges](experiment-001/target-ranges.csv),
[leafsummary](experiment-001/leaf-summary.csv),
[actualbytecomparisons](experiment-001/artifact-byte-comparisons.csv),
[identities](experiment-001/retired-identities.csv),
[recompute](experiment-001/recompute.py).
Alllargeactualoleans remainoriginalPVCpaths, no redundant110MBGitcopy.
Post-run owneraffinity/default and byte-mismatch-outcome tests are implementation
repairs,not scientific observations. Frozenv16calls useexplicitmask and no
running code/binary is hot-edited byroot.

## WRITE_GATE — local result and boundary update
Re-read recordeduserintent. Preserve title/fullabstract/fourRQ/sectionhierarchy/
all19existing tablebodies/fourdesignimplicationbodies. Add two localRQ4paragraphs
for count/actualserializedoutput comparisons and CPU/timing/trust limits.
RQ3points to this separate boundary instead of implying capturestillpending.
No extra table, fullwritingrefinement/idea discussion or mechanismclaim.
Keep older2524/30288/22716panel separate; sample100isnot census2524.
Canonical status/plan/index/novelty/evaluation receiveactualcompletedlinks.
No Wsource/paired/dynamic denominators or O/Wclocktransfer models change.

## REVIEW_GATE — 自审 and meta-review
Freshindependentreview skipped by direct no-new-agent instruction; these are
same-rootstaticreviews and do not claim external acceptance.
Direction unchanged: two-cost characterization, RQ4 empirical boundaries.
Efficiency: no newnative/redundantcontrol; selectedbytecomparisons only.
Maintenance: retainallsource/failed/partial/raw/log/PDF and comparefrozenmetadata;
onlyroot's currentrenderings after all-pageview may be removed withmanifest.
Openobjections:1wholecandidate/kernelpoll/near-threshold guarantees;
2fullaxiom/context/declaration andcrossmachine/observer scope;
3native module-task baseline/cluster/completeEnvelopepair;
4globalphaseweights/source10/paired11/dynamic13/software gaps.
None invalidates this finitecapture; none is filled bystablebytes.
Owhole-library read2469source+10744dependencies with160628sourcemissing,notfull;
WreadHodge616current348withnooverallterminal,source32qualified remains.
Keepownerrequests/lockwaiters,do not reuse stalePIDs or restartcompletedv16.
Route: finish fullcompile/all-page self-review and oneownedmaincommit/push.
'''
(s/'step-report.md').write_text(step)
(s/'outer-audit.md').write_text('''# Root0267 outer audit — 自审
Same-root review, not independent or venue acceptance.
EXPERIMENT intake independently reconstructs100×12targets,900countpairs,
12fullleaf3425job/6wavecells and13actualbinary comparisons includingoriginal.
Selection reproducesoldBarrier1320rankspacing; no100newworkload/countpooling.
Full4449graph/refset/reachability, originalkernelcalls, serialization source
and native clocks/resource records inspected. Native3PIDbirth/cgroupretired.
Onlyoneartifactpart exists here; metadata/extensions staytrusted. Byteequality
is finite outputevidence,not wholeelaboration/IR/axiomsafety or unchangedTCB.
All16CPUallowedmask/workerTIDunions/callclockcounterreads disclosed.
UnitCPUvaries despite0countspread,observer/runtimefreedom notestablished.
WRITE changes local RQ4result and RQ3cross-boundary sentence, no newtable.
19oldtablebodies/title/abstract/RQ/sections/fourimplications mustcompareunchanged.
Fullcompile/render/allpages/preservation andGitpublication stillrequired.
No newnative/agent/queue/infra/foreignsourcechange; originalfailedbuildsand
post-runownerregressions retained butnot promoted to scientificsamples.
Meta-direction remains the fixed characterization; outstandingglobal,
budget/context/axiom/cluster/native-baseline questions remainexplicit.
''')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+f'\n## Root0267 — streaming count and serialized payload boundary\n[{s.name}]({drel}/step-report.md),[outer self-audit]({drel}/outer-audit.md).\nM17c4989completecapture independentlyreconstructed:100overlappingtargets×12,\n1200accepts/900countpairs0change;12actual9160440B.oleans equaloriginal andeachother.\n4448checkedprefix/12full3425jobleafcells,nottrustedimportsubstitution;\nmetadata/extensions stilltrusted,19oldtables/frozenstorypreserved.\nCPUcallwindow3.575→9.941s,not free overhead/globalbudget guarantee.\n3PIDbirth/cgroupretired;0newrootnative/agent. W32/Owholeprefix denominators unchanged.\n')
print('EDITED',s)
