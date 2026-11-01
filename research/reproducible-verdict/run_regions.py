"""One bounded kernel-regime task, after the currently owned task has retired."""
from pathlib import Path
import json,os,time
import native
ROOT=Path(__file__).resolve().parent
MODULES=[("grid","OAI.Analysis.PlanarPacking.Grid"),
         ("envelope","OAI.Analysis.Triangular.Envelope.EnvelopePsiB")]
def main():
 start=time.monotonic();records=[]
 try:
  for rep in [0,1]:
   for short,module in MODULES:
    for threads in ([1,2,4,8]if rep==0 else[8,4,2,1]):
     left=int(1690-(time.monotonic()-start))
     if left<20:raise RuntimeError("finite whole-task budget exhausted")
     env=native.environment();env['LEAN_NUM_THREADS']=str(threads)
     key=f'{short}-r{rep}-j{threads}'
     result=native.run(key,[native.SDK/'bin/lean','-j'+str(threads),'--run',
       ROOT/'RegionProbe.lean',module,str(threads)],limit=min(180,left),measured=True,env=env)
     records.append(result)
     rows=[json.loads(x[7:])for x in(ROOT/'runs'/key/'stdout').read_text().splitlines()if x.startswith('REGION ')]
     if result['returncode']or len(rows)!=8:raise RuntimeError('incomplete native kernel cell '+key)
     if any(x['result']['verdict']!='accepted'for x in rows):raise RuntimeError('original kernel rejected stored proof')
  state='complete'
 except BaseException as error:
  records.append(dict(error=repr(error)));state='partial'
 (ROOT/'region-terminal.json').write_text(json.dumps(dict(state=state,cells=records,
   wall_s=time.monotonic()-start),indent=2))
 return 0 if state=='complete'else 1
if __name__=='__main__':raise SystemExit(main())
