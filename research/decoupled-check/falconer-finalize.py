#!/usr/bin/env python3
"""Exit-driven final reduction, reproducible without the optional queue process."""
import os,json,csv,subprocess,select,argparse
from pathlib import Path
os.sched_setaffinity(0,{8})
R=Path('/workspaces/repository');OWN=R/'research/decoupled-check'
D=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
O=D/'checkpoint-recheck-v2'
def wait_record(file):
 v=json.loads(file.read_text());p=Path('/proc/'+str(v['pid']))
 if not p.exists():return
 if p.joinpath('stat').read_text().split(') ')[1].split()[19]!=str(v['birth']):return
 fd=os.pidfd_open(v['pid'])
 try:
  if not select.select([fd],[],[],43200)[0]:raise RuntimeError('finite queue wait expired; raw data retained')
 finally:os.close(fd)
def aggregate(pattern,expected):
 rows=[];accepted=set();complete=False
 for p in sorted(O.glob(pattern+'-*-terminal.json')):
  v=json.loads(p.read_text());c=v['cell'];valid=c['returncode']==0 and not v['malformed']and(v['checkpoint']or v['complete'])
  rows.append(dict(key=c['key'],returncode=c['returncode'],wall_s=c['wall_s'],
   cpu_s=c['user_s']+c['system_s'],peak_rss_kib=c['peak_rss_kib'],valid=bool(valid)))
  if valid:accepted.update(v['accepted']);complete=bool(v['complete'])
 return dict(complete=complete and len(accepted)==expected,modules=len(accepted),segments=len(rows),
  wall_s=sum(x['wall_s']for x in rows),cpu_s=sum(x['cpu_s']for x in rows),
  peak_rss_gib=max((x['peak_rss_kib']for x in rows),default=0)/1024**2)
def reduce():
 source=sum(float(x['source_compiler_wall_s'])for x in csv.DictReader((OWN/'falconer-source-costs.csv').open()))
 b=D.parent.parent
 mods=set(json.loads((b/'cohort-plan.json').read_text())['cases']['math']['modules'])
 mathbuild=sum(x['wall_s']for x in map(json.loads,(b/'measured.jsonl').read_text().splitlines())if x['operation']=='build'and x['module']in mods and x['returncode']==0)
 falc=aggregate('segment',13205);math=aggregate('math-segment',1330)
 parity=json.loads((D/'bounded-recheck-v1/oracle-progress.json').read_text())if(D/'bounded-recheck-v1/oracle-progress.json').exists()else{}
 rows=[]
 for name,v,denom in [('Falconer',falc,source),('Mathlib',math,mathbuild)]:
  rows.append(dict(cohort=name,**v,source_wall_sum_s=denom,check_over_build=v['wall_s']/denom if v['complete']else''))
 with(OWN/'falconer-final-costs.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
 text='# Falconer complete-closure recovery: final reduction\n\nSelf-review.\n\n'
 text+='Successful source build:13,205 modules,8,128 newly constructed plus5,077 exact same-capture common nodes, **'+str(source)+'s** summed compiler wall. One prior source-overlay fault0.053097s is retained separately. Source construction is complete; no source gap remains.\n\n'
 for row in rows:text+='- '+json.dumps(row,sort_keys=True)+'\n'
 text+='\nOriginal module-local parity status: '+json.dumps(parity,sort_keys=True)+'.\n\n'
 if falc['complete']and math['complete']:
  fr=falc['wall_s']/source;mr=math['wall_s']/mathbuild
  text+=f'**Falconer segmented check/build: {fr*100:.4f}%; matched segmented Mathlib: {mr*100:.4f}%.** Falconer is {"higher"if fr>mr else"lower"} by{abs(fr-mr)*100:.4f}percentage points. These are measured aggregate native process costs including startup, verified-prefix import, snapshot writes and normal exits; no unfinished prefix is extrapolated. The historical unsegmented Mathlib10.5551% used another adapter and is not the causal workload control.\n\n'
 else:text+='No complete matched ratio yet. Partial source or checker prefixes are not finalized costs.\n\n'
 text+='The AI subtree contains2,461 Falconer modules and7,312 source theorem/lemma sites with zero explicit decide+kernel/native_decide/bv_decide. Its source compiler wall sum is6476.297931s, versus15601.472317s for10,744 dependencies. This is not a declaration-level CPU attribution: the full numerator checks dependencies too. Shared original-kernel terms avoid rerunning tactics and repeated per-module frontend imports; wide dependency graphs, context fallbacks, prefix import and serialization still cost work. Source composition and these overheads, rather than AI authorship alone, can change the ratio. We have not causally isolated those factors.\n\n'
 text+='The original full checker timed out at1500.210998s with8942 surviving accepts and a JSON-truncated final line; a reachability-cached full attempt timed out at1500.204755s with9040 accepts. Both remain operational failures, with no complete ratio or demonstrated optimization benefit. Their3000.415754s are diagnostic recovery overhead, excluded from the successful segmented protocol but never hidden. Queue wait, reference qualification and controls are likewise separate from service cost.\n\n'
 text+='A segment exports only already original-kernel-checked constants and pure audit metadata; the next imports that certified delta and checks new terms. All inputs are frozen. This is not a standalone verifier of arbitrary snapshots, a public failure cache, a modified kernel or production implementation. Five native cases across18 fresh processes qualified checkpoint/restore, including bad-proof rejection after restore. Whole-input parity requires the independent original module-local union to cover all13,205 plus segmented native import-graph equality. See falconer-segmented-result.md and falconer-parity-progress.md for those conditions; do not infer equality from a partial status.\n\n'
 text+='Finally, the17-vs14.33 admission comparison is resolved in admission-control-reconciliation.md: both policies use predicted-type upper bounds and FIFO, but serial Grid costs557.350 CPU s while the class-selected parallel method costs744.406. The all-serial control completes17/20, versus13/15/15 for the classified method; both interrupt zero. It shows no incremental CPU-budget benefit from changing checker mode, not a paradox or a native throughput result.\n'
 (OWN/'falconer-final-analysis.md').write_text(text)
 return dict(falconer=falc,mathlib=math,parity=parity)
def publish():
 files=['research/decoupled-check/falconer-final-analysis.md','research/decoupled-check/falconer-final-costs.csv']
 a=subprocess.check_output(['git','show','-s','--format=%an%n%ae','58ab893'],cwd=R,text=True).splitlines()
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=R,text=True).strip()=='main'
 subprocess.run(['git','add','--']+files,cwd=R,check=True)
 if subprocess.run(['git','diff','--cached','--quiet','--']+files,cwd=R).returncode==0:return
 subprocess.run(['git','-c','user.name='+a[0],'-c','user.email='+a[1],'commit','--only','-m','research: close Falconer native check and source-cost comparison','--']+files,cwd=R,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=R,check=True)
 subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R,check=True)
 subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=R,check=True)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--reduce-only',action='store_true');args=parser.parse_args()
 if not args.reduce_only:
  wait_record(O/'queue-submission.json')
  if aggregate('segment',13205)['complete']:
   for i in range(3):
    if aggregate('math-segment',1330)['complete']:break
    cmd=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','taskset','-c','0-7','timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(O/'math-checkpoint-worker.py'),'math-segment']
    with(O/f'math-queue-{i}.log').open('w')as f:
     locks=Path('/proc/locks').read_text();p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
     (O/f'math-queue-{i}-submission.json').write_text(json.dumps(dict(pid=p.pid,args=cmd,locks_before=locks),indent=2));rc=p.wait()
    if rc:break
  wait_record(D/'bounded-recheck-v1/oracle-queue-submission.json')
 print(json.dumps(reduce(),indent=2));publish()
if __name__=='__main__':main()
