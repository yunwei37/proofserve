from pathlib import Path
import os,json,re,gzip,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-heterogeneous-root-step.txt').read_text().strip());e=s/'experiment-001'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
user=(r/'docs/user-instruction.md').read_text();questions=(r/'docs/questions-for-author.md').read_text()
t=(r/'docs/paper/main.tex').read_text()
old='Full eight-worker closure costs and general service throughput remain\nunmeasured. The coordinator and internal-ABI adapter still add trusted\nimplementation code; acceptance-set parity is not a proof of universal\nmalformed-input equivalence.'
new='These pairs do not measure complete eight-worker costs for that version or\ngeneral service throughput. A later-version heterogeneous closure curve is\nreported separately below. The coordinator and internal-ABI adapter still add\ntrusted implementation code; acceptance-set parity is not a proof of universal\nmalformed-input equivalence.'
assert t.count(old)==1;t=t.replace(old,new)
needle=r'\paragraph{Pooled certificates pass a broader native qualification.}'
insert=r'''\paragraph{More heterogeneous workers do not accelerate the full closure.}
\measured{\expref{0266-20261102T083616+0000}{0266}; one fixed-order observation per setting.}
A later frozen driver checks the same complete 4,449-module Barrier closure
from an empty checked environment at 8, 12, 16 and 24 requested workers
(Table~\ref{tab:heterogeneous}).
The allowed CPU masks expand from eight performance cores (8P) to
8P+4E, 8P+8E and 8P+16E, where E denotes efficiency cores.
This changes both worker count and available hardware; it is not
homogeneous strong scaling or a matched comparison with the earlier v14
four-worker result.
All four invocations retain the original kernel and proof terms, accept the
same module set as the retained serial reference, and traverse the same
import graph: 425,463 entries and 3,595 upstream unsafe/partial exclusions.
The added coordinator and internal-ABI adapter remain trusted implementation.

\begin{table}[t]
\centering\small
\begin{tabular}{lrr}
\toprule
Allowed hardware / workers & Wall (s) & Native CPU (s)\\
\midrule
8P / 8 &284.720&668.786\\
8P+4E / 12 &299.807&809.696\\
8P+8E / 16 &310.591&937.934\\
8P+16E / 24 &319.705&1172.473\\
\bottomrule
\end{tabular}
\caption{\measured{\expref{0266-20261102T083616+0000}{0266}} Complete Barrier closure, one fresh process per setting in the
fixed order shown, with retained filesystem caches.
Wall spans launch through \texttt{wait4}, including reads, planning,
checking and native result audit; sampler join and cgroup deletion follow
the clock. CPU is native user plus system time. No per-target observer
is enabled for this curve.}
\label{tab:heterogeneous}
\end{table}

At 24 versus eight workers, wall time increases 12.29\% and native CPU
increases 75.31\%.
Each setting routes 1,231 complex/cyclic modules through the upstream
fallback and 3,218 through parallel replay.
At 8P, fallback windows take 99.819 seconds and time outside recorded
kernel-work windows takes 46.726 seconds, together 51.47\% of process wall.
The parallel-route windows also increase, from 138.175 to 161.525 seconds.
These are disjoint elapsed windows, not a causal CPU profile; a fallback
module can contain ordinary work, so its entire cost is not proved
inherently serial.
Workers may migrate within their allowed masks. Live snapshots show
E-core placements in the 12- and 16-worker cells; the 24-worker mask is
recorded at launch without a live thread snapshot.
External E-core load, frequency, P/E-specific CPU shares and order effects
are not independently controlled.
The four processes and their cgroups retire without a sampled resource stop
or OOM, under separate 14\,GiB charged-memory and sampled-RSS protections
and without \texttt{-M}.
This observed negative result bounds this heterogeneous extension:
the earlier P-core gains do not imply continued complete-closure speedup
when adding E cores.
It neither isolates contention or scheduling as the cause nor establishes
a hardware-independent scaling limit, repeated uncertainty or cluster behavior.
The separate resident-leaf determinism experiment is not a result of this curve.

'''
assert t.count(needle)==1;t=t.replace(needle,insert+needle)
(r/'docs/paper/main.tex').write_text(t)
rel=str(s.relative_to(r));drel=rel.removeprefix('docs/')
link='['+'0266'+']('+drel+'/step-report.md)'
for n in ['docs/research-status.md','docs/research-plan.md','research/README.md']:
 p=r/n;x=p.read_text().replace('root0265','root0266')
 # Remove duplicate exact paper-summary lines; keep one only until final verification.
 lines=x.splitlines();seen=set();z=[]
 for line in lines:
  if line.startswith('Paper root0266:'):
   if line in seen:continue
   seen.add(line)
  z.append(line)
 x='\n'.join(z)+'\n'
 if n=='docs/research-status.md':
  row=f'| Heterogeneous full closure |Barrier4449modules,8P/8P+4E/8P+8E/8P+16E:284.720/299.807/310.591/319.705s;24versus8 wall+12.29%,nativeCPU+75.31%. One fixed-order capture/settings,not homogeneous scaling or a cross-version speed ratio. | {link} |\n'
  x=x.replace('## Terminal failures and trust that remain visible',row+'\n## Terminal failures and trust that remain visible')
 elif n=='docs/research-plan.md':
  x+=f'\nNew RQ3 boundary {link}: four complete later-version Barrier curves8/12/16/24workers add E cores and get slower. Do not repeat completed curves or call this homogeneous strong scaling. Resident-leaf determinism remains a separate actual owner capture; no result imputed. Whole-library O and Wremaining original draws are ongoing owner paths, not new root queues.\n'
 else:
  row=f'- [Heterogeneous Barrier closure](parallel-stream-check/extended-results/heterogeneous-scaling.md):4,449modules at8/12/16/24workers,284.720→319.705s and668.786→1172.473nativeCPU-s.8P→8P+16E is12.29%slower/75.31%more CPU in one ordered capture; neither homogeneous scaling nor a cluster result. [Root0266](../{rel}/step-report.md).\n'
  x=x.replace('## Existing research directories',row+'\n## Existing research directories')
 p.write_text(x)
p=r/'docs/novelty-20261101.md'
p.write_text(p.read_text()+f'\n## Root0266 — heterogeneous expansion is a measured limit\n{link}. Same4449-module Barrier closure in frozenv16,8/12/16/24workers with\n8P/8P+4E/8P+8E/8P+16E allowed masks:284.720/299.807/310.591/319.705s.\n24vs8 wall+12.29%,wait4nativeCPU+75.31%; graph and retained serial accept set\nmatch at all four settings. One fixed-order capture, no P/E-specific CPU or\nexternal-load/frequency control; no isolated contention/scheduling explanation.\nNo homogeneous scaling/cluster/general limit or cross-version v14ratio.\nAdded coordinator/Cadapter trust and native module-task baseline gap remain.\nThis bounds the existing RQ3 case, not a new parallel-checking mechanism.\n')
report=f'''# Root0266 — complete heterogeneous Barrier extension (自审)

2026-11-02 UTC. BUILD_AND_EVALUATE; parent root0265/678b82a.
This step independently integrates owner M4798b3e, not a new native run.
Exactly two root Markdown reports; both are self-review, not independent review
or venue acceptance. User instruction log/questions and canonical status/plan/index/
novelty read; no new user words or scientific-contract change.

## EXPERIMENT_GATE — intake and independent qualification
RQ3 asks which original-kernel parallelism survives complete cost/trust boundaries.
The completed full-closure negative can change the scaling interpretation.
New experiment/design/agent loops skip: owner already completed the declared four
cells, and root is prohibited from starting another agent or native queue.
Owner [plan](../../../../research/parallel-stream-check/extended-plan.md),
[result](../../../../research/parallel-stream-check/extended-results/heterogeneous-scaling.md),
[step](../../../../research/parallel-stream-check/step017.md) and self-audit are
primary handoff; root reads raw command/stdout/stderr/memory/source/terminal.

The complete frozenv16 matrix has4rc0 native cells, workers8/12/16/24 in fixed
order, each fresh checked environment with retained filesystem caches.
All4449unique headers/accepts, exact per-module imports/counts, complete events,
root reachability and retained serial-reference membership are independently
reconstructed.425463entries/3595unsafe-partial exclusions/0contextfallback.
Wall284.719637447/299.807094451/310.591231680/319.704814081s;
wait4CPU668.786065/809.695921/937.934061/1172.473277s.
24vs8 increaseswall12.287588%/CPU75.313652%.
Nativewall sum1214.822778s and controller1214.984666s include all4settings,
not one configuration gain. Separate cgroup CPU differs <.001s per cell.
Raw [curve](experiment-001/curve.csv), [path windows](experiment-001/paths.csv),
[recompute source](experiment-001/recompute.py) and
[complete raw/source archive](experiment-001/raw-source-and-owner-reports.tar.gz).
All9actually recorded PID/birth identities (controller plus sampled native
parents/children) are retired; all4cgroups absent. No recorded sampled stop/OOM.
Wait4HWM3834044KiB, independent tree sample3914645504B, charged1662562304B
maxima are separate measures. Neither sampledRSS nor cgroupcharge is a hard RSS cap.

Allowed masks0–7/0–11/0–15/0–23 change heterogeneous capacity. Native snapshots
show E placements at12/16, but no live24worker snapshot; launch mask only.
No causal P/E-frequency/load/contention separation or homogeneous scaling claim.
The owner calls this a new user-requested extension; root records the observed
resource point, which differs from the standing eight-core-per-line summary,
without changing runtime limits or retroactively authorizing a larger footprint.
Original kernel/proofs remain; coordinator/internalABI visibility/metadata trust
is additional, and finite accept parity does not prove general context safety.

W080 returns no new original endpoint; source32/42,paired31/42 anddynamic13missing
remain. Cost-concentration offline output is not merged as a population tail claim.
O whole-library has only5000acceptedIDs=3source+4997dependencies at read, not a
complete163097-source result or validation of Wscenario ranges.
Its continuation400547/birth765801115 retired after GitHubDNS publication failure.
Read-only fetch later succeeds; ownercdf1504 independently fixes publication and
qualifies the prior5000checks. Root does not edit O source or start a replacement.
Healthy W399234/birth765754231 remains protected; current work progressed.
No frozen native source is hot-edited by root.

Two early root read-only lookups incorrectly assumed RQ3 was a subsection/label;
ValueError substring-not-found receipts are retained here and in tool history.
Correct entry is the existing RQ3 paragraph; no native/PDF rerun resulted.

## WRITE_GATE — targeted RQ3 update
Re-read user words and fixed four RQs; preserve title/abstract/RQ descriptions/
section hierarchy/four implication bodies and all18existing table bodies.
Add one four-row heterogeneous complete-cost table and local negative interpretation.
Qualify the earlier 'eight-worker missing' sentence as version-specific so it does
not contradict the new finite curve. No cross-version ratio or broad mechanism claim.
Status/plan/index and novelty/evaluation receive compact current links.
No full writing refinement or idea loop: frozen story and evaluation meaning unchanged.
Compile/render/all-page review follow; prior PDF/log/source/failures stay.

## REVIEW_GATE — 自审 and meta-review
Fresh independent review is skipped under the user's no-new-agent instruction;
this is a same-root static evidence audit and must not be called independent.
Direction: two-cost characterization and four RQs remain; the result narrows only
the observed extension of original-kernel parallelism.
Efficiency: no native rerun, no duplicate control, no new helper/schedule/entity.
Maintenance: remove duplicated identical canonical paper-summary lines while
archiving entry text; root-owned new renderings only may be removed after review.
Open objections ranked:1matched native module-task baseline;2complete single-config
Envelope parity/pairs;3repeats/general failure/budget/object and cluster behavior;
4source/paired/dynamic/global/software/axiom gaps. None invalidates this finite curve.
Resident-leaf determinism remains the existing owner's separate pending capture.
Route: finish local paper verification and one main commit/push; integrate only
new actual qualified owner results afterward, with no root queue/agent creation.
'''
(s/'step-report.md').write_text(report)
(s/'outer-audit.md').write_text(f'''# Root0266 outer audit — 自审
Same-root audit, not independent review or venue acceptance.
Covered EXPERIMENT intake, targeted WRITE and REVIEW/meta-routing.
User-selected title/four RQs and two-cost mainline retained; no idea skill invoked.
Original kernel unchanged does not mean implementation TCB unchanged.
Four original full-closure processes, equal graph/accept set, fresh checking env,
fixed order and warm filesystem caches qualify a finite negative extension.
Heterogeneous masks and absent24worker live snapshot prevent homogeneous/causal
worker-count interpretation. Actual9PIDbirth and4cgroups retired; clocks/memory
labels and noM checked against source, not just owner summaries.
Raw/code/commands/stdout/stderr/memory/terminal archived; analysis reproducible.
One new four-row table,18old bodies/title/abstract/RQ/sections/four implications
must remain byte-identical. Native taskbaseline/cluster/single-config Envelope
remain missing; separate leaf experiment not filled by short qualification controls.
O GitDNS fault is real; fetch recovers and ownercdf1504 fixes own publication.
Root neither changes foreign source nor launches a replacement. Wholelibraryprefix
is not global cost/coverage; Wdependencyprogress does not alter32originaldraws.
Owner's expanded footprint is observed/disclosed, not new root authorization.
Fresh reviewer cannot be created under user boundary; this report is explicitly自审.
No unrequested infrastructure, cap, scheduler, testing or new scientific entities.
Compile/all-page visual review/preservation checks and publication remain required.
''')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+f'\n## Root0266 — heterogeneous full-closure negative\n[{s.name}]({drel}/step-report.md), [outer self-audit]({drel}/outer-audit.md).\nM4798b3e complete4cell/4449module v16 curve independently reconstructed;\n24vs8 allowed8P+16Evs8P wall+12.2876%/CPU+75.3137%,oneorderedcapture.\n9PIDbirth/4cgroups retired,raw frozen,0newrootnative/agent. Distinct masks,\nnot equal-core scaling or cross-version ratio; source32/paired31/grainmissing13\nand all global/cluster/axiom gaps unchanged. OpublicationDNS failed then owner\ncdf1504 repairs existing path; rootdoesnotrestart. New paper table/localRQ3 only.\n')
print('EDITED',s)
