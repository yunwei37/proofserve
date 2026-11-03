from pathlib import Path
import json,subprocess
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-reboot-method-root-step.txt').read_text().strip());e=s/'experiment-001';sid=s.name.removeprefix('step-')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
p=r/'docs/paper/main.tex';t=p.read_text();needle='Raw, failed and partial captures remain retained on the PVC.'
assert t.count(needle)==1
addition='''
Runs interrupted by a host reboot are recorded as host-reboot interruptions.
They contribute neither cost values nor censored observations, and do not
count as completed samples. Completed records undergo an integrity check
before reuse or continuation; interrupted raw records are preserved.
'''
p.write_text(t.replace(needle,needle+'\n'+addition))
note=f'''## Post-reboot policy and pending wall decomposition — root0282

[Root report](tmp/build-and-evaluate/{s.name}/step-report.md).
The user reports phobos-vt lost around14:38UTC, rebooted14:48, Ready14:50.
Current6qph8 is onphobos-vt/privileged. The cause remains unknown.
Host-reboot interrupted runs are excluded from all cost values, censored
observations and completed samples; retain raw. Completed root0281 files
match the pushed commit and recent0279/0280/0281raw archives read fully
through gzipEOF. No completed work rerun or owner queue resumed.
The nine pre-existing modified tracked paths are five October historical
documents and four M implementation files; current paper/root records had
no pending edits. Preserve all nine without staging/stash/overwrite.

**Pending paper integration; Partial evidence:** the existing M eight-worker
wall decomposition is approximately299s: serial fallback115s,
dependency/context audit31s, planning11s, parallel waves123s,
unattributed18s. These rounded components total298s; the figures are approximate,
not an exact accounting identity or pure kernel CPU decomposition.
There is no corrected-version remeasurement yet. Do not describe it as
a corrected measured partition, infer an intrinsic serial fraction, or fill
a corrected speedup. Qualify capture/version/window definitions before adding
numbers to the paper; label Partial if written. Current paper change is the
interruption methodology, with old20table bodies and frozen narrative retained.

A subsequent outage means preserve the scene and wait for the user;
do not change scheduling or perform recovery. No infrastructure mutation,
owner interruption, agent/session/queue or new native collection.
'''
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;z=p.read_text().replace('root0281.','root0282.',1)
 # Current direct post-reboot decision takes precedence over old PID snapshots.
 marker='## Scientific contract' if 'status' in n else '## Fixed questions'
 idx=z.index(marker);z=z[:idx]+note+'\n'+z[idx:];p.write_text(z)
for n in ['docs/evaluation.md','docs/novelty-20261101.md']:
 p=r/n;p.write_text(p.read_text()+'\n\n'+note+'\n')
p=r/'research/README.md';p.write_text(p.read_text()+'\n\nPost-reboot handling and pending M wall breakdown: [root0282](../docs/tmp/build-and-evaluate/'+s.name+'/step-report.md). Interrupted runs enter no cost/censor/completed-sample totals. Existing299s approximate partition awaits corrected remeasurement/integration, Partial only.\n')
# Preserve the existing M preparation code as evidence of a plan, not an executed matrix.
q=r/'research/parallel-stream-check/wall-ceiling/matrix.py'
if q.exists():
 import gzip
 (e/'M-wall-ceiling-prepared-matrix.py.gz').write_bytes(gzip.compress(q.read_bytes()))
j=json.loads((e/'integrity-recheck.json').read_text())
text=f'''# Root step0282 — reboot integrity and cost-exclusion methodology (self-review)

## Entry
Direct user recovery message read and appended verbatim to user-instruction.
Fixed characterization/fourRQs/main/no-M remain. New direct decision supersedes
standing automatic recovery for any further outage: preserve scene, no scheduling
or recovery action, wait for user. Existing Cloudflare-J CLI path only.
Current pod6qph8 actualRunning/phobos-vt/privileged; boot_id{j['boot_id']}.
User supplied14:38loss/14:48reboot/14:50Ready; cause unknown, not independently diagnosed.

## EXPERIMENT_GATE — integrity, no new native experiment
[Integrity recheck](experiment-001/integrity-recheck.json):36current root0281
paper/canonical/report/evidence files exactly equal pushedac032095 bytes.
Recent0279/0280/0281raw tars:271/88/62members,322547403/126607018/47994391payload
bytes fully read; gzip EOF/CRC verified. All root0281othergzip files read
throughEOF. This is retained-record integrity, not another native qualification,
new performance observation, or audit of every historical capture.
No completed native work rerun. Analysis{j['root_analysis_seconds']:.6f}s/
{j['root_analysis_maxrss_kib']}KiB/E22–23; no new native/agent/session/queue.

[Tracked dirty receipt](experiment-001/entry-tracked-dirty.txt) has9paths.
Five historical documents haveOctober11–14mtime, four implementation files
belong toM. Current paper and current root canonical paths were clean.
They are not this step's unpublished work; preserve exact foreign/pre-existing
dirty bytes without stage/stash/reset/overwrite. a.out and untracked historical
artifacts also preserved. No attempt to make arbitrary old progress prose current.

Postboot read [process/lock receipt](experiment-001/postboot-process-lock-read.json):
only this query's python3 among selected native comms, no matchingPcorelock.
OldWmaster/controller PID/birth belong to previous boot and are no longer
health evidence. Wpreparation last wholewindow16terminal14:20:43UTC, not final;
ledger has later completed dependency rows through14:37:58UTC but no new
population-cost result/root qualification. User reports all in-flight processes
killed by reboot. Those interrupted attempts/continuations are platform
interruptions, never native timeout/censor/cost/complete samples. Precise
interrupted child IDs not inferred from an earlier snapshot; owner raw preserved,
no foreign ledger rewritten or owner resumed. ExistingO13169/14721source/kernel0
prefix remains incomplete, not fullcost or zero checking. No native cost is
derived from postboot elapsed time or partial output.

## WRITE_GATE
Methods explicitly record host-reboot interruption exclusion from allcost,
censored observations and completed samples, and completed-record integrity
check before reuse/continuation. Oldfailed/partial/raw retained.
User-supplied existingM wall partition is pending integration/Partial:
~299s=~115fallback+31dependency/context audit+11planning+123parallelwaves+18residual.
Rounded sum298s, not exact identity. No corrected-version remeasurement;
prepared wall-ceiling/matrix.py retained gzip as preparation only, not run evidence.
Do not write corrected scaling gain/purekernel phase/intrinsicserial fraction.
Currentpaper numbers/tables unchanged; only methodology added.
Status/plan/index/evaluation/novelty record pending Partial evidence and new
postboot policy. No new scientific framing/title/abstract/RQ/section changes.

## REVIEW_GATE — self-review
Accept explicit platform exclusion and actual completed-file integrity.
Do not equate archival integrity with independent review, native outcome
reverification, restored old processes, research completion or venue acceptance.
No controller restart/recovery/scheduler/network/server/PVC mutation.
No arbitrary censors or new originalsource endpoints inferred. Source38,
paired31/dynamic13 gaps and all existing RQ denominators remain.
Build/frozen-fields/local links/all-page static self-review follow before
one coherent own-path main commit/push. Nine unrelatedtracked dirty preserved.
'''
(s/'step-report.md').write_text(text)
(s/'outer-audit.md').write_text(text.replace('# Root step0282 — reboot integrity and cost-exclusion methodology (self-review)','# Root step0282 outer audit — self-review',1)+'\n## Outer disposition\nAuthorized methodology correction and pending Partial evidence only. No completed experiment repeat, broad writing/idea/review loop or native collection needed. Compilation/layout verification supplies document validation, not a research result. Currentroot had no unpublished changes to recover; record that finding and commit this new coherent step only.\n')
print('EDIT282',sid)
