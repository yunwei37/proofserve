import os,json,sys,time,collections,importlib.util
from pathlib import Path
from native import ROOT,run
from attribution import runtime,MODULE
PERF=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103')
def events(path):
 return [json.loads(s)for s in path.read_text().splitlines()if s.startswith('{')]
def main():
 arm=sys.argv[1];mode=int(sys.argv[2]);n=int(sys.argv[3]);rep=sys.argv[4]
 assert arm in ['plain','stat']and mode in [0,1]and n in [1,2,4,8]
 assert json.loads((ROOT/'qualification-terminal.json').read_text())['state']=='qualified'
 key='full-'+arm+'-m'+str(mode)+'-P'+str(n)+'-'+rep
 assert not(ROOT/(key+'-terminal.json')).exists()
 e=runtime(n,list(range(8)),list(range(n)),0,True)
 e.update(PARALLEL_PERSIST_BASE=str(mode),PARALLEL_PERSIST_DIAGNOSTIC='0',LC_ALL='C')
 app_time=ROOT/(key+'-application.time')
 app=['/usr/bin/time','-o',str(app_time),'-f','%e,%U,%S,%M,%x',str(ROOT/'parallel-stream'),'parallel','none',MODULE]
 argv=app
 if arm=='stat':
  spec=importlib.util.spec_from_file_location('frozen_event_selectors',PERF/'perf_run.py')
  old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
  argv=['perf','stat','--json-output','-o',str(ROOT/(key+'-stat.json'))]
  for selector in old.selectors(False):argv+=['-e',selector]
  argv+=['--']+app
 state='partial';err=None;c=None
 try:
  c=run(key,argv,1100,True,e)
  es=events(ROOT/'runs'/key/'stdout')
  accepted=[x['module']for x in es if x.get('event')=='accept']
  reference=events(PERF/'runs/full-plain-P8-r1-before/stdout')
  ids=[x['module']for x in reference if x.get('event')=='accept']
  expected={x['module']:(x['metrics']['checks'],x['metrics']['raw_HB'])for x in reference if x.get('event')=='profile_module'}
  profiles=[x for x in es if x.get('event')=='profile_module']
  actual={x['module']:(x['metrics']['checks'],x['metrics']['raw_HB'])for x in profiles}
  mismatches=[dict(module=k,reference=v,actual=actual.get(k))for k,v in expected.items()if actual.get(k)!=v]
  persist=collections.Counter();before=[0]*5;after=[0]*5;ready=[0]*5
  for x in profiles:
   v=x['persistence']
   assert v['enabled']==bool(mode)and not v['diagnostic']
   for k in ['calls','window_wall_ns','window_thread_cpu_ns']:persist[k]+=v[k]
   for dst,k in [(before,'base_before'),(after,'base_after'),(ready,'after_enqueue')]:
    for i in range(5):dst[i]+=v[k][i]
  c.update(arm=arm,persistent=bool(mode),workers=n,repeat=rep,binary=str(ROOT/'parallel-stream'),
   accepted_IDs=accepted,accepted_set_equal_to_reference=set(accepted)==set(ids)and len(accepted)==len(ids),
   checks=sum(x['metrics']['checks']for x in profiles),allocation_units=sum(x['metrics']['raw_HB']for x in profiles),
   kernel_CPU_ns=sum(x['metrics']['kernel_cpu_ns']for x in profiles),
   work_equal_to_frozen_reference=not mismatches,work_mismatches=mismatches,
   persistence=dict(persist,base_before=before,base_after=after,after_enqueue=ready))
  if app_time.exists():
   vals=app_time.read_text().strip().splitlines()[-1].split(',')
   if len(vals)==5:c['application_time']=dict(zip(['wall_s','user_s','system_s','peak_RSS_KiB','exit'],vals))
  if c['returncode']or not c['native_retired']or not c['cgroup_retired']or c['stop_reasons']:
   raise RuntimeError('native/resource failure; preserve partial outcomes')
  if not c['accepted_set_equal_to_reference']or not any(x.get('event')=='complete'for x in es):
   raise RuntimeError('full accepted set mismatch or incomplete')
  if mismatches or c['checks']!=237863 or c['allocation_units']!=3283925639:
   state='complete_verdict_but_work_mismatch'
   raise RuntimeError('allocation/check work differs; no matched-work speedup claim')
  if mode and (after[0]!=persist['calls']or ready[0]!=persist['calls']):
   raise RuntimeError('marked frontier did not remain persistent through enqueue')
  state='complete'
 except BaseException as ex:err=repr(ex);raise
 finally:
  (ROOT/(key+'-terminal.json')).write_text(json.dumps(dict(state=state,error=err,cell=c,
   utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main()
