from pathlib import Path
import os,json,gzip,shutil,re
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-hybrid-source40-root-step.txt').read_text().strip());e=s/'experiment-001'
m=json.loads((e/'reanalysis.json').read_text());w=json.loads((e/'source40-reanalysis.json').read_text());rel=str(s.relative_to(r)).removeprefix('docs/')
body=f'''## Entry and scientific contract
Latest direct user decisions, canonical0284, questions-for-author, root0284
both reports and actual M073/074/W115 reports read. BUILD_AND_EVALUATE keeps
the title/fullabstract/fourRQ/sectionhierarchy/fourdesignimplication bodies.
The auto-research-orchestrator skill supplies the existing gate/report workflow.
User forbids new agents; both reports are self-review, not independent audit,
completed research or OSDI acceptance. No new experiment admission/native run,
agent/session/queue/foreign implementation or infrastructure change.
Sameboot585778d2-4fc1-48f5-aa9d-01cb7301e944/6qph8/phobos-vt.
Any later outage preserves scene and waits user, without recovery/scheduling.
Reboot-interrupted attempts remain excluded from cost/censor/complete samples.

## EXPERIMENT_GATE — node1: completed Hybrid policy ablation
[Root reducer](experiment-001/step0285-hybrid-recompute.py),
[reanalysis](experiment-001/reanalysis.json),
[all sixteen processes](experiment-001/sixteen-hybrid-control-processes.csv),
[plain medians/ranges](experiment-001/hybrid-three-repeat-summary.csv),
[diagnostic phases](experiment-001/diagnostic-phase-reconciliation.csv).
Raw parallel-stream-wall-hybrid-20261103; eight finite controls, two diagnostic
and six plain processes all actualcomplete. Source diff against qualified0284
retains ParallelStream/checked_commit/placement_profile bytes; Core adds
complexPrefix and flag-selected partition only. Existing makePlan/original
Kernel.addDeclCore/proof conversion/checked-token commit remain.
ComplexPrefix starts safe nonordinary names, follows incoming used constants,
retains their ordinary prerequisites, uses original replay then plans remainder.
No axiom skeleton or mathematical proof rewrite; prefix/FFI/quiescence/context
and coordinator code remain trusted, not unchanged implementationTCB.

All8full processes have exactordered4449unique accepts/header/imports/counts
against actualoldv14serialreference,425463entries/3595unsafe-partial exclusions/
0modulelocalfallback. Plain does not emit per-module observedchecks/HBvector.
All1231oldcomplex fallbacks become hybrid routes;3218ordinary routes unchanged.
183645safe incoming CIs partition into168713ordinaryparallel and14932prefix:
1636ordinaryprerequisites/3819inductive/5542constructor/3931recursor/4quotient.
These are CI counts, not time weights or independent inductive groups.
Sameordinary-route diagnostic check/HBvectors match; total observedcoverage
changes237863/3283925639 to406576/3968705445, not extra whole mathematical work.

Wholefallback/prefixonly plainwall medians257.658745209/196.669274689s;
ranges257.409904–257.710752/194.488453–199.060219.
CPUmedians542.368921/542.941920s; ranges541.691296–543.049094/
539.967844–544.445873. Ratioofmedians1.310111839,wall-23.670638647%,
CPU+0.105647462%. Same-repeat ratios{m['same_repeat_ratios']}.
Medianwait4HWM3373400→3436472KiB,3.217→3.277GiB,not precise objectretention.
Sampled/charged peaks separate inCSV. Threefixedrepeats withsecondorderreverse,
cachesretained; no CI/no-overhead guarantee. This is same8workerpolicy ablation,
not originalserial/stocknativebaseline/service/wholelibrary gain.
Do not multiply Math/Grid/marking ratios or divide oldserial bynewarm.

Diagnostic ownwalls271.180807703/211.674932751s,CPU551.571132/560.544735.
Source time windows read after imports-read call/context audit separately,
plan measured before prefix replay, profile fallback prefix replay, batchmetrics.
Wholemodulefallback94.478685745→1.792398284s; parallelbatches112.950909606→
141.024025570s. Read/context/plan4.166110058/25.539828409/8.897425909 versus
0.311630888/25.671300918/13.172920960s; duplicates0.028511984/0.028728065;
unassigned25.119335992/29.673928066, residualnotOSidle/purecoordination/waste.
Readcache/observerdifferences notisolated. No interpolation toplainmedians or
user~299s; old115fallback is anothercapture. Prefix1.7924 is conservativepolicy,
not proved intrinsicseriallowerbound. Full traces frozen but per-jobmodel/
wavebounds not independentlyrootqualified inthisstep; owner166/138model not
adopted. Old294diagnostic/~299partition remain separatelyPartial.

Fourpositivecontrols accept2modules; fourbadproofcontrols acceptInit.Prelude
then originalkernel explicitlyrejects good withlooseboundvariables,rc1.
Finitecontrols not arbitraryextension/context/unsafeFFIproof or fullrealbadroot
replacement. Samecommand noM(evenM0omitted)/P0–7/blockingpercellpcorelease/
1100native/14GiBcharged+14GiBsampleownRSSresponse.16cgroupsabsent/noOOM/
sample-stop/wait4complete;32actualnative/sampledPIDbirths retired.
No inventedcheckingTIDbirth/launcher or whole16GiBlanetree/hardRSSqualification.
Clock Popenbefore→wait4after; samplerjoin/delete/queue excluded.
Runtime flags/paths from frozenrunner,not per-openexecutiontrace.
Controller23773/birth922484 remains separate, runs historicalprotocol continuation;
completedcells do not imply its retirement. Root no signal/resume/dispatch.

RootMoffline{m['root_analysis_seconds']:.6f}s/{m['root_analysis_maxrss_kib']}KiB/E22–23.
Raw/source/commands/stdout/stderr/memory/terminals/trace/ownerreports archived
{m['archive_B']}B/{m['archive_members']}members/{m['archive_payload_B']}payloadB,
read throughgzipEOF/CRC. NoSDK/ELF/buildtree intoGit; ownerfailedbuilds retained.

## EXPERIMENT_GATE — node2: fixed original PacketLocality and uncertainty
[Root reducer](experiment-001/step0285-source40-recompute.py),
[reanalysis](experiment-001/source40-reanalysis.json),
[fixed frame](experiment-001/source40-frame.csv),
[forty costs](experiment-001/source40-costs.csv),
[twenty variance terms](experiment-001/source20-variance.csv),
[scenarios](experiment-001/source40-scenarios.csv).
Raw openai4341-noM-final-PacketLocality-targetP-remaining-four-hostrecovery-
20261103T1512; actualterminal17:50:35.232134UTC1planned/1compile_ok.
34579sourcebytes match existing4eaee875pin, no newdownload/census.
23.155user+1.012262system=24.167262CPU-s/nativewall16.947551851s.
Controller262.006130657s; residual245.058578806 includesqueue/setup/cleanup,
ownerrow245.052072035 is anotherboundary, not exactsame/purewait.
noM/j8/P0–7/unprofiled/authoredHB/3facets/1200actualselfwall,not1700pool.
15GiBcharged+16GiBsampleRSSresponse; HWM7400788KiB/sample7578406912B/
charged893702144B separate. Native29556/birth1093783+controlleridentity
actualretired,cgroupabsent/noOOM/stop. C52391/olean2605568/ilean156344B
actualsizeschecked. UntimedEdeps not drawweights or rootcoldtransitiveaudit.

Prior39ownframe cost/raw links unchanged; onlyPacketadded; Wpublished40rowsmatch.
40/42originals,2ordinarymissing;20/21complete strata/163057of163097modules.
All9markedcells/5848filesunchanged;40moduleordinarycellhas0of2.
Actualsum978.678429CPU/651.159591292nativewall-s.
Conditional278.091767959CPUh/marked57.546404277=20.693314548%;
summednativeelapsed242.289717194h/marked40.018606450=16.516840629%.
Prior19cell23.311/18.595% usesdifferentdomain,not temporal/samepopulationtrend.
KnownHTsubtotal278.091767959h hereequalscomplete20subtotal;notfullpoint/
lowerCI/zeroimputation. Missing2each+1CPU-s adds0.011111111h.

Independent N²(1-n/N)s²/n variance36409250823.301125CPU-s²,
Satterthwaite2.608579055; independentStudentdensitySimpsonintegration/bisection
critical3.470416608 gives coverednominal95%94.148040145–462.035495774CPUh.
Matchesownerwithin1e-6. n2/cell fragile, excludes40modulemissingdomain,
nonresponse/runtime/protocoltransferuncertainty; notfullframeCI/guarantee.
Old19interval43.99–449.74retainedhistory,notcurrent.
Observedordinarysupport1.204525–86.977989 unchanged;40known+2missing source
278.105151571–279.058190059CPUh,outward278.1–279.1.
Separate mixedcheckpointordinary0.063124174–0.089514277/oldunsegmentedcompute
0.084421495–0.084671469transfer18.780742224–24.701005939h,outward18.7–24.8.
Neither matchedfullchecking/CI/guaranteedgain. Missingrange narrow doesnot
remove samplingvariance. No-assumptionupperunbounded;10xordinarymaxsource
287.755988959h. OldLowBlock/Allocatedsupportcounterexamples remain.
Paired31/42/14/11missing,dynamic13/RQ2CPU6.31/8.95andwall9.26/10.56/14.67,
B2524/30288/22716and100/50overlap denominators untouched.

RootWoffline{w['root_analysis_seconds']:.6f}s/{w['root_analysis_maxrss_kib']}KiB.
Rawsourcearchive183941B/45members/1820569payloadB fullyreadgzipEOF/CRC.
Initialrootonlyreducer varianceCSV handle shadowed transferfactor, failed final
output after reads; exactfailedsource/errorreceipt preserved, renamedhandle and
reran offline only. No native/raw/PDFscientificrun changed or imputed.

## WRITE_GATE
ActualMethods/RQ1 currentcoverage/domain/clockshares/CI/subtotal/scenarios updated;
RQ3 adds same-executablehybrid plain+distinctdiagnosticwindows/trustlimits.
No newtable;20oldtablebodies/title/fullabstract/4RQ/sections/4implicationbodies
preserved. Canonicalstatus/plan/index/evaluation/novelty synchronized.
OldGrid/Math/historicalunmarked/nativestock/Ramsey/Falconer controls remain
their originalscopes. No fullwriting/idearefinement/newresearchcontract.
Rootcannotfillglobalweights/software/axioms/cluster/nativebaseline/Envelope
fullsingleconfigpairwithlocalresults. A/Cgenericnoveltydowngrade/Bglobalbudget
unproven unchanged. ExistingownerGroundEprep andfragmentretest autonomous.

## REVIEW_GATE — self-review and routing
Accept actual16Hybrid and1originalcost plus independentlyrecomputed20cell
uncertainty. Root per-jobmodel not qualified; keep distinctPartial~299/294models.
No fixedintrinsicserialfraction/OSidle/stockgain/wholelibrary or servicespeedup.
No recovery/infra/network/credentials/UI/CronJob/resource mutation.
Frozenfields/link/citation/fullcompile/all-page staticreview follow.
Onlyownedpathsordinarymaincommit/push; no stash/reset/amend/force.
Next root action reads actualnewterminals/identities; no completedpoint rerun.
'''
(s/'step-report.md').write_text('# Root step0285 — Hybrid fallback and source40 (self-review)\n\n'+body)
(s/'outer-audit.md').write_text('# Root step0285 outer audit — self-review\n\n'+body+'''
## Outer disposition
Two completed owner evidence nodes strengthen the existing characterization.
The prototype serial policy is avoidable on this closure, while residual prefix
seriality is unproved. Population coverage is nearly complete in module count,
yet sampling precision remains weak. Neither supports generic newmechanism
firstness or finished research. User no-agent decision makes this self-review.
''')
note=f'''## Hybrid fallback and source40 — root0285

[Root report]({rel}/step-report.md). Same8worker/defaultpersistentexecutable:
wholemodule versus dependencyclosednonordinaryprefix,6plain/2diagnostic/
8finitecontrols complete. All8full4449orderedIDs/imports/counts equal original
serialreference;425463entries/3595exclusions/0modulelocalfallback.
Plainwallmedians257.658745→196.669275s,1.310111839ratio/-23.67064%;
CPU542.368921→542.941920s/+0.10565%,notzerooverheadguarantee.
1231complexmodules move168713ordinaryCIs toparallel,14932prefix remains.
Diagnostic94.479→1.792s upstreamreplay usesown271.181/211.675sdenominators,
notplain/~299. Prefixnotintrinsicseriallimit; no multiplicationwithMath/Grid.
16cgroupsabsent/32actualPIDbirthsretired; controllercontinuationseparate.
Finite4positive/4kernelbadproofrejections, notarbitraryFFI/contextproof.
Fulltraces frozen; per-job/wavemodel not independentlyqualified.

WPacketLocality24.167262CPU/16.947552wall-s,exact34579pinnedsourceB,
1200selfwall/noM/j8/P0–7/authoredHB/3facets/15GiBcharged+16GiBsampleRSS.
Native/controllerretired/cgroupabsent/noOOM/stop;Edepsunweighted.
40/42originals/20completecells/163057modules;2ordinarycosts/40moduledomain
missing. ConditionalCPU278.091768h/marked20.693315%;elapsed16.516841%.
Coverednominal95%94.15–462.04CPUh/df2.60858,n2fragile/notfullframeCI.
KnownHTsubtotal278.091768h notfullpoint/lowerCI/zeroimputation;
missing2each+1CPU-s adds0.011111h.
Sourceassumption278.1–279.1CPUh; separatemixedtransfer18.7–24.8CPUh.
Narrowcompletionrange isnot samplingprecision/fullchecking/gain.
No-assumptionupperunbounded;10xordinarymaxsource287.755989h.
Old39ranges/19cellshares/CI staydatedhistory. Paired31/42/14/11missing,
dynamic13/RQ2/Bdenominators unchanged. No newnative/agent/session/queue,
foreignimplementation/infrachange. Lateroutagepreserves scene/waitsuser.

'''
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;t=p.read_text();a=t.index('## Corrected Grid and source39');b=t.index('\n## ',a+4)
 t=t[:a]+note+'Prior [root0284]('+str(Path(rel).parent/'step-0284-20261103T172738+0000/step-report.md')+') qualifies Grid12/Math9complete matrix; serial/4/8ratios2.125/2.532 and prior source39 unchanged in history.\n'+t[b:]
 t=t.replace('root0284.', 'root0285.').replace('Source3/paired11','Source2/paired11').replace('3original source costs','2original source costs')
 # Current table rows only; all detailed historical entries keep dates.
 lines=t.splitlines()
 for i,l in enumerate(lines):
  if l.startswith('| Source probability frame |'):lines[i]=f'| Source probability frame |40/42originals;20/21complete strata/163057modules. ConditionalCPU20.6933%/elapsed16.5168%;2ordinarycosts missing/40moduledomain. | [0285]({rel}/step-report.md) |'
  if l.startswith('| Whole-frame scenarios |'):lines[i]=f'| Whole-frame scenarios |40known+2ordinarymissing source278.1–279.1CPUh; separate mixedtransfer18.7–24.8CPUh. Assumptions, notCI/fullchecking. CoverednominalCI94.15–462.04/df2.61 remains fragile. | [0285]({rel}/step-report.md) |'
  if l.startswith('Current source39data '):lines[i]='Current source40data:20completecells/163057modules,conditionalCPU20.6933%/elapsed16.5168%. Coverednominal94.15–462.04CPUh/df2.61 remains fragile; missingcostscenario278.1–279.1/transfer18.7–24.8 answers a separate question. No-assumptionupperunbounded; old31inputforecast unchanged.'
  if l.startswith('| W source continuations |'):lines[i]=f'| W source continuations |Source40/42/20strata,2missing. Dependencies/censors receive no original-draw weights. | [0285]({rel}/step-report.md) |'
 t='\n'.join(lines).rstrip()+'\n';p.write_text(t)
p=r/'research/README.md';t=p.read_text().replace('root0284.','root0285.').replace('and current39-draw271.6–296.8CPUh','and historical39-draw271.6–296.8CPUh')
t=t.replace('## Latest complete results\n','## Latest complete results\n\n- [Hybrid policy and source40](../docs/'+rel+'/step-report.md):6plain/2diagnostic/8controls complete, same4449accepts;wall-23.67%/CPU+0.106%. Source40/42/20cells,nominalcoveredCI94.15–462.04CPUh;sourceassumptions278.1–279.1 and mixedtransfer18.7–24.8CPUh,notfullframeprecision/gain.\n')
p.write_text(t)
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text().rstrip()+'\n\n'+note)
shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0285-paper-edit.py',e/'step0285-paper-edit.py')
print('DOCS_REPORTS_WRITTEN',s)
