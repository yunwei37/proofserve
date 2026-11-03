from pathlib import Path
import os,json,gzip,shutil,re,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-ramsey-sample-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text());rel=str(s.relative_to(r));link=rel.removeprefix('docs/')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
p=r/'docs/paper/main.tex';t=p.read_text();old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode();assert t==old
tag=s.name.removeprefix('step-')
addition=r"""
\paragraph{A stopped certificate project yields a limited module-local sample.}
\measured{\expref{STEPTAG}{0275}; complete 20-file sample, incomplete directory.}
Ramsey production stops after 190 of 444 target files, consuming
22,146.098 native CPU-s for those new source files; no full-closure stream
runs. Four files are sampled without replacement from each of five equal-sized
source-byte strata of the retained 190-file prefix (seed 20261103).
All 20 separate original-kernel module-local processes accept.
Their summed checking CPU is 815.679s versus 2,271.357s for the same files'
source compilation, a pooled ratio of 35.91\%.
Individual CPU ratios have P10/median/P90 of 35.51/40.62/48.83\%.
Startup and imported-context loading are charged to each separate checker
process, and those imports remain trusted. These observations therefore do
not form a matched comparison with the shared-stream closure ratios above.

Weighting each sampled stratum mean by its 38 retained files estimates
7,748.952 CPU-s for independent module-local checking of the 190-file prefix,
or 34.99\% of its known source CPU.
A within-stratum percentile bootstrap (10,000 resamples) gives
29.41--40.41\%; with only four observations per stratum, this describes
resampling variation inside the observed prefix, not uncertainty from
dependency-order selection or the 254 unbuilt targets.
The built files all belong to Construction; their median source size is
4,457 bytes versus 81,652.5 bytes among the unbuilt files.
Only 24 of 180 kernel-marked files are built.
Neither the sample fraction nor its interval is extrapolated to all 444 files
or to whole-closure streaming.

A separate, excluded-from-sampling reference checks CertificatesK10 in
356.443 CPU-s against 1,725.134 source CPU-s (20.66\%).
This finite-certificate file has no \texttt{+kernel} marker but uses ordinary
\texttt{by decide}; marker absence cannot identify a cheap mathematical case.
The small-file process/import floor and the large certificate work must
remain distinct from a pure kernel-phase fraction.
\partialev{trusted imports, one observation per sampled file, a selected prefix,
and the recorded O resource-share deviation remain; full-directory cost,
axiom closure and repeated captures are missing.}

""".replace('STEPTAG',tag)
needle=r'\paragraph{System-design implication.}'
idx=t.index(needle,t.index(r'\paragraph{A bounded whole-source attempt remains partial.}'))
t=t[:idx]+addition+t[idx:];p.write_text(t)
for pattern in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pattern,t,re.S)==re.findall(pattern,old,re.S),pattern
assert t.count(r'\begin{tabular}')==20
row=f"| Ramsey retained-prefix sample | Production stopped190/444; no full stream.20/20 module-local references accept, pooled CPU35.91%; prefix-only weighted34.99%, resampling29.41–40.41% omits selection/missing-target uncertainty. Trusted imports, not a comparable full-closure ratio. | [0275]({link}/step-report.md) |\n"
p=r/'docs/research-status.md';txt=p.read_text().replace('Snapshot2026-11-03UTC, root0274.','Snapshot2026-11-03UTC, root0275.')
idx=txt.index('\n## Terminal failures');txt=txt[:idx]+row+txt[idx:];txt=txt.replace('Separate from current source36coverage/full closure.','Separate from current source37coverage/full closure.')
p.write_text(txt)
summary=f"""
[Root0275]({link}/step-report.md) independently qualifies the completed20-file Ramsey sample and the190-source stopped prefix. Source CPU22146.098430s is separate from815.679164sample checkerCPU-s; sampled source2271.356756s gives35.9115% pooled, individual P10/median/P90=35.5103/40.6179/48.8260%. Five38-file size strata,4uniform without-replacement samples each, seed20261103 exactly reproduced. Independent module-local prefix estimate7748.952058CPU-s/22146.098430=34.9901%;10000within-stratum percentile resamples29.4130–40.4104%, not an interval for dependency-order bias,254missing targets or whole streaming.190Construction files median4457B versus81652.5B in254unbuilt;24/180marked built. K10supplement excluded:356.442522/1725.133882CPU-s=20.6617%, no+kernel marker but finite ordinary-decide certificates. Imports trusted; process/import floor not kernel dominance. Historical whole-source2488/163097 and completeFalconer/Mathlib fractions unchanged. No newrootnative/Agent/queue or foreign edit.
"""
for name in ['docs/research-status.md','docs/research-plan.md']:
 p=r/name;txt=p.read_text()
 if name.endswith('research-plan.md'):
  txt=txt.replace('root0274','root0275',1)
  insert="\nCurrent owner snapshot at root0275: Ramsey full production is stopped at190/444, not a running closure to restore;20-file sample complete. M original PMUmatrix is13/16 at entry, P2 pending; raw inherited worker READ metadata defects prevent treating all counters as qualified. W source37 unchanged, Tracked preparation belongs to its existing master. Owner's SubexponentialSAT plan is preparation, not a root dispatch/result. Refresh actual terminals before any next integration.\n"
  ix=txt.index('\n## ',txt.index('\n')+1);txt=txt[:ix]+insert+txt[ix:]
 txt+=summary;p.write_text(txt)
p=r/'research/README.md';txt=p.read_text().replace('Current2026-11-03UTC, root0274.','Current2026-11-03UTC, root0275.')
needle='## Latest complete results\n'
txt=txt.replace(needle,needle+f"\n- [Ramsey completed sample](decoupled-check/ramsey-sampled-result.md), [root0275](../{rel}/step-report.md):20/20 retained-prefix module-local references accept, pooledCPU35.91%; weighted190-file estimate34.99% is prefix-only. Production stopped190/444, stream0/444; trusted imports and selection bias remain. Raw/source frozen in rootstep and original PVC size-sample directory.\n",1);p.write_text(txt)
p=r/'docs/novelty-20261101.md';p.write_text(p.read_text()+f"\n## Ramsey sampled boundary: root0275\n{summary}The result adds a finite cost-distribution and marker-only classification counterexample, not a new checking/sampling mechanism, a causal AI-authorship effect, or a complete computational-directory ratio. A/Cfirstness/Bglobalbudget claims do not change.\n")
p=r/'docs/evaluation.md';p.write_text(p.read_text()+f"""
## Root0275: stopped Ramsey production and completed retained-prefix sample
{summary}
All190source command/result/stdout/stderr records,20sample command/result/stdio records and separateK10oracle were independently read.211actual cgroups absent/noOOM; no-M/P0–7/sharedlock/1400s native limits/11.75GiBcharged observed. Sourcewait4HWM{a['source_HWM_KiB']}KiB/charged{a['source_charged_peak_B']}B; checkHWM{a['check_HWM_KiB']}KiB/charged{a['check_charged_peak_B']}B reported separately. No independentRSSsample/nativechildPIDbirth was emitted;3recordedcontroller/waiter births retired and20PID-only request IDs absent do not repair that gap. O4share deviation is not retroactively authorized.
190currentoleans remain; only10currentilean/Cfacets remain at outputpaths. Actual commands emit3facets, but their historical retention/cleanup timing is unknown. Initial root assertion expecting everycurrentfacet failed onFastLayoutGraph.ilean; failure and source retained, corrected to actual presence counts, no native rerun.
All190current source bytes108933392B match exact members of existing fixed4eaee875archive896084751B. This is selected-source comparison, not a new full lexical census/download.21selected/source-supplement files18489463B frozen with raw/code/reports in{a['raw_frozen_bytes']}Btar;190rawrecords retained without copying SDK/build/native objects. Source data/failedoldattempts remain onPVC.
Stopreceipt records originalcontroller491697/birth771798493 and waitingrequest548230/birth773592704 retired, noLean signalled. Root did not perform that stop, infer new authorization, restart production, or append relayed owner prose to user-instruction.md. Samplecontroller549487/birth773636437 retired. Next native plans are owner-owned, not root dispatch.
Rootoffline{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23;0native/Agent/queue. PaperlocalRQ2slot/canonicalindexupdated,20oldtables/title/fullabstract/fourRQ/sections/fourimplications preserved. Compilation/render review follows; root reports are self-review only.
""")
report=f"""# Root step0275 — Ramsey retained-prefix original-kernel sample
**自审. This is not independent review or venue acceptance.** Existing BUILD_AND_EVALUATE and the frozen four-RQ characterization contract remain.

## EXPERIMENT_GATE — entry and selected evidence
Read the latest verbatim direct decisions, current canonical status/plan/index/novelty, root0274's two reports, and actual W/M/O owner terminals. RQ2 is selected: compare production/checking cost at the declared trust boundary without confusing a module-local sample with a complete closure. The O20-file sample is genuinely complete; the444-file directory is not. No fresh experiment, replacement Agent, session, queue or implementation edit is started. Full experiment-design/review loops are skipped because this step independently qualifies an existing owner's completed finite capture, rather than proposing or executing a new native experiment. Full writing/idea/milestone-review skills are outside this incremental gate.

### Node1: source and protocol qualification
Read all190new source build command/result/stdout/stderr records and their ledger rows. All return0/no-sorry; command source and fixed input frame agree. All have no-M (also omit-M0), P0–7, authored autoImplicit=false,j8,1400s native allowance and olean/ilean/C output arguments. Actual190source CPU{a['source_cpu_s']:.6f}s and nativewall{a['source_wall_s']:.9f}s are new target costs only. The10744reused dependency costs remain the owner's separate historical premise; root does not claim to re-audit their entire raw ledger this step. No full Ramsey stream ran, so0/444records is absence of a streaming run, not a measured zero-cost full check.
All190current source files/{a['source_archive_bytes_compared']}B match exact selected members of the retained fixed4eaee875archive; no new download or full lexical census. All190typedoleans exist. Only10ilean/C outputs remain at current paths. The initial root all-facets-present assumption failed; original code/receipt stay retained, corrected presence is reported without inventing historical cleanup time. It is not nativefailure or evidence that commands omitted facets.

### Node2: exact planned sample and original-kernel acceptance
The original plan has five source-byte strata of38retained files each and four uniform draws without replacement per stratum, seed20261103. Root sorts the190actual file sizes/module IDs, regenerates all20selections exactly, verifies raw20results are ordered exactly as planned, and reads every original-kernel accept/command/result/stdio. All20return0/exactlyoneexpectedaccept/no reject. The ordinary one-mode AuditedStream source calls importModulesCore/finalizeImport then original Kernel.Environment.replay, retaining trusted imports. No new proof rules; adapter implementation remains trusted, not generalTCB/context/axiom transparency.
Samplechecking815.679164CPU-s / matching-source2271.356756CPU-s =35.911539%. Individual P10/median/P90=35.510335/40.617945/48.825980%. Per-process startup/import are included and source emits compiler work; these are not purekernelcomponent fractions or a matched Falconer/Mathlib stream comparison. Each is one fixed-order observation, retained caches, no repeatCI/causal hardware inference.

### Node3: estimands and selection bias
Weighted independent module-local checking estimate for the190retained prefix=7748.952058CPU-s; denominator is its known22146.098430sourceCPU-s, ratio34.990145%.10000within-stratum resamples/seed20261103 independently reproduce29.412983–40.410395%. This is a small-n within-prefix resampling interval, excludes dependency-order selection and missing254, not a full-directory/population/stream bound. Sample-pooled35.91% and prefix-weighted34.99% are different aggregations.
190built files allConstruction, median4457B;254unbuilt median81652.5B;only24/180kernel-marked files built. These size facts are checked against actual files/census, not a new validated semantic classifier. No scaling to444 or pooling into Wfixed42draws.
K10supplement was excluded by plan, not an extra random draw:356.442522checker/1725.133882sourceCPU-s=20.661731%, wall52.939625%. Its finite plain-decide certificates lack+kernel; marker absence does not prove noncomputational or cheap input. No phase attribution is inferred from its wholeprocess clock.

### Node4: resources and retirement
All211selected native source/checkcgroups are actually absent/noOOM.11.75GiBcharged cap; sourcewait4HWM{a['source_HWM_KiB']}KiB versus charged{a['source_charged_peak_B']}B; checkingHWM{a['check_HWM_KiB']}KiB versus charged{a['check_charged_peak_B']}B. No independentRSSsample or nativechildPIDbirth was emitted; no hardRSS/fullOtree4GiBclaim. Oresource-share deviation remains disclosed, never retroactively authorized.
Samplecontroller549487/birth773636437, originalproductioncontroller491697/birth771798493 and cancelledwaitingrequest548230/birth773592704 are actually retired.20requestPID-only records are absent, not birth-qualified nativechildren. Ownerstopreceipt says only nextwaitingflock cancelled after the window, noLean signalled; root did not stop/restart/changeownerpolicy or append that relay to the verbatimuserlog.
Root first analysis failed on current facet presence; code and receipt retained. Corrected offlineanalysis{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23. Raw/source/code/reports tar{a['raw_frozen_bytes']}B, source190/sample20/strata/currentfacets CSVs and entrygzips preserve provenance. No SDK/buildtrees/nativeobjects copied.

## WRITE_GATE — targeted result integration
Actual RQ2 paragraph now reports20/20sample, pooled/weighted estimates, clocks, trustedimports, stopped190/444production,0fullstream and nonresponse limits. No new table or narrative/RQ/title/abstract/section/implication rewrite. Canonical status/plan/index/evaluation/novelty synchronized. Historic wholelibrary2488/163097/Falconer/Mathlib and W37/42/18strata/5missing/31paired/13dynamic/Bdenominators remain separate.20oldtablebodies and all frozen fields compare exactly with0274.
Compilation/full-page visual review/link checks are pending at entry and will be appended only after actual completion.

## REVIEW_GATE — self-review and route
Accept this finite module-local cost distribution with explicit prefix/trust boundaries; reject full444acceptance/cost, whole-stream ratio, purekernelphase dominance from tinyprocessfloor, hardwarecausality or genericnewmechanism. No full iter-review milestone is invoked. Self-review does not establish OSDI acceptance.
M original16-point PMUmatrix was13/16at entry; newer P8inherited READ totals have a known coverage defect, so neither old0273bracket95.95% nor incomplete PMU source proves RC/cachecause. Wsource37remainslatestpublished, existingTrackedprep/master protected. OnewSubexponentialSATplan is preparation, not root-dispatched/result. Actual next terminals determine future work; do not restore cancelledRamsey, completedFalconer/Physical or oldMfinite series.
No network/Tailscale/server/credentials/UI/CronJob/frequency/target/resource settings changed. No confirmed owner hot-deliverytarget, no claimed dispatch/consumption. Globalphaseweights/causalrepeats/software/axioms/cluster/native module-taskbaseline/Envelopecompletepair still missing.
"""
(s/'step-report.md').write_text(report)
audit=f"""# Root step0275 outer audit — 自审
**Self-review, not independent audit or venue acceptance.**

## EXPERIMENT_GATE audit
The selected evidence answers the existing RQ2 boundary question: what a completed original-kernel module-local sample costs relative to its matching source work. The20-file finite sample is complete, while full Ramsey production is stopped190/444 and no full stream has run. This distinction is explicit in paper and records. Root invokes no new native capture, Agent, session or queue and does not alter foreign code.
Original20planned names match independently regenerated seed/size strata and20actualaccepts. All190source raws and21reference raws/commands/stdio are read; actual source bytes108933392match existing pinnedarchive.211cgroupsabsent/noOOM; noM/actualclock/11.75GiBcap verified. No invented nativechildbirth/RSSsample. SourceHWM{a['source_HWM_KiB']}KiB and charged{a['source_charged_peak_B']}B differ; observedOshare deviation remains.3realrecordedbirthsretired,20PID-only requests absent. Owner stop is retained evidence, not root action or reconstructed verbatimuserapproval.
Initial all-current-facets assumption failed; only10ilean/Cpaths remain. The failure, original code and corrected current-presence table stay preserved.190oleans remain, command3facets not misrepresented as currentretention. No native rerun follows.

## WRITE_GATE audit
20/20originalkernelreferences,815.679/2271.357CPU-s=35.91% are finite observations. Weighted190prefix7748.952/22146.098CPU-s=34.99% and29.41–40.41resamplinginterval have distinct estimation scope. Built/unbuilt size and24/180markercoverage document nonresponse. Neither proportion is a444-target/full-stream ratio. K10is excluded supplemental20.66%, not reweighted into the random sample. Trustedimports/process/importfloor remain visible.
TargetedRQ2paragraph/canonicalnavigation updated;20oldtables/title/fullabstract/4RQ/sections/fourdesignimplicationbodies unchanged. Fullwriting/refineideas/milestonereview skipped because their entry conditions are absent and no scientific contract change is needed. Actual compilation/visual/link checks append after completion.

## REVIEW_GATE audit and disposition
Self-review accepts bounded new cost observations and retained-prefix inference; rejects generalmechanismnovelty, full-directorycost/acceptance, causalAIauthorship, kernel-onlyphase claim, CIcoveringmissingtargets or retroactive resources. HistoricalW/O/Mdenominators stay untouched. MnewPMUmatrix ongoing, worker READ coverageproblem remains partial, no RCcause conclusion. Ownerplans are not measurements or rootdispatch.
Raw/source/code/failures/entrygzips retained. Rootoffline{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23,0native/Agent/foreignimplementation/infrachanges. Preserve actual activeowners and waiters. No useractionneeded and no false hotdelivery claim.
"""
(s/'outer-audit.md').write_text(audit)
for name in ['step0275-recompute.py','step0275-recompute-fixed.py']:
 q=Path('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030')/name;shutil.copy2(q,e/name)
print('EDIT275',s)
