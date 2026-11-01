"""One bounded, one-process real-module stream curve per lock acquisition."""
import json,os,sys,time
from pathlib import Path
from native import run,ROOT,environment
def main():
 module=sys.argv[1];repeat=int(sys.argv[2])
 assets=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets')
 frame=json.loads((assets/'assets.json').read_text())
 matches=[r['module']for r in frame['selected']if r['module'].endswith('.'+{'barrier':'BarrierData41','envelope':'EnvelopePsiB','grid':'Grid'}[module])]
 assert len(matches)==1
 root=matches[0]
 e=environment()
 prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 e.update(LEAN_PATH=str(assets/'overlay-complete-v2')+':'+prep['lean_path'],PARALLEL_WORKERS='4',
  PARALLEL_CURVE_MODULES=root)
 if module=='envelope':e['PARALLEL_CHUNK_ASSETS_CURVE']=str(assets/'all-envelope')
 os.sched_setaffinity(0,set(range(8)))
 key=module+'-stream-r'+str(repeat)
 result=run(key,[ROOT/'parallel-stream','parallel','none',root],1680,True,e)
 events=[]
 for line in(ROOT/'runs'/key/'stdout').read_text().splitlines():
  if line.startswith('{'):
   try:events.append(json.loads(line))
   except json.JSONDecodeError:pass
 curves=[];pending=[]
 for event in events:
  if event.get('event')=='chunk_work':pending.append(event)
  elif event.get('event')=='curve_cell':
   event=dict(event,actual_chunk_parents=sum(x['parents']for x in pending),
    actual_chunk_subjobs=sum(x['children']for x in pending),chunk_axioms=[x['axioms']for x in pending])
   curves.append(event);pending=[]
 chunks=[x for x in events if x.get('event')=='chunk_work']
 accepted=[x['module']for x in events if x.get('event')=='accept']
 expected=9 if module=='envelope'else 5
 record=dict(result=result,curves=curves,chunks=chunks,accepted=accepted,
  completed=result['returncode']==0 and len(curves)==expected,
  measurement_scope='single process checks prefix once; root trial costs are incremental, not complete module invocation',
  certificate_generation_excluded=module=='envelope')
 (ROOT/(key+'-summary.json')).write_text(json.dumps(record,indent=2))
 if not record['completed']:raise RuntimeError('incomplete native curve; preserve raw')
if __name__=='__main__':
 try:main()
 finally:
  (ROOT/(sys.argv[1]+'-r'+sys.argv[2]+'-terminal.json')).write_text(json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
