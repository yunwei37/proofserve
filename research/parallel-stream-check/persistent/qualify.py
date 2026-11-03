import os,json,time
from pathlib import Path
from native import ROOT,run
from attribution import runtime
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2')
def events(folder):
 return [json.loads(s) for s in (folder/'stdout').read_text().splitlines() if s.startswith('{')]
def work(ev):
 return {e['module']:(e['metrics']['checks'],e['metrics']['raw_HB']) for e in ev if e.get('event')=='profile_module'}
def main():
 reference=events(BASE/'runs/attribution-two-core-control')
 ids={e['module']for e in reference if e.get('event')=='accept'}
 expected_work=work(reference);rows=[];state='partial';error=None
 try:
  e=runtime(1,list(range(8)),[0],0,True);e.update(PARALLEL_PERSIST_BASE='0',PARALLEL_PERSIST_DIAGNOSTIC='1')
  c=run('qual-official-import-probe',[ROOT/'persistence-probe','ComputeControl'],180,True,e);rows.append(c)
  if c['returncode']:raise RuntimeError('import object probe failed')
  observed=events(ROOT/'runs'/c['key'])
  assert len([x for x in observed if x.get('event')=='official_import_snapshot'])==2
  for n in [1,8]:
   for mode in [0,1]:
    e=runtime(n,list(range(8)),list(range(n)),0,True)
    e.update(PARALLEL_PERSIST_BASE=str(mode),PARALLEL_PERSIST_DIAGNOSTIC='1')
    key='qual-m'+str(mode)+'-P'+str(n)+'-valid'
    c=run(key,[ROOT/'parallel-stream','parallel','none','ComputeControl'],180,True,e);rows.append(c)
    ev=events(ROOT/'runs'/key);passed={x['module']for x in ev if x.get('event')=='accept'}
    c.update(reference_IDs_equal=passed==ids,work_equal=work(ev)==expected_work)
    if c['returncode']or passed!=ids or not any(x.get('event')=='complete'for x in ev):raise RuntimeError('positive outcome mismatch')
    if work(ev)!=expected_work:raise RuntimeError('original per-module checks/allocation units changed')
    bad=dict(e,DECOUPLED_MUTATE_MODULE='ComputeControl',DECOUPLED_MUTATE_CONSTANT='c0')
    key='qual-m'+str(mode)+'-P'+str(n)+'-bvar'
    c=run(key,[ROOT/'parallel-stream','parallel','bvar','ComputeControl'],180,True,bad);rows.append(c)
    ev=events(ROOT/'runs'/key)
    if c['returncode']!=1 or not any(x.get('event')=='reject'and'kernel_reject:c0:'in x.get('error','')for x in ev):
     raise RuntimeError('bad proof was not rejected by original kernel')
  for mode in [0,1]:
   for fault,reason in [('stale','stale checked frontier'),('duplicate','base-index cover differs')]:
    e=runtime(8,list(range(8)),list(range(8)),0,True)
    e.update(PARALLEL_PERSIST_BASE=str(mode),PARALLEL_PERSIST_DIAGNOSTIC='0',PARALLEL_FAULT=fault)
    key='qual-m'+str(mode)+'-'+fault
    c=run(key,[ROOT/'parallel-stream','parallel','none','ComputeControl'],180,True,e);rows.append(c)
    text=(ROOT/'runs'/key/'stdout').read_text()+(ROOT/'runs'/key/'stderr').read_text()
    if c['returncode']!=1 or reason not in text:raise RuntimeError('coordination fault not rejected')
  state='qualified'
 except BaseException as ex:error=repr(ex);raise
 finally:
  (ROOT/'qualification-terminal.json').write_text(json.dumps(dict(state=state,error=error,cells=rows,
    utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main()
