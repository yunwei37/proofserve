"""Matched actual modules: finite, no-M, one shared P-core task."""
from pathlib import Path
import json,time,os
import native
P=Path(__file__).resolve().parent
def main():
 start=time.monotonic();records=[];errors=[]
 e=native.environment()
 e['LEAN_PATH']=json.loads((P/'runtime.json').read_text())['LEAN_PATH']
 modules=json.loads((P/'modules.json').read_text())
 def run(key,args,threads,measured=True):
  left=int(1690-(time.monotonic()-start))
  if left<15:raise RuntimeError('finite task budget reached')
  env=dict(e,LEAN_NUM_THREADS=str(threads))
  r=native.run(key,args,min(120,left),measured,env);records.append(r)
  return r
 try:
  assert json.loads((P/'build-v4-terminal.json').read_text())['complete']
  # Whole-source original frontend acceptance control, separate from counted sync.
  for x in modules:
   if x['regime']!='mathematical':continue
   name=x['module'].split('.')[-1]
   r=run('stock-'+name,[native.SDK/'bin/lean','-j1',x['source']],1)
   if r['returncode']:errors.append(dict(key=r['key'],reason='stock source failed'))
  for rep in [0,1]:
   for x in modules:
    short=x['module'].split('.')[-1]
    modes=['front','kernel']if x['regime']=='mathematical'else['kernel']
    for mode in modes:
     for j in ([1,2,4,8]if rep==0 else[8,4,2,1]):
      key=f'{mode}-{short}-r{rep}-j{j}'
      r=run(key,[P/'module-probe',mode,x['module'],x['source'],str(j)],j)
      prefix='FRONT 'if mode=='front'else'KERNEL '
      rr=[json.loads(line[len(prefix):])for line in(P/'runs'/key/'stdout').read_text().splitlines()if line.startswith(prefix)]
      if r['returncode']or len(rr)!=(8 if mode=='front'else(rr[0]['selected']if rr else -1)):
       errors.append(dict(key=key,reason='native operational failure or missing rows',rows=len(rr)))
       # Preserve independent modules while stopping a broken module/mode.
       break
      if mode=='front':
       if any(row['verdict']!='accepted'for row in rr):
        errors.append(dict(key=key,reason='source not accepted',rows=rr))
      elif any(row['result']['verdict']!='accepted'for row in rr):
       errors.append(dict(key=key,reason='original kernel rejected',rows=rr))
  state='complete'if not errors else'partial'
 except BaseException as ex:
  errors.append(dict(error=repr(ex)));state='partial'
 (P/'module-terminal.json').write_text(json.dumps(dict(state=state,cells=records,errors=errors,wall_s=time.monotonic()-start),indent=2))
 return 0 if state=='complete'else 1
if __name__=='__main__':raise SystemExit(main())
