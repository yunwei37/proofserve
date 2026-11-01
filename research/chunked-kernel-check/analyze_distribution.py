"""Completed-unit native kernel grain; incomplete units are never zeros."""
import os,pathlib,json,csv,gzip,statistics,argparse
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/declaration-distribution-v1')
def quantile(values,p):
 v=sorted(values)
 if not v:return None
 at=(len(v)-1)*p;lo=int(at);hi=min(lo+1,len(v)-1)
 return v[lo]*(hi-at)+v[hi]*(at-lo) if hi!=lo else v[lo]
def write(name,rows):
 if not rows:return
 with (HERE/name).open('w') as f:
  w=csv.DictWriter(f,lineterminator='\n',fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 inputs=json.loads((RAW/'inputs.json').read_text());lookup={r['module']:r for r in inputs}
 units=[]
 for artifact in sorted((RAW/'runs').glob('[0-9][0-9]-*/result.json')):
  try:
   rr=json.loads(artifact.read_text())
   if rr['returncode']!=0 or not rr.get('native_retired'):continue
   records=[json.loads(line) for line in (artifact.parent/'stdout').read_text().splitlines() if line.startswith('{')]
   final=[r for r in records if r.get('event')=='complete']
   if len(final)==1:
    done=final[0];units.append(dict(module=done['module'],mode=done['mode'],key=artifact.parent.name,complete=done))
  except (json.JSONDecodeError,FileNotFoundError):continue
 # Raw final receipts and complete events are authoritative, not a running checkpoint.
 summaries=[];points=[];pergoal=[];overheads=[];histogram=[]
 for unit in units:
  path=RAW/'runs'/unit['key'];rr=json.loads((path/'result.json').read_text())
  assert rr['returncode']==0 and rr['native_retired'] and not rr['stop_reasons']
  events=[json.loads(s) for s in (path/'stdout').read_text().splitlines() if s.startswith('{')]
  complete=[e for e in events if e['event']=='complete'];assert len(complete)==1
  done=complete[0]
  if unit['mode']!='timed':continue
  decl=[x for x in events if x['event']=='kernel_declaration']
  for row in decl:
   row['thread_cpu_ns']=int(row['thread_cpu_ns']);row['wall_ns']=int(row['wall_ns'])
   assert row['accepted'] and row['thread_cpu_ns']<=row['wall_ns']*1.05+1000000
  dec=[r for r in decl if r['decide_helper']];big=[r for r in dec if r['thread_cpu_ns']>=10**9]
  allcpu=sum(r['thread_cpu_ns'] for r in decl)/1e9;dcpu=sum(r['thread_cpu_ns'] for r in dec)/1e9
  bigcpu=sum(r['thread_cpu_ns'] for r in big)/1e9
  source=lookup[unit['module']]
  values=[r['thread_cpu_ns']/1e9 for r in dec]
  summary=dict(module=unit['module'],source_sites=source['source_sites'],input_native_decide_helpers=done['native_decide_helpers'],
    traced_declarations=len(decl),traced_decide_helpers=len(dec),all_kernel_call_cpu_s=allcpu,decision_call_cpu_s=dcpu,
    large_decision_count_ge1s_cpu=len(big),large_decision_cpu_s=bigcpu,large_decision_share_of_decision_cpu=bigcpu/dcpu if dcpu else None,
    large_decision_share_of_all_kernel_cpu=bigcpu/allcpu if allcpu else None,
    wall_ge1s_decision_count=sum(r['wall_ns']>=10**9 for r in dec),
    median_decision_cpu_s=statistics.median(values) if values else None,p90_decision_cpu_s=quantile(values,.9),
    p99_decision_cpu_s=quantile(values,.99),max_decision_cpu_s=max(values) if values else None,
    replay_cpu_s=int(done['replay_process_cpu_ns'])/1e9,replay_wall_s=int(done['replay_wall_ns'])/1e9,
    native_wall_s=rr['wall_s'],native_cpu_s=rr['user_s']+rr['system_s'],raw=str(path))
  summaries.append(summary)
  bins=[(0,.001,'<1ms'),(.001,.01,'1-10ms'),(.01,.1,'10-100ms'),(.1,1,'100ms-1s'),(1,float('inf'),'>=1s')]
  for low,high,label in bins:
   chosen=[r for r in dec if low<=r['thread_cpu_ns']/1e9<high]
   histogram.append(dict(module=unit['module'],bin=label,count=len(chosen),decision_cpu_s=sum(r['thread_cpu_ns'] for r in chosen)/1e9))
  for row in dec:
   pergoal.append(dict(module=unit['module'],names='|'.join(row['names']),wall_s=row['wall_ns']/1e9,
     thread_cpu_s=row['thread_cpu_ns']/1e9,ge1s_cpu=row['thread_cpu_ns']>=10**9,goal_head=row.get('goal_head','')))
  for row in sorted(dec,key=lambda x:x['thread_cpu_ns'],reverse=True)[:5]:
   points.append(dict(module=unit['module'],names='|'.join(row['names']),cpu_s=row['thread_cpu_ns']/1e9,wall_s=row['wall_ns']/1e9,goal=row['goal']))
  stock=[x for x in units if x['module']==unit['module'] and x['mode']=='stock']
  if stock:
   sd=stock[0]['complete'];assert set(sd['eligible_names'])==set(done['eligible_names'])
   scpu=int(sd['replay_process_cpu_ns'])/1e9;swall=int(sd['replay_wall_ns'])/1e9
   overheads.append(dict(module=unit['module'],stock_replay_cpu_s=scpu,timed_replay_cpu_s=summary['replay_cpu_s'],
     timed_to_stock_cpu_ratio=summary['replay_cpu_s']/scpu,stock_replay_wall_s=swall,timed_replay_wall_s=summary['replay_wall_s'],
     accepted_eligible_names_equal=True,scope='one ordered pair, observer and cache/allocation effects; not zero-overhead claim'))
 write('declaration-histogram.csv',histogram);write('declaration-distribution.csv',summaries);write('declaration-top-goals.csv',points);write('declaration-observer-controls.csv',overheads)
 if pergoal:
  with gzip.open(HERE/'declaration-per-goal.csv.gz','wt',compresslevel=9) as f:
   w=csv.DictWriter(f,lineterminator='\n',fieldnames=list(pergoal[0]));w.writeheader();w.writerows(pergoal)
 sampled=[r for r in summaries if lookup[r['module']]['inclusion_probability'] not in [None,'','0']]
 def weight(r):return 1/float(lookup[r['module']]['inclusion_probability'])
 den=sum(weight(r)*r['all_kernel_call_cpu_s'] for r in sampled)
 decision_den=sum(weight(r)*r['decision_call_cpu_s'] for r in sampled)
 num=sum(weight(r)*r['large_decision_cpu_s'] for r in sampled)
 result=dict(completed_timed_modules=len(summaries),planned_input_modules=len(inputs),
  completed_available_probability_modules=len(sampled),available_probability_input_modules=sum(bool(r['inclusion_probability']) for r in inputs),
  completed_purposeful_modules=[r['module'] for r in summaries if not lookup[r['module']]['inclusion_probability']],
  missing_input_modules=[r['module'] for r in inputs if r['module'] not in {x['module'] for x in summaries}],
  available_case_weighted_large_decision_share_of_all_kernel_cpu=num/den if den and len(sampled)==sum(bool(r['inclusion_probability']) for r in inputs) else None,
  available_case_weighted_large_decision_share_of_decision_kernel_cpu=num/decision_den if decision_den and len(sampled)==sum(bool(r['inclusion_probability']) for r in inputs) else None,
  estimate_ready_for_retained_random_frame=len(sampled)==sum(bool(r['inclusion_probability']) for r in inputs),
  population_claim='conditional available-case ratio only; missing original draws/censored modules and phenotype mismatch prevent unbiased whole-library claim',
  denominator='this capture actual native-call threadCPU, not source compiler clocks or lexical counts',
  source_scope='31 retained no-M artifacts;29original sampled plus2purposeful; not all original42draws')
 (HERE/'declaration-estimate.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(completed_modules=len(summaries),findings=summaries,estimate=result),indent=2))
if __name__=='__main__':main()
