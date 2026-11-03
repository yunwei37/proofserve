from pathlib import Path
import json,re
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-persistence-pmu-memory-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text());suffix=s.name.removeprefix('step-');rel=str(s.relative_to(r));drel=rel.removeprefix('docs/')
p=r/'docs/paper/main.tex';t=p.read_text()
old='The remaining planned counter cells are outside this admitted subset.'
assert t.count(old)==1;t=t.replace(old,'The remaining counter cells were subsequently collected and are reported below.')
anchor='\\paragraph{Pooled certificates pass a broader native qualification.}'
new=r"""
\paragraph{The complete counter matrix supports the prototype correction.}
\measured{\expref{"""+suffix+r"""}{0280}; all eight stat cells, one observation per arm/worker setting.}
The remaining six stat processes complete the 32-cell primary matrix,
together with the already reported 24 plain and two one-worker stat runs.
All 56 counter readings report 100\% running time, with the same accepted
module graph and per-module check/allocation vectors.
At eight workers, persistence reduces retired lock-load events from
5,818,993,726 to 112,656,010 (98.06\%), modified-line forwarding from
779,885,830 to 43,550,844 (94.42\%), and demand-RFO snoop-HITM responses
from 517,381,271 to 143,426,518 (72.28\%).
User-mode cycles fall 14.42\% and aggregate IPC rises from 1.697 to 2.006,
while instructions increase 1.172\%.
L3-miss loads increase 0.762\% at eight workers and also increase at two
and four workers: the intervention does not generally reduce ordinary misses.

Within this same stat matrix, moving from four to eight workers increases
user cycles 8.431\% without marking and 0.679\% with marking.
Modified-line forwarding grows 47.616\% versus falling 0.883\%;
RFO snoop-HITM responses grow 50.308\% versus 10.852\%.
These outcomes strengthen the prototype-lifetime explanation while
preserving the distinction between event counts and stall time.
The two coherence event types are not disjoint counts to sum.
The marked runs retain positive total-CPU growth, rising system time and
a changing cycles/reference-cycles ratio; effective frequency is uncontrolled.
Whole-command user counters exclude system execution and are not gated
to original-check brackets. One stat observation per setting supplies no
repeat confidence interval, and stat clocks do not enter the plain medians.

\paragraph{Aligned memory snapshots bound a finite resident tradeoff.}
\measured{\expref{"""+suffix+r"""}{0280}; separate observer-enabled eight-worker pair.}
Two further full-closure processes record \texttt{smaps\_rollup} after every
module, giving 4,449 boundaries per arm matched by module ID, input entries,
checks, allocation units and cumulative frontiers.
At the final heavy module, marking adds 7,315,456 bytes of anonymous memory
(6.98\,MiB) and 7,708,672 bytes of RSS (7.35\,MiB).
Across prefixes the anonymous-memory difference ranges from about
$-208$ to $+265$\,MiB and is nonmonotone.
These net resident differences include allocator/layout and transient-storage
effects; they do not measure the exact objects retained by persistence.
No checkpoint reports swap, but snapshots and one-second tree sampling
cannot rule out unobserved transient behavior.

The memory-observed runs use 63--69 system-CPU seconds, compared with about
ten seconds in the primary eight-worker runs.
Their clocks are separate diagnostics, not additional plain replicates or a
production speedup. Persistence still delays reclamation until process exit.
This one completed pair neither establishes a full-library memory bound nor
an unbounded resident service, and cannot project the incomplete compiled
AI-library subset onto the full source population.
"""
assert t.count(anchor)==1;p.write_text(t.replace(anchor,new+'\n'+anchor))
note=f'Root0280 independently completes qualification of the primary32 through root0279’s26 plus remaining6stat natives, and separately qualifies the complete2native aligned-memory pair. [Report]({drel}/step-report.md): 8P lockloads−98.06%/modifiedlineforwarding−94.42%/RFO−72.28%,cycles−14.42%,instructions+1.172%,L3miss+0.762%;56readings100%running. Whole-command user counters/one stat per setting, not RCstall seconds/CI. Memory finalAnonymous+6.98MiB/RSS+7.35MiB,nonmonotone prefix deltas; not leaked-object bytes/full-library fit. Stock/bad-root controls require their actual separate latest qualification. Prior0279storage15.172GiB was completed, never recounted.\n'
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text().replace('root0279.','root0280.',1)
 v=re.sub(r'^Root0279 user-directed correction:.*$',note.strip(),v,flags=re.M)
 if n.endswith('research-plan.md'):v=re.sub(r'^Current owner read.*$', 'Current primary32 is complete and root-qualified through prior0279 plus remaining6stat; aligned memory2native pair also separately qualified. No native/queue restart. Stock/bad-root and W/O progress are governed by latest actual terminals, never prepared reports.',v,flags=re.M)
 p.write_text(v)
p=r/'research/README.md';v=p.read_text().replace('root0279.','root0280.',1);entry=f'- [Complete persistence PMUs and aligned memory](../{rel}/step-report.md): remaining6stat complete primary32qualification;8P lockedloads−98.06%/modifiedlineforwarding−94.42%/RFO−72.28%,ordinaryL3miss+0.762%. Separate4449matched-boundary memory pair endsAnonymous+6.98MiB/RSS+7.35MiB,not precise retained bytes or global fit. Original proof/kernel retained;unsafequiescence/coordinator still trusted.\n\n';p.write_text(v.replace('## Latest complete results\n\n','## Latest complete results\n\n'+entry))
p=r/'docs/novelty-20261101.md';p.write_text(p.read_text()+f'\n## Root0280 — complete causal counters and finite memory diagnostic\n{note}This is a method correction to our prototype, not novel persistence/parallel checking or a Lean/workload intrinsic law. Historic unmarked gains and all wider missing denominators remain.\n')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+f'\n## Root0280 — remaining primary PMUs and complete aligned-memory pair\n[Step]({drel}/step-report.md), [outer self-audit]({drel}/outer-audit.md). {note}No new native verifier/Agent/queue; original raw retained.\n')
report=f"""# Root step0280 — complete persistence PMUs and aligned resident-memory diagnostic
**自审; not independent review, research completion or venue acceptance.**

## EXPERIMENT_GATE
Existing BUILD_AND_EVALUATE/RQ3. Entry rereads latest direct user words, canonical0279, both0279reports and latest actual M primary/auxiliary terminals. No new native experiment, Agent/session/queue or foreign implementation edits. No idea/whole-writing/milestone-review invocation. Contract unchanged: characterize checking/recomputation and the actual method/trust boundary.

### Node E1 — finish primary32 through previously qualified26 plus remaining6stat
Root0279 already independently qualified24plain+P1stat2+13correctnesscontrols; no repetition/relabeling of that completed work. This step directly reads the six missing2/4/8worker flag0/1 stat command/result/stdout/stderr/memory/terminal. Rebuilds all six4449uniqueheader/accept imports/constants against original v14serial accept schema;425463entries/3595unsafe-partial exclusions/0contextfallback. Exact per-module work equal,237863checks/3283925639units. Each18990root is ST before, offST after noop/MT afterenqueue or markedpersistent aftermark/afterenqueue.
All32frozen primary keys in originalterminal return wrapperrc0/statecomplete at12:52:54UTC; no auxiliary timing enters this fixed32. Read all8actual stat JSONs without owner reducer import:56readings,7events each,100%running. Source9files byte-equal to0279rawfreeze, same declared executable path/buildsource; no per-openfile or invented per-invocationenv trace.
At8P off→on cycles1969934773331→1685877381562(-14.419634%), instructions3343139005793→3382326167887(+1.172167%),lockloads5818993726→112656010(-98.063995%),modified-lineforwarding779885830→43550844(-94.415741%),demandRFOsnoopHITM517381271→143426518(-72.278371%),L3miss532289687→536343258(+0.761535%). XSNP_HITM selector is the previously qualified XSNP_FWD alias; event types not summed or RC-exclusive stall seconds. AggregateIPC1.697081→2.006271,notmeanofworkerIPCs.
Matched4→8 stat changes off/on: cycles+8.430829/+0.679347%,instructions+0.040554/+0.027543%,forwarding+47.615997/−0.883124%,RFO+50.307734/+10.852398%. OrdinaryL3miss rises at2/4/8P treatment;notgeneralcachemissreduction. Wholecommandusermode excludeskernel/systemCPU and is not bracketgated. Marked4→8totalCPU/systemtime remain positive andcycles/refchanges;nofrequencycontrol/exactatomicstallfraction. Eachstatsetting1observation,notrepeatCI/statclockpooledinto24plain.

### Node E2 — separate complete observer-enabled memory pair
Actual run keys are full-plain-m0/m1-P8-memory-r1, launched via aux-memory-m0/m1-P8. Initial read of nonexistent runs/aux-memory-* corrected from actual auxiliary.py naming, not a native failure/retry. Complete planned2native/oneperarm separatefrom32primary. Original frozen sourcehook DECOUPLED_MEMORY_PROFILE/STEP1 reads own smaps_rollup after every acceptedmodule. Native/raw/all4449checkpoints perarm read;8898snapshots aligned on cumulative moduleID/inputentries/checks/HB/frontiers,including heavy finalBarrierData41. Allgraph/workvectors exactly equal primary.
FinalAnonymous527917056→535232512B(+7315456B=6.9765625MiB);RSS3131170816→3138879488B(+7708672B=7.3515625MiB). PSS+8096768B,PrivateDirty+7315456B. Across4449matchedboundaries anonymousdelta min−218017792/max277487616B,notmonotone. No sampledSwap at8898checkpoints. Netresidentdifference is not exactretained-object bytes;layout/allocator/transientworkingstore remain. Nofull-librarysource extrapolation/guaranteedfit/leakbound/servicegain.
Diagnosticoffwall379.479240s/user717.943755/system68.551252;on355.148637/user613.137557/system63.182173. High systemcost is separateobserver-enableddiagnostic,notnewprimaryrepeats orisolatedobserveronlycausaloverhead. Originalprimitive logically retainsmarkedobjects untilprocess exit;smallnetRSSdoesnotdisproveit.

### Node E3 — resource/lifecycle/source qualification
All8newselectednative rc0/noM/P0–7/14GiBcharged+14GiBsampledownRSS/wait4complete/noOOM/noRSSstop/cgroupsabsent. 34actualemitted native/sampledchild/auxcontroller/primarycontroller/finalrequest PIDbirth identities rootcheckedretired. No fabricated launcher/checkingTIDbirth. Sameblockingpcorelock/native1100/outer1740afterlock fromfrozenrunner/actualauxlaunch. Nativeclockendswait4,beforesamplerjoin/cgroupdelete;queueexcluded. HWM/treeRSS/chargedpeaks are distinct in CSV; nothardRSS/whole16GiBlane-treeaudit.
Original mathematical Kernel.addDeclCore/proofs unchanged; officialmark primitive atquiescentdeclaredenqueue site remains unsafeadapter/coordinatortrust, not arbitraryextension/TCB unchanged. Prior13controls remain0279,notnewcorpus. Source/runners/raw8+56counterJSONs/terminal/reference/ownercurrentreports retained in [new raw/source](experiment-001/new-qualified-raw-source.tar.gz),12124594B;5CSVs includingall4449aligneddeltas. Rootanalysis11.097518s/58008KiB/E22–23,zero nativeverifier/Agent. NoSDK/ELF/buildtreecopiedintoGit.

## WRITE_GATE
Actual RQ3newparagraphs report fullPMU pattern and separatememorytradeoff,notonlyrecords. Old0279plain/P1numbers and historicalunmarked3.33×/1.52×/1.88× retained; remaining-counter sentence updated to subsequentcompletedresults. All20oldtablebodies/title/fullabstract/4RQ/sectionhierarchy/4designimplicationbodies frozen. No newtable. Canonicalstatus/plan/index/novelty/evaluation synchronized. AllRQ1source38/weights/CI/scenarios,RQ2CPUwallratios,RQ4census/overlap denominators unchanged.

## REVIEW_GATE — root self-review
Direction: finite prototype method correction and scoped residenttradeoff only; no genericLeanlaw/novelpersistence/uniqueRCstall fraction/exactleak/whole-librarymemoryfit. Completeplannedprimary32 andcompleteplannedmemory2pair admitted; stock/default/fresh/real-rootfaults remainseparateactualqualification,notfilledfrompreparedoroneintermediatecontrol. No rootdispatch/hotdeliveryclaim/newqueue/nativebudget/infra/network/UI/CronJob/permission/resourcechange. W/Oexistingowners protected. Root0279historicalcleanup targetalready met15.172115GiB/<75%;this stepdoesnotrepeatthatcleanup orcreditconcurrentdfmovement. Fullcompile/allpage selfreview follows; raw/failed/partial/history retained.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0280 — complete persistence PMUs and aligned resident-memory diagnostic','# Root step0280 outer audit — 自审')+'\n## Outer disposition\nAdmit complete remaining6primary plus separatememorypair. Wholecommand events and snapshot net-memory effects preserve their distinct scopes; onepair is not a population fit. Preserve prior raw qualification and unsafe trust limits. Open RQs remain, so no milestone acceptance or new experiment authorization.\n')
print('EDITED',s)
