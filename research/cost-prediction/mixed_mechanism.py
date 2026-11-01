#!/usr/bin/env python3
"""Trace-driven checker selection; uses actual complete costs, not runtime forecasts."""
import os,csv,json,random,collections,statistics,argparse,subprocess,io
from pathlib import Path
os.sched_setaffinity(0,{8})
REPO=Path('/workspaces/repository')
BASE=Path('/workspaces/.agent-state/gpu-smt-captures')
OUT=BASE/'cost-mechanism-mixed-20261101-v2'
INPUT_REVISION='c63757f'
POLICIES=['all_build','all_stream','classified','classified_upper','all_stream_upper']
def writecsv(path, rows):
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
def freeze_costs():
 b=BASE/'decoupled-check-20261031'
 plan=json.loads((b/'cohort-plan.json').read_text())
 builds=[json.loads(s)for s in(b/'measured.jsonl').read_text().splitlines()]
 builds=[r for r in builds if r['operation']=='build']
 full=list(csv.DictReader(io.StringIO(subprocess.check_output(['git','show',INPUT_REVISION+':research/parallel-stream-check/full-cells.csv'],cwd=REPO,text=True))))
 math=list(csv.DictReader(io.StringIO(subprocess.check_output(['git','show',INPUT_REVISION+':research/parallel-stream-check/v14-math-cells.csv'],cwd=REPO,text=True))))
 feat={r['module']:r for r in csv.DictReader((BASE/'cost-prediction-20261101-v2/features-and-costs.csv').open())}
 costs=[]
 for tag,cohort in [('math','math'),('compute','compute-grid')]:
  spec=plan['cases'][cohort];mods=set(spec['modules'])
  rows=[r for r in builds if r['module']in mods]
  assert len(rows)==len(mods) and len({r['module']for r in rows})==len(mods)
  assert all(r['returncode']==0 and all(r['outputs'].values()) and not r['sorry_warning']for r in rows)
  # Qualify raw native argv; never borrow a wall sum for CPU.
  for r in rows:
   command=json.loads((b/(r['key']+'.command.json')).read_text())
   args=command.get('args',command.get('argv',[]))
   assert args and not any(str(a).startswith('-M')for a in args)
  expected=int(feat[spec['root']]['explicit_kernel_sites'])>0
  assert expected==(tag=='compute')
  costs.append(dict(kind=tag,module=spec['root'],operation='build',repeat='single',
   cpu_s=sum(r['user_s']+r['system_s']for r in rows),wall_s=sum(r['wall_s']for r in rows),
   peak_rss_kib=max(r['peak_rss_kib']for r in rows),nodes=len(mods),
   source=str(b/'measured.jsonl'),scope='sum of actual per-module compiler invocations; not parallel Lake makespan'))
  if tag=='math':
   for op,variant in [('stream','reference'),('parallel','parallel4')]:
    rs=[r for r in math if r['variant']==variant]
    assert len(rs)==3
    for row in rs:
     assert row['returncode']=='0' and row['accepted_set_equal']=='True'
     costs.append(dict(kind=tag,module=spec['root'],operation=op,repeat=row['repeat'],
      cpu_s=float(row['cpu_s']),wall_s=float(row['wall_s']),peak_rss_kib=int(row['peak_rss_kib']),
      nodes=len(mods),source='research/parallel-stream-check/v14-math-cells.csv:'+row['key'],
      scope='one native complete artifact closure, empty checked environment, OS cache warm'))
  else:
   for op,variant in [('stream','reference'),('parallel','parallel')]:
    row=next(r for r in full if r['cohort']=='grid'and r['variant']==variant)
    assert row['complete']=='True' and row['returncode']=='0'and row['accepted_set_equal_to_full_curve']=='True'
    costs.append(dict(kind=tag,module=spec['root'],operation=op,repeat='single',
     cpu_s=float(row['whole_cpu_s']),wall_s=float(row['whole_wall_s']),
     peak_rss_kib=float(row['wait4_peak_rss_mib'])*1024,nodes=len(mods),
     source='research/parallel-stream-check/full-cells.csv:'+row['key'],
     scope='one native complete artifact closure; interrupted pair repair disclosed upstream'))
 assert max(r['peak_rss_kib']for r in costs)<12*1024**2
 return costs
def main():
 global OUT
 parser=argparse.ArgumentParser()
 parser.add_argument('--out',type=Path,default=OUT)
 OUT=parser.parse_args().out
 OUT.mkdir(exist_ok=False)
 costs=freeze_costs();writecsv(OUT/'operation-costs.csv',costs)
 upper={}
 for predicted in ['math','compute']:
  for operation in ['stream','parallel']:
   upper[predicted,operation]=max(r['cpu_s']for r in costs if r['kind']==predicted and r['operation']==operation)
 summaries=[];requests=[];route_counts=collections.Counter()
 with (OUT/'requests.jsonl').open('w')as trace:
  for mix in [0,.1,.5,.9,1]:
   for repeat in range(3):
    rng=random.Random(20261101+repeat)
    kinds=['compute']*round(20*mix)+['math']*(20-round(20*mix));rng.shuffle(kinds)
    flip_order=list(range(20));random.Random(90261101+repeat).shuffle(flip_order)
    for noise in [0,.1,.2]:
     flips=set(flip_order[:round(20*noise)])
     for request_budget in [100,800,10000]:
      for total in [1000,5000,20000]:
       for policy in POLICIES:
        left=float(total);passed=attempted=interrupted=deferred=unattempted=0
        wasted=wall_complete=0.;wrong_compute=wrong_math=0
        for index,kind in enumerate(kinds):
         predicted=('math'if kind=='compute'else'compute')if index in flips else kind
         wrong_compute+=kind=='compute' and predicted=='math'
         wrong_math+=kind=='math' and predicted=='compute'
         mode='build'if policy=='all_build'else'stream'if policy in ['all_stream','all_stream_upper']or predicted=='math'else'parallel'
         rs=[r for r in costs if r['kind']==kind and r['operation']==mode]
         cost=next((r for r in rs if r['repeat']==str(repeat)),rs[0])
         allowed=min(left,request_budget);consumed=0.
         if left<=1e-9:
          status='unattempted';unattempted+=1
         elif policy in ['classified_upper','all_stream_upper']and upper[predicted,mode]>allowed:
          status='deferred';deferred+=1
         else:
          attempted+=1;route_counts[policy,kind,mode]+=1
          if cost['cpu_s']<=allowed+1e-9:
           status='passed';passed+=1;consumed=cost['cpu_s'];wall_complete+=cost['wall_s']
          else:
           status='CPU_interruption';interrupted+=1;consumed=allowed;wasted+=consumed
          left=max(0.,left-consumed)
         trace.write(json.dumps(dict(mix=mix,repeat=repeat,noise=noise,request_budget=request_budget,total_budget=total,
          policy=policy,request_index=index,kind=kind,predicted_kind=predicted,flipped=index in flips,mode=mode,
          actual_recorded_cost_cpu_s=cost['cpu_s'],allowed_cpu_s=allowed,consumed_cpu_s=consumed,status=status))+'\n')
        assert passed+interrupted+deferred+unattempted==20
        assert total-left<=total+1e-8
        summaries.append(dict(certificate_fraction=mix,repeat=repeat,noise=noise,request_cpu_budget=request_budget,
         total_cpu_budget=total,policy=policy,passed=passed,completed=passed,attempted=attempted,
         pass_decision_fraction=passed/20,completed_per_allocated_CPU_hour=passed*3600/total,pass_fraction_among_attempts=passed/attempted if attempted else '',
         interruptions=interrupted,discarded_cpu_s=wasted,CPU_spent_s=total-left,unused_cpu_s=left,
         deferred=deferred,unattempted=unattempted,false_negative_compute=wrong_compute,false_positive_math=wrong_math,
         completed_service_wall_sum=wall_complete,batch_wall_s=wall_complete if interrupted==0 else '',
         scope='trace-driven mixed requests; all unbounded reference inputs valid; source/artifacts provided; not native batch throughput'))
 writecsv(OUT/'batches.csv',summaries)
 groups=collections.defaultdict(list)
 for row in summaries:
  key=tuple(row[k]for k in ['certificate_fraction','noise','request_cpu_budget','total_cpu_budget','policy'])
  groups[key].append(row)
 aggregate=[]
 for key,rs in groups.items():
  assert len(rs)==3
  row=dict(zip(['certificate_fraction','noise','request_cpu_budget','total_cpu_budget','policy'],key))
  row['batches']=3
  for k in ['completed','pass_decision_fraction','completed_per_allocated_CPU_hour','interruptions','discarded_cpu_s','unused_cpu_s','CPU_spent_s','deferred']:
   values=[r[k]for r in rs];row.update({k+'_mean':statistics.mean(values),k+'_min':min(values),k+'_max':max(values)})
  row['interval_scope']='observed3seed range; only Mathlib checker has3native cost repeats; no population CI'
  aggregate.append(row)
 writecsv(OUT/'summary.csv',aggregate)
 writecsv(OUT/'route-engagement.csv',[dict(policy=p,actual_kind=k,selected_mode=m,dispatched_requests=n)for(p,k,m),n in route_counts.items()])
 # Paired noise changes, not a manufactured accuracy-to-utility conversion.
 paired=[]
 index={(r['certificate_fraction'],r['repeat'],r['request_cpu_budget'],r['total_cpu_budget'],r['policy'],r['noise']):r for r in summaries}
 for r in summaries:
  if r['noise']==0:continue
  base=index[r['certificate_fraction'],r['repeat'],r['request_cpu_budget'],r['total_cpu_budget'],r['policy'],0]
  paired.append({k:r[k]for k in ['certificate_fraction','repeat','request_cpu_budget','total_cpu_budget','policy','noise']}|
   dict(delta_completed=r['completed']-base['completed'],delta_interruptions=r['interruptions']-base['interruptions'],
        delta_discarded_cpu_s=r['discarded_cpu_s']-base['discarded_cpu_s']))
 writecsv(OUT/'noise-paired.csv',paired)
 (OUT/'terminal.json').write_text(json.dumps(dict(status='complete',batch_replays=len(summaries),summary_rows=len(aggregate),
  request_replays=len(summaries)*20,cost_table_rows=len(costs),checker_native_cells=8,build_aggregate_cells=2,
  new_native_runs=0,regression_fitted=False,all_unbounded_inputs_previously_accepted=True,
  scope='two-template mechanism feasibility; no general workload/native-throughput/novelty claim'),indent=2))
 print((OUT/'terminal.json').read_text())
if __name__=='__main__':main()
