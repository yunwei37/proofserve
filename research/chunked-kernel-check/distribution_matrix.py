"""One bounded P-core capture: per-declaration costs and stock replay controls."""
import os,json,time,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from declaration_native import run,SDK,environment
def events(key):
 path=BASE/'runs'/key/'stdout'
 return [json.loads(line) for line in path.read_text().splitlines() if line.startswith('{')]
def finish(key):
 ee=events(key);out=[r for r in ee if r['event']=='complete']
 assert len(out)==1,(key,'missing complete event')
 return out[0]
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 start=time.monotonic()
 common=[str(SDK/'bin/lean'),'--root='+str(BASE),'-j1','--load-dynlib='+str(BASE/'clock.so'),'--run',str(BASE/'TimedReplay.lean')]
 init=str(SDK/'lib/lean/Init/Data/Nat/Basic.olean')
 controls={}
 for mode in ['stock','timed']:
  key='control-'+mode
  r=run(key,common+[mode,'Init.Data.Nat.Basic',init],limit=90,measured=True)
  assert r['returncode']==0 and not r['stop_reasons']
  controls[mode]=finish(key)
 assert set(controls['stock']['eligible_names'])==set(controls['timed']['eligible_names'])
 negatives=[]
 for mode in ['stock','timed']:
  key='invalid-'+mode
  r=run(key,common+[mode,'Init.Data.Nat.Basic',init,'bvar'],limit=90,measured=True)
  assert r['returncode'] not in [0,124,137,-9] and not r['stop_reasons']
  if mode=='timed':assert any(e['event']=='kernel_declaration' and not e['accepted'] for e in events(key))
  negatives.append(dict(mode=mode,returncode=r['returncode']))
 (BASE/'controls.json').write_text(json.dumps(dict(positive_names_equal=True,invalid_proof_rejections=negatives),indent=2)+'\n')
 inputs=json.loads((BASE/'inputs.json').read_text())
 suffix=['Certificate.UMoments9','Certificates.BarrierData41','PlanarPacking.Grid']
 hot=[next(r for r in inputs if r['module'].endswith(x)) for x in suffix]
 remainder=[r for r in inputs if r not in hot]
 units=[(r,mode) for r in hot for mode in ['stock','timed']]+[(r,'timed') for r in remainder]
 rows=[];comp=[]
 for index,(target,mode) in enumerate(units):
  limit=min(600,max(90,int(2*target['source_compile_cpu_s']+30)))
  if time.monotonic()-start+limit+15>1680:
   (BASE/'window-budget-stop.json').write_text(json.dumps(dict(next_index=index,next_module=target['module'],mode=mode,declared_limit_s=limit,completed=len(rows)))+'\n')
   break
  key=f"{index:02d}-{target['module'].split('.')[-1]}-{mode}"
  result=run(key,common+[mode,target['module'],target['path']],limit=limit,measured=True)
  row=dict(module=target['module'],mode=mode,key=key,result=result)
  rows.append(row)
  (BASE/'progress.json').write_text(json.dumps(dict(planned=len(units),completed=len(rows),last=row),indent=2)+'\n')
  assert result['returncode']==0 and not result['stop_reasons'],key
  done=finish(key);comp.append(dict(module=target['module'],mode=mode,key=key,complete=done))
  if mode=='timed' and target in hot:
   stock=next(x for x in comp if x['module']==target['module'] and x['mode']=='stock')
   assert set(stock['complete']['eligible_names'])==set(done['eligible_names']),(target['module'],'acceptance set mismatch')
  (BASE/'completed-units.json').write_text(json.dumps(comp,indent=2)+'\n')
 (BASE/'terminal.json').write_text(json.dumps(dict(complete=len(rows)==len(units),planned=len(units),completed=len(rows),all_completed_returned_zero=True,
   meaning='kernel replay distribution; queue/import/graph/frontend distinct; not source compilation or service throughput'),indent=2)+'\n')
if __name__=='__main__':
 try:main()
 except BaseException as e:
  (BASE/'failure.json').write_text(json.dumps(dict(error=repr(e)))+'\n')
  raise
