"""Summarize real stored-computation replay; never compare its cost with frontend time."""
from pathlib import Path
import json,csv,collections
def analyze(point,out):
 terminal=json.loads((point/'region-terminal.json').read_text())
 if terminal['state']!='complete':raise ValueError('partial collection; preserve missing units')
 rows=[]
 for rep in [0,1]:
  for module in ['grid','envelope']:
   for workers in [1,2,4,8]:
    cell=f'{module}-r{rep}-j{workers}'
    native=json.loads((point/'runs'/cell/'result.json').read_text())
    data=[json.loads(x[7:])for x in(point/'runs'/cell/'stdout').read_text().splitlines()if x.startswith('REGION ')]
    if native['returncode']or not native['native_retired']or len(data)!=8:raise ValueError('incomplete '+cell)
    for x in data:
     rows.append(dict(module=module,repeat=rep,workers=workers,**x['result']))
 index={(x['module'],x['repeat'],x['workers'],x['target']):x for x in rows}
 summary={}
 for module in ['grid','envelope']:
  targets=sorted({x['target']for x in rows if x['module']==module})
  diffs=[];pairs=0
  for rep in [0,1]:
   for workers in [2,4,8]:
    for target in targets:
     a=index[module,rep,1,target];b=index[module,rep,workers,target];pairs+=1
     fields=[k for k in ['rawHB','verdict','error']if a[k]!=b[k]]
     if fields:diffs.append(dict(target=target,repeat=rep,workers=workers,fields=fields,
       rawHB1=a['rawHB'],rawHBk=b['rawHB'],verdict1=a['verdict'],verdictk=b['verdict']))
  repeat_diffs=[dict(target=t,workers=w,hb0=index[module,0,w,t]['rawHB'],hb1=index[module,1,w,t]['rawHB'])
   for w in [1,2,4,8]for t in targets if index[module,0,w,t]['rawHB']!=index[module,1,w,t]['rawHB']]
  concurrency=[]
  for rep in [0,1]:
   for workers in [1,2,4,8]:
    rr=[index[module,rep,workers,t]for t in targets]
    span=max(x['stopNS']for x in rr)-min(x['startNS']for x in rr)
    concurrency.append(dict(repeat=rep,workers=workers,tids=len({x['tid']for x in rr}),
      kernel_span_s=span/1e9,sum_unit_wall_s=sum(x['wallNS']for x in rr)/1e9,
      overlap_ratio=sum(x['wallNS']for x in rr)/max(1,span)))
  summary[module]=dict(targets=targets,pairs=pairs,differences=diffs,
    repeat_hb_differences=repeat_diffs,concurrency=concurrency)
 out.mkdir(exist_ok=True)
 (out/'summary.json').write_text(json.dumps(dict(modules=summary,native=terminal,raw=str(point)),indent=2))
 with(out/'units.csv').open('w')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return summary
if __name__=='__main__':
 import sys
 s=analyze(Path(sys.argv[1]),Path(sys.argv[2]))
 print(json.dumps({m:dict(pairs=x['pairs'],differences=len(x['differences']),repeat_differences=len(x['repeat_hb_differences']))for m,x in s.items()},indent=2))
