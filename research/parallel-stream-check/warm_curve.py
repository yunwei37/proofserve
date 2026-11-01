"""Optional trusted-prefix leaf curves: not a cold independently checked stream."""
import json,os,sys,time
from pathlib import Path
from native import ROOT,environment,run
def main():
 assets=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets')
 selected=json.loads((assets/'assets.json').read_text())['selected']
 label=sys.argv[1];repeat=int(sys.argv[2])
 suffix={'barrier':'.BarrierData41','envelope':'.EnvelopePsiB','grid':'.Grid'}[label]
 roots=[x['module']for x in selected if x['module'].endswith(suffix)]
 assert len(roots)==1
 e=environment()
 prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 e['LEAN_PATH']=str(assets/'overlay-complete-v2')+':'+prep['lean_path']
 if label=='envelope':e['PARALLEL_CHUNK_ASSETS_CURVE']=str(assets/'all-envelope')
 os.sched_setaffinity(0,set(range(8)))
 key=label+'-warm-leaf-r'+str(repeat)
 rr=run(key,[ROOT/'warm-curve',roots[0]],1680,True,e)
 events=[]
 for x in(ROOT/'runs'/key/'stdout').read_text().splitlines():
  if x.startswith('{'):
   try:events.append(json.loads(x))
   except json.JSONDecodeError:pass
 curves=[x for x in events if x.get('event')=='curve_cell']
 complete=next((x for x in reversed(events)if x.get('event')=='complete'),None)
 summary=dict(result=rr,curves=curves,complete_event=complete,scope='trusted_stock_imports_entire_leaf',
  completed=rr['returncode']==0 and len(curves)==(9 if label=='envelope'else 5) and complete is not None)
 (ROOT/(key+'-summary.json')).write_text(json.dumps(summary,indent=2))
 if not summary['completed']:raise RuntimeError('incomplete; preserve raw')
if __name__=='__main__':main()
