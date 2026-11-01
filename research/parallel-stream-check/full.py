"""One full cold closure, one selected configuration per P-lock task.

Unlike curve.py this does not run all leaf variants or reuse a prefix for timing.
Import/audit/read/check/commit/cleanup are included in the native subprocess wall.
"""
import json,os,sys,time
from pathlib import Path
from native import ROOT,run,environment
def main():
 label=sys.argv[1];mode=sys.argv[2];workers=int(sys.argv[3]);repeat=int(sys.argv[4])
 assert mode in ['audit','parallel'] and workers in [1,2,4,8]
 assert mode!='audit' or workers==1
 assets=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets')
 frame=json.loads((assets/'assets.json').read_text())
 suffix={'barrier':'.BarrierData41','envelope':'.EnvelopePsiB','grid':'.Grid'}[label]
 roots=[x['module']for x in frame['selected']if x['module'].endswith(suffix)]
 assert len(roots)==1
 e=environment()
 prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 e.update(LEAN_PATH=str(assets/'overlay-complete-v2')+':'+prep['lean_path'],PARALLEL_WORKERS=str(workers))
 # No leaf-curve option, prepared chunk input or profiling environment is inherited.
 for option in ['PARALLEL_CURVE_MODULES','PARALLEL_CHUNK_ASSETS','PARALLEL_CHUNK_ASSETS_CURVE','DECOUPLED_MEMORY_PROFILE']:
  e.pop(option,None)
 os.sched_setaffinity(0,set(range(8)))
 key=label+'-full-'+mode+str(workers)+'-r'+str(repeat)
 rr=run(key,[ROOT/'parallel-stream',mode,'none',roots[0]],1680,True,e)
 events=[]
 for line in(ROOT/'runs'/key/'stdout').read_text().splitlines():
  if line.startswith('{'):
   try:events.append(json.loads(line))
   except json.JSONDecodeError:pass
 accepted=[x['module']for x in events if x.get('event')=='accept']
 completion=next((x for x in reversed(events)if x.get('event')=='complete'),None)
 expected=None
 prior=ROOT/(label+'-stream-r1-summary.json')
 if prior.exists():
  p=json.loads(prior.read_text())
  if p['completed']:expected=set(p['accepted'])
 equality=None if expected is None else expected==set(accepted)
 complete=rr['returncode']==0 and completion is not None
 summary=dict(result=rr,accepted=accepted,complete_event=completion,
  completed=complete,accepted_set_equal_to_same_input_curve=equality,
  scope='one_full_cold_closure_single_configuration',
  source='qualified v14 original mathematical kernel; no chunk rewrite')
 (ROOT/(key+'-summary.json')).write_text(json.dumps(summary,indent=2))
 if not complete or equality is False:raise RuntimeError('incomplete/acceptance difference; preserve raw')
if __name__=='__main__':
 try:main()
 finally:
  (ROOT/('-'.join(sys.argv[1:])+'-terminal.json')).write_text(json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
