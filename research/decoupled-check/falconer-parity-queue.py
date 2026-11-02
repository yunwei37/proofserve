#!/usr/bin/env python3
"""Optional finite queue convenience. Each replay chunk is independently resumable."""
import os,json,subprocess,time
from pathlib import Path
os.sched_setaffinity(0,{8})
R=Path('/workspaces/repository')
D=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
O=D/'bounded-recheck-v1'
def summarize():
 frame=json.loads((D/'build-frame.json').read_text());wanted={r['module']for r in frame}
 common=set(json.loads((D/'progress.json').read_text())['reused'])
 old=set(json.loads((D.parent.parent/'progress.json').read_text())['oracle_global'])
 accepted=common&old;chunks=[]
 for p in O.glob('oracle-*-terminal.json'):
  v=json.loads(p.read_text());accepted.update(v['accepted'])
  chunks.append(dict(chunk=p.name,accepted=len(v['accepted']),complete=v['complete'],
   wall_s=v['cell']['wall_s'],returncode=v['cell']['returncode']))
 assert accepted<=wanted
 status=dict(verified=len(accepted),expected=len(wanted),remaining=len(wanted-accepted),
  reused_exact_common=len(common&old),chunks=len(chunks),complete=accepted==wanted)
 (O/'oracle-progress.json').write_text(json.dumps(status,indent=2))
 own=R/'research/decoupled-check'
 text='# Falconer native module-local parity progress\n\nSelf-review.\n\n'
 text+='\n'.join('- '+k+': '+str(v)for k,v in status.items())+'\n\n'
 text+='Only complete native accept events count. Common nodes retain the earlier exact-artifact qualification; new nodes run the frozen original measurement-v1 checker in one mode. Independently saved chunks survive queue exit. No partial prefix finalizes a whole-closure ratio.\n'
 (own/'falconer-parity-progress.md').write_text(text)
 return status
def publish():
 path='research/decoupled-check/falconer-parity-progress.md'
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=R,text=True).strip()=='main'
 subprocess.run(['git','add','--',path],cwd=R,check=True)
 if subprocess.run(['git','diff','--cached','--quiet','--',path],cwd=R).returncode==0:return
 author=subprocess.check_output(['git','show','-s','--format=%an%n%ae','58ab893'],cwd=R,text=True).splitlines()
 subprocess.run(['git','-c','user.name='+author[0],'-c','user.email='+author[1],'commit','--only','-m','research: retain completed Falconer reference replay segment','--',path],cwd=R,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=R,check=True)
 subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R,check=True)
 subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=R,check=True)
def main():
 for number in range(17):
  state=summarize()
  if state['complete']:
   (O/'oracle-complete.json').write_text(json.dumps(state,indent=2));publish();return
  args=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','taskset','-c','0-7',
   'timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(O/'oracle-reference-worker.py'),'oracle']
  locks=Path('/proc/locks').read_text()
  with(O/('oracle-queue-'+str(number).zfill(2)+'.log')).open('w')as f:
   p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   (O/('oracle-queue-'+str(number).zfill(2)+'-submission.json')).write_text(json.dumps(dict(pid=p.pid,args=args,locks_before=locks),indent=2))
   rc=p.wait()
  state=summarize();publish()
  if rc:
   (O/'oracle-queue-terminal.json').write_text(json.dumps(dict(status='bounded chunk incomplete; explicit continuation required',returncode=rc,state=state),indent=2));return
 (O/'oracle-queue-terminal.json').write_text(json.dumps(dict(status='finite queue exhausted',state=summarize()),indent=2))
if __name__=='__main__':main()
