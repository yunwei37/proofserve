from pathlib import Path
import json,csv,collections
def analyze(point,out):
 data={}
 for rep in [0,1]:
  for j in [1,2,4,8]:
   path=point/f'runs/math-r{rep}-j{j}'
   terminal=json.loads((path/'result.json').read_text())
   assert terminal['returncode']==0 and terminal['native_retired']
   rows=[json.loads(s[5:])for s in(path/'stdout').read_text().splitlines()if s.startswith('MATH ')]
   assert len(rows)==32
   data[rep,j]={(x['result']['id'],x['result']['budget']):x for x in rows}
 pairs=[];differences=[]
 for rep in[0,1]:
  for j in[2,4,8]:
   assert data[rep,1].keys()==data[rep,j].keys()
   for key,x in data[rep,1].items():
    a=x['result'];z=data[rep,j][key]['result']
    av=a['command_raw_heartbeats'];zv=z['command_raw_heartbeats'];assert len(av)==len(zv)==3
    pairs.append(dict(id=key[0],budget=key[1],repeat=rep,workers=j,
     opening_changed=av[0]!=zv[0],theorem_changed=av[1]!=zv[1],terminal_changed=av[2]!=zv[2],
     verdict_changed=a['verdict']!=z['verdict'],errors_changed=a['errors']!=z['errors'],
     axioms_changed=a['axioms']!=z['axioms'],opening_delta=zv[0]-av[0],theorem_delta=zv[1]-av[1]))
    if a['errors']!=z['errors']:
     differences.append(dict(id=key[0],budget=key[1],repeat=rep,workers=j,baseline=a['errors'],current=z['errors']))
 ranges=[]
 for key in data[0,1]:
  obs=[data[rep,j][key]['result']for rep in[0,1]for j in[1,2,4,8]]
  values=[x['command_raw_heartbeats'][1]for x in obs]
  ranges.append(dict(id=key[0],budget=key[1],min_theorem_HB=min(values),max_theorem_HB=max(values),
   relative_range=(max(values)-min(values))/min(values),all_accepted=all(x['verdict']=='accepted'for x in obs)))
 out.mkdir(exist_ok=True)
 for name,rows in [('pairs',pairs),('ranges',ranges)]:
  with(out/(name+'.csv')).open('w')as f:
   writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 (out/'diagnostic-differences.json').write_text(json.dumps(differences,indent=2))
 return pairs,ranges
if __name__=='__main__':
 import sys
 pairs,ranges=analyze(Path(sys.argv[1]),Path(sys.argv[2]))
 print(json.dumps(dict(pairs=len(pairs),theorem_changes=sum(x['theorem_changed']for x in pairs),
   verdict_changes=sum(x['verdict_changed']for x in pairs),error_changes=sum(x['errors_changed']for x in pairs))))
