#!/usr/bin/env python3
"""Optional finite FIFO queue. Each native kernel-state segment is durable alone."""
import os,json,subprocess,csv
from pathlib import Path
os.sched_setaffinity(0,{8})
R=Path('/workspaces/repository');OWN=R/'research/decoupled-check'
D=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
O=D/'checkpoint-recheck-v2'
def reduce():
 accepted=set();rows=[];last=None;headers={}
 for p in sorted(O.glob('segment-*-terminal.json')):
  v=json.loads(p.read_text());c=v['cell']
  valid=c['returncode']==0 and not v['malformed']and(v['checkpoint']or v['complete'])
  rows.append(dict(key=c['key'],returncode=c['returncode'],valid=bool(valid),
   newly_accepted=len(v['accepted']),wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],
   peak_rss_kib=c['peak_rss_kib'],snapshot=v['snapshot'],previous=v.get('previous_snapshot')))
  if not valid:continue
  assert not (accepted&set(v['accepted'])),'a successful declaration was recharged as new'
  accepted.update(v['accepted']);last=v
  for line in(O/(c['key']+'.stdout')).read_text().splitlines():
   if not line.startswith('{'):continue
   e=json.loads(line)
   if e.get('event')=='module_header':headers[e['module']]=set(e['imports'])
 frame=json.loads((D/'build-frame.json').read_text());wanted={x['module']for x in frame}
 complete=bool(last and last['complete']and accepted==wanted)
 graph_match=complete and set(headers)==wanted and all(headers[x['module']]==set(x['imports'])for x in frame)
 assert accepted<=wanted
 work=sum(x['wall_s']for x in rows)
 source=sum(float(x['source_compiler_wall_s'])for x in csv.DictReader((OWN/'falconer-source-costs.csv').open()))
 status=dict(accepted_modules=len(accepted),expected_modules=len(wanted),complete=complete,
  native_graph_match=graph_match,segments=len(rows),native_wall_sum_s=work,
  ratio_over_source=work/source if complete and graph_match else None,
  pending=len(wanted-accepted),single_uninterrupted_process=False)
 (O/'segmented-progress.json').write_text(json.dumps(status,indent=2))
 if rows:
  with(OWN/'falconer-segmented-costs.csv').open('w',newline='')as f:
   w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
 text='# Falconer segmented original-kernel checking\n\nSelf-review.\n\n'
 text+='\n'.join('- '+k+': '+str(v)for k,v in status.items())+'\n\n'
 text+='Each native process checks at most500 new modules then exports only original-kernel-accepted constants and pure audit metadata. Delta snapshots import only the successful preceding certified snapshot. New processes reload that checked prefix; they do not rerun its proofs. This is one chained validation of frozen artifacts, not a standalone verifier of an untrusted supplied snapshot or a cross-candidate result cache. All startup, snapshot writing/loading and normal exits are charged. A complete ratio here is segmented work, never an uninterrupted single-process number. The failed1500s full-check attempts and separately run module-local differential chunks remain explicit. Native final import-graph equality and all13,205 acceptance events are required for completion; module-local reference equality is a separate condition.\n'
 (OWN/'falconer-segmented-result.md').write_text(text)
 return status
def publish():
 files=['research/decoupled-check/falconer-segmented-result.md']
 if(OWN/'falconer-segmented-costs.csv').exists():files.append('research/decoupled-check/falconer-segmented-costs.csv')
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=R,text=True).strip()=='main'
 subprocess.run(['git','add','--']+files,cwd=R,check=True)
 if subprocess.run(['git','diff','--cached','--quiet','--']+files,cwd=R).returncode==0:return
 a=subprocess.check_output(['git','show','-s','--format=%an%n%ae','58ab893'],cwd=R,text=True).splitlines()
 subprocess.run(['git','-c','user.name='+a[0],'-c','user.email='+a[1],'commit','--only','-m','research: retain completed original-kernel Falconer checkpoint segment','--']+files,cwd=R,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=R,check=True)
 subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R,check=True)
 subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=R,check=True)
def main():
 assert json.loads((O/'checkpoint-controls.json').read_text())['complete']
 for i in range(28):
  s=reduce()
  if s['complete']:publish();return
  args=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','taskset','-c','0-7','timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(O/'falconer-checkpoint.py'),'segment']
  locks=Path('/proc/locks').read_text()
  with(O/('queue-'+str(i).zfill(2)+'.log')).open('w')as f:
   p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   (O/('queue-'+str(i).zfill(2)+'-submission.json')).write_text(json.dumps(dict(pid=p.pid,args=args,locks_before=locks),indent=2));rc=p.wait()
  s=reduce();publish()
  if rc:
   (O/'queue-terminal.json').write_text(json.dumps(dict(status='bounded segment incomplete; state retained',returncode=rc,state=s),indent=2));return
 (O/'queue-terminal.json').write_text(json.dumps(dict(status='finite queue exhausted',state=reduce()),indent=2))
if __name__=='__main__':main()
