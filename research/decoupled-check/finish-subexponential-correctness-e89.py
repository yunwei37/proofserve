#!/usr/bin/env python3
"""Existing SubexponentialSAT correctness continuation; no performance sampling."""
from pathlib import Path
import os,json,sys,signal,time,threading,importlib.util,datetime
A=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103')
B=A/'correctness-cpu89-20261104'
F=A.parent/'scale-study/falconer-project-20261101'
def atomic(path,value):
 tmp=path.with_name(path.name+'.write-'+str(os.getpid()))
 tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)
def main():
 assert sorted(os.sched_getaffinity(0))==[8,9]
 resume=sys.argv[1:]==['--resume']
 assert not sys.argv[1:]or resume
 B.mkdir(exist_ok=True);(B/'items').mkdir(exist_ok=True)
 claim=B/'controller.json'
 if claim.exists():
  assert resume,'inspect prior controller before explicit resume'
  old=json.loads(claim.read_text());q=Path('/proc',str(old['pid']),'stat')
  assert not q.exists()or q.read_text().split(') ')[1].split()[19]!=old['birth'],'do not restart an active controller'
 else:assert not resume
 atomic(claim,dict(pid=os.getpid(),birth=Path('/proc/self/stat').read_text().split(') ')[1].split()[19],affinity=[8,9],performance_eligible=False))
 frame=json.loads((A/'frame.json').read_text());expected={v['module']for v in frame}
 legacy=json.loads((A/'state.json').read_text())
 baseline=set(legacy['oracle_ids'])
 assert len(expected)==14721 and len(baseline)==13208
 assert set(legacy['built'])==set(legacy['stream_ids'])==expected
 seed=json.loads((A/'qualification-cpu89-probe-20261104/terminal.json').read_text())
 assert seed['valid']and seed['measured']is False and seed['affinity']==[8,9]
 state_path=B/'state.json'
 state=json.loads(state_path.read_text())if state_path.exists()else dict(phase='references',qualified=[seed['module']],controls=[],correctness_only=True)
 done=set(state['qualified'])
 if state['phase']=='complete':
  print((B/'terminal.json').read_text());return
 assert done<=expected and not done&baseline
 spec=importlib.util.spec_from_file_location('original_native',F/'native_project.py')
 n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=B
 stop=threading.Event();sample=dict(peak_tree_rss=0,peak_scope='current controller invocation, not per module',rss_budget_stop=False)
 def watch():
  while not stop.wait(1):
   active=n.ACTIVE
   if active is None:continue
   cg,pid=active
   try:pids=(cg/'cgroup.procs').read_text().split()
   except OSError:continue
   rss=0
   for pid in pids+[str(os.getpid())]:
    try:rss+=int(Path('/proc',pid,'stat').read_text().split(') ')[1].split()[21])*os.sysconf('SC_PAGE_SIZE')
    except (OSError,IndexError,ValueError):pass
   sample['peak_tree_rss']=max(sample['peak_tree_rss'],rss)
   if rss>12*1024**3:
    sample['rss_budget_stop']=True
    try:(cg/'cgroup.kill').write_text('1')
    except OSError:pass
 thread=threading.Thread(target=watch);thread.start()
 def run(key,module,mode='one',mutation='none',prefix=None):
  assert sorted(os.sched_getaffinity(0))==[8,9]
  env=n.environment();env['LEAN_PATH']=str(A)+':'+str(A/'check-lib')
  for name in ['DECOUPLED_TIMING','DECOUPLED_CHECKPOINT_INPUT','DECOUPLED_CHECKPOINT_OUTPUT','DECOUPLED_CHECKPOINT_MODULE','DECOUPLED_SEGMENT_MODULES','DECOUPLED_MUTATE_MODULE']:
   env.pop(name,None)
  if mutation!='none':env['DECOUPLED_MUTATE_MODULE']=module
  if prefix:env['DECOUPLED_CHECKPOINT_INPUT']=prefix
  binary=A/'checkpoint-audit'if prefix else F.parent/'measurement-v1/audited-stream'
  cell=n.run(key,[binary,mode,mutation,module],120 if mutation!='none'else 1400,False,env=env)
  events=[];errors=[]
  for line in(B/(cell['key']+'.stdout')).read_text(errors='replace').splitlines():
   if not line.startswith('{'):continue
   try:events.append(json.loads(line))
   except json.JSONDecodeError as err:errors.append(repr(err))
  accepted=[e['module']for e in events if e.get('event')=='accept']
  valid=not errors and not sample['rss_budget_stop']
  if mutation=='none':valid=valid and cell['returncode']==0 and accepted==[module]
  else:
   valid=valid and cell['returncode']==1 and module not in accepted and any(e.get('event')=='reject'and e.get('module')==module and 'loose bound variables'in e.get('error','')for e in events)
  item=dict(module=module,mode=mode,mutation=mutation,cell=cell,events=events,parse_errors=errors,valid=bool(valid),correctness_only=True,performance_eligible=False,resource_observation=dict(sample))
  atomic(B/'items'/(cell['key']+'.json'),item)
  assert valid,('native correctness/operational outcome',cell['key'])
  return item
 try:
  atomic(state_path,state)
  for i,row in enumerate(frame):
   module=row['module']
   if module in baseline|done:continue
   run('reference-'+str(i).zfill(5),module)
   done.add(module);state['qualified']=sorted(done);atomic(state_path,state)
  assert baseline|done==expected
  state['phase']='negative-controls';atomic(state_path,state)
  plan=json.loads((B/'negative-control-plan.json').read_text())
  for i,module in enumerate(plan['roots']):
   for mode in ['one','audit']:
    key='negative-'+str(i)+'-'+mode
    if key in state['controls']:continue
    run(key,module,mode,'bvar',plan['certified_predecessor']if mode=='audit'else None)
    state['controls'].append(key);atomic(state_path,state)
  assert len(state['controls'])==6
  state['phase']='complete';atomic(state_path,state)
  result=dict(complete=True,correctness_only=True,performance_eligible=False,affinity=[8,9],legacy_pcore_references=len(baseline),e89_references=len(done),combined_reference_count=len(baseline|done),expected=len(expected),accepted_set_equal=baseline|done==set(legacy['stream_ids'])==expected,malformed_theorem_bodies=3,native_bad_proof_rejections=6,resource_observation=sample,source_stream_performance_unchanged=True,legacy_rss_failure_retained=True,scope='Mixed-CPU correctness parity only; no E CPU/wall figure or final system timing.')
  atomic(B/'terminal.json',result);print(json.dumps(result),flush=True)
 except BaseException as err:
  atomic(B/'failure.json',dict(error=repr(err),phase=state['phase'],completed_e89=len(done),completed_legacy=len(baseline),performance_eligible=False,resource_observation=sample));raise
 finally:stop.set();thread.join()
if __name__=='__main__':main()
