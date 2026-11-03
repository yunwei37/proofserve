from pathlib import Path
import os,json,re,gzip,shutil
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-grid-source39-root-step.txt').read_text().strip());e=s/'experiment-001';m=json.loads((e/'reanalysis.json').read_text());w=json.loads((e/'source39-reanalysis.json').read_text());rel=str(s.relative_to(r)).removeprefix('docs/')
note=f'''## Corrected Grid and source39 — root0284

[Root report]({rel}/step-report.md). Root0283 Mathlib9 remains qualified;
all12Grid cells are now independently qualified and the21cell matrix has its
actual17:17:37UTC complete terminal. Source/runners equal root0283 frozen bytes.
Original serial/parallel1/4/8 wall medians561.213/581.429/264.097/221.614s,
CPU558.456/579.927/630.129/662.182s;4/8strongserial ratios2.125021/2.532391,
CPU+12.8342/+18.5737%.4to8wall-16.0864%/CPU+5.0867%;1worker slower.
All12ordered3793IDs/imports/counts exact historical original reference;
382707entries/3554exclusions/209672jobs/14887waves/0modulelocalfallback.
12cgroupsabsent/noOOM/sample-stop;25actualnative+controllerPID/birthsretired.
No profile/HB vector invented for plain runs. Kernel7.0.0-42 after reboot,
date/runtime/code/cache/order/host differences prevent old/new marking causality.
Oldunmarked1.882x four-worker pair retained;2.532x is new8configuration.
No full-library/source/service/cluster gain or universal coordinator safety.

W AllocatedForecastPrimitiveCapBound original returns79.405758wall/
86.977989CPU-s at17:07:47.727918UTC. Exact64383sourcebytes match pinned4eaee875;
noM/j8/P0–7/authoredHB/3facets/1200selfwall/15GiBcharged+
16GiBsampledRSSresponse. Native20800/birth830787 andcontroller20263/birth777032
retired;cgroupabsent/noOOM/stop. HWM9207032KiB/sample9414340608B/
charged1419362304B distinct. Controller616.925765s includesqueue/setup/
cleanup, not native cost. UntimedEdeps not weighted or cold-build requalified.

Fixed42IDs/strata unchanged; onlyAllocated added to ownprior38frame.
39/42originals,3ordinary costs missing.19completecells/161034domain unchanged;
sameconditionalCPU23.311065%/elapsed18.594528% and coverednominalCI
43.99–449.74CPUh/df2.13 remain, not full-frameCI.
Newpartialcellhas1of2draws; knownHTsubtotal271.301439h differs from
complete19cell246.863040h. Every3missing+1CPU-s adds0.292083h.
New86.978ordinarycost exceedsold40.792support, expandsobservedmax:
assumption source271.6–296.8CPUh, separate mixedtransfer18.3–26.3CPUh.
Old247.5–270.3/16.8–24.0 are dated38costassumptions, not currentbounds.
No-assumptionupperunbounded;10xordinarymaxsource525.349648h.
Missingcheck1x43.756084/2x69.160905/4x119.970547/12x323.209115h;
12xexceeds296.706260source, stress not measurement. Paired31/42/14/11missing,
dynamic13missing/RQ2/Bdenominators unchanged.

Root uses only completed owner raw; no new native/agent/session/queue or
foreignimplementation/infra mutation. No restart of completedMath/Grid/Allocated.
HistoricalBarrier exactprotocol retest remains unqualified/pending;
supplied~299Barrierpartition staysPartial; separate294diagnostic/model still
not root-phase-qualified. Hybrid finitecontrols do not yet supply full gains.
Hostrebootinterrupted runs never enter cost/censor/completed samples;raw kept.
A later outage means preserve scene/wait user, no recovery/scheduling changes.
'''
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;z=p.read_text().replace('root0283.','root0284.',1)
 a=z.index('## Corrected Mathlib comparison');b=z.index('## Scientific contract'if 'status'in n else'## Fixed questions',a)
 z=z[:a]+note+'\n'+z[b:]
 z=z.replace('Source4/paired11/dynamic13 gaps differ','Source3/paired11/dynamic13 gaps differ')
 if n.endswith('status.md'):
  z=re.sub(r'^\| Source probability frame .*$', '| Source probability frame |39/42originals;19/21complete strata/161034modules unchanged. ConditionalCPU23.311%/elapsed18.5945%;3ordinary costs missing/2063module domain incomplete. | [0284]('+rel+'/step-report.md) |',z,flags=re.M)
  z=re.sub(r'^\| Whole-frame scenarios .*$', '| Whole-frame scenarios |39known+3ordinary missing within current observed support:271.6–296.8sourceCPUh; mixed-protocol check transfer18.3–26.3CPUh. Assumptions, not CI/guarantee/full checking; no-assumptionupperunbounded. | [0284]('+rel+'/step-report.md) |',z,flags=re.M)
 else:
  z=z.replace('Source38/42/19strata,4missing.','Source39/42/19strata,3missing.')
  z=z.replace('W source38 now completes Tracked; Allocated preparation belongs to its existing master.','W source39 now completes Allocated; further originals belong to its existing owner.')
 p.write_text(z.rstrip()+'\n')
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text().rstrip()+'\n\n'+note.rstrip()+'\n')
p=r/'research/README.md';z=p.read_text().replace('root0283.','root0284.',1)
p.write_text(z.rstrip()+f'\n\nGrid/source39 [root0284](../docs/{rel}/step-report.md): all12Grid cells complete,4/8strongserial ratios2.125/2.532x withCPU+12.83/18.57%; originalAllocated cost86.978CPU-s expands source39assumptions to271.6–296.8h/mixedtransfer18.3–26.3h.39/42originals/3missing,19completecells unchanged. No whole-library measurement/CI/cross-date marking causality.\n')
base=f'''# Root step0284 — corrected Grid and original source39 (self-review)

## Entry
Latest direct user recovery decision, canonical0283, questions-for-author,
root0283 two reports and M071/W114 actual reports read. Mainline characterizes
checking versus recomputation costs; fixedfourRQs/title/abstract/sections/
designimplications remain. RQ3 receives completed Grid12; RQ1 receives a fixed
original cost and arithmetic consequences. These are qualification of owner
completed work, no experiment admission, new native run, agent/session/queue,
or full writing/idea/milestone-review loop. No existing completed point rerun.
The auto-research-orchestrator gates are recorded here; user forbids new agents,
so both root reports are self-review, not independent review.

## EXPERIMENT_GATE — node1: complete corrected Grid
[Independent reducer](experiment-001/step0284-grid-recompute.py),
[raw reanalysis](experiment-001/reanalysis.json),
[twelve actual clocks](experiment-001/twelve-grid-processes.csv),
[three-repeat summary](experiment-001/grid-three-repeat-summary.csv).
All12plannedcells complete with actualmatrix17:17:37UTC terminal.
Six source/runner files byte-equal root0283 tar; no hot implementation change.
Every command/result/stdout/stderr/memory/terminal read,12rc0/noresource stop,
ordered3793uniqueaccepts and imports/constants equal old actualserialreference.
382707entries/3554unsafe-partial exclusions;9parallelcells each209672jobs/
14887waves/2676parallel+1117complex-cycle/0modulelocalfallback. Plain runs do not
emit observedcheck/HB vectors; absent is not0. No new mathematicalchecker orproof
rewriting. Quiescent markPersistent/FFI/tokencommit/context trust still applies.

Originalserial/parallel1/4/8 medianswall561.212538/581.429215/264.097424/
221.613656s; CPU558.456121/579.926791/630.129415/662.182196s.
Ratiosofstrongserialmedians4=2.125020869,8=2.532391496.
CPU+12.834185/+18.573720%;4to8wall-16.086400%/CPU+5.086698%.
Same-repeat4ratios{m['same_repeat_4_ratios']};
8ratios{m['same_repeat_8_ratios']}. FullrangesinCSV,notCI.
Slower1worker retained; no weakbaseline substitution.
Historical1.8818094worker pair remains; new4point is same configurationfamily,
8point additional, not relabeled4 or multiplied with ablation.
Kernel7.0.0-42 after reboot; old/new dates/runtime/generatedcode/cache/order/
sharedhosteffects unnormalized. Samebinary0279toggle remains isolated contrast.

P0–7/sharedblocking percelllock/1100native/noM(evenM0omitted)/
14GiBcharged+14GiBsampledownRSSresponse. All12cgroupsabsent/noOOM/
sample-stop/wait4complete;24native/sampledPIDbirths+controller5528/birth68581
retired. This does not qualify every earlier diagnostic process. HWM/sample/
chargedcolumns separate; not hardRSS/whole16GiBlane-tree audit.
ClockPopenbefore-to-wait4after; samplerjoin/cgroupdelete andqueue excluded.
Runtimefromfrozenmatrix; no per-openenv trace invented.
Archive{m['archive_B']}B/{m['archive_members']}members/{m['archive_payload_B']}
payloadB fullyread throughgzipEOF/CRC. NoSDK/ELF/buildtree intoGit.
Rootoffline{m['root_analysis_seconds']:.6f}s/{m['root_analysis_maxrss_kib']}KiB/E22–23.
Initial reducer parse error else1 retained exactsource/error receipt, fixed
before any analysisbody/native execution. No performance record changed.

## EXPERIMENT_GATE — node2: original Allocated source cost
[Independent reducer](experiment-001/step0284-source39-recompute.py),
[source39 reanalysis](experiment-001/source39-reanalysis.json),
[fixedframe](experiment-001/source39-frame.csv),
[costs](experiment-001/source39-costs.csv),
[scenarios](experiment-001/source39-scenarios.csv).
17:07:47.727918UTCterminal1planned/1actualcompile_ok, rawcommand/result/plan/
identity/memory/cleanup/empty native.log/outputfacet sizes read.
64383sourceB exactexisting4eaee875pin, no archivecensus/download.
CPU85.787497+1.190492=86.977989s;nativewall79.405758209s,
controller616.925765337s. Queue/setup/cleanup residual537.520007s by clocks;
ownerrow537.502644s is its own broader boundary, neither purewait.
noM/-j8/P0–7/unprofiled/authoredHB/olean-ilean-C/1200actualselfallowance,
not600or1700pool.15GiBcharged+16GiBsampleRSSresponse,
HWM9207032KiB/sample9414340608B/charged1419362304B separate.
Native20800/birth830787+controller20263/birth777032retired;cgroupabsent/
noOOM/stop; no inventedlauncheridentity. C4256669/olean5308280/ilean222479B
actualsizesverified. UntimedEprerequisites are unweighted, not root-requalified
as complete coldtransitivebuild. Original reboot-interruptedattempt excluded,
rawpreserved. Newcompletecost alone added to originalfixedframe.

Ownprior38 IDs/strata/costs and W39publishedcompletedrows match; onlyAllocated
enters.39/42originals/3ordinarymissing.19completecells/161034domain unchanged,
9markedcells/5848markedfiles unchanged. Actual39sum954.511167CPU/
634.212039441nativewall-s. Same covered19cell246.863040CPUh,marked57.546404h,
share23.311065%;elapsed215.217114/marked40.018606h=18.594528%.
Partialcell2023modules nowhas1draw, no newcompletecell. CoverednominalCI
43.99–449.74/df2.13 remains separate and unchanged, not full-frame precision.
KnownHTsubtotal271.301439h nowincludeshalfcell and differs from complete19.
Missing3+1CPU-s each changes eventualpoint0.292083h, not imputedcost.
Observedordinarymax rises40.791652→86.977989; sourceassumptionrange now
271.653260–296.706260h,outward271.6–296.8; separatemixedtransfer
18.373472–26.280760h,outward18.3–26.3. Missingfewer neednotnarrowoldrange;
old38rangesremainhistory,notcurrentbounds. Neither fullmeasurement/CI/guarantee.
No-assumptionupperunbounded;10xordinarymaxsource525.349648h;
unknownchecking1x43.756084/2x69.160905/4x119.970547/12x323.209115h.
12xstress exceeds296.706260source;4xdoesnot, no fabricatedmeasurement.
OldLowBlockobservedsupportcounterexample remains.
RootWoffline{w['root_analysis_seconds']:.6f}s/{w['root_analysis_maxrss_kib']}KiB/E22–23.
Rawsource39tar fullyread toEOF/CRC; [integrity](experiment-001/source39-archive-integrity.json).
No old38native re-run or claim of re-auditing all oldprepared dependencies.

## WRITE_GATE
Methods/RQ1update39/3/unchanged19domain/knownsubtotal/newassumptionranges,
retainingfragilecoveredCI unchanged. RQ3localparagraph reportsallGridarmcosts,
strongbaseline/CPU/orderedrepeat/cache/kernel/trustlimits. Mathlibroot0283nine
costs unchanged; its obsoleteGrid-pending sentence nowlinksnewcompletedboundary.
No newtable;20oldtablebodies/title/fullabstract/fourRQ/sections/fourdesignimplications
remain frozen. Canonicalstatus/plan/index/evaluation/noveltysynchronize.
Paired31/42/14cells/11missing,dynamic13missing,RQ2CPU6.31/8.95 andwall9.26/
10.56/14.67,B2524/30288/22716 andoverlap100/50 unchanged.
No correctedBarrierphase/finiteworkermodel/hybridgain adopted. Original~299s
partition remainsPartial. MfiniteHybridcontrols are not completeperformance.
No recovery/schedule/resource/network/credentials/UI/CronJobmutation.

## REVIEW_GATE — self-review
Accept completeplannedGrid12 and newfixedoriginalAllocated; rejectincomplete
Hybrid/Barrier and Osourceprefix asfullgain. Record newordinarycostoutsidetheold
support instead of keeping convenientoldbounds or treatingmissingaszero.
No full-frameCI, globalphaseweights, intrinsicseriallimit, newmechanismnovelty,
unchangedTCB, cluster/service/wholelibrarygain, researchcompletion orOSDIacceptance.
A/Cgenericnoveltydowngrade/Bglobalbudget/software/axiom/nativebaseline/Envelope
fullsingleconfigpairmissing remain. Allraw/failed/partial/foreigndirty preserved.
Fullcompile/frozenfield/link/allpage static self-review follows; ordinaryownedmain
commit/push only, no stash/reset/amend/force. Later outage preserves scene
andwaitsuser without recovery. No rootdispatch/consumptionclaim.
'''
(s/'step-report.md').write_text(base)
(s/'outer-audit.md').write_text(base.replace('# Root step0284 — corrected Grid and original source39 (self-review)','# Root step0284 outer audit — self-review',1)+'\n## Outer disposition\nTwo already-completed evidence nodes change fixed RQ1/RQ3 results without changing the scientific contract. The Grid gain costs CPU; the new original cost raises assumption scenarios without improving covered-domain precision. Both limitations remain reader-visible. This is self-review, not independent verification or venue acceptance.\n')
shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0284-paper-edit.py',e/'step0284-paper-edit.py')
print('DOCS_READY',s)
