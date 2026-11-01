"""Analyze only a complete frozen matrix; retain interrupted cells separately."""
from pathlib import Path
import json,csv,collections
from replay import rows_from_log
def analyze(point,out):
 term=json.loads((point/'matrix-terminal.json').read_text())
 if term['state']!='complete':raise ValueError("partial matrix; do not label missing units as failed proofs")
 allrows=[];tasks=[]
 for rep in [0,1]:
  for threads in [1,2,4,8]:
   key=f'matrix-r{rep}-j{threads}'
   result=json.loads((point/'runs'/key/'result.json').read_text())
   rows=rows_from_log((point/'runs'/key/'stdout').read_text())
   req=json.loads((point/(key+'.json')).read_text())
   if len(rows)!=len(req)or result['returncode']!=0 or not result['native_retired']:
    raise ValueError("incomplete native unit: "+key)
   for row in rows:allrows.append(dict(row,repeat=rep,threads=threads))
   text=(point/'runs'/f'tasks-r{rep}-j{threads}'/'stdout').read_text()
   ts=[json.loads(x[6:])for x in text.splitlines()if x.startswith('TASKS ')]
   if len(ts)!=1:raise ValueError('task control incomplete')
   tasks.append(dict(ts[0],repeat=rep,threads=threads))
 index={(x['repeat'],x['threads'],x['id'],x['mode'],x['observer'],x['budget']):x for x in allrows}
 ids=sorted({x['id']for x in allrows})
 budgets=sorted({x['budget']for x in allrows})
 comparisons={}
 def add(label,pairs):
  diffs=[];count=0
  for a,b in pairs:
   count+=1
   fields=[f for f in ['verdict','axioms','new_axioms','errors']if a[f]!=b[f]]
   if a['mode']==b['mode']=='sync'and a['command_raw_heartbeats']!=b['command_raw_heartbeats']:
    fields.append('command_raw_heartbeats')
   if fields:diffs.append(dict(id=a['id'],budget=a['budget'],repeat=a['repeat'],threads_a=a['threads'],threads_b=b['threads'],
      mode_a=a['mode'],mode_b=b['mode'],observer_a=a['observer'],observer_b=b['observer'],
      fields=fields,verdict_a=a['verdict'],verdict_b=b['verdict'],
      units_a=a['command_raw_heartbeats'],units_b=b['command_raw_heartbeats']))
  comparisons[label]=dict(pairs=count,verdict_mismatches=sum(x['verdict_a']!=x['verdict_b']for x in diffs),
    acceptance_mismatches=sum((x['verdict_a']=='accepted')!=(x['verdict_b']=='accepted')for x in diffs),
    heartbeat_mismatches=sum('command_raw_heartbeats'in x['fields']for x in diffs),
    differences=diffs)
 for obs in ['off','native','trace']:
  add('threads_'+obs,((index[rep,1,key,mode,obs,budget],index[rep,t,key,mode,obs,budget])
    for rep in [0,1]for t in [2,4,8]for key in ids for mode in ['stock','sync']for budget in budgets))
 for obs in ['native','trace']:
  add('observer_'+obs,((index[rep,t,key,mode,'off',budget],index[rep,t,key,mode,obs,budget])
    for rep in [0,1]for t in [1,2,4,8]for key in ids for mode in ['stock','sync']for budget in budgets))
 add('frontend',((index[rep,t,key,'stock',obs,budget],index[rep,t,key,'sync',obs,budget])
   for rep in [0,1]for t in [1,2,4,8]for key in ids for obs in ['off','native','trace']for budget in budgets))
 add('repeat_and_order',((index[0,t,key,mode,obs,budget],index[1,t,key,mode,obs,budget])
   for t in [1,2,4,8]for key in ids for mode in ['stock','sync']for obs in ['off','native','trace']for budget in budgets))
 summary=dict(sources=len(ids),budgets=budgets,rows=len(allrows),verdict_counts=dict(collections.Counter(x['verdict']for x in allrows)),
   comparisons=comparisons,task_controls=tasks,native_cells=term['cells'],raw=str(point))
 out.mkdir(exist_ok=True)
 (out/'matrix-summary.json').write_text(json.dumps(summary,indent=2))
 with (out/'matrix-rows.csv').open('w')as f:
  fields=['id','repeat','threads','mode','observer','budget','verdict','main_thread_raw_heartbeats','command_raw_heartbeats']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for row in allrows:w.writerow({k:row[k]for k in fields})
 return summary
if __name__=='__main__':
 import sys
 s=analyze(Path(sys.argv[1]),Path(sys.argv[2]))
 print(json.dumps({k:{f:v for f,v in x.items()if f!='differences'}for k,x in s['comparisons'].items()},indent=2))
