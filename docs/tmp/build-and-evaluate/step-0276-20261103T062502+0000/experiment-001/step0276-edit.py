from pathlib import Path
import os,json,re,gzip,shutil
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-source38-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text());rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');tag=r'\expref{'+s.name.removeprefix('step-')+r'}{0276}'
a['scenario_missing_check_four_times_source_CPU_h']=3*a['scenario_missing_check_twice_source_CPU_h']-2*a['scenario_missing_check_equals_source_CPU_h']
a['scenario_missing_check_twelve_times_source_CPU_h']=11*a['scenario_missing_check_twice_source_CPU_h']-10*a['scenario_missing_check_equals_source_CPU_h']
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n')
raw=Path(a['new_originals'][0]['raw']);assert(raw/'native.log').read_bytes()==b''
cmd=json.loads((raw/'command.json').read_text());assert cmd['self_wall_s']==1200
base=raw.parent.parent;launch=json.loads((base/'launch.json').read_text());rr=json.loads((raw/'result.json').read_text())
t=(r/'docs/paper/main.tex').read_text();old=t
t=t.replace(r'\expref{0274-20261103T040607+0000}{0274}'+'}\nSource-frame coverage is now 37/42 with 18 complete strata and 5 missing',tag+'}\nSource-frame coverage is now 38/42 with 19 complete strata and 4 missing')
t=t.replace(r'The 37 completed no-\texttt{-M} random source targets sum to 549.607 seconds'+'\nof native wall intervals and 862.121 user-plus-system CPU seconds.',r'The 38 completed no-\texttt{-M} random source targets sum to 554.806 seconds'+'\nof native wall intervals and 867.533 user-plus-system CPU seconds.')
st=t.index(r'\measured{\expref{0274-20261103T040607+0000}{0274}; one further original-frame source cost.}');en=t.index('\nThese are source-compilation estimates',st)
t=t[:st]+r"""\measured{TAG; one further original-frame source cost.}
TrackedTestBounds completes in 5.199 native elapsed seconds and 5.412 CPU
seconds. Its untimed E-core prerequisites receive no sampling weight.
It completes the matching 9,146-module ordinary stratum, increasing the
complete-stratum domain to 161,034 modules across 19 strata.
Stratified compiler CPU is 57.546 hours in marked files and 189.317 hours
in other files, a conditional marked share of 23.31\%.
All nine marked strata have both draws, covering 5,848 marked modules;
two ordinary strata and 2,063 ordinary modules remain incompletely observed.""".replace('TAG',tag)+t[en:]
st=t.index(r'\paragraph{Clock choice and nonresponse alter the estimand.}');en=t.index(r'\paragraph{Source features do not establish bounded prediction error.}',st)
add=r"""\paragraph{Clock choice and nonresponse alter the estimand.}
\measured{TAG; same 19 complete source strata, offline arithmetic.}
The conditional marked share is 23.31\% of weighted compiler CPU and
18.59\% of summed native elapsed time, a 4.72-percentage-point difference.
The latter adds native process durations; it is not parallel Lake makespan
or an isolated checking-phase share of whole-library time.
CPU weights include worker execution; elapsed weights reflect each module's
wall duration at the measured concurrency point.
Earlier clock contrasts use different covered domains and are not a
population time trend.

The two incomplete strata contain 2,063 of 163,097 modules (1.26\%),
not necessarily that many unbuilt files. Four original source costs are absent.
The 38 known terms in the eventual complete-sample Horvitz--Thompson point
sum to 246.863 CPU-hours, equal here to the complete-stratum subtotal because
both incomplete strata have zero observed draws.
This is not a lower confidence limit or a zero-filled population estimate.
Increasing every missing draw by one CPU second would increase the eventual
point by 0.573 CPU-hours under the fixed original weights.
This sensitivity does not predict missing costs or variance.

\paragraph{Whole-frame costs require explicit missing-cost scenarios.}
\partialev{TAG; fixed 38-source sensitivity, not measurements
or confidence limits.}
Preserving 38 known costs and original inclusion weights, assume the four
remaining ordinary-marker draws cost between the observed ordinary minimum
and maximum, 1.204525--40.791652 CPU-s.
Whole-frame construction scenarios then span 247.5--270.3 CPU-hours,
with endpoints rounded outward.
The earlier 37-draw 242.2--315.2-hour range remains a dated assumption
scenario; the smaller current width follows an additional observed cost.

A separate transfer model gives 16.8--24.0 checking CPU-hours.
It assigns ordinary modules the complete checkpoint-closure CPU
fractions 0.063124--0.089514 and marked modules the older unsegmented
computation fractions 0.084421--0.084671.
This deliberately mixes protocol-specific anchors; it is neither a measured
matched protocol nor evidence that source markers identify checking cost.
The earlier 16.5--28.0-hour transfer used the 37-cost snapshot.
Neither model is measured whole-library checking cost, a confidence interval
or a guaranteed saving. Their known terms use all 38 observed draws; they
also differ from RQ2's trusted-import target checks and complete selected closures.

The LowBlock15\_1 observation remains 184.589 CPU-s, above the old
31-draw marked-class maximum of 163.846 CPU-s, demonstrating that observed
support is only an assumption.
Without missing-cost assumptions, the completion-cost upper remains unbounded.
Assigning all missing draws ten times the observed ordinary maximum raises
the source scenario to 480.6 CPU-hours.
At the current class-maximum source scenario, giving missing draws no
checking savings yields 40.2 modeled checking CPU-hours; twice their source
work yields 63.6 and four times yields 110.3, below the 270.2-hour source value.
A separate stress assumption of twelve times their source work yields
297.3 checking CPU-hours, reversing that comparison.
These are different stress assumptions, not measured checking costs.
A subunit factor assigned to unknown modules cannot establish general benefit.
All four unobserved original source costs remain missing in the primary evidence.

""".replace('TAG',tag)
t=t[:st]+add+t[en:]
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
assert 'Source-frame coverage is now 38/42'in t and t.count(r'\begin{tabular}')==20 and 'complete 20-file sample'in t
(r/'docs/paper/main.tex').write_text(t)
entry=f"""[Root0276]({drel}/step-report.md) independently qualifies TrackedTestBounds actual06:22:07UTC original return5.198824wall/5.412330CPU-s. Fixed42frame adds onlythisID;prior37rawcosts match W38publishedrows.38/42originals,19/21complete strata/161034coveredmodules;4ordinarycostsmissing/2063module domain(1.26489%)in2cells. Conditional246.863040CPUh/marked57.546404h=23.311065%, summednativeelapsed215.217114h/marked40.018606h=18.594528%. Differentcovered domain than18-cell24.4844%,notpopulationtimetrend/semanticphaseweight. KnownHTsubtotal246.863040h equalsthecomplete-stratumsubtotalonlybecausemissing2cellshave0observations;notfullpoint/CI. Missing+1CPU-s eachadds0.573056h. Sourceobservedsupportscenarios247.5–270.3CPUh; separatemixed-protocolchecktransfer16.8–24.0CPUh,notmeasuredfullchecking/CI/guarantees.10xordinarymaxsource480.621868h;missingcheck1x40.184493/2x63.560375/4x110.312141/12x297.319203h. Fourtimesno longer exceedsactualmaxsource270.238923;explicit12xstressdoes,notmeasurement. Paired31/42/14strata/11missing,dynamic13missingunchanged."""
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text().replace('root0275.','root0276.',1)
 v=re.sub(r'Paper root0275:[^\n]+','Paper root0276: source38 qualification; final compile/all-page verification pending.',v)
 v=v.replace('Source5/paired11/dynamic13 gaps differ','Source4/paired11/dynamic13 gaps differ')
 if n.endswith('status.md'):
  v=re.sub(r'^\| Source probability frame .*$', '| Source probability frame |38/42originals;19/21complete strata/161034modules.9marked cells/5848files complete; markedCPU57.546/246.863h=23.311%, nativeelapsed18.5945%.4ordinary costs missing/2063module domain incomplete. | [0276]('+drel+'/step-report.md) |',v,flags=re.M)
  v=re.sub(r'^\| Whole-frame scenarios .*$', '| Whole-frame scenarios |38known+4ordinary missing within observed support:247.5–270.3sourceCPUh; mixed-protocol check transfer16.8–24.0CPUh. Assumptions, not CI/guarantee/measured full checking; no-assumption upper unbounded. | [0276]('+drel+'/step-report.md) |',v,flags=re.M)
 else:
  v=v.replace('Source37/42/18strata,5missing.','Source38/42/19strata,4missing.')
  v=v.replace('W source37 unchanged, Tracked preparation belongs to its existing master.','W source38 now completes Tracked; Allocated preparation belongs to its existing master.')
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';v=p.read_text().replace('Current2026-11-03UTC, root0275.','Current2026-11-03UTC, root0276.');p.write_text(v+'\n\nTracked/source38 [root0276](../'+rel+'/step-report.md), [Wresult](../workloads/openai-math/final-seven-20261102/collection-remaining-six-20261103T0325/source38-TrackedTestBounds/README.md):38/42originals/19complete strata/161034domain; source247.5–270.3CPUh/mixedtransfer16.8–24.0CPUh assumptions,notCI/wholelibrarymeasurement.4source/11paired/13dynamicmissingseparate;root0275Ramseysampleunchanged.\n')
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0276 Tracked/source38\n\n'+entry+f"\nActualnative/source/commands/stdout(empty)/memory/nativeidentity/cleanup/outputfacetsread.2929sourcebytesmatchfixed4eaee875tree,noarchivecensus/download. noM/P0–7/j8/unprofiled/authoredHB/3facets/1200selfallowance/15GiBcharged+16GiBRSSresponse;native561245/birth773950547 andcontroller{launch['pid']}/birth{launch['birth_ticks']} retired. HWM7236692KiB/sample7367950336B/charged763092992Bseparate,nohardRSS/fullWtreeclaim. C739810/olean743560/ilean14874Bactualsizesverified. Native5.198824vscontroller390.941586s;row385.736827s/wholecontrollerdifference385.742762includequeue/setup/cleanup,notpurewait. Epreparationisuntimed/unweightedandnotrootre-auditedasacoldtransitivebuild. Rootoffline{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23;0newnative/Agent/queue/foreignimplementation. Root0275Ramseysampleandallotherprotocolsunchanged.\n")
report=f"""# Root step0276 — TrackedTestBounds original source cost
**自审; not independent review or venue acceptance.** Existing BUILD_AND_EVALUATE and frozen four-RQ characterization.

## EXPERIMENT_GATE
Entry rereads latest direct decisions/canonical0275 and Wactual38terminal. This is an independent collection of an already-completed owner's native point, not a new experiment/queue/Agent. Full experimental design, idea refinement, full writing and milestone review entry conditions are absent; no scientific contract change.
1planned/1actualcompile_okterminal06:22:07UTC. Source2929Bbyte-identicaltoexisting4eaee875pinnedtree. Actualplan/command/result/empty native.log/memory/nativeidentity/cleanup/controller/outputfacets read. noM(alsoomit-M0)/P0–7/j8/unprofiled/authoredHB/3facets/sharedpertasklock/1200actualselfallowance,not600or1700pool. CPU4.283929user+1.128401sys=5.412330s;nativewall5.198824103s. Controller390.941585794s;row385.736826989s andwholecontroller-minusnative385.742761691s includequeue/setup/cleanup,notpurewait.
Controller{launch['pid']}/birth{launch['birth_ticks']}+native561245/birth773950547actual2identitiesretired;cgroupabsent/noOOM/sample-stop. HWM7236692KiB/sample7367950336B/charged763092992Bseparate,15GiBcharged+16GiBsampledresponse,not hardRSS/full16GiBlane-treeaudit. ActualC739810/olean743560/ilean14874Bverified. No inventedlauncherbirth.
UntimedEprerequisitesareexistingownerwork,notaddedtodraws/weights/notfullcoldtransitivebuildqualified. OriginalWmaster526699/birth772878773isaseparatedriver;childcompletiondoesnotretiremaster. LatestmasterhasmovedtoAllocatedEpreparation561457/birth773951593,norootdispatch/restart.
Fixed42module/stratum IDs comparedown0274frame,onlyTrackedadded;allprior37rawcostsandW38publishedrowsmatch.38actualsum867.533178CPU/554.806281232nativewall-s.19completecells/161034domain,4ordinaryoriginalcostsmissing/2063module domain(1.26489%)in2incompletecells.9markedcells/5848filesunchanged.
Conditional246.863040CPUh/marked57.546404h=23.311065%;same19domainelapsed215.217114h/marked40.018606h=18.594528%. Coveragechangedfrom18-cell24.4844/19.6382%,notpopulationtimeevolution/semanticphaseweights. KnownHTsubtotal246.863040equalstocompletecellsbecausemissingcellshave0observations,notfullpoint/lowerCI/zeroimputation. Every4missing+1CPU-sadds0.573056h.
Observedordinarysupport1.204525–40.791652CPU-sassumption→247.553300–270.238923sourceCPUh,outward247.5–270.3. Separatemixedcheckpointordinary0.063124–0.089514/unsegmentedcomputation0.084421–0.084671→16.852182–23.911556modeledcheckingCPUh,outward16.8–24.0. Nofullchecking/matchedprotocol/CI/guarantee. No-assumptionupperunbounded;10xordinarymaxsource480.621868h. Missingcheck1x40.184493/2x63.560375/4x110.312141/12x297.319203h;4xno longer exceeds270.238923source,explicit12xstressdoes. Old4xcomparisonretainedashistory,notstillcurrent. LowBlockold-supportcounterexamplepreserved.
Paired31/42/14strata/11missing/dynamic13missing/RQ2CPU6.31/8.95andwall9.26/10.56/14.67/Bcensusdenominators/Ramseysampleallunchanged.

## WRITE_GATE
ActualMethods/RQ1updated38/4/19cells/domain/clock/subtotal/scenarios/stress.20oldtablebodies/title/fullabstract/fourRQ/sections/fourdesignimplicationsidenticaltoroot0275. No newtable/narrativeframing. Canonicalstatus/plan/index/evaluation/noveltysynchronized. Root0275paragraphretainedunchanged.
Raw/source/commands/stdio/memory/terminal/ownerW38smalloutputs/archive/own38frame/3CSV/analysisandeditcode/entrygzipsretained. Rootanalysis{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23,0native. Build/fullvisual/linkcheckspendingatentry,actualcompletionappends.

## REVIEW_GATE — self-review
Accepttheadditionalfixedoriginalandnewcompletecell;rejectdependencyweighting/coldbuild/fullpopulationpoint/CI/markersemanticphaseclaims/guaranteedgains. Resource/clock/trustdenominatorsseparate. FullmatrixMstill14/16atlastactualread,notfullPMU/RCcause;originalkerneldifferential/READrepairpreparednotrootqualified. OproductionRamsey190/444stopped;20samplequalified0275,notwholeclosure. SubexponentialSATownerplanisnotresult/rootdispatch.
Protectactualactiveowners/waiters;noforeignimplementation/infra/network/Tailscale/credential/UI/CronJob/resource/frequency/targetchanges. Noconfirmedhotdeliverytarget,nofalsedispatch/consumption. A/Cgenericnoveltydowngraded,Bglobalbudget/globalphaseweights/causalrepeats/software/axioms/cluster/nativebaseline/Envelopepairgapsremain. Self-review/normalpushnotresearchcompletion/OSDIacceptance.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0276 — TrackedTestBounds original source cost','# Root step0276 outer audit — 自审')+'\n## Outer disposition\nThe new cost completes one preselected stratum. Complete-domain and sensitivity changes are arithmetic consequences, not a population trend. Missing four stays missing; twelve-times stress is separately labeled. Existing owner work, original failures and earlier root results preserved.\n')
shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0276-recompute.py',e/'step0276-recompute.py')
print('EDIT276',s,'12stress',a['scenario_missing_check_twelve_times_source_CPU_h'])
