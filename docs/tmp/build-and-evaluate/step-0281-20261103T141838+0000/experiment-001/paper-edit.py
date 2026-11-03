from pathlib import Path
import json,subprocess
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-stock-negative-root-step.txt').read_text().strip());e=s/'experiment-001';sid=s.name.removeprefix('step-')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
t=(r/'docs/paper/main.tex').read_text()
insert=r'''
\paragraph{Official checker controls retain a different verification scope.}
\measured{\expref{SID}{0281}; three installed-SDK controls and two real-root rejection controls.}
With the same eight-P-core mask, the installed Lean 4.34.1 checker takes
65.423 seconds in its default one-root mode.
Its \texttt{--fresh} mode takes 534.698 and 580.090 seconds with one and eight
configured threads, respectively; each run's total CPU/wall ratio is about one.
The matched source imports the dependencies and checks the leaf in default
mode, whereas \texttt{--fresh} replays the final imported constant map into
an empty kernel environment, sequentially.
The slower eight-thread observation is retained, but one observation per setting
does not isolate a thread-count effect.
These controls lack the stream's per-module check/allocation ledger and use
the SDK's duplicate policy. Dividing their clocks by the stream time would
not establish a matched-workload speedup.
The native module-task comparison with an equivalent verification ledger
therefore remains \missing{matched native module-task baseline}.

Two further eight-worker runs corrupt only the first real root theorem's
proof in memory, replacing it by a loose bound variable.
Both persistence settings accept exactly the same ordered 4,448-module prefix
and reject the root with the same original-kernel diagnostic for theorem
\texttt{C41.fourth226}; neither emits a root acceptance or completion event.
The two native exit codes are 1, with no resource stop or OOM.
These finite negative controls extend the earlier small controls to the real
prefix; they do not prove unsafe coordinator/FFI safety for arbitrary inputs.
'''.replace('SID',sid)
anchor=r'\paragraph{Pooled certificates pass a broader native qualification.}'
assert t.count(anchor)==1
(r/'docs/paper/main.tex').write_text(t.replace(anchor,insert+'\n'+anchor))
summary=f'Root0281 independently qualifies [three official checker scopes and two real-root rejects](tmp/build-and-evaluate/{s.name}/step-report.md). Stock default65.423s checks one root with trusted imports; fresh1/8 take534.698/580.090s, approximately1CPU occupancy and sequential replay of final imported map, not equivalent to4449 per-module ledger. No stock speedup/isolated thread effect. Both flags reject the same corrupted real-root theorem after identical4448accepted prefix, native rc1/noOOM or resource stop. Finite correctness controls, not arbitrary unsafe-FFI safety; native matched module-task baseline remains missing. Prior0279/0280 primary, memory and storage conclusions retain their denominators.'
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;z=p.read_text().replace('root0280.','root0281.',1)
 lines=z.splitlines()
 for i,line in enumerate(lines):
  if line.startswith('Root0280 independently completes qualification'):
   lines[i]=summary;break
 p.write_text('\n'.join(lines).rstrip()+'\n')
p=r/'research/README.md';z=p.read_text();z=z.replace('root0280','root0281',1);z+='\n\nOfficial checker/rejection scope [root0281](../docs/tmp/build-and-evaluate/'+s.name+'/step-report.md): three original-SDK procedures are complete but lack matched stream work ledgers; two real corrupted-root controls accept the same4448prefix then original-kernel reject. No cross-scope speedup or universal safety claim.\n';p.write_text(z)
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+'\n\n'+summary+'\n')
analysis=json.loads((e/'reanalysis.json').read_text());snapshot=json.loads((e/'owner-latest-read.json').read_text())
body=f'''# Root step0281 — official checker scope and real-prefix rejection (self-review)

## Entry and disposition
Continue the fixed two-cost characterization and four RQs in BUILD_AND_EVALUATE. Read direct user words, current canonical docs, questions-for-author, root0280 reports and M step066/causal/stock/negative/source reports. No new author question or authorization is introduced. User's persistence correction and historical-unmarked labels stand. One RQ3 decision: can the installed SDK controls supply a matched baseline, and does original-kernel rejection survive the real prefix? They supply scoped procedure costs and finite rejection evidence, not a matched-workload speedup or universal implementation proof.

## EXPERIMENT_GATE
No new experiment is launched: existing M owner completed all five auxiliary controls. No substitute agent/session/queue/budget or foreign edit. Complete raw collection is independently reduced by [root reducer](experiment-001/reducer.py), with [raw/source archive](experiment-001/qualified-auxiliary-raw-source.tar.gz), [resources](experiment-001/five-native-resources.csv), [prefix/errors](experiment-001/negative-prefix-errors.csv), [reanalysis](experiment-001/reanalysis.json).
Actual scope: three SDK native rc0 controls; two intentionally invalid real-root native rc1 controls. All five command/result/stdout/stderr/memory/launch/application-time/controller/terminal records read. Seven frozen core/source/runner files equal root0280 byte for byte. SDK LeanChecker/Replay/Environment installed source frozen; no new SDK/ELF/buildtree copied into Git.

Native no-M (including no-M0), P0–7/shared blocking lock,1100native/1740outer-afterlock and14GiBcharged+14GiBsampled own-tree response from actual command/frozen runner. NoOOM/sample stop; wait4 complete, five cgroups absent; {analysis['retired_actual_PID_births']} actual emitted PID/birth identities independently retired. HWM/sample/charged separately in CSV, not hard RSS or whole-lane audit. Clock excludes lock queue and ends after wait4 before samplerjoin/cgroupdelete. Runtime settings derive from frozen auxiliary/runtime source, not per-open env trace.

Stock default8:65.423053645wall/64.985488CPU-s; fresh1:534.698397249/534.531571; fresh8:580.090347835/579.905846. Each stdout names exactly the one real root, each stderr empty and rc0. Default source loads imports and replays module-local constants. Fresh replays final imported map into emptybase; Replay uses sequential constant loop and SDK duplicate theorem policy. Configured8 is not8-way declaration checking; CPU/wall~1 is occupancy, not actual thread count. Preserve slowerfresh8; one fixed-order observation, not causal thread effect/CI or stock-native full4449ledger parity. Existing native module-task baseline gap remains.

Both bad-root flags reconstruct all4449headers/imports/constants identical to positive reference; exactly same ordered4448accept prefix excludes only root, per-module prefix work equal234438checks/2821724037units. Root mutation applies only first thmInfo proof to Expr.bvar0 and keeps name/type/levels; no disk mutation. Both reject C41.fourth226 with exact same kernel_reject/loose-bvar stderr, no root accept/no complete. Native rc1 is expected original-kernel rejection, controller success not mathematical acceptance. Counts/clocks excluded from32primary/24plain/repeat medians. Finite evidence, not universal unsafequiescence/coordinator/FFI safety/TCBunchanged/axiom closure.

## WRITE_GATE
Actual local RQ3 paragraph adds scope clocks, sequential-source explanation, remaining matched-baseline gap and real-prefix rejection. No new table. Preserve20oldtable bodies/title/fullabstract/fourRQ/section hierarchy/fourdesignimplication bodies and all old numeric denominators. Canonicalstatus/plan/index/novelty/evaluation synchronized. Source38/42/19strata/4missing, paired31/42/14/11missing, dynamic13missing, conditionalCPU23.311065%/elapsed18.594528%, covered nominal fragile43.99–449.74CI, scenarios247.5–270.3/16.8–24.0, RQ2CPU6.31/8.95 and wall9.26/10.56/14.67, B2524/30288/22716 and overlapping100/50 unchanged.

## REVIEW_GATE — root self-review
Admit finite real-prefix rejection and source-scoped SDK observations. Reject cross-scope speedups, native-Lean scaling law, full baseline parity, arbitrary-input/extension safety, universal leak/service claims, or oldgain×newwall correction. No new novelty: known runtime method correction. Existing complete32/memory2/oldqueues stay complete; no resumption. Self-review only, not independent review/research completion/venue acceptance.

## Owner read
[Snapshot](experiment-001/owner-latest-read.json) at {snapshot['UTC']}: Wwindow15 terminal13:52:33UTC/all_original_deps_ready=false/preparation_final=false/no_population_cost_measurements=true, stillAllocatedRecoveredForecastDecay. Master526699/birth772878773 andcontroller561457/birth773951593 samebirth sleeping. No originalsource cost admitted; source38 remains. O{snapshot['latest_O']} is sourceprefix, kernel0 not completechecking zero cost. Mprimary32/memory2 already rootqualified; fiveaux controls now qualified separately. No root hot-delivery/dispatch/restart/stop/allowance change. Prior0279attributed15.172GiB cleanup not repeated or credited to concurrentdfchange; retain all unique raw, tracked, foreignruntime/snapshots/SDK.
'''
(s/'step-report.md').write_text(body)
(s/'outer-audit.md').write_text(body.replace('# Root step0281 — official checker scope and real-prefix rejection (self-review)','# Root step0281 outer audit — self-review',1)+'\n## Outer disposition\nRQ3 gains scoped procedure and finite failure evidence; matched native baseline remains missing. Gate review accepts only those conclusions. Broader review/idea/writing loops skipped because no framing or frozen-contract change is authorized or needed. No new agents/native collection. Compile, frozen-field checks and full-page self-review follow before one main commit/push.\n')
print('EDIT281',sid)
