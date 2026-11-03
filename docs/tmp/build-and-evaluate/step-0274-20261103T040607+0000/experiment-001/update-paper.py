from pathlib import Path
import os,json,re,gzip
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-source37-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text());rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');suf=s.name.removeprefix('step-');tag=r'\expref{'+suf+r'}{0274}'
a['scenario_missing_check_three_times_source_CPU_h']=2*a['scenario_missing_check_twice_source_CPU_h']-a['scenario_missing_check_equals_source_CPU_h'];a['scenario_missing_check_four_times_source_CPU_h']=3*a['scenario_missing_check_twice_source_CPU_h']-2*a['scenario_missing_check_equals_source_CPU_h'];(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n')
raw=Path(a['new_originals'][0]['raw']);assert (raw/'native.log').read_bytes()==b'';cmd=json.loads((raw/'command.json').read_text());assert cmd['self_wall_s']==1200
t=(r/'docs/paper/main.tex').read_text()
oldtag=r'\expref{0272-20261103T025723+0000}{0272}'
t=t.replace(oldtag+'}\nSource-frame coverage is now 36/42 with 18 complete strata and 6 missing',tag+'}\nSource-frame coverage is now 37/42 with 18 complete strata and 5 missing')
t=t.replace(r'The 36 completed no-\texttt{-M} random source targets sum to 545.802 seconds'+'\nof native wall intervals and 858.220 user-plus-system CPU seconds.',r'The 37 completed no-\texttt{-M} random source targets sum to 549.607 seconds'+'\nof native wall intervals and 862.121 user-plus-system CPU seconds.')
st=t.index(r'\measured{'+oldtag+'; one further original-frame source cost.}');en=t.index('\nThese are source-compilation estimates',st)
add=r"""\measured{TAG; one further original-frame source cost.}
PhysicalFieldPopulationLimit completes in 3.806 native elapsed seconds and
3.901 CPU seconds. Its untimed E-core prerequisites receive no sampling
weight or imputed CPU cost.
It supplies one draw in a 9,146-module ordinary stratum; the matching
TrackedTestBounds draw remains missing, so no additional stratum completes.
For the same 18 completed strata (151,888 modules), stratified compiler CPU
estimates remain 57.546 hours in marked files and 177.487 hours in other files:
a conditional marked-file share of 24.48\%.
All nine marked strata have both draws, covering 5,848 marked modules;
three ordinary strata and 11,209 ordinary modules remain incompletely observed.""".replace('TAG',tag)
t=t[:st]+add+t[en:]
st=t.index(r'\paragraph{Clock choice and nonresponse alter the estimand.}');en=t.index(r'\paragraph{Source features do not establish bounded prediction error.}',st)
add=r"""\paragraph{Clock choice and nonresponse alter the estimand.}
\measured{TAG; same 18 complete source strata, offline arithmetic.}
The conditional marked share remains 24.48\% of weighted compiler CPU and
19.64\% of summed native elapsed time, a 4.85-percentage-point difference.
The latter adds native process durations; it is not parallel Lake makespan
or an isolated checking-phase share of whole-library time.
CPU weights include worker execution; elapsed weights reflect each module's
wall duration at the measured concurrency point.
Earlier clock contrasts remain separate coverage snapshots.

The three incomplete strata contain 11,209 of 163,097 modules (6.87\%),
not necessarily that many unbuilt files. Five original source costs are absent.
The 37 known terms in the eventual complete-sample Horvitz--Thompson point
sum to 239.988 CPU-hours. This subtotal includes the newly observed draw
in an incomplete stratum; it is not a lower confidence limit or a zero-filled
population estimate.
Increasing every missing draw by one CPU second would increase the eventual
point by 1.843 CPU-hours under the fixed original weights.
This sensitivity does not predict the missing costs or their variance.

\paragraph{Whole-frame costs require explicit missing-cost scenarios.}
\partialev{TAG; fixed 37-source sensitivity, not measurements
or confidence limits.}
Preserving 37 known costs and original inclusion weights, assume the 5 remaining
ordinary-marker draws cost between the observed ordinary minimum and maximum,
1.204525--40.791652 CPU-s.
Whole-frame construction scenarios then span 242.2--315.2 CPU-hours,
with endpoints rounded outward.
The earlier 36-draw 238.7--362.1-hour source range remains a dated assumption
scenario; the smaller current width follows an additional observed cost.

A separate transfer model gives 16.5--28.0 checking CPU-hours.
It assigns ordinary modules the complete checkpoint-closure CPU
fractions 0.063124--0.089514 and marked modules the older unsegmented
computation fractions 0.084421--0.084671.
This deliberately mixes protocol-specific anchors; it is neither a measured
matched protocol nor evidence that source markers identify checking cost.
The earlier 16.2--32.2-hour transfer used the 36-cost snapshot.
Neither model is measured whole-library checking cost, a confidence interval
or a guaranteed saving. Their known terms use all 37 observed draws; they
also differ from RQ2's trusted-import target checks and complete selected closures.

The LowBlock15\_1 observation remains 184.589 CPU-s, above the old
31-draw marked-class maximum of 163.846 CPU-s, demonstrating that observed
support is only an assumption.
Without missing-cost assumptions, the completion-cost upper remains unbounded.
Assigning all missing draws ten times the observed ordinary maximum raises
the source scenario to 991.9 CPU-hours.
At the current class-maximum source scenario, giving missing draws no
checking savings yields 91.6 modeled checking CPU-hours; twice their source
work yields 166.8 and three times yields 242.0.
Four times their source work yields 317.1, above the 315.2-hour source scenario.
These are different stress assumptions, not measured checking costs.
A subunit factor assigned to unknown modules cannot establish general benefit.
All 5 unobserved original source costs remain missing in the primary evidence.

""".replace('TAG',tag)
t=t[:st]+add+t[en:]
old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
assert 'Source-frame coverage is now 37/42'in t and t.count(r'\begin{tabular}')==20
(r/'docs/paper/main.tex').write_text(t)
entry=f"""[Root0274]({drel}/step-report.md) independently qualifies PhysicalFieldPopulationLimit actual03:32:26UTC original return3.805640wall/3.900684CPU-s. Fixed42frame adds onlythisID;prior36costs match.37/42originals,18/21complete strata/151888coveredmodules unchanged becauseTrackedTestBoundsstillmissing in9146cell.5ordinary costs missing/11209module domain incomplete. Conditional235.032925CPUh/marked24.4844%/elapsed19.6382% unchanged;KnownHTsubtotal239.987877hincludesoneincomplete-celloriginal,notfullestimate/CI. Eachmissing+1CPU-sadds1.843333h. Sourceobservedsupportscenarios242.2–315.2CPUh; separate mixed-protocolchecktransfer16.5–28.0CPUh,notmeasuredfullchecking/CI/guarantees. Stressmissingcheck3xnow242.0hdoesnotexceedsource315.2;explicit4x317.1hdoes. Paired31/42/14strata/11missing,dynamic13missingnotfilledbysource37."""
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text().replace('root0273.','root0274.')
 v=re.sub(r'Paper root0273:[^\n]+','Paper root0274: source37 qualification; final compile/all-page verification pending.',v)
 v=v.replace('Source6/paired11/dynamic13 gaps differ','Source5/paired11/dynamic13 gaps differ').replace('6original source costs,11paired','5original source costs,11paired')
 v=v.replace('Current source36data preserve conditional marked CPU24.484% over18complete strata,','Current source37data preserve conditional marked CPU24.484% over18complete strata,')
 v=v.replace('Whole-frame238.7–362.1source/\n16.2–32.2modeledstream CPUh','Whole-frame242.2–315.2source/\n16.5–28.0modeledstream CPUh')
 v=v.replace('do not become36-input experiments.','do not become37-input experiments.')
 if n.endswith('status.md'):
  v=re.sub(r'^\| Source probability frame .*$', '| Source probability frame |37/42originals;18/21complete strata/151888modules unchanged.9marked cells/5848files complete; markedCPU57.546/235.033h=24.484%, nativeelapsed19.6382%.5ordinary costs missing/11209module domain incomplete. | [0274]('+drel+'/step-report.md) |',v,flags=re.M)
  v=re.sub(r'^\| Whole-frame scenarios .*$', '| Whole-frame scenarios |37known+5ordinary missing within observed support:242.2–315.2sourceCPUh; mixed-protocol check transfer16.5–28.0CPUh. Assumptions, not CI/guarantee/measured full checking; no-assumption upper unbounded. | [0274]('+drel+'/step-report.md) |',v,flags=re.M)
 else:v=v.replace('Source36/42/18strata,6missing.','Source37/42/18strata,5missing.')
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';v=p.read_text();v=re.sub(r'^Current[^\n]+','Current2026-11-03UTC, root0274. [Status](../docs/research-status.md) ·',v,count=1,flags=re.M);p.write_text(v+'\n\nPhysical/source37 [root0274](../'+rel+'/step-report.md), [Wresult](../workloads/openai-math/final-seven-20261102/collection-remaining-six-20261103T0325/source37-PhysicalFieldPopulationLimit/README.md):37/42originals/18complete strata; source242.2–315.2CPUh/mixed checktransfer16.5–28.0CPUh scenarios, notCI/wholelibrarymeasurement.5source/11paired/13dynamicmissingremainseparate; no completednewcelluntilTracked.\n')
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0274 Physical/source37\n\n'+entry+'\nRootactualraw/command/result/stdio/memory/nativeidentity/cleanup/source/outputfacetsread;3354sourcebytesmatchfixed4eaee875tree,no new fullarchive scan. noM/P0–7/j8/unprofiled/authoredHB/3facets/1200selfallowance/15GiBcharged+16GiBRSSresponse. Controller526701/birth772878788+native527183/birth772932569retired,cgroupabsent/noOOM/sample-stop;HWM7190800KiB/sample7285751808B/charged714616832Bdifferent,nohardRSS/wholelaneclaim. C1904/olean160624/ilean12421Bverified;empty native.lognoerror/sorry. Native3.805640wallvscontroller541.579913s;per-row537.766580queue/setup/cleanupseparate,wholecontrollerdifference537.774273notpureschedulerwait. Eprep1200attempts/1199deps/retainedclippedcensornotneworiginals/costweights;rootdidnotrequalifythatentiredependencysequence. MnewPMUmatrix5/16partial,notfinalhardwarecause;OreadRamsey10928/11188source184/444new,kernel0/444stillprefix. Existingowners/mastershealthyprocessesprotected,0rootnative/agent/queue/foreignimplementation/infrachanges. Prior0273referencegraphpostcheckreceiptandliteraloldaccept/newheaderfailureexplanationnowfrozenherewithoutchangingoldreports.\n')
post=Path('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0273-reference-graph-postcheck.json');(e/'root0273-reference-graph-postcheck.json.gz').write_bytes(gzip.compress(post.read_bytes()))
report=f"""# Root step0274 — PhysicalFieldPopulationLimit original source cost
**自审; not independent review or venue acceptance.** Existing BUILD_AND_EVALUATE;centralcharacterization/fourRQcontractunchanged.

## EXPERIMENT_GATE
Readlatestdirectuserdecisions/canonical0273/tworootreports/W103realoriginalterminal/M037newpartialPMUreport/Oactualprefix. No newnative/Agent/session/queue. OwnerordinaryfiniteglueisnotnewAIagentorrootdispatch;protectactualongoingWmaster/Trackedprep,don'tretiremasterfromcompletedchild.
Actual1planned/1nativecompile_okterminal03:32:26UTC,sourcePhysicalFieldPopulationLimit. Rawplan/command/result/native.log(empty)/memory/nativeidentity/cleanup/controller/outputfacetsread. Source3354Bbyte-identicaltoexisting4eaee875pinnedtree,notnewarchivecensus. noM(alsoomit-M0)/P0–7/j8/unprofiled/authoredHB/3facets/sharedper-tasklock/15GiBcharged+16GiBRSSresponse. Actualselfallowance1200snot600or1700pool. CPU2.743075user+1.157609sys=3.900684s;nativewall3.805639804s. Controller541.579912785s;per-rowqueue/setup/cleanup537.766580389s,notpurewaitnoridenticaltocompletecontrollerdifference.
Controller526701/birth772878788andnative527183/birth772932569retired,cgroupabsent/noOOM/stop. HWM7190800KiB/sample7285751808B/charged714616832Bseparate;no hardRSS/fullWtreequalification. OutputC1904/olean160624/ilean12421Bsizechecked. No inventedlauncherbirth. W1200Eprep rows/1199depsincludeoldcensorandlatersuccess,untimed/noweights;rootdidnotre-auditallprerequisitesorcoldtransitivebuild.

Exact42module/stratumframecomparedwithroot0272source36;onlyPhysicaladded. Prior36costs/W37publishedcompletedrowsmatch,rootownsource37frame,noWfileedit.37actualCPU862.120848/nativewall549.607457129s.18completestrata/151888domainstayunchanged:TrackedTestBoundsmissingin9146cell.5ordinaryoriginalcostsmissing/3incompletecells/11209module domain(6.8726%). ConditionalCPU235.032925h/marked57.546404h=24.484401%,elapsed203.778943h/marked40.018606h=19.638244%,samecoveredestimandunchanged. KnownHTsubtotal239.987877hincludesPhysicalhalfcell,notfullpopulationpoint/lowerCI/zeroimputation. Everymissing+1CPU-sadds1.843333333h.
Observedordinarysupport1.204525–40.791652CPU-swith5missing→242.208218–315.180489sourceCPUh,paperoutward242.2–315.2. Mixedcheckpointordinary0.063124–0.089514/unsegmentedcomputation0.084421–0.084671transfer16.514778–27.934467h,outward16.5–28.0. Neitherfullchecking/matchedprotocol/CI/guarantee. No-assumptionupperunbounded;10xordinarymaxsource991.913996h. Missingcheck1x91.567233/2x166.759844/3x241.952456/4x317.145068CPUh;3xnowNOTexceedsource315.180489,retainthatfactandlabel4xasnewexplicitstressassumption,notmeasurement. LowBlock184.589>oldmarkedmax163.846supportcounterexampleretained. Oldsource36/35etcdatedscenariosnotcurrent. Paired31/42/14strata/11missing,dynamic13missingunchanged,noPhysicalkernel/replay/axiomresult.

## WRITE_GATE
ActualMethods/RQ1new37cost/clock/subtotal/scenarioandstressslotsupdated;18completestratanotfalsely19.20oldtablebodies/title/fullabstract/fourRQ/sections/fourdesignimplicationsidentical,nounrequestednewtable/framing. Canonicalstatus/plan/index/evaluation/noveltysynchronized;indexstale0267headerupdatedonlycurrentnavigation,historyintact.
Raw/source/commands/stdio/memory/terminal/smallW37outputs/rawtar/beforeentry/rootframe/3smallCSV/recomputeandeditcodepreserved,noSDK/nativeobjectcopies. Root0273postpublisholdserialgraphschemafailure/exact4449imports+countsmatchreceiptcopiedherefromretainedPVC,notretroactiveoldreportrewrite. Prior0273fixedworkCPUinflationresultunchanged.
Compile/render/linkchecks initiallypending;completedreceiptsappendlater.

## REVIEW_GATE — self-review/routing
Directionunchanged. Acceptactualneworiginal/fixedweights;rejectdependencycosts/coldbuild/completepopulation/CI/markersassemanticphases/guaranteedgain. Rootreduce{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23,no newnative. Missing5not0;singleobservedPhysicalnotnewindependentfullclosure. Userfixedoriginalframeandownersretained.
M037actualnewPMUmatrix5/16returned,notcompleteP8cohort/operationcause. ItsfreshCcallclockhasdifferentobserverboundaryfrom0273andcannotreplaceold95.95%withnewdenominatorbeforefullterminalqualification. OcurrentRamsey10928/11188source184/444new,kernel0/444stillprefix,historicalwholelibrary2488/163097acceptanceunchanged. WnextTrackedownerprepongoing,rootdidnotdispatchreplacement/resumeoldqueues. Currenthotdeliverytargetunconfirmed,nofalsecommunicationclaim. No network/Tailscale/server/credential/UI/CronJob/resourcechange. Globalphaseweights/causalrepeats/software/axioms/cluster/nativebaseline/Envelopepairgapsremain;self-reviewnotindependentacceptance.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0274 — PhysicalFieldPopulationLimit original source cost','# Root step0274 outer audit — 自审')+'\n## Disposition\nOneoriginalfillsonefixedhalfcell;complete-stratumdomainandconditionalshareunchanged. Stress3xdoesnotexceedcurrentsource;4xseparatelylabeled. Alloriginal/raw/failure/historypreserved. NeithernewPMUprefixnoruntimedEworkusedascompletedcostevidence. Rootself-reviewonly.\n')
print('EDIT274',s,'stress3',a['scenario_missing_check_three_times_source_CPU_h'],'stress4',a['scenario_missing_check_four_times_source_CPU_h'])
