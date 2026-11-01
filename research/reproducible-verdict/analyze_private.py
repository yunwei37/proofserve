"""Matched input-runtime cache comparison; keep parent counters out of total-work claims."""
from pathlib import Path
import json,csv
def readrows(path):
 return [json.loads(x[6:])for x in path.read_text().splitlines()if x.startswith('REPRO ')]
def analyze(point,out):
 terminal=json.loads((point/'private-terminal.json').read_text())
 if terminal['state']!='complete':raise ValueError('partial runtime experiment: no complete paired cache claim')
 rows=[];comparisons=[];conditions=json.loads((point/'cache-conditions.json').read_text())
 for rep in [0,1]:
  for threads in [1,8]:
   pair={}
   for state in ['cold','warm']:
    key=f'private-r{rep}-j{threads}-{state}'
    result=json.loads((point/'runs'/key/'result.json').read_text())
    rr=readrows(point/'runs'/key/'stdout')
    if len(rr)!=64 or result['returncode']or not result['native_retired']:raise ValueError('incomplete '+key)
    pair[state]={(x['id'],x['mode'],x['budget']):x for x in rr}
    if len(pair[state])!=64:raise ValueError('duplicate observation')
    rows.extend(dict(x,repeat=rep,threads=threads,cache=state)for x in rr)
   if pair['cold'].keys()!=pair['warm'].keys():raise ValueError('unmatched inputs')
   for key,c in pair['cold'].items():
    w=pair['warm'][key]
    fields=[k for k in ['verdict','errors','axioms','new_axioms']if c[k]!=w[k]]
    vector_same=(c['command_raw_heartbeats']==w['command_raw_heartbeats'])if c['mode']=='sync'else None
    comparisons.append(dict(id=key[0],mode=key[1],budget=key[2],repeat=rep,threads=threads,
      fields=fields,verdict_cold=c['verdict'],verdict_warm=w['verdict'],
      sync_raw_HB_equal=vector_same,parent_HB_equal=c['main_thread_raw_heartbeats']==w['main_thread_raw_heartbeats'],
      units_cold=c['command_raw_heartbeats'],units_warm=w['command_raw_heartbeats']))
 summary=dict(rows=len(rows),pairs=len(comparisons),verdict_differences=sum(x['verdict_cold']!=x['verdict_warm']for x in comparisons),
   sync_pairs=sum(x['mode']=='sync'for x in comparisons),
   sync_HB_differences=sum(x['sync_raw_HB_equal']is False for x in comparisons),
   parent_HB_differences=sum(not x['parent_HB_equal']for x in comparisons),
   comparisons=comparisons,conditions=conditions,native=terminal,raw=str(point),
   scope='private runtime inputs; residual resident pages must be reported; no global OS cold boot')
 out.mkdir(exist_ok=True)
 (out/'summary.json').write_text(json.dumps(summary,indent=2))
 fields=['id','repeat','threads','cache','mode','budget','verdict','main_thread_raw_heartbeats','command_raw_heartbeats']
 with(out/'rows.csv').open('w')as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for row in rows:writer.writerow({k:row[k]for k in fields})
 return summary
if __name__=='__main__':
 import sys
 result=analyze(Path(sys.argv[1]),Path(sys.argv[2]))
 print(json.dumps({k:result[k]for k in ['rows','pairs','verdict_differences','sync_pairs','sync_HB_differences','parent_HB_differences']},indent=2))
