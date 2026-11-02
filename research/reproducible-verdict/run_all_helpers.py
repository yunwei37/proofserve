from pathlib import Path
import os,json,time
import native
P=Path(__file__).resolve().parent
def main():
 start=time.monotonic();records=[];errors=[]
 e=native.environment();e['LEAN_PATH']=json.loads((P/'runtime.json').read_text())['LEAN_PATH']
 modules=[x for x in json.loads((P/'modules.json').read_text())if x['regime']=='computation']
 expected={'UMoments9':1164,'BarrierData41':1320,'EnvelopePsiB':40}
 try:
  assert json.loads((P/'build-terminal.json').read_text())['complete']
  for rep in [0,1,2]:
   for x in modules:
    short=x['module'].split('.')[-1]
    for j in ([1,2,4,8]if rep%2==0 else[8,4,2,1]):
     left=int(1690-(time.monotonic()-start))
     if left<15:raise RuntimeError('finite whole-task budget')
     key=f'kernel-{short}-r{rep}-j{j}'
     env=dict(e,LEAN_NUM_THREADS=str(j))
     r=native.run(key,[P/'all-helpers','kernel',x['module'],x['source'],str(j)],min(180,left),True,env)
     records.append(r)
     rows=[json.loads(s[7:])for s in(P/'runs'/key/'stdout').read_text().splitlines()if s.startswith('KERNEL ')]
     names=[x['result']['target']for x in rows]
     if r['returncode']or len(rows)!=expected[short]or len(set(names))!=expected[short]:
      errors.append(dict(key=key,reason='operational failure or incomplete unique helper census',rows=len(rows)))
      break
     if any(x['result']['verdict']!='accepted'for x in rows):
      errors.append(dict(key=key,reason='kernel outcome differs from accepted source'))
  state='complete'if not errors else'partial'
 except BaseException as ex:
  errors.append(dict(error=repr(ex)));state='partial'
 (P/'census-terminal.json').write_text(json.dumps(dict(state=state,repeats=[0,1,2],expected=expected,cells=records,errors=errors,wall_s=time.monotonic()-start),indent=2))
 return 0 if state=='complete'else 1
if __name__=='__main__':raise SystemExit(main())
