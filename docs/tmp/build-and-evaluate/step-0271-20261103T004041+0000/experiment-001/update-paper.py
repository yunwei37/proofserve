from pathlib import Path
import os,json,re,gzip,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-producer-errors-root-step.txt').read_text().strip());e=s/'experiment-001';rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');suf=s.name.removeprefix('step-');a=json.loads((e/'reanalysis.json').read_text())
t=(r/'docs/paper/main.tex').read_text()
old=r"""\partialev{\expref{0268-20261102T190628+0000}{0268}; source coverage and compilation failures unresolved.}"""
assert old in t;t=t.replace(old,r"""\partialev{\expref{STEP}{0271}; incomplete source coverage and scoped producer diagnostics.}""".replace('STEP',suf))
old=r"""The production ledger records 9,124 source-compilation returns of
\texttt{rc=1}, whose causes remain under investigation.
These returns are not classified as kernel or mathematical rejections."""
new=r"""The production ledger records 9,124 source-compilation returns of
\texttt{rc=1}.
\measured{\expref{STEP}{0271}; retained diagnostic census and finite controls.}
Of these, 9,118 report unavailable interpreter or native declarations,
four lack module data and two report IR/code-generation errors.
The diagnostics do not establish a single failing phase for all invocations.
A separate four-case qualification, using complete original package paths,
compiles three pinned source files named in the failures and an Init import
control; an earlier metadata-only copy retry still fails.
These controls also differ in output facets and resource limits, so they
neither isolate one missing runtime component nor provide a timing comparison.
They do not establish that every failed source will compile after repair;
the two IR/code-generation cases still need qualified retries.
None of the 9,124 returns is counted as a qualified kernel or mathematical
rejection, and the four controls do not increase source acceptance coverage."""
assert old in t;t=t.replace(old,new.replace('STEP',suf))
before=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,before,re.S),pat
assert t.count(r'\begin{tabular}')==20
(r/'docs/paper/main.tex').write_text(t)
entry=f"""[Root0271]({drel}/step-report.md) reads all9124retained rc1source records/stdout/stderr:4697unknowninterpreterdecl+4421missingnativeexternal=9118unavailabledecldiagnostics,4missingmoduledata,1compilerIRmissingcode,1LakeinterpreterIR.139of9118are not atsource line1, so no uniform import/phase claim.4successful qualification controls=3pinned sourcefiles+1Init import control, plus preserved failedmetadata-copy retry. Current3source bytes11197match fixed full archive; old duplicate failure-input source copies are absent, so no direct historical-byte recheck. Old600s/11.5GiB/olean-only versuscontrols300s/11.75GiB/3facets and unlogged per-open env trace prevent isolatedfacet/cost causal claims.9124do not become proofrejection or repairedpasses. Historical2488/163097source+10744dependencies remains partial; currentRamsey is a separate unfinished closure, not its denominator."""
for fn in ['docs/research-status.md','docs/research-plan.md']:
 p=r/fn;v=p.read_text().replace('root0270.','root0271.')
 v=re.sub(r'Paper root0270:[^\n]+','Paper root0271: producer diagnostic census and scoped controls; final compile/all-page verification pending.',v)
 v=v.replace('O newly visible source-error report is retained for later independent attribution qualification; root0268 audits9124rc1count and2488source accepted, not all log causes or a repaired producer run.','Historical0268scope audited rc1count only. Root0271now independently classifies the retained9124diagnostics and qualifies finitecontrols, without asserting uniform phase/singlefacet/all-source repair.')
 if fn.endswith('status.md'):
  where='## Terminal failures and trust that remain visible'
  assert where in v
  row='| Whole-source producer diagnostics |9124rc1:9118unavailable interpreter/native declarations,4module-data,2IR/codegen.4finitecontrols pass;139declaration diagnostics notline1. Whole-source2488/163097stillpartial, no proof rejection/yield/globalcost conclusion. | [0271]('+drel+'/step-report.md) |\\n\\n'
  v=v.replace(where,row+where)
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';p.write_text(p.read_text()+'\n\nProducer diagnostics [root0271](../'+rel+'/step-report.md), [Oreport](decoupled-check/whole-library-source-errors.md), [finitecontrols](decoupled-check/ramsey-qualification.md): all9124rc1logs classified;4controls do not prove all-source repair, uniformphase or isolatedruntimefacet.2488/163097historicalsource acceptance unchanged; Ramsey is separate/pending. No new native run byroot.\n')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0271 producer diagnostics and finite qualification\n\n'+entry+f'\n\nFailed-source work9235.245726CPU-s/9379.187498nativewall-s retained as failure diagnostics, not added to successfulFalconer6.31% numerator or whole-library cost. Maximumwait4RSS6239176KiB/charged353288192B;no independentRSSsample or nativechildPIDbirth emitted, all9124selectedcgroupsabsent/noOOM and allrc1. Controls4rc0 have maxwait4RSS6956988KiB/charged715358208B, no childPIDbirth/sampleRSS either; cgroupsabsent/noOOM. Actualcap11.5GiBfailures and11.75GiBcontrols deviate from listedO4share, no retrospective lane/hardRSS qualification. No proof yield, speedup, singlefacet or allfailed-input success claim. Allflags omit-M; P0–7/j8. Rootanalysis{a["root_analysis_seconds"]:.6f}s/{a["root_analysis_maxrss_kib"]}KiB/E22–23; includes selected3-source archive read, no download/census/native rerun. Current Wsource35/7missing andallscenario/paired/grain denominators unchanged. Mv2fullsixprimaryhardwarepoints andprofileoffcontrols have complete subsetterminals, but remaining observer/placement/det24/naturalprofile sequence is active; root did not audit or fit its full finalmatrix inthisstep. NewRamsey sourceprefix is not whole-librarysuccess.\\n')
p=r/'docs/novelty-20261101.md';p.write_text(p.read_text()+'\n\n## 2026-11-03 — separate producer diagnostics from proof rejection\n\n'+entry+'\nNo new novelty claim or literature search. Runtime availability diagnostics and finite source controls bound the acceptance interpretation; a bad producer environment is not a newly discovered mathematical soundness or corpus verified gap. A/B/C mechanism claims stay downgraded, generalbudget/globalphaseweights/software/axiom/cluster/nativebaseline/Envelopepair gaps remain.\n')
report=f"""# Root step0271 — producer diagnostic census and finite qualification
**自审; not independent audit or venue acceptance.** Existing BUILD_AND_EVALUATE; title/fullabstract/fourRQ/sections/fourdesignimplications preserved.

## EXPERIMENT_GATE
Entry: current direct user words and canonical0270, O d7d0ae7classification/ramseyqualification and rawcompletev2fourcontrols read. No new native experiment/agent/session/queue. CurrentWsource35nativecoverage unchanged. M sixprimaryhardwarepoints/profileoffcontrols returned but restoforiginal observer/placement/det24/naturalprofileplannedsequence remainsactive; no rootfit or cause claim from incompleteoverallsequence.
Independently read all9124sourceproduction rc1cells/results/commands/stdout/stderr. Exactfivecategorycounts4697/4421/4/1/1matchO v2CSV/JSON. All P0–7/j8/noM/measured/600s/12348030976Bcharged; cgroupsabsent/noOOM, failure costs9235.245726CPU/9379.187498wall separate from successfulclosure costs. HWM6239176KiB/charged353288192B; no independentRSSsample/nativechildPIDbirth emitted, so no identity/wholelane/hardRSS invention. Counts are invocations, not9124qualified proof rejections.
First read-only reduction incorrectly assumed all unavailable-declaration errors were atline1. It failed after reading all9124logs; 139of9118do notmatchline1. Originalcode/receipt preserved, correctedreducer reports exceptioncount andpaperdoesnotassert uniformfailurephase. Diagnostics identify unavailable runtime declarations, not per-source proof falsity or isolated import phase.

Qualifiedproducer-v2complete4calls:3pinnedComparatorChallenges sourcefiles+oneInit iterator import/rflcontrol.4rc0/no-sorry, P0–7/j8/noM/300s/12616466432Bcharged/3facets. All outputfacets exist; allcgroupsabsent/noOOM; no nativechildPIDbirth or independentRSSsamples inactualrecords. Maxwait4RSS6956988KiB/charged715358208B distinct; exceedsO4share, notretroactivelyauthorized. Earliermetadata-onlyretry qualified-producer-0rc1 retained as incompletev1, not pooledinto a successratio.
Source availability recheck found oldwhole-library duplicate source copies absent, not mismatched. Originalfailedassumption/script preserved. Current3controls11197B match retained fixed4eaee875fullsourcearchive byselectedbytecompare; no newdownload/fulllexicalcensus or restoration of oldsource namespace. Historicalper-invocationbytescannot nowbedirectlyrechecked; oldinput provenance reliesonfrozen sourceconstruction/commands/pin/archive. Current .ir.sig/library path construction is in frozenqualifier/preparecode; commands omit env/per-open trace, so no fabricated openfileaudit.
Controls differ fromoldcapture inroot/outputfacets/timecap/chargedcap aswellasproducerlayout. They boundtestedexamples, do not isolateone runtimefacet or proveall9124willpass. TwoIR/codegencases requirequalifiedretries. Initialv1metadata-onlyretryfailed remains. SyntheticInitcontrol is not a corpus candidate or addedsourceaccept. Fourcontrols not counted as Ramsey nativechecking throughput or globalcost.
Historicalall-state13232unique=2488OAI source+10744deps/163097sourceframe remains incomplete. NewRamsey source work is another closure capture, notsilentrepair of oldprefix. Rootdoesnotresume oldallqueue or changelimits.

## WRITE_GATE
Actual RQ2partialwhole-sourceparagraph replaces blanketunattributed wordingwithfivefamilyscope andfinitecontrols. No statement thatallfailures areinitializationerrors or repairedpasses; no singlefacet or timingcomparison. One additionalMeasuredtag foractualcensus, partialcoverage remains. No newtable, all20oldtablebodies/title/fullabstract/fourRQ/sections/fourimplications compared identical. Canonicals/index/novelty/evaluation updatewithinrootownership, foreignimplementation read-only.
Raw9124records/commands/stdout/stderr/5controlattempts/qualifiers/prepare/sourceinputs+Oreports frozen in smalltar; failedrowsgzip and3smallCSV, beforeentry/source/failedread-onlyscripts retained. All nativeobjects/raw remainPVC. Currentcompile/render/linkchecks pending atinitialreport; completedreceipts appended later.

## REVIEW_GATE — root selfreview and routing
Direction unchanged: costs and meaning of formal artifact validation, notnovelmechanism. Accepteddiagnosticfamilies/finitepassingcontrols; rejectedallproofreject/allsourcefixed/onephase/onefacet/unchangedresource comparison/wholelibrarygain. Failednativecosts remain distinct; no missingdataaszero. Rootanalysis{a['root_analysis_seconds']:.6f}s/{a['root_analysis_maxrss_kib']}KiB/E22–23includes selectedarchivecomparison. No nativecollection, Agent, queue, infra/CronJob/network/Tailscale change.
Selfreviewnotindependent. Earlierroot0270source35/newendpoints alreadycomplete; no repeat. ProtectremainingMrealprocess/ownerwaiters andO/Wongoingcaptures; integrateactualcompleteplannedterminals ratherthan titles/preparedcontrols. Existinghotdeliveryroute stillunconfirmed, no newagentorfalse dispatch. Next rootcanqualifyfinalMmatrixwhenoverallsequencecompleted; currentunqualifiedbulkIRcasesnotproofcounterexamples. Allglobalphaseweight/causality/software/axiom/cluster/nativebaseline/Envelopepair gaps remain.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0271 — producer diagnostic census and finite qualification','# Root step0271 outer audit — 自审')+'\n## Audit disposition\nRead-only source/phase assumptions were explicitly corrected before paper propagation; no failed invocation was replaced or rerun. Complete9124log classification and4finitecontrols support a narrower statement than blanket environment causality. Remainingbyte/env/identity/resource boundaries remain explicit. No independentreview or venueacceptance claimed.\n')
print('EDIT271',s,'TABLES',t.count(r'\begin{tabular}'))
