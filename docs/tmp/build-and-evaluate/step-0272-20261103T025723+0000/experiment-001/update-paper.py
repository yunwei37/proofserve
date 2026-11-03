from pathlib import Path
import os,json,re,gzip,subprocess,tarfile
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-source36-root-step.txt').read_text().strip());e=s/'experiment-001';rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');suf=s.name.removeprefix('step-');a=json.loads((e/'reanalysis.json').read_text())
a['scenario_missing_check_three_times_source_CPU_h']=2*a['scenario_missing_check_twice_source_CPU_h']-a['scenario_missing_check_equals_source_CPU_h']
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n')
t=(r/'docs/paper/main.tex').read_text()
oldtag=r'\expref{0270-20261102T233639+0000}{0270}'
newtag=r'\expref{'+suf+r'}{0272}'
t=t.replace(oldtag+'\nSource-frame coverage is now 35/42 with 17 complete strata and 7 missing',newtag+'\nSource-frame coverage is now 36/42 with 18 complete strata and 6 missing')
# The coverage tag closes a measured brace before the newline.
t=t.replace(oldtag+'}\nSource-frame coverage is now 35/42 with 17 complete strata and 7 missing',newtag+'}\nSource-frame coverage is now 36/42 with 18 complete strata and 6 missing')
t=t.replace(r'The 35 completed no-\texttt{-M} random source targets sum to 540.820 seconds'+'\nof native wall intervals and 851.200 user-plus-system CPU seconds.',r'The 36 completed no-\texttt{-M} random source targets sum to 545.802 seconds'+'\nof native wall intervals and 858.220 user-plus-system CPU seconds.')
st=t.index(r'\measured{'+oldtag+'; two further original-frame source costs.}')
en=t.index('\nThese are source-compilation estimates',st)
new=r"""\measured{TAG; one further original-frame source cost.}
NativeCodeAssembly completes in 4.982 native elapsed seconds and 7.020 CPU
seconds. Its prerequisites were prepared separately; untimed dependency work
receives no sampling weight or imputed CPU cost.
Together with the previously measured IntrinsicHolomorphicLogarithm, it completes
the 7,225-module stratum. For the 18 completed strata (151,888 modules),
stratified compiler CPU estimates are 57.546 hours in marked files and
177.487 hours in other files: a conditional marked-file share of 24.48\%.
All nine marked strata have both draws, covering 5,848 marked modules;
three ordinary strata and 11,209 ordinary modules remain incompletely observed.""".replace('TAG',newtag)
t=t[:st]+new+t[en:]
t=t.replace(r'The earlier 14-, 15- and 16-stratum shares, 17.14\%, 33.02\% and 26.47\%,'+'\nuse different covered domains, rather than repeated measurements of the same\npopulation.\nThe increase reflects newly observed cost and coverage, not a temporal trend\nfor a fixed population.',r'The earlier 14-, 15-, 16- and 17-stratum shares, 17.14\%, 33.02\%,'+'\n'+r'26.47\% and 26.37\%, use different covered domains, rather than repeated'+'\nmeasurements of the same population. Changes reflect newly observed cost and\ncoverage, not a temporal trend for a fixed population.')
st=t.index(r'\paragraph{Clock choice and nonresponse alter the estimand.}')
en=t.index(r'\paragraph{Source features do not establish bounded prediction error.}',st)
new=r"""\paragraph{Clock choice and nonresponse alter the estimand.}
\measured{TAG; same 18 complete source strata, offline arithmetic.}
The conditional marked share is 24.48\% of weighted compiler CPU but 19.64\%
of summed native elapsed time, a 4.85-percentage-point difference.
The latter adds native process durations; it is not parallel Lake makespan
or an isolated checking-phase share of whole-library time.
CPU weights include worker execution; elapsed weights reflect each module's
wall duration at the measured concurrency point.
Earlier clock contrasts remain separate coverage snapshots.

The three incomplete strata contain 11,209 of 163,097 modules (6.87\%),
not necessarily that many unbuilt files. Six original source costs are absent.
The 36 known terms in the eventual complete-sample Horvitz--Thompson point
sum to 235.033 CPU-hours. This subtotal happens to equal the current
complete-stratum total because all remaining incomplete strata lack both draws;
it is not a lower confidence limit or a zero-filled population estimate.
Increasing every missing draw by one CPU second would increase the eventual
point by 3.114 CPU-hours under the fixed original weights.
This sensitivity does not predict the missing costs or their variance.

\paragraph{Whole-frame costs require explicit missing-cost scenarios.}
\partialev{TAG; fixed 36-source sensitivity, not measurements
or confidence limits.}
Preserving 36 known costs and original inclusion weights, assume the 6 remaining
ordinary-marker draws cost between the observed ordinary minimum and maximum,
1.204525--40.791652 CPU-s.
Whole-frame construction scenarios then span 238.7--362.1 CPU-hours,
with endpoints rounded outward.
The earlier 35-draw 232.9--396.0-hour source range remains a dated assumption
scenario; the smaller current width follows an additional observed cost.

A separate transfer model gives 16.2--32.2 checking CPU-hours.
It assigns ordinary modules the complete checkpoint-closure CPU
fractions 0.063124--0.089514 and marked modules the older unsegmented
computation fractions 0.084421--0.084671.
This deliberately mixes protocol-specific anchors; it is neither a measured
matched protocol nor evidence that source markers identify checking cost.
The earlier 15.9--35.2-hour transfer used the 35-cost snapshot.
Neither model is measured whole-library checking cost, a confidence interval
or a guaranteed saving. Their known terms use all 36 observed draws; they
also differ from RQ2's trusted-import target checks and complete selected closures.

The LowBlock15\_1 observation remains 184.589 CPU-s, above the old
31-draw marked-class maximum of 163.846 CPU-s, demonstrating that observed
support is only an assumption.
Without missing-cost assumptions, the completion-cost upper remains unbounded.
Assigning all missing draws ten times the observed ordinary maximum raises
the source scenario to 1,505.1 CPU-hours.
At the current class-maximum source scenario, giving missing draws no
checking savings yields 143.1 modeled checking CPU-hours; twice their source
work yields 270.1. Three times their source work yields 397.1, above the
362.1-hour source scenario.
These are different stress assumptions, not measured checking costs.
A subunit factor assigned to unknown modules cannot establish general benefit.
All 6 unobserved original source costs remain missing in the primary evidence.

""".replace('TAG',newtag)
t=t[:st]+new+t[en:]
t=t.replace('The original eleven missing costs remain missing.','The eleven costs absent from that forecast capture are not imputed into its\n31-input evaluation.')
t=t.replace('the two new source-compilation draws.','the additional source-compilation observations.')
old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
assert 'Source-frame coverage is now 36/42'in t and t.count(r'\begin{tabular}')==20
(r/'docs/paper/main.tex').write_text(t)
entry=f"""[Root0272]({drel}/step-report.md) independently qualifies the actual NativeCodeAssembly original terminal01:09:45UTC:4.981634wall/7.020013CPU-s, not E-core prerequisite timing. Exact42frame gains only that ID, prior35costs unchanged. Current36/42,18/21complete strata/151888modules;6ordinary original costs missing/11209module domain incomplete. Conditional source235.032925CPUh, marked57.546404h=24.4844%; nativeelapsed203.778943h/marked19.6382%. KnownHTsubtotal235.032925h equals complete-stratum subtotal here because incompletecells have0observations, not whole-frame point/CI. Missing+1CPU-s each adds3.113611h. Source support scenarios238.7–362.1CPUh; mixed-protocol checking transfer16.2–32.2CPUh, not actual full checking/CI/guarantees. Source35scenarios retained ashistory. Paired31/42/14strata/11missing and dynamic13missing remain distinct."""
for fn in ['docs/research-status.md','docs/research-plan.md']:
 p=r/fn;v=p.read_text().replace('2026-11-02UTC, root0271.','2026-11-03UTC, root0272.')
 v=re.sub(r'Paper root0271:[^\n]+','Paper root0272: source36 qualification; final compile/all-page verification pending.',v)
 v=v.replace('Source7/paired11/dynamic13 gaps differ','Source6/paired11/dynamic13 gaps differ').replace('7original source costs,11paired','6original source costs,11paired')
 v=v.replace('Current source35data preserve conditional marked CPU26.371% over17complete strata,','Current source36data preserve conditional marked CPU24.484% over18complete strata,')
 v=v.replace('Whole-frame232.9–396.0source/\n15.9–35.2modeledstream CPUh','Whole-frame238.7–362.1source/\n16.2–32.2modeledstream CPUh')
 v=v.replace('do not become35-input experiments.','do not become36-input experiments.')
 v=v.replace('Separate from source32coverage/full closure.','Separate from current source36coverage/full closure.').replace('separate from source32coverage.','separate from source36coverage.')
 if fn.endswith('status.md'):
  v=re.sub(r'^\| Source probability frame .*$', '| Source probability frame |36/42originals;18/21complete strata/151888modules.9marked cells/5848files complete; markedCPU57.546/235.033h=24.484%, nativeelapsed19.6382%.6ordinary costs missing/11209module domain incomplete. | [0272]('+drel+'/step-report.md) |',v,flags=re.M)
  v=re.sub(r'^\| Whole-frame scenarios .*$', '| Whole-frame scenarios |36known+6ordinary missing within observed support:238.7–362.1sourceCPUh; mixed-protocol check transfer16.2–32.2CPUh. Assumptions, not CI/guarantee/measured full checking; no-assumption upper unbounded. | [0272]('+drel+'/step-report.md) |',v,flags=re.M)
 else:
  v=v.replace('Source35/42/17strata,7missing.','Source36/42/18strata,6missing.')
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';p.write_text(p.read_text()+'\n\nSource36 [root0272](../'+rel+'/step-report.md), [Wresult](../workloads/openai-math/final-seven-20261102/source36-NativeCodeAssembly/README.md): NativeCodeAssembly actualP0–7 compiler endpoint,36/42originals/18complete strata.238.7–362.1sourceCPUh/16.2–32.2mixed checking transferCPUh are assumptions, not measured full-library cost/CI.6source/11paired/13dynamic costs missing remain separate.\n')
for fn in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/fn;p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0272 NativeCodeAssembly/source36\n\n'+entry+'\n\nRoot reads actualrawplan/command/result/native.log/memory/identity/cleanup/outputfacets. Source22249B matchesexisting pinned4eaee875tree; no new archive download/fullscan. Controller498608/birth772021650andnative499397/birth772076392retired,cgroupabsent,noOOM/sample-stop. Native1200s allowance,P0–7/j8/noM/unprofiled/authoredHB/3facets/15GiBcharged+16GiBRSSresponse. HWM7328472KiB/sample7458926592B/charged789512192B separate; no hardRSS/wholelane claim. Controller552.376165s includesqueue/setup/cleanup vsnative4.981634s;547.386020difference notpurewait. Prior35originalcosts retained;untimedEdependencies do notgetweights/costs. Rootdoesnotrequalifyall411Edependenciesorclaimcompletecoldbuild. Mownerstep028nowreportscompleted originalfinite plusnaturalpair;rootthisstepdoesnotfit/unqualifiedmatrixorborrowPMUcontrolstep029aswholeclosurecause. Ramseyreading10921/11188source,177/444targets,kernel0/444stillprefix. No newrootnative/agent/queue/foreignimplementation/infrachange. A/Cgenericnoveltydowngrade/Bglobalbudget/causality/globalphaseweights/software/axioms/cluster/nativebaseline/Envelopepair gapsremain.\n')
report=f"""# Root step0272 — NativeCodeAssembly original source cost
**自审; not independent audit or venue acceptance.** Existing BUILD_AND_EVALUATE. Central position remains two checking-cost regimes with scope-matched evidence, not new generic mechanisms.

## EXPERIMENT_GATE
Read latest direct user decisions/canonical0271/two rootreports, W101actualterminal and M028/029/Olatestprogress. No new native experiment/Agent/session/queue. Existing owners continue autonomouswork. This originalsample endpoint fillsone existingdraw, nochangedframe orreplacementtask.
Actualcomplete terminal01:09:45UTC has1planned/1actualcompile_ok. Root reads original plan/command/result/native.log/memory/identity/cleanup/controller andoutputfacets. NativeCodeAssembly22249sourcebytes equalexistingfixed4eaee875pinnedtree; no new fullarchive/lexicalcensus. Raw emptylog hasno sorry/error diagnostic. noM(includingno-M0)/P0–7/j8/unprofiled/authoredHB/3facets/15GiBcharged+16GiBRSSresponse andstockper-tasklock. Actualselfallowance1200s,not1700controllernativepoolor600. Native4.981634wall/7.020013CPU-s;controller552.376165s includesqueue/setup/cleanup,547.386020difference notpurewait.
Controller498608/birth772021650+native499397/birth772076392 retired,actualcgroupabsent/noOOM/sample-stop. HWM7328472KiB/sample7458926592B/charged789512192B distinct. OutputC920142/olean3439096/ilean100436Bsizechecked. No hardRSS orwholelane audit claim; unissuedlauncheridentity notinvented.
411untimedEprerequisites and1retainedPdependencyareownerpreparation,notneworiginals/measuredcostlabels. Rootdoesnotrequalifyalltheirrawhere orcallthiscoldtransitivebuild.

Fixed42module/stratumframe comparedto root0270source35,onlyNativeCodeAssemblyadded. Allprior35actualvalues unchangedandW36publishedrowsmatch;rootownsource36frame doesnoteditWfiles.36originalsCPU858.220164s/wall545.801817s.18complete strata/151888modules,6ordinarymissing/11209module domain(6.8726%). New7225cellcomplete;9markedstrata/5848markedfiles unchanged. Conditional235.032925CPUh/marked57.546404=24.484401%;nativeelapsed203.778943h/marked40.018606=19.638244%. Earliercoverage snapshotsnotpopulationtrends/semanticphaseweights.
KnownHTsubtotal235.032925h numericallyequalscomplete-stratumtotal because3missingcellsall0costs;notfullframeestimate/lowerCI/zeroimputation. Eachmissing+1CPU-sadds3.113611h. Ordinarysupport1.204525–40.791652s gives238.783347–362.042266sourceCPUh, outward238.7–362.1. Mixedcheckpointordinary0.063124–0.089514/unsegmentedcomputation0.084421–0.084671transfer16.298586–32.129266h,outward16.2–32.2. Notmatchedprotocol/fullchecking/CI/guarantee. No-assumptionupperunbounded;10xmaxsource1505.126334h. Missingcheck1x143.071184/2x270.080525/3x397.089866CPUh;3xexplicitstress exceedssource362.042266,notmeasurement. LowBlock184.589>oldmarkedmax163.846supportcounterexampleretained.
Paired31/42/14strata/11missing,dynamic13missing unchanged;newsource endpointnotnewkernel/replay/axiomresult. Wparalleltransfer/halfquota/CI notindependentlyqualifiedorpropagated.

## WRITE_GATE
Methods/RQ1current36numbers/clocks/assumptions/canonicalstatus/plan/index/evaluation/noveltyupdated.20oldtablebodies/title/fullabstract/4RQ/sectionhierarchy/4designimplicationsidentical;no newtable. Historicalforecasts31/14pairedremainhistorical,not36experiments. Raw/source/commands/stdio/memory/terminal/owneroutputs andbeforeentry archived withrootframe/3smallCSV/recomputesource. No SDK/nativeobjects copiedGit.
Compile/render/links pendingatinitialreport;actualverification appendedlater.

## REVIEW_GATE — self-review and routing
Direction unchanged;acceptedactualnewdrawandfixedweightarithmetic,rejecteddependencyweights/untimedcosts/coldbuild/globalphaseweights/guaranteedcheckinggain. Datareduce{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23,0newnative. Explicitmissingdataandtrustedimports/producercostscopepreserved. Userauthorizesrootintegration,notforeignimplementation/hotcapturechanges.
Mownerstep028finiteoriginalplusfinalnaturalpairnowactuallycomplete;do notsaystillrunning. Its12fullpoints/compoundleaf/PMUq2shortcontrolareseparated;rootthisstephasnotqualifiedwholematrix/PIDbirth/placement/observerdifferentialorCPUfit. Mstep029q3perfqueued,notwholeclosurecausalresult. Needlatestactualrawqualificationnextwithoutrestartingcompletedfinitecaptures.
OnewRamseyread10921/11188source=10744reused+177newtargets,kernel0/444;notfullresult,nothistorical2488/163097wholelibrary. Wsource36complete,remaining6originalsownerplansnotnewrootqueue. Existingcommunicationtargetunconfirmed,no fabricateddispatch. Allglobalphaseweights/causality/software/axioms/cluster/nativebaseline/Envelopepairgapsremain;self-reviewnotindependent/venueacceptance.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0272 — NativeCodeAssembly original source cost','# Root step0272 outer audit — 自审')+'\n## Disposition\nTerminal/nativeidentity/source/outputmode/fixed42IDjoinverifiedbeforepaperpropagation. Prior35valuesand20tablebodiespreserved. Modelanchorsremainmixed; missing6not0. OriginalownerMfinitecompletionisrecognizedwithoutprematurecausalqualification. No independentauditclaimed.\n')
# Small exact owning inputs beyond the native tar.
for n in ['workloads/openai-math/build-planning-4eaee875/strata.csv','workloads/openai-math/cost_staircase/calibration.csv','workloads/reports/W101-step.md','research/parallel-stream-check/step028.md','research/parallel-stream-check/step029.md']:
 (e/('input-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
print('EDIT272',s, a['scenario_missing_check_three_times_source_CPU_h'])
