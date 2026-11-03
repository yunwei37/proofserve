# Final cells of the placement x observation control, after the original series.
# Copy beside the frozen runner on PVC; never run this from the Git checkout.
import os,json,time
from pathlib import Path
from attribution import ROOT,MODULE,runtime,events
from native import run
def main():
 assert ROOT==Path(__file__).resolve().parent
 assert str(ROOT).startswith('/workspaces/.agent-state/gpu-smt-captures/')
 assert json.loads((ROOT/'series-terminal.json').read_text())['state']=='complete'
 assert (ROOT/'qualified.json').exists()
 output=ROOT/'placement-profile-results.json'
 assert not output.exists(),'existing cells must be inspected, never overwritten'
 reference=set(json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/barrier-full-reference1-r1-summary.json').read_text())['accepted'])
 cells=[];begin=time.monotonic();state='partial';error=None
 try:
  for name,count,allowed in [('P8-unpinnedProfile',8,list(range(8))),('M24-unpinnedProfile',24,list(range(24)))]:
   os.sched_setaffinity(0,set(allowed))
   env=runtime(count,allowed,[],0,True)
   left=1690-(time.monotonic()-begin)
   if left<120:raise RuntimeError('finite window ended; retain partial cells')
   c=run('full-'+name,[ROOT/'parallel-stream','parallel','none',MODULE],min(750,int(left)),True,env)
   cells.append(c);ev=events(c['key'])
   ids=[x['module'] for x in ev if x.get('event')=='accept']
   c.update(accepted_IDs=ids,accepted_set_equal_to_serial=set(ids)==reference,
    profile_enabled=True,worker_pins=[],coordinator_cpu=None,
    complete_events=[x for x in ev if x.get('event')=='complete'])
   output.write_text(json.dumps(cells,indent=2))
   if (c['returncode'] or not c['native_retired'] or not c['cgroup_retired'] or c['stop_reasons']
    or len(ids)!=4449 or not c['complete_events'] or not c['accepted_set_equal_to_serial']):
    raise RuntimeError('incomplete or differing full-closure verdict')
  state='complete'
 except BaseException as ex:error=repr(ex);raise
 finally:
  (ROOT/'placement-profile-terminal.json').write_text(json.dumps(dict(state=state,error=error,cells=cells,
   wall_s=time.monotonic()-begin,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main()
