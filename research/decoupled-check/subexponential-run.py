#!/usr/bin/env python3
"""Same-pin source-work DAG and matched original-kernel SubexponentialSAT closure."""
import argparse,csv,graphlib,importlib.util,json,os,select,shutil,subprocess,sys,time
from pathlib import Path
R=Path('/workspaces/repository');OWN=R/'research/decoupled-check'
B=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
F=B/'scale-study/falconer-project-20261101';A=B/'subexponential-20261103'
LOCK='/workspaces/.agent-state/gpu-smt-captures/pcore.lock'
def atomic(p,v):
 t=p.with_suffix('.pending')
 with t.open('w')as f:json.dump(v,f,indent=2);f.flush();os.fsync(f.fileno())
 t.replace(p)
def state():
 return json.loads((A/'state.json').read_text())if(A/'state.json').exists()else dict(
  phase='source',built=[],stream_ids=[],oracle_ids=[],snapshot=None,segments=0,tasks=0)
def append(v):
 with(A/'ledger.jsonl').open('a')as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
def events(key):
 es=[];bad=[]
 for i,line in enumerate((A/(key+'.stdout')).read_text().splitlines()):
  if not line.startswith('{'):continue
  try:es.append(json.loads(line))
  except ValueError:bad.append(i)
 return es,bad
def artifact(root,m,suffix='.olean'):return root.joinpath(*m.split('.')).with_suffix(suffix)
def link_parts(srcbase,destbase):
 destbase.parent.mkdir(parents=True,exist_ok=True)
 for suffix in ['.olean','.olean.server','.olean.private','.ir','.ir.sig']:
  src=srcbase.with_suffix(suffix);dest=destbase.with_suffix(suffix)
  if src.exists():
   if dest.exists():assert os.path.samefile(src,dest)
   else:os.link(src,dest)
def native():
 spec=importlib.util.spec_from_file_location('native',F/'native_project.py')
 n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=A
 return n
def next_action():
 frame=json.loads((A/'frame.json').read_text());s=state()
 if s['phase']in ['complete','failure']:return None
 built=set(s['built'])
 for i,v in enumerate(frame):
  if v['module']not in built:return['build',str(i)]
 if s['phase']=='source':s['phase']='stream';atomic(A/'state.json',s)
 if s['phase']=='stream':return['stream',str(s['segments'])]
 qualified=set(s['oracle_ids'])
 pending=[v['module']for v in frame if v['module']not in qualified]
 if pending:return['oracle']+pending[:16]
 s['phase']='complete';atomic(A/'state.json',s);return None
def worker(args):
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 n=native();s=state();frame=json.loads((A/'frame.json').read_text())
 env=n.environment();s['tasks']+=1
 operation=args[0]
 if operation=='build':
  v=frame[int(args[1])];m=v['module'];out=artifact(A/'check-lib',m);out.parent.mkdir(parents=True,exist_ok=True)
  if out.exists():
   # A prior interrupted worker may have produced files before its cursor
   # advanced. Preserve only this uncommitted node's owned outputs for retry.
   backup=A/'interrupted-artifacts'/(str(int(args[1]))+'-'+str(time.monotonic_ns()))
   for base,label in [(out.with_suffix(''),'checker'),(artifact(A/'producer-ai',m).with_suffix(''),'producer')]:
    for suffix in ['.olean','.olean.server','.olean.private','.ir','.ir.sig','.c','.ilean']:
     part=base.with_suffix(suffix)
     if part.exists():
      dest=backup/label/part.name;dest.parent.mkdir(parents=True,exist_ok=True);part.rename(dest)
  env['LEAN_PATH']=str(A/'producer-ai')+':'+':'.join(json.loads((A/'prepare.json').read_text())['production_providers'])
  flags=json.loads((B/'mathlib-options.json').read_text())['flags']if m.startswith('Mathlib')else['-DautoImplicit=false']if v['target']else[]
  c=n.run('source-'+str(int(args[1])).zfill(5),[n.SDK/'bin/lean','--root='+v['source_root'],'-j8']+flags+['-o',out,'-i',out.with_suffix('.ilean'),'-c',out.with_suffix('.c'),v['source']],1400,True,env=env,cwd=v['source_root'])
  text=(A/(c['key']+'.stdout')).read_text(errors='replace')+(A/(c['key']+'.stderr')).read_text(errors='replace')
  good=c['returncode']==0 and out.exists()
  append(dict(operation='build',module=m,cell=c,valid=good,sorry_warning="declaration uses 'sorry'"in text))
  if good:
   s['built'].append(m)
   # Only new SubexponentialSAT outputs enter the producer overlay. SDK/Mathlib Meta/IR
   # remain those of the distribution, even when their terms were rebuilt.
   if v['target']:link_parts(out.with_suffix(''),artifact(A/'producer-ai',m).with_suffix(''))
  else:s['phase']='failure';s['failure']=dict(operation=operation,module=m,key=c['key'])
 elif operation=='stream':
  chosen=env.copy();chosen['LEAN_PATH']=str(A)+':'+str(A/'check-lib')
  mod='SubexponentialSATCertified'+str(s['segments']).zfill(4)
  base=mod;attempt=0
  while(A/(mod+'.olean')).exists():attempt+=1;mod=base+'Attempt'+str(attempt)
  chosen.update(DECOUPLED_CHECKPOINT_OUTPUT=str(A/(mod+'.olean')),DECOUPLED_CHECKPOINT_MODULE=mod,DECOUPLED_SEGMENT_MODULES='500')
  if s['snapshot']:chosen['DECOUPLED_CHECKPOINT_INPUT']=s['snapshot']
  c=n.run('stream-'+str(s['segments']).zfill(4),[A/'checkpoint-audit','audit','none','@'+str(A/'roots.txt')],1400,True,env=chosen)
  es,bad=events(c['key']);ids=[v['module']for v in es if v.get('event')=='accept']
  cp=next((v for v in reversed(es)if v.get('event')=='checkpoint'),None)
  complete=next((v for v in reversed(es)if v.get('event')=='complete'),None)
  good=c['returncode']==0 and not bad and not any(v.get('event')=='reject'for v in es)and bool(cp or complete)
  append(dict(operation='stream',cell=c,valid=good,accepted=ids,checkpoint=cp,complete=complete,previous=s['snapshot'],snapshot=mod if cp else None))
  s['segments']+=1
  if good:
   assert not set(ids)&set(s['stream_ids'])
   s['stream_ids']+=ids
   if cp:s['snapshot']=mod
   if complete:
    expected={v['module']for v in frame}
    assert set(s['stream_ids'])==expected,'native closure differs from measured source frame'
    s['phase']='oracle'
  else:s['phase']='failure';s['failure']=dict(operation=operation,key=c['key'])
 else:
  env['LEAN_PATH']=str(A/'check-lib')
  c=n.run('oracle-'+str(len(s['oracle_ids'])).zfill(5),[F.parent/'measurement-v1/audited-stream','one','none']+args[1:],1400,True,env=env)
  es,bad=events(c['key']);ids=[v['module']for v in es if v.get('event')=='accept']
  good=c['returncode']==0 and not bad and set(ids)==set(args[1:])
  append(dict(operation='oracle',cell=c,valid=good,accepted=ids,requested=args[1:]))
  if good:s['oracle_ids']=sorted(set(s['oracle_ids'])|set(ids))
  else:s['phase']='failure';s['failure']=dict(operation=operation,key=c['key'])
 atomic(A/'state.json',s)
 return 0 if good else 2
def source_window():
 # Keep each native compiler's 1400s limit and clock unchanged. A new call
 # starts only in the first 200s of a 1740s outer lock window.
 begin=time.monotonic()
 for _ in range(25):
  action=next_action()
  if action is None or action[0]!='build':return 0
  if time.monotonic()-begin>=200:return 0
  if worker(action):return 2
 return 0
def sync_whole(summary):
 p=OWN/'whole-library-progress.md';text=p.read_text();marker='<!-- subexponential-current -->'
 if marker in text:text=text[:text.index(marker)].rstrip()
 text+='\n\n'+marker+'\n## SubexponentialSAT complete-directory attempt\n\n'
 text+=f"Source **{summary['source_targets_built']}/3977**; native stream **{summary['kernel_accepted_targets']}/3977** and **{summary['kernel_accepted_dependencies']}** dependencies; new sourceCPU **{summary['source_new_cpu_s']/3600:.6f}h**, streamCPU **{summary['kernel_cpu_h']:.6f}h**, segment **{summary['current_segment']}**; complete **{summary['complete']}**. [Directory progress](subexponential-progress.md).\n"
 text+='Historical whole-library accepted2488/163097; certified dependencies10744; kernelCPU0.694505h; source errors9124/blocked151485 stay unchanged. Ramsey190/444 production is cancelled. Directory costs are not a global full-library measurement.\n'
 p.write_text(text)
def reduce():
 s=state();frame=json.loads((A/'frame.json').read_text());targets={v['module']for v in frame if v['target']}
 rows=[json.loads(v)for v in(A/'ledger.jsonl').read_text().splitlines()]if(A/'ledger.jsonl').exists()else[]
 builds={v['module']:v['cell']for v in rows if v['operation']=='build'and v['valid']}
 source=[]
 for v in frame:
  if'reused'in v:cost=v['reused'];cpu=cost['source_cpu_s'];wall=cost['source_wall_s'];key=cost['source_key'];capture=cost['source_capture'];reuse=True
  elif v['module']in builds:
   c=builds[v['module']];cpu=c['user_s']+c['system_s'];wall=c['wall_s'];key=c['key'];capture=str(A);reuse=False
  else:continue
  source.append(dict(module=v['module'],target=v['target'],source_cpu_s=cpu,source_wall_s=wall,source_key=key,source_capture=capture,reused_same_artifact=reuse))
 checks=[v for v in rows if v['operation']=='stream'];kernel_cpu=sum(v['cell']['user_s']+v['cell']['system_s']for v in checks)
 complete=s['phase']=='complete'and len(source)==len(frame)and set(s['stream_ids'])=={v['module']for v in frame}and {v['module']for v in frame}<=set(s['oracle_ids'])
 with(OWN/'subexponential-source-costs.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=['module','target','source_cpu_s','source_wall_s','source_key','source_capture','reused_same_artifact'],lineterminator='\n');w.writeheader();w.writerows(source)
 costs=[]
 for v in rows:
  c=v['cell'];costs.append(dict(key=c['key'],operation=v['operation'],returncode=c['returncode'],cpu_s=c['user_s']+c['system_s'],wall_s=c['wall_s'],peak_rss_kib=c['peak_rss_kib'],valid=v['valid']))
 if costs:
  with(OWN/'subexponential-native-costs.csv').open('w',newline='')as f:
   w=csv.DictWriter(f,fieldnames=costs[0],lineterminator='\n');w.writeheader();w.writerows(costs)
 summary=dict(complete=complete,phase=s['phase'],target_modules=3977,closure_modules=len(frame),
 source_built=len(source),reused_source_nodes=sum('reused'in v for v in frame),new_source_nodes_built=len(builds),source_targets_built=len(targets&set(s['built'])),source_cpu_s=sum(v['source_cpu_s']for v in source),source_reused_cpu_s=sum(v['source_cpu_s']for v in source if v['reused_same_artifact']),source_new_cpu_s=sum(v['source_cpu_s']for v in source if not v['reused_same_artifact']),
 kernel_accepted_targets=len(targets&set(s['stream_ids'])),kernel_accepted_dependencies=len(set(s['stream_ids'])-targets),
 kernel_cpu_s=kernel_cpu,kernel_cpu_h=kernel_cpu/3600,current_segment=s['segments'],remaining_segments_min=(len(frame)-len(s['stream_ids'])+499)//500,
 oracle_qualified=len(s['oracle_ids']),kernel_peak_rss_gib=max((v['cell']['peak_rss_kib']for v in checks),default=0)/1024**2)
 summary['kernel_over_source_cpu']=kernel_cpu/summary['source_cpu_s']if complete else None
 atomic(A/'reduced.json',summary)
 sync_whole(summary)
 text='# SubexponentialSAT complete-closure measurement: actual progress\n\nReview: 自审.\n\n'
 text+='**Historical whole-library point:2488 /163097accepted source IDs;10744dependencies;0.694505kernelCPUh;32attempts/31successful;9124producer errors/151485blocked. It is partial and retired, not this SubexponentialSAT denominator.**\n\n'
 text+=f'**SubexponentialSAT phase {s["phase"]}: baseline source coverage {len(source)}/{len(frame)} closure nodes (reused {summary["reused_source_nodes"]}, new {summary["new_source_nodes_built"]}) ({summary["source_targets_built"]}/3977targets); kernel accepts {summary["kernel_accepted_targets"]}/3977targets and {summary["kernel_accepted_dependencies"]}dependencies; kernelCPU {kernel_cpu/3600:.6f}h; current segment {s["segments"]}; at least {summary["remaining_segments_min"]} segments (500 nodes each) remain.**\n\n'
 text+='These are separate experiment costs. No global CPU estimate is formed by adding or rescaling this prefix. Producer uses official SDK/cache Meta/IR; checker consumes exact source-produced terms. Same-capture immutable shared source artifacts and actual compiler costs are charged once per complete closure; newly built targets use -o/-i/-c. This is summed source compiler work, not a fresh parallel Lake wall time. Oracle cost is a separate qualification. All timing uses P0–7/shared flock/no-M,12GiB total allocation. A complete CPU ratio requires full source, stream and original module-local coverage.\n\n'
 text+='\n'.join('- '+k+': '+str(v)for k,v in summary.items())+'\n'
 if s.get('failure'):text+='\nFailure: '+json.dumps(s['failure'])+'\n'
 if complete:text+=f'\n**Complete native check/source CPU ratio: {summary["kernel_over_source_cpu"]:.6f}.** No extrapolated module costs enter either side.\n'
 (OWN/'subexponential-progress.md').write_text(text)
 if complete:(OWN/'subexponential-result.md').write_text(text)
 return summary
def publish():
 files=['research/decoupled-check/'+n for n in ['whole-library-progress.md','subexponential-progress.md','subexponential-source-costs.csv','subexponential-native-costs.csv','subexponential-result.md']if(OWN/n).exists()]
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=R,text=True).strip()=='main'
 subprocess.run(['git','add','--']+files,cwd=R,check=True)
 if subprocess.run(['git','diff','--cached','--quiet','--']+files,cwd=R).returncode!=0:
  s=json.loads((A/'reduced.json').read_text());a=subprocess.check_output(['git','show','-s','--format=%an%n%ae','58ab893'],cwd=R,text=True).splitlines()
  title=f'SubexponentialSAT {s["phase"]}: build {s["source_built"]}/{s["closure_modules"]}; kernel {s["kernel_accepted_targets"]}/3977, {s["kernel_cpu_h"]:.4f} CPUh'
  subprocess.run(['git','-c','user.name='+a[0],'-c','user.email='+a[1],'commit','--only','-m',title,'--']+files,cwd=R,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 for i in range(3):
  try:
   subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=R,check=True)
   subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R,check=True)
   subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=R,check=True);return
  except subprocess.CalledProcessError as e:
   if'merge-base'in e.cmd or i==2:raise
   time.sleep(5*(i+1))
def queue():
 os.sched_setaffinity(0,{8})
 # The source is finite; every successful task advances a source, stream or
 # reference cursor. Stop on a real failure, retaining original evidence.
 while True:
  action=next_action()
  if action is None:reduce();publish();break
  key='task-'+str(time.monotonic_ns())
  if shutil.disk_usage('/workspaces').used/shutil.disk_usage('/workspaces').total>=.85:
   s=state();s['phase']='failure';s['failure']=dict(operation='disk_ceiling',limit=.85);atomic(A/'state.json',s);reduce();publish();break
  suffix=['window']if action[0]=='build'else['worker']+action
  cmd=['flock',LOCK,'taskset','-c','0-7','timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(Path(__file__).resolve())]+suffix
  with(A/(key+'.log')).open('w')as f:
   locks=Path('/proc/locks').read_text();p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   atomic(A/(key+'.submission.json'),dict(pid=p.pid,args=cmd,locks_before=locks));rc=p.wait()
  s=state()
  reduce();publish()
  if rc:break
 atomic(A/'queue-terminal.json',dict(state=state(),reduced=reduce()))
def main():
 p=argparse.ArgumentParser();p.add_argument('op',choices=['worker','window','reduce','queue']);p.add_argument('args',nargs='*');a=p.parse_args()
 if a.op=='worker':raise SystemExit(worker(a.args))
 elif a.op=='window':raise SystemExit(source_window())
 elif a.op=='queue':queue()
 else:os.sched_setaffinity(0,{8});print(json.dumps(reduce(),indent=2))
if __name__=='__main__':main()
