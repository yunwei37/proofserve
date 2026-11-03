import sys,json,os,time,subprocess
from pathlib import Path
from native import ROOT,SDK,run
from attribution import runtime,MODULE
def live(a):
 f=Path('/proc',str(a['pid']),'stat')
 if not f.exists():return False
 fields=f.read_text().split(') ',1)[1].split()
 return fields[19]==a['birth']and fields[0]!='Z'
def main():
 launch=json.loads((ROOT/'matrix-launch.json').read_text())
 assert not live(launch),'primary matrix still live: no second collection'
 assert (ROOT/'matrix-terminal.json').exists()
 active=json.loads((ROOT/'matrix-active.json').read_text())
 assert not live(active),'primary child still live'
 kind=sys.argv[1];mode=int(sys.argv[2]);n=int(sys.argv[3])
 assert kind in ['memory','stock-default','stock-fresh','bad-root']
 e=runtime(n,list(range(8)),list(range(n)),0,True)
 e.update(PARALLEL_PERSIST_BASE=str(mode),PARALLEL_PERSIST_DIAGNOSTIC='0')
 if kind=='memory':
  assert n==8 and mode in [0,1]
  import cell
  original=cell.run
  def with_snapshots(key,argv,*args,**kwargs):
   supplied=args[-1]if args else kwargs['env']
   supplied.update(DECOUPLED_MEMORY_PROFILE='1',DECOUPLED_MEMORY_STEP='1')
   (ROOT/(key+'-auxiliary-config.json')).write_text(json.dumps(dict(kind=kind,memory_step=1,
     instrumentation='existing compiled memory checkpoints; exclude from primary timing'),indent=2))
   return original(key,argv,*args,**kwargs)
  cell.run=with_snapshots
  sys.argv=[str(ROOT/'cell.py'),'plain',str(mode),'8','memory-r1']
  cell.main();return
 key='aux-'+kind+'-m'+str(mode)+'-P'+str(n)
 assert not(ROOT/(key+'-terminal.json')).exists()
 tfile=ROOT/(key+'-application.time')
 app=[str(SDK/'bin/leanchecker'),'-v']
 scope='stock module-local leaf, imports trusted; not4449 independent module checks'
 if kind=='stock-fresh':
  app+=['--fresh'];scope='stock replay of one final imported environment into empty base; upstream duplicate policy'
 if kind.startswith('stock'):
  app+=[MODULE]
 else:
  app=[str(ROOT/'parallel-stream'),'parallel','bvar',MODULE]
  e['DECOUPLED_MUTATE_MODULE']=MODULE;e.pop('DECOUPLED_MUTATE_CONSTANT',None)
  scope='invalid first real-root theorem after full independently checked prefix'
 argv=['/usr/bin/time','-o',str(tfile),'-f','%e,%U,%S,%M,%x']+app
 state='partial';err=None;c=None
 try:
  c=run(key,argv,1100,True,e)
  stdout=(ROOT/'runs'/key/'stdout').read_text();stderr=(ROOT/'runs'/key/'stderr').read_text()
  c.update(kind=kind,persistent=bool(mode),configured_threads=n,scope=scope)
  if tfile.exists():
   vals=tfile.read_text().strip().splitlines()[-1].split(',')
   if len(vals)==5:c['application_time']=dict(zip(['wall_s','user_s','system_s','peak_RSS_KiB','exit'],vals))
  if not c['native_retired']or not c['cgroup_retired']or c['stop_reasons']:
   raise RuntimeError('auxiliary resource/native failure; retain all results')
  if kind.startswith('stock'):
   if c['returncode']or 'INTERNAL PANIC'in stderr:raise RuntimeError('stock native did not complete')
   c['verbose_replayed']=[s for s in stdout.splitlines()if s.startswith('replaying ')]
   if not c['verbose_replayed']:raise RuntimeError('stock scope not observed')
   state='stock_scope_completed_no_M_work_equivalence_claim'
  else:
   events=[json.loads(s)for s in stdout.splitlines()if s.startswith('{')]
   rejected=[x for x in events if x.get('event')=='reject'and x.get('module')==MODULE]
   if c['returncode']!=1 or not any('kernel_reject:'in x.get('error','')for x in rejected):
    raise RuntimeError('real corrupted root not rejected by original kernel')
   c['root_rejections']=rejected;c['prefix_accepted']=[x['module']for x in events if x.get('event')=='accept']
   state='expected_real_root_kernel_reject'
 except BaseException as ex:err=repr(ex);raise
 finally:
  (ROOT/(key+'-terminal.json')).write_text(json.dumps(dict(state=state,error=err,cell=c,
   utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main()
