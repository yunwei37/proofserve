from pathlib import Path
import json,csv,collections
def rows(p):
 return [json.loads(x[6:])for x in p.read_text().splitlines()if x.startswith('REPRO ')]
def analyze(point,out):
 t=json.loads((point/'extra-terminal.json').read_text())
 if t['state']!='complete':raise ValueError('partial collection')
 result=dict(raw=str(point),native=t['cells'],cache_conditions=t['cache'],ladders={},input_only_cache={})
 allrows=[]
 for threads in [1,8]:
  rr=rows(point/'runs'/f'ladder-j{threads}'/'stdout')
  if len(rr)!=84:raise ValueError('missing ladder observation')
  allrows.extend(dict(r,threads=threads,cell='ladder')for r in rr)
  by=collections.defaultdict(list)
  for r in rr:by[r['id']].append(r)
  violations=[];passed_pairs=0;chains={}
  for key,values in by.items():
   values.sort(key=lambda x:x['budget'])
   if key=='budget-sensitive-control':continue
   chains[key]=[(x['budget'],x['verdict'])for x in values]
   for i,a in enumerate(values):
    if a['verdict']=='accepted':
     for b in values[i+1:]:
      passed_pairs+=1
      if b['verdict']!='accepted':violations.append(dict(id=key,smaller=a['budget'],larger=b['budget'],larger_verdict=b['verdict']))
  result['ladders'][str(threads)]=dict(sources=len(chains),budgets=[500,1000,1500,3000,6000],
    lower_accepted_larger_pairs=passed_pairs,violations=violations,chains=chains,
    intentional_control=[x for x in rr if x['id']=='budget-sensitive-control'])
 pairs=[];diffs=[]
 for rep in [0,1,2]:
  cold=rows(point/'runs'/f'cache-r{rep}-cold'/'stdout')
  warm=rows(point/'runs'/f'cache-r{rep}-warm'/'stdout')
  if len(cold)!=16 or len(warm)!=16:raise ValueError('missing cache observations')
  allrows.extend(dict(r,threads=1,cell=f'input-r{rep}-{kind}')for kind,rr in [('cold',cold),('warm',warm)]for r in rr)
  for a,b in zip(cold,warm):
   if a['id']!=b['id']:raise ValueError('cache order mismatch')
   fields=[f for f in ['verdict','axioms','new_axioms','errors','main_thread_raw_heartbeats']if a[f]!=b[f]]
   if fields:diffs.append(dict(id=a['id'],repeat=rep,fields=fields,main_cold=a['main_thread_raw_heartbeats'],main_warm=b['main_thread_raw_heartbeats']))
   pairs.append((a,b))
 result['input_only_cache']=dict(pairs=len(pairs),differences=diffs,
   verdict_differences=sum(a['verdict']!=b['verdict']for a,b in pairs),
   parent_counter_not_total=True,not_an_SDK_or_Mathlib_cold_test=True)
 out.mkdir(exist_ok=True)
 (out/'summary.json').write_text(json.dumps(result,indent=2))
 with(out/'rows.csv').open('w')as f:
  fields=['cell','threads','id','budget','mode','observer','verdict','main_thread_raw_heartbeats','command_raw_heartbeats']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in allrows:w.writerow({k:r[k]for k in fields})
 return result
if __name__=='__main__':
 import sys
 s=analyze(Path(sys.argv[1]),Path(sys.argv[2]))
 print(json.dumps(dict(ladders={k:{x:v for x,v in d.items()if x not in ['chains','intentional_control']}for k,d in s['ladders'].items()},cache=s['input_only_cache']),indent=2))
