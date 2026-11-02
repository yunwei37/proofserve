from pathlib import Path
import os,json,re,gzip,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-source35-root-step.txt').read_text().strip());e=s/'experiment-001';rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');suf=s.name.removeprefix('step-');a=json.loads((e/'reanalysis.json').read_text())
# Retain every sensitivity value, including the twice-source scenario that no longer exceeds source35.
a['scenario_missing_check_three_times_source_CPU_h']=a['scenario_missing_check_twice_source_CPU_h']+(a['scenario_missing_check_twice_source_CPU_h']-a['scenario_missing_check_equals_source_CPU_h'])
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n')
t=(r/'docs/paper/main.tex').read_text()
t=t.replace(r"""\measured{\expref{0269-20261102T191745+0000}{0269}}
Source-frame coverage is now 33/42 with 16 complete strata and 9 missing
costs.""",r"""\measured{\expref{STEP}{0270}}
Source-frame coverage is now 35/42 with 17 complete strata and 7 missing
costs.""".replace('STEP',suf))
t=t.replace(r"""The 33 completed no-\texttt{-M} random source targets sum to 522.338 seconds
of native wall intervals and 821.311 user-plus-system CPU seconds.""",r"""The 35 completed no-\texttt{-M} random source targets sum to 540.820 seconds
of native wall intervals and 851.200 user-plus-system CPU seconds.""")
begin=t.index(r'\measured{\expref{0269-20261102T191745+0000}{0269}; original-frame source-cost increment.}')
end=t.index('\nThese are source-compilation estimates',begin)
new=r"""\measured{\expref{STEP}{0270}; two further original-frame source costs.}
IntrinsicHolomorphicLogarithm completes in 9.698 native elapsed seconds and
9.735 CPU seconds; DihedralIntervals takes 8.784 elapsed and 20.154 CPU seconds.
Their completed 84-call continuation contains 82 dependencies and these two
original draws. Dependency work receives no additional sampling weight.
The Intrinsic cell still lacks its other draw; Dihedral completes a separate
98-module cell. For the 17 completed strata (144,663 modules), stratified
compiler CPU estimates are 57.546 hours in marked files and 160.674 hours
in other files: a conditional marked-file share of 26.37\%.
All nine marked strata have both draws, covering 5,848 marked modules;
four ordinary strata and 18,434 ordinary modules remain incompletely observed."""
t=t[:begin]+new.replace('STEP',suf)+t[end:]
t=t.replace(r"""The earlier 14- and 15-stratum shares, 17.14\% and 33.02\%, use different
covered domains, rather than successive measurements of the same population.""",r"""The earlier 14-, 15- and 16-stratum shares, 17.14\%, 33.02\% and 26.47\%,
use different covered domains, rather than repeated measurements of the same
population.""")
begin=t.index(r'\paragraph{Clock choice and nonresponse alter the estimand.}')
end=t.index(r'\paragraph{Source features do not establish bounded prediction error.}',begin)
new=r"""\paragraph{Clock choice and nonresponse alter the estimand.}
\measured{\expref{STEP}{0270}; same 17 complete source strata, offline arithmetic.}
The conditional marked share is 26.37\% of weighted compiler CPU but 21.17\%
of summed native elapsed time, a 5.20-percentage-point difference.
The latter adds native process durations; it is not parallel Lake makespan
or an isolated checking-phase share of whole-library time.
CPU weights include worker execution; elapsed weights reflect each module's
wall duration at the measured concurrency point.
Earlier clock contrasts remain separate coverage snapshots.

The four incomplete strata contain 18,434 of 163,097 modules (11.30\%),
not necessarily that many unbuilt files. Seven original source costs are absent.
The 35 known terms in the eventual complete-sample Horvitz--Thompson point
sum to 227.989 CPU-hours. This is an algebraic subtotal, not a lower confidence
limit or a zero-filled population estimate.
Increasing every missing draw by one CPU second would increase the eventual
point by 4.117 CPU-hours under the fixed original weights.
This sensitivity does not predict the missing costs or their variance.

\paragraph{Whole-frame costs require explicit missing-cost scenarios.}
\partialev{\expref{STEP}{0270}; fixed 35-source sensitivity, not measurements
or confidence limits.}
Preserving 35 known costs and original inclusion weights, assume the 7 remaining
ordinary-marker draws cost between the observed ordinary minimum and maximum,
1.204525--40.791652 CPU-s.
Whole-frame construction scenarios then span 232.9--396.0 CPU-hours,
with endpoints rounded outward.
The earlier 33-draw 224.1--427.4-hour source range remains a dated assumption
scenario; the smaller current width follows additional observed costs.

A separate transfer model gives 15.9--35.2 checking CPU-hours.
It assigns ordinary modules the complete checkpoint-closure CPU
fractions 0.063124--0.089514 and marked modules the older unsegmented
computation fractions 0.084421--0.084671.
This deliberately mixes protocol-specific anchors; it is neither a measured
matched protocol nor evidence that source markers identify checking cost.
The earlier 15.3--38.0-hour transfer used the 33-cost snapshot.
Neither model is measured whole-library checking cost, a confidence interval
or a guaranteed saving. Their known terms include incomplete-stratum draws,
not just the 17 complete strata; they also differ from RQ2's trusted-import
target checks and its complete selected closures.

The LowBlock15\_1 observation remains 184.589 CPU-s, above the old
31-draw marked-class maximum of 163.846 CPU-s, demonstrating that observed
support is only an assumption.
Without missing-cost assumptions, the completion-cost upper remains unbounded.
Assigning all missing draws ten times the observed ordinary maximum raises
the source scenario to 1,907.4 CPU-hours.
At the current class-maximum source scenario, giving missing draws no
checking savings yields 183.6 modeled checking CPU-hours; twice their source
work yields 351.5. Three times their source work yields 519.4, above the
396.0-hour source scenario.
These are different stress assumptions, not measured checking costs.
A subunit factor assigned to unknown modules cannot establish general benefit.
All 7 unobserved original source costs remain missing in the primary evidence.

""".replace('STEP',suf)
t=t[:begin]+new+t[end:]
old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
assert t.count(r'\begin{tabular}')==20
(r/'docs/paper/main.tex').write_text(t)
entry=f"""[Root0270]({drel}/step-report.md) qualifies the actual84/84rc0terminal (19:44:26UTC), advancing the earlier Wsource34/77prefix:82dependencies+Intrinsic9.734671CPU/9.698324wall andDihedral20.154170CPU/8.784143wall. Original35/42,17/21complete strata/144663modules;7ordinary original costs missing/18434module domain incomplete. Conditional source218.220065CPUh, marked57.546404h=26.3708%; nativeelapsed marked21.1685%. KnownHTsubtotal227.988537h only; each missing+1CPU-s adds4.117083h. Source support scenarios232.9–396.0CPUh; separate mixed-protocol check transfer15.9–35.2CPUh, not actual full checking/CI/guarantees. Wpaired31/42/14strata/dynamic13missing unchanged."""
for fn in ['docs/research-status.md','docs/research-plan.md']:
 p=r/fn;v=p.read_text().replace('root0269.','root0270.')
 v=re.sub(r'Paper root0269:[^\n]+','Paper root0270: actual84terminal/source35 qualification; final compile/all-page verification pending.',v)
 v=v.replace('Source9/paired11/dynamic13 gaps differ','Source7/paired11/dynamic13 gaps differ').replace('9original source costs,11paired','7original source costs,11paired')
 v=v.replace('Current source33data preserve conditional marked CPU26.467% over16complete strata,','Current source35data preserve conditional marked CPU26.371% over17complete strata,')
 v=v.replace('Whole-frame224.1–427.4source/\n15.3–38.0modeledstream CPUh','Whole-frame232.9–396.0source/\n15.9–35.2modeledstream CPUh')
 v=v.replace('Forecast/classification historical31-input panels do not become33-input experiments.','Forecast/classification historical31-input panels do not become35-input experiments.')
 if fn.endswith('status.md'):
  v=re.sub(r'^\| Source probability frame .*$', '| Source probability frame |35/42originals;17/21complete strata/144663modules.9marked cells/5848files complete; markedCPU57.546/218.220h=26.371%, nativeelapsed21.1685%.7ordinary costs missing/18434module domain incomplete. | [0270]('+drel+'/step-report.md) |',v,flags=re.M)
  v=re.sub(r'^\| Whole-frame scenarios .*$', '| Whole-frame scenarios |35known+7ordinary missing within observed support:232.9–396.0sourceCPUh; mixed-protocol check transfer15.9–35.2CPUh. Assumptions, not CI/guarantee/measured full checking; no-assumption upper unbounded. | [0270]('+drel+'/step-report.md) |',v,flags=re.M)
 else:
  v=v.replace('Source33/42/16strata,9missing.','Source35/42/17strata,7missing.')
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';p.write_text(p.read_text()+'\n\nActual84terminal/source35 [root0270](../'+rel+'/step-report.md):35/42originals,17complete strata; source232.9–396.0CPUh/mixed transfer15.9–35.2CPUh are assumptions. Wpublished34is an earlierprefix, fullterminal includesDihedral. Raw input/source35frame and originalcosts are in root record; no new replay/grain denominator.\n')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+'\n\n## 2026-11-02 — root0270 actual84terminal and source35\n\n'+entry+'\n\nRoot reads all84actualcommands/results/stdio/memory/outputfacets;1240925sourcebytes equal pinnedtree, no archive rescan. Controller480233/birth769918349+84actualnativeidentities=85retired;84cgroupsabsent/noOOM/stop. noM/P0–7/j8/unprofiled/authoredHB/3facets/15GiBcharged+16GiBsampledresponse. HWM7388300KiB/sample7565619200B/charged1166446592B separate. Native1026.542661wall/1183.254075CPU vs2066.092917controller includesqueue/setup/cleanup. IntegralPairingsdependency nowrc0 at703.398393wall/738.797420CPU under1200s allowance, aftertwo old600s censors; different budget/capture, not same-budget recovery or mathematical falsity. Dihedralactualselfallowance672.241481s clipped bygroup, not600or1200. Intrinsic1200s. No dependency gets originalweight. Rootsource35frame extends exact42frame bytwoactualIDs from0269source33; earlierWsource34prefixretained. M v1P2alias is invalid for fit and v2plan alone is not curve. Osourcecauseclassification still not independently qualified here. Allraw/failure/partial preserved,0rootnative/agent/foreignedits/queue/infra changes.\n')
p=r/'docs/novelty-20261101.md';p.write_text(p.read_text()+'\n\n## 2026-11-02 — actual source35 coverage\n\n'+entry+'\nA narrowed missing-support scenario does not establish global phase weights, a cost classifier, CI, fullchecking benefit or new A/B/C mechanism. No new literature search/independent review. Source34ownerprefix is not the latest terminal; root qualifies84actualreturns before using35costs.\n')
report=f"""# Root step0270 — actual84terminal/source35
**自审; not independent audit/venue acceptance.** BUILD_AND_EVALUATE, original characterization title/abstract/fourRQ/sections/fourdesignimplications preserved.

## EXPERIMENT_GATE
Entry reads latest direct user decision/canonical0269 and owner W091/a068d38, Mplan/qualification and Oprogress. No rootnative or new agent/session/queue admitted. Heartbeat text not user-authored speech; user-instruction unchanged.
Wpublished34reflects77prefix, butactualterminal19:44:26UTC is84/84compile_ok,82dependencies+2originals. Root reads84rawcommands/noM/P0–7/j8/defaultauthoredHB/unprofiled/3facets/sharedtasklock/15GiBcharged+16GiBsampleRSSresponse. All1240925sourcebytes equal existing pinned4eaee875tree; original .olean/.ilean/C sizeschecked. No new fullarchive/corpus scan. Controller480233/birth769918349plus84nativebirths retire,84cgroupsabsent/noOOM/stop. wait4HWM7388300KiB/sample7565619200B/charged1166446592B distinct; no hardRSS or wholetreecompliance claim.
Native1026.542661wall/1183.254075CPU; controller2066.092917s includesqueue/setup/cleanup, not pure wait. Intrinsic9.698324wall/9.734671CPU,1200selfallowance; Dihedral8.784143wall/20.154170CPU,actual672.241481selfallowance. IntegralPairings703.398393wall/738.797420CPU succeeds atdifferent1200allowance; two600censors retained, notsamebudgetrecovery or proofrejection.

Exact42module+stratumframe compared with0269source33; only2originalIDsadded. Root creates ownsource35frame without editingWowner files; existingpublished34completedrows match.35originalCPU851.200151s/nativewall540.820183s;17complete strata/144663modules,7ordinarycosts missing/18434domain. IntrinsiccellN7225stillhalf; DihedralcellN98nowcomplete. ConditionalCPU218.220065h/marked57.546404=26.370813%; nativeelapsed189.048013h/marked40.018606=21.168488%. Coverage-dependent, not same-population trend or kernelphase.
KnownHTsubtotal227.988537h is notpopulationestimate/lowerCI/zeroimputation; missing+1CPU-s each adds4.117083h. Observedordinarysupport1.204525–40.791652s→232.947667–395.931168sourceCPUh. Mixedcheckpointordinary0.063124–0.089514/unsegmentedcomputation0.084421–0.084671transfer15.930213–35.162806h; notmatchedprotocol/fullcheck/CI/guarantee.10xmaxsource1907.414843h. Missingcheck1xsource183.559803h/2x351.502434h/3x519.445064h; 2x no longer exceeds currentsource, retainedhonestly. 3x is anotherexplicitstressassumption, notmeasurement. No-assumption upperunbounded.
Source34/33/32oldscenarios remain dated. Paired31/42/14strata anddynamic13missing do not become35; no new targetcheck/grain/axiomclaims.

## WRITE_GATE
Methods/RQ1current35source slots andcanonicals updated. All20tablebodies/title/fullabstract/fourRQ/sectionhierarchy/fourdesignimplication bodies compared identical; no newtable. Onlyscoped result/limits changed, no new mechanism/authorhypothesis or literaturesearch. Raw84commands/results/memory/stdio/terminal/source frozen;2oldcensors preserved atoldpaths. No largeobjects copiedGit. Source35CSVrootown beforeinputs/analysis/code retained.
Compile/render/links pending atinitialreport; actualcompletion appended later.

## REVIEW_GATE — root selfreview/routing
Direction preserved. User intent wants realdata thenpaper, so terminal overrulesstaleW77prefix; no easy replacements or duplicateweights. Rootanalysis{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB onE22–23. No rootnative. Sourcecostsample additionaloriginals matter, dependencies unweighted, modeledchecking never actualchecking. FourRQglobal/software/axiom/cluster/nativebaseline/Envelopepair gaps remain.
Moldp12completefile isv1withinvalidP2physicalalias, notcorrectedfullcurve. Readcorrectedv2fullterminal beforeperformanceintegration. Oexistingclassification/differential notnewroot-qualifiedcause. Wactual84controllercompleted; do notresume it fromoldrunning. Existingowners decideownnextplan; no replacementAgent/session/collection launched or falselydispatched. Host/network/Tailscale/CronJobs/resources unchanged.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0270 — actual84terminal/source35','# Root step0270 outer audit — 自审')+'\n## Disposition\nRoot independently reconciled terminal, PIDbirth/cgroups, source/outputmode and42-IDweights before writing35. Self-review lacks independence and is not venueacceptance. Keep raw/resource/censor/trust boundaries explicit, integrate only actualfutureterminal withinexistingowners.\n')
print('EDIT270',s,'stress3x',a['scenario_missing_check_three_times_source_CPU_h'])
