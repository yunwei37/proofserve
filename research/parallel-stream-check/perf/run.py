# One finite native cell; copy beside the frozen helpers on PVC before use.
import os,json,sys,time
from pathlib import Path
from native import ROOT,run
from attribution import runtime,MODULE
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2')
EVENTS=['cpu-cycles','instructions','ref-cycles','mem_load_retired.l3_miss',
 'mem_inst_retired.lock_loads','mem_load_l3_hit_retired.xsnp_hitm','ocr.demand_rfo.l3_hit.snoop_hitm']
def selectors(record=False):
 return ['cpu_core/'+name+(',period=0/u' if record and i else '/u') for i,name in enumerate(EVENTS)]
def main():
 assert ROOT==Path(__file__).resolve().parent
 assert str(ROOT).startswith('/workspaces/.agent-state/gpu-smt-captures/')
 arm=sys.argv[1];n=int(sys.argv[2]);rep=sys.argv[3];control='--control' in sys.argv[4:]
 assert arm in ['plain','stat','record'] and n in [1,2,4,8]
 key=('control-' if control else 'full-')+arm+'-P'+str(n)+'-'+rep
 point=ROOT/'runs'/key;assert not point.exists(),'inspect existing cell; never overwrite'
 os.sched_setaffinity(0,set(range(8)))
 env=runtime(n,list(range(8)),list(range(n)),0,True)
 env['LC_ALL']='C';env['DEBUGINFOD_URLS']=''
 mod='ComputeControl' if control else MODULE
 app_time=ROOT/(key+'-application.time')
 app=['/usr/bin/time','-o',str(app_time),'-f','%e,%U,%S,%M,%x',str(BASE/'parallel-stream'),'parallel','none',mod]
 if arm=='plain':argv=app
 elif arm=='stat':
  argv=['perf','stat','--json-output','-o',str(ROOT/(key+'-stat.json'))]
  for ev in selectors():argv+=['-e',ev]
  argv+=['--']+app
 else:
  argv=['perf','record','--no-buildid-cache','--compression-level=1','-s','--running-time',
   '--call-graph','dwarf,16384','-F','99','-o',str(ROOT/(key+'.perf.data'))]
  # No :S groups and no --per-thread: those can disable inheritance. Only the
  # cycles event samples; period=0 followers still provide exit-time -s counts.
  for ev in selectors(True):argv+=['-e',ev]
  argv+=['--']+app
 state='partial';error=None;c=None
 try:
  c=run(key,argv,180 if control else 1100,True,env)
  ev=[json.loads(s) for s in (point/'stdout').read_text().splitlines() if s.startswith('{')]
  ids=[x['module'] for x in ev if x.get('event')=='accept']
  if control:
   ref=[json.loads(s)['module'] for s in (BASE/'runs/attribution-control/stdout').read_text().splitlines()
    if s.startswith('{') and json.loads(s).get('event')=='accept']
  else:
   ref=json.loads((BASE/'p12-results.json').read_text())[0]['accepted_IDs']
  complete=[x for x in ev if x.get('event')=='complete']
  c.update(accepted_count=len(ids),accepted_set_equal_to_reference=set(ids)==set(ref),complete_events=complete,
   arm=arm,workers=n,repeat=rep,C_observer=True,binary=str(BASE/'parallel-stream'),
   counter_scope='whole command; per-thread READ/call-stack scopes analyzed separately')
  if app_time.exists():
   values=app_time.read_text().strip().splitlines()[-1].split(',')
   if len(values)==5:c['application_time']=dict(zip(['wall_s','user_s','system_s','peak_RSS_KiB','exit'],values))
  profiles=[e for e in ev if e.get('event')=='profile_module']
  c['ordinary_checks']=sum(e['metrics']['checks'] for e in profiles)
  c['ordinary_allocation_units']=sum(e['metrics']['raw_HB'] for e in profiles)
  c['observed_worker_TIDs']=sorted({w['tid'] for e in profiles for w in e['metrics']['workers']})
  if (c['returncode'] or not complete or len(ids)!=len(ref) or set(ids)!=set(ref)
    or not c['native_retired'] or not c['cgroup_retired'] or c['stop_reasons']):
   raise RuntimeError('native cell incomplete or verdict mismatch; preserve all outputs')
  if not control and (c['ordinary_checks']!=237863 or c['ordinary_allocation_units']!=3283925639):
   raise RuntimeError('observed ordinary work differs from frozen complete reference')
  state='complete'
 except BaseException as ex:error=repr(ex);raise
 finally:
  (ROOT/(key+'-terminal.json')).write_text(json.dumps(dict(state=state,error=error,cell=c,
   utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main()
