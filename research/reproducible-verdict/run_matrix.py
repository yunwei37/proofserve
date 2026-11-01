"""Frozen, bounded workload/control matrix. Run only under the shared P-core lock."""
from pathlib import Path
import json,time,os,sys
import native
ROOT=Path(__file__).resolve().parent
START=time.monotonic()
def cell(label,threads,args):
  remaining=int(960-(time.monotonic()-START))
  if remaining<10:raise RuntimeError("finite whole-task budget exhausted")
  env=native.environment();env['LEAN_NUM_THREADS']=str(threads)
  result=native.run(label,[native.SDK/'bin/lean','-j'+str(threads),'--run']+args,
    limit=min(100,remaining),measured=True,env=env)
  if result.get('returncode')!=0:raise RuntimeError("native operational failure: "+label)
  return result
def main():
  records=[]
  try:
    for repeat in [0,1]:
      for threads in ([1,2,4,8] if repeat==0 else [8,4,2,1]):
        key=f"matrix-r{repeat}-j{threads}"
        records.append(cell(key,threads,[ROOT/'Probe.lean',ROOT/(key+'.json')]))
        records.append(cell(f"tasks-r{repeat}-j{threads}",threads,[ROOT/'TaskProbe.lean','5000']))
    state="complete"
  except BaseException as e:
    state="partial";records.append(dict(error=repr(e)))
  (ROOT/'matrix-terminal.json').write_text(json.dumps(dict(state=state,cells=records,
      wall_s=time.monotonic()-START),indent=2))
  return 0 if state=="complete" else 1
if __name__=='__main__':raise SystemExit(main())
