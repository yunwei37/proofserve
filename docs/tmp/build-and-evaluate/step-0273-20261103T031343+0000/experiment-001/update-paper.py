from pathlib import Path
import os,json,re,gzip,statistics
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-attribution-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text());rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');suf=s.name.removeprefix('step-');tag=r'\expref{'+suf+r'}{0273}'
# Distinguish two valid aggregation choices for solo work-rate calibration.
groups={}
b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2')
kind=None
for line in(b/'runs/hardware-leaf/stdout').open():
 j=json.loads(line)
 if j['event']=='curve_begin':kind=(j['kind'],j['repeat']);groups[kind]=[]
 elif j['event']=='unit_check':groups[kind].append(int(j['cpu_ns']))
a['solo_E_P_work_rate_sum_target_medians']=a.pop('solo_E_P_work_rate')
a['solo_E_P_work_rate_ratio_of_mode_median_sums']=statistics.median(sum(v)for(k,rep),v in groups.items()if k=='p1')/statistics.median(sum(v)for(k,rep),v in groups.items()if k=='e1')
a['solo_rate_scope']='sum of per-target medians and ratio of per-mode median sums are different aggregations, not a hardware constant'
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n')
t=(r/'docs/paper/main.tex').read_text()
mark=r'\paragraph{Pooled certificates pass a broader native qualification.}'
assert mark in t
addition=r"""\paragraph{Observed CPU growth extends inside the checking calls.}
\measured{TAG; a separate corrected placement and observer protocol.}
Twelve fresh-process cells each check the same 4,449-module Barrier closure
and match the retained serial reference's accepted IDs and import graph.
The earlier two-worker placement trial is excluded: two active workers
had shared CPU0. The corrected driver gives active tasks distinct per-wave
slots; its same-source profile-on P1/P2/P4/P8 wall times are
655.448/433.980/346.351/315.062 seconds, with native CPU
647.069/625.008/648.965/723.951 seconds.
E16 and P-first mixed24 take 425.347/325.296 wall seconds and
1,121.948/1,100.116 CPU seconds.
These are different versions and treatments from Table~\ref{tab:heterogeneous},
not a continuous tuning curve. Observed use of up to 24 cores is reported
without retroactively changing the earlier eight-core allocation.

Eight observer-enabled full cells have the same 237,863 ordinary checks
and 3,283,925,639 observed allocation units, including identical per-module sums.
At P4 to P8, native CPU rises 74.986 seconds, of which 71.953 seconds
(95.95\%) lie in the observer brackets around original-kernel calls.
Those brackets include heartbeat and timing reads; they are not a pure
kernel-cycle count.
The observer records thread CPU, interval-union wall occupancy and
per-check start cores; occupancy must not be added as concurrent CPU.
Implementation-serialized preparation, complex replay and duplicate checks
are not proved inherent dependency lower bounds.

Natural-placement P8 to mixed24 adds 19.230 wall seconds with the observer
enabled: 4.629 seconds in implementation-serialized windows, 7.410 in
ordinary-call wall occupancy, 3.386 in batch time outside that occupancy,
and 3.805 in the remaining process residual.
Native CPU increases 458.725 seconds, including 438.492 in ordinary-call brackets.
The natural-placement wall regression is 6.36\% with the observer and
5.53\% without it. Under deliberate P-first placement, the corresponding
wall differences are +3.25\% and -0.37\%.
Each cell is one ordered observation with retained filesystem caches;
the sign-sensitive control differences do not isolate observer overhead,
thermal drift or placement as the cause.
Unpinned per-core attribution uses check-start cores and detects differing
endpoints, without reconstructing intervening migrations.
A fixed intrinsic serial fraction, atomic-reference-count cause, cache cause
and frequency cause remain unestablished.
All cells omit \texttt{-M}; charged-memory and sampled-RSS guards are separate.
The original mathematical kernel is retained, while the coordinator, observer
and internal-ABI adapter remain trusted implementation.

""".replace('TAG',tag)
t=t.replace(mark,addition+mark)
mark=r'\paragraph{System-design implication.}'
# Add the compound calibration immediately before the RQ4 implication, after existing count/bytes evidence.
idx=t.index(mark,t.index(r'\paragraph{Parallel checking preserves observed counts and serialized payloads.}'))
addition=r"""\measured{TAG; separate resident hardware calibration.}
One further process checks the complete Barrier closure, then runs nine
resident leaf trials: P1 on CPU0, E1 on CPU8 and mixed24, three repeats each
with the middle order reversed.
Fifty overlapping real helpers yield 450 accepted observations; every
target's allocation-count range is zero.
All nine actually emitted 9,160,440-byte \texttt{.olean} files equal the
original input byte for byte, with 3,425 checked payload substitutions
and trusted extension metadata.
These helpers are not added to the earlier 2,524-target census.
Normalizing each mixed check against that target's median solo CPU cost
on the same core type gives median ratios 2.301 for P and 2.834 for E;
all 150 mixed observations cost more CPU than their solo-type reference.
The references are CPU0 and CPU8, not the same physical core or controlled
frequency for every mixed observation.
This shows concurrency-associated CPU growth at fixed observed counts,
without identifying an instruction-level cause or a general budget guarantee.
The compound native process costs 782.484 wall and 1,688.835 CPU seconds,
including the checked prefix, all nine trials and serialization;
it is not nine independent complete-closure measurements.

""".replace('TAG',tag)
t=t[:idx]+addition+t[idx:]
old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
assert t.count(r'\begin{tabular}')==20
(r/'docs/paper/main.tex').write_text(t)
entry=f"""[Root0273]({drel}/step-report.md) independently qualifies corrected-v2 twelve full Barrier cells+one compound leaf process and3finite controls. Every fullclosure has4449unique accepts/identicalimports/counts/referenceIDset,425463entries/3595unsafe-partialexclusions/0contextfallback.8observedcohorts preserve237863ordinarychecks/3283925639allocationunitsandper-modulesums. P4→P8nativeCPU+74.986s,observer-bracketCPU+71.953s=95.9549%; brackets includeheartbeat/timingreads,notpurecycles. NaturalP8→mixed24wall+19.230s/CPU+458.725s,phasewindows4.629serial+7.410occupancy+3.386batchoutside+3.805other;notinstructioncausality. Naturalwall+6.36%on/+5.53%off; P-first+3.25%on/-0.37%off,1orderedobservation/cell,notCI/isolatedcausalA-B.50overlappinghelpers×9=450accepted/zeroobservedcountranges;9actual9160440Boleansidenticaltooriginal,extensionmetadata trusted. Mixedchecks/same-targetsolo-typemedianCPUratiosP2.301/E2.834,notcontrolledphysicalcore/frequencyorRC/cachecause. Old2524census/100helperpaneldenominatorsunchanged."""
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text().replace('root0272.','root0273.');v=re.sub(r'Paper root0272:[^\n]+','Paper root0273: corrected full attribution qualification; final compile/all-page verification pending.',v);v+='\n\n'+entry+'\n'
 if n.endswith('status.md'):
  at='| Whole-source producer diagnostics'
  i=v.index(at);v=v[:i]+'| Corrected full attribution |12full Barrier cells+compoundleaf complete; P4→P8 extraCPU95.95%in observed kernel-call brackets, natural mixedwall+6.36%on/+5.53%off. Fixedcount work with CPUinflation; causes notisolated. | [0273]('+drel+'/step-report.md) |\\n'+v[i:]
 p.write_text(v)
p=r/'research/README.md';p.write_text(p.read_text()+'\n\nCorrected full attribution [root0273](../'+rel+'/step-report.md), [Mfinal](parallel-stream-check/attribution-results/final.md):12fullclosurecells+separatecompoundleaf. CPUgrowthinsideobservedordinarykernelbracketsdespitefixedcounts; phase/placement/observercomparisonsand50helpercount/bytequalification,notPMUcausality/generalbudget. Rawfrozeninrootstep;originalcaptureonPVC.\n')
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0273 complete corrected attribution\n\n'+entry+'\nRootreadsall13rawcompleteclosuregraphs,16native/controlresourcesand42actualPIDbirthidentities(allretired)/16absentcgroups/noOOM/stop. Primary+compoundmaxwait4RSS3864992KiB/sample3958272000B/charged1774395392Bseparate,14GiBcharged/sampledRSSresponse;notcomplete16GiBlane-treeorhardRSSproof. Oldbeyond8resourceobservationsreported,notretroactiveauthorization.12fullnativewall4398.095417/CPU10382.227379sissumofdifferentsettings,notgain;compound782.483628wall/1688.834875CPUincludesall9leaftrials/serialization.3controlsincludeexpectedkernelbvarrejectionandreal2coreplacement. Initialrootreducerincorrectlyexpectedprofile-onlydependency_phaseeventsinthe4observer-offruns;rawshowstheyareomitted,notzero. Failurecode/receiptretained,offcellscontributefullclocks/graphsbutnophaseimputation. Sourcev2distinctper-frontierslots/observerTLSandoriginalCheckstockkernelread;actualcommanddoesnotlogenv, frozenrunner/terminalgiveplacementconfiguration,notper-openexecutiontrace. Allraw/source/failurespreserved;no native rerun/foreignedit/agent/queue/infrachange. No fitintrinsicseriallimit/PMUcausality. CurrentWsource36/42/source238.7–362.1/mixed16.2–32.2scenarios/paired31/dynamic13gapsunchanged;historicalwholelibrary2488/163097partialunchanged.\n')
report=f"""# Root step0273 — complete corrected Barrier attribution and resident calibration
**自审; not independent audit/venue acceptance.** BUILD_AND_EVALUATE;centralcharacterization/fourRQcontractunchanged. Rootonlydocs/paper/records,index.

## EXPERIMENT_GATE
Readcurrentverbatimuserdecisions/canonical0272/tworootreports/ownerlatestM028finalandM030shortperfqualification,Olatestprefix. No rootnative/Agent/session/queue. Existingownersremainautonomous. FullfiniteMsequenceactuallycomplete,notpending. Preserveinvalidv1P2aliasCPU0andallraw;correctedv2selectedbyactualcapture/source,notfiletitle.
Independent13stdoutreconstruction:12freshsingleconfig+1compoundcompleteclosure,each4449uniqueheaders/acceptswithidenticalper-moduleconstantcounts/imports,rootreachability,retainedOserialreferenceIDset.425463entries/3595upstreamunsafe-partialexclusions/0contextfallback. Mathematicalkernel originaladdDeclCore retained;frozenC/Leanobserver/coordinator/ABIcodeistrusted. Extrae773018wrapperusesexistingfrozenbinarypath;commandsomitenv,soconfigurationprovenanceisfrozenrunner/terminal,notper-openlogornewbinaryidentitygate.
16primary/compound/controlnativeattemptsresourcesread;42actualnativeparents/sampledchildren/controllersPIDbirthretired/16cgroupsabsent/noOOM/sample-stop. Full+compoundwait4HWM3864992KiB/sample3958272000B/charged1774395392Bseparate;14GiBcharged+sampledRSSresponse,nothardRSS/full16GiBlaneaudit. Actualbeyond8footprintisreported,notretroactiveresourceauthorization. Wait4wallstopsbeforecollectorjoin/cgroupcleanup,originalflockqueueoutsideclock.12fullwallsum4398.095417/CPU10382.227379snotasingleconfigurationgain;compound782.483628wall/1688.834875CPUincludesprefix/all9trials/serialization.
Initialread-onlyreducerincorrectlyexpecteddependency_phaseeventswithobserveroff. Fouroffcellsomittheseevents,notzerophasecosts;rawcompletegraph/clocksvalid. Initialcode/tracepreserved;correctedreduceonlyuses8observedcohortsforphasecomparisons. Nonewrootnativeorrepairruntask.

Same-sourcecorrectedprofile-onP1/P2/P4/P8wall655.448141/433.980392/346.351494/315.062388s,CPU647.069201/625.007943/648.964642/723.951002. E16wall425.347178/CPU1121.947796;P-firstM24wall325.296082/CPU1100.115790. Oldv1P2excluded;notcross-versiontuningwith0266/oldv14. V2atomicdistinctslotsperwaveandactualP2core0/1nonzerochecksread;rawper-moduleTID/coreunionsnotclaimedper-waveconcurrencysnapshots.
All8observedcohorts237863checks/3283925639allocationunitsandper-modulevectorsidentical. P4→P8CPU+74.986360s,kernelbrackets+71.953059=95.954863%;observerincludesclock/HBreads,notpureC++cycles. P1→P2CPUnotmonotonic;donotclaimallsettingsCPUalwaysincreases. NaturalprofileonP8→M24wall+19.229983/CPU+458.724846,kernelbrackets+438.492075. Nonoverlappingelapsedidentity4.629134serial+7.410035kerneloccupancy+3.385942batchoutside+3.804872other. ImplementationserialnotinherentDAGlowerbound,residualnotpurecoordinationcause. Naturalwall+6.3622%on/+5.5342%off;P-first+3.2481%on/-0.3655%off. Sign-sensitiveorderedobservationsnotreplicatedCI/orisolatedobserver/placement/frequency/thermalcausality.
Unpinnedper-coreCPUatcheck-start,endpointchangesdeduplicated596P8/576M24,notfullschedulertrace/migrationexclusion. Pinnedwithin-checkendpoints0doesnotmeanzerobetween-waveplacementchanges. NoPMU/RC/cache/frequencyclaimorintrinsicserialfractionfitadopted.

Compound50realoverlappinghelpers×3modes×3repeats=450accepted,alltargetranges0. Nineactual9160440Boleanscomparebyte-for-bytewithoriginal;3425checkedpayloadsubstitutionsandextensionmetadatatrusted,notIR/C/ilean/transitivebytes/wholeaxiomguarantee. Notnewindependentcensustargets. Mixed150checksnormalizedtosame-targetsolo-typemedianP2.301104/E2.833873,all>1. CPU0/8soloreferencesnotsamephysicalcore/frequencyforothermixedplacements. SumtargetmediansE/Pworkrate0.728104andratioofmodemedianhelpersums{a['solo_E_P_work_rate_ratio_of_mode_median_sums']:.6f}aredifferentaggregations,notcontradictoryhardwareconstants. PaperdoesnotneedageneralEworkrate. Old2524/30288/22716and100/1200denominatorsunchanged.

## WRITE_GATE
ActualRQ3completecurve/phase/observerplacementlimitsandRQ4scoped50helpercalibrationadded;20oldtablebodies/title/fullabstract/fourRQ/sections/fourdesignimplicationsidentical,nounrequestednewtableorframing. Canonicalstatus/plan/index/evaluation/noveltysynchronized. Rootraw/source/commands/results/stdout/stderr/memory/terminals/ownerreports/smallderivedCSV/beforeentryandread-onlyfailurepreserved,nobuildtree/SDK/nativeobjectcopies. No newclaimforglobalsoftware/axioms/cluster/nativebaseline/Envelopepair.
Compile/render/linkverificationpendingatinitialreport;actualreceiptsappendedlater.

## REVIEW_GATE — root self-review and routing
Directionstilltwoverificationcostregimes,notnovelmechanismorhardwarecausalbreakthrough. Acceptfixedobservedallocation/CPUinflationattributionasmeasuredscope;rejectpurekernelcycles/allCPUmonotonic/fixedserialfraction/RC/cachecause/25%Ecapacity/zeroobserveroverhead/generalbudget. Rootfinalreduce{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23includesrawfreezeand9bytecomparisons;failedread-onlyschemaassumptionseparate,preserved.
OwnerM030newshort650moduleperfcontrolhasactualinheritedcounters/stacksbutisnotthis4449closurecurveorP1/2/4/8PMUcomparison. Newadmittedperfseriesonlyownerlatestterminalcanqualify;don'trestartoldfiniteMsequence. Wsource36alreadyqualified0272,6source/11paired/13dynamicgapsstaydifferent. Oread10923/11188source/179newtargets,kernel0/444prefix,nothistorical2488/163097wholelibrarycompletion. ExistingCLICloudflare-Jrouteonly;nohealthroutinechanges,newcommunicationtargetorfalse dispatch. Remainingglobalphaseweights/causalrepeats/software/axioms/cluster/nativebaseline/Envelopepairgapsremain. Self-reviewnotindependent/venueacceptance.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0273 — complete corrected Barrier attribution and resident calibration','# Root step0273 outer audit — 自审')+'\n## Audit disposition\nProtocolcorrectionisread-only:missingoffobserverphasesremainunknown,notzero. Currentgraphs/referenceIDs/scopedclocksactualresourcesreadbeforepaperintegration. Biological/hardwarecausalitynotinferredfromtimingorper-corelabels. Preserveoldinvalidv1/negativecurvesandallinitialfailures. No independentreviewclaimed.\n')
print('EDIT273',s,'rateaggregations',a['solo_E_P_work_rate_sum_target_medians'],a['solo_E_P_work_rate_ratio_of_mode_median_sums'])
