from pathlib import Path
import os,json,re,subprocess,shutil
os.sched_setaffinity(0,{22,23})
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-worker-pmu-root-step.txt').read_text().strip());e=s/'experiment-001';a=json.loads((e/'reanalysis.json').read_text())
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
rel=str(s.relative_to(r));drel=rel.removeprefix('docs/');tag=r'\expref{'+s.name.removeprefix('step-')+r'}{0278}'
p=r/'docs/paper/main.tex';t=p.read_text();old=t
text=r"""\paragraph{Supplemental counts retain the trend on checking threads.}
\measured{TAG; two separate counting-only processes.}
A later 4-worker process and an 8-worker process provide complete inherited
counts for all 5 and 9 historical TIDs that execute observed kernel calls.
Each has all eight expected CPU-shard READ IDs exactly once for each of
seven hardware events. Historical TID counts are not simultaneous
concurrency. Both accept the same 4,449 modules and preserve every module's
check and allocation-count pair.

Summing these checking-thread lifetime counts, 4-to-8-worker instructions
increase 0.037\% and locked loads 0.108\%, while cycles increase 10.60\%,
L3-miss loads 36.46\%, modified-line forwarding 43.01\%, and demand-RFO
snoop-HITM responses 42.11\%. Aggregate IPC falls from 1.834 to 1.659.
The corresponding observer-bracket CPU rises 13.21\%; hardware counts
cover whole thread lifetimes and are not gated to those brackets.
Thus the trend is also present among threads that perform checking,
without establishing an exclusive coherence or reference-counting cause.

The first 4-worker counter attempt has complete READ sets for only one
of five checking TIDs and remains excluded from aggregate comparisons.
The later 4-worker process adds a parent that waits five seconds after
the measured child exits. Both parentage and teardown timing differ, so
complete metadata does not isolate a universal recorder fix.
These supplemental points neither fill the original sampled recordings'
missing counters nor supply an ordinary runtime speedup or confidence
interval. Effective frequency and fixed-order effects remain unresolved.

""".replace('TAG',tag)
anchor=r'\paragraph{Pooled certificates pass a broader native qualification.}';assert t.count(anchor)==1;t=t.replace(anchor,text+anchor)
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
p.write_text(t)
entry=f"""[Root0278]({drel}/step-report.md) independently qualifies three supplemental counting-only attempts, not original16 missing-counter imputation. All3rc0/full4449same graph/425463entries/3595upstream exclusions/0fallback; per-module237863checks/3283925639units equal. Direct perf binary headers/READ records independently parsed and compared to fresh perf report-D plus existing CSV:1019/672/800READs,zero samples. P8r2 has9complete historical checkingTIDs, P4r3drain5has5complete, each7events×8expectedIDs unique. P4r2only1/5complete remains excluded. Valid checking-thread lifetime sums P4→P8:instructions+0.0372775%,cycles+10.5976603%,lockedloads+0.1082902%,L3missloads+36.4636325%,modifiedlineforwarding+43.0077816%,RFOsnoopHITM+42.1119891%,IPC1.833853090→1.658748204;observerCPU474.358940→537.001279s(+13.2056832%). PMUthreadlifetime notbracketgated; historicalTIDs notsimultaneousworkers. No uniqueRC/coherencecause/removablestallshare. P4parent+5.000239286s drain changes ancestry andtailtiming; no universalmetadatafix/ordinaryspeedup/CI. Original16/0273clock scopes unchanged.
Threecgroupsabsent/noOOM/stop,16emittedPIDbirthidentitiesretired;noM/P0–7/sharedlock/1100native/1740outer-afterlock/14GiBcharged+14GiBsampleRSSresponse. HWM3391748KiB/sample3465015296B/charged1196441600B separate, nothardRSS/fullMtreeclaim. Root3.106923s/56352KiB/E22–23/0native/Agent. Source38/42/19cells/4missing, nominal43.99–449.74CPUhdf2.13 and247.5–270.3source/16.8–24.0mixedtransfer assumptions unchanged;paired11/dynamic13/B/RQ2denominators unchanged."""
for f in ['docs/research-status.md','docs/research-plan.md']:
 p=r/f;v=p.read_text().replace('root0277.','root0278.',1)
 v=re.sub(r'Paper root0277:[^\n]+','Paper root0278: supplemental checking-thread PMU qualification; final compile/all-page verification pending.',v)
 if f.endswith('status.md'):
  marker='## Terminal failures and trust that remain visible'
  v=v.replace('\n'+marker,'\n| Supplemental checking-thread PMU |Two valid counting-only points have14historical checkingTIDs/complete7×8READsets. Instructions+0.037%,cycles+10.60%,L3missloads+36.46%,IPC1.834→1.659. Thread-lifetime scope, not pure kernel/uniqueRC cause. FailedP4r2retained. | [0278]('+drel+'/step-report.md) |\n\n'+marker)
 else:
  v=re.sub(r'Current owner snapshot at root0277:[^\n]+','Current owner snapshot at root0278: original16 and supplemental counting-only points complete; root now qualifies14valid historical checkingTIDs and preserves partialP4r2. New persistence intervention has owner correctness controls, not full performance results/root dispatch or new resource authorization. Wsource38 unchanged; Allocated untimed prerequisite windows follow existing master, not a new original cost. O source directories remain prefixes, not complete ratios. Refresh actual terminals before integration.',v)
 v+='\n\n'+entry+'\n';p.write_text(v)
p=r/'research/README.md';v=p.read_text().replace('root0277.','root0278.',1);v=v.replace('## Latest complete results\n','## Latest complete results\n\n- [Supplemental checking-thread PMU qualification](../'+rel+'/step-report.md):14historical checkingTIDs have complete seven-event/eight-shard READs; instructions+0.037%,cycles+10.60%,L3missloads+36.46%. PMUthreadlifetime differs from observer CPU; failedP4r2retained, no uniqueRCcause. [Owner supplement](parallel-stream-check/perf/supplemental-worker-report.md).\n',1);p.write_text(v)
for f in ['docs/novelty-20261101.md','docs/evaluation.md']:
 p=r/f;p.write_text(p.read_text()+'\n\n## 2026-11-03 — root0278 supplemental checking-thread counters\n\n'+entry+'\nThe new qualification narrows scope from whole command to observed checking-TID lifetime. It does not promote a generic mechanism, isolate a removable RC fraction, or qualify the new persistence ablation performance. All global/replication/software/axiom/cluster/native-baseline/Envelope-pair gaps remain.\n')
report=f"""# Root step0278 — supplemental checking-thread PMU qualification
**自审; not independent review, research completion or venue acceptance.**

## EXPERIMENT_GATE
Existing BUILD_AND_EVALUATE: collect three already completed owner supplemental native points and independently decode retained data. No new native experiment/Agent/session/queue/old-series restart. Entry rereads latest direct decisions/canonical0277/both root reports and actual supplemental raw/terminal. Existing RQ3 scope only; no idea change/full writing/milestone review invoked.

### Node E1 — exact native work and resource/lifecycle qualification
Raw /workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103:
full-record-P8-r2-count-only terminal06:42:08UTC; P4-r2-count-only06:53:09; P4-r3-count-only-drain5 07:04:09. All3 actualcommand/result/stdout/stderr/memory/launch/terminal read. Header/accept graph rebuilt independently against original v14 serial accept schema:4449unique modules each,425463entries/3595unsafe-partial exclusions/0contextfallback. Per-modulecheck/allocation vectors exactly equal;237863checks/3283925639units. No extra independent corpus/helpers.
Same fd1e9be binary and original mathematical Kernel.addDeclCore; frozen C/Lean/runners/read_times/read_worker_counts/counter_repair/counter_drain/post_native_drain/native code read. Runtime workers4/8 with allowedP0–7/jobpins, coordinator0/profileon from frozenrunner, no invented per-open or per-invocationenv trace. Trustedcoordinator/CABI/observer remain.
AllnoM(omitM0)/P0–7/sharedblockingpcorelock/1100native/1740outer-afterlock/14GiBcharged+14GiBsampledownRSSresponse. Allrc0/wait4complete/noOOM/noRSSstop/3actualcgroupsabsent;16actualemitted PIDbirth identities retired includingparents/sampledchildren/controllers, no fabricated launcher or checkingTIDbirth. MaximumHWM3391748KiB/sample3465015296B/charged1196441600B distinct, nothardRSS/full16GiBlane-treeproof.
GuardwallP8r2 330.648745s /P4r2 351.719278/P4r3 355.722622;wait4CPU729.442607/660.636024/658.147946s. GNUtimechildwall329.24/350.56/349.94s separate. Nativeguardclockendsafterwait4,beforejoin/cgroupcleanup;queueexcluded. P4r3actualdrain5.000239286s afterchildrc0, parentagealsochanged. RecorderwallnotLeanapplicationwall or speedup.

### Node E2 — independent binary metadata and checking-thread reduction
Read rawperf173032/143120/154696B, directPERFILE2attributes/8IDsper7hardwareevent and READ non-group enabled/running/ID/lost binary fields. No owner parser import. Fresh perf report-D command/results/stdout/stderr frozen; all1019/672/800READrecords match directparser and oldCSV exactly,zeroPERF_RECORD_SAMPLE. Hardwareattrs/configs/read_format=23/userinheritverified; RFOconfig1=0x10003c0002; XSNP_HITM aliasXSNP_FWD semantics preserved. Alllostfields0 doesnotreplacecoveragecheck.
EachactualcheckingTID identified only by profile_module work. P8r2all9 andP4r3all5 have each7events×8expectedheaderIDs exactlyonce. Historicalpool TIDs are not a concurrentthreadsnapshot; fullthreadlifetimecounts include activityoutside observedcalls. P4r2only570957of5hasfullsets;133coverage rows retainmissingIDs, unaffectednativeacceptance andpartialmetadata distinct. No completeaggregate/IPC fabricated for partialTIDs. Enabled/runningperCPUcontexts notnaivelymultiplexscaled.
Complete14per-TIDrawcounters matchownerpublishedCSV integers. Aggregateinstructions/cycles,notmeanofTIDIPC. Independent totalsP4cycles1366503123771/instructions2505965975665/ref1505272364377/L3miss212641848/lock5287278662/forward530642071/RFO351933616;P8cycles1511320483021/instructions2506900137431/ref1701909591554/L3miss290178790/lock5293004268/forward758859454/RFO500139862.
Instructions+0.037277512%,cycles+10.597660315%,lockedloads+0.108290226%,L3missloads+36.463632502%,modifiedlineforwarding+43.007781605%,RFO+42.111989097%,IPC1.833853090→1.658748204(-9.548468542%). ObserverCPU474.358940427→537.001279479s(+13.205683231%); bracketcontainsHB/timingreads,notpureC++cycles. Cycles/ref.907811208→.888014552(-2.180701923%),uncontrolled effectivefrequency.
Finite check-threadlifetime pattern,notexactkernelgatedPMU/uniqueRC/coherencecause/removablestallshare/CI/hardwareconstant. Original16periodsamples/worker missingcounters remainunchanged; these separate supplementalpoints nevernormalizeoriginalsamples. P4drainchangesparent+timing,sodoesnotisolateuniversalfix. No new sample-family/offset RC causal qualification.

## WRITE_GATE
ActuallocalRQ3paragraph reports completeworkercoverage/fixedwork/threadlifetimechanges andfailedP4metadata/boundaries. Old0277wholecommand and0273brackettext preserved.20oldtablebodies/title/fullabstract/fourRQ/sectionhierarchy/fourdesignimplication bodies unchanged, no newtable. Status/plan/index/novelty/evaluation synchronized.
Raw3native+decode+rawperf/source/terminal/frozenprimaryeventsemantics/reference/ownerreports tar3722998B retained;freshreportDgzip/4smallCSV/directreducer/entrygzips retained. NoSDK/ELF/buildtreecopy. Rootanalysis3.106923s/56352KiB/E22–23,0native/Agent. Fullcompile/allpage/linkverification follows actual execution.

## REVIEW_GATE — self-review
Admit narrow evidence that fixed-work cycle/cache-traffic trend persists among checkingTIDs, evenwhenwholecommandcoordinationexcludedasfarasTIDselectionpermits. Rejectequatingthreadlifetimewithpurekernel/RCuniquecause/atomicsstalltime, filling original READs orusinginstrumentedchild/guardclock asordinaryspeedup. FailedP4r2andallpriorfailuresremain.
No sourceoriginaldraw/weight changes:38/42/19completecells/4missing/2063domain;sourceconditional23.311%/elapsed18.595%,43.99–449.74nominalCPUhCI/df2.13 conditionalandfragile;247.5–270.3source/16.8–24.0mixedtransfer assumptions unchanged. Paired11/dynamic13/BcensusandM100/50overlap/RQ2CPUwallunitsseparate.
M persistencecontrolsareownerqualificationnotfullperformanceclaim; actualnewmatrixterminalmustbequalifiedlater,norootqueue. WexistingdriverandOsourceprefixesprotected,Ramseyproductioncancelled/samplecomplete,nooldrestoration. NoUI/network/Tailscale/server/credential/CronJob/schedule/target/resource/foreignimplementationchange. Nohotdeliverytargetconfirmed,nofalsedispatch/consumption. A/Cgenericnoveltydowngraded,Bgeneralbudget/globalweights/causalreplication/software/axioms/cluster/nativebaseline/Envelopepairgapsremain.
"""
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(report.replace('# Root step0278 — supplemental checking-thread PMU qualification','# Root step0278 outer audit — 自审')+'\n## Outer disposition\nChecking-TID PMUs add narrower scope while leaving lifetime/observer/causal and metadata limits explicit. No redundant original16 audit or new native control. The new persistence implementation and its pending full results remain owner work, not root acceptance. Publication only after actual compile/fullpage review.\n')
shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0278-recompute.py',e/'step0278-recompute.py')
print('EDIT278',s,'tex_added_chars',len(t)-len(old))
