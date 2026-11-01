#!/usr/bin/env python3
"""Counterfactual CPU-work replay. No claim of native/server throughput."""
import os,csv,json,random,math,statistics
from pathlib import Path
os.sched_setaffinity(0,{8})
OUT=Path('/workspaces/.agent-state/gpu-smt-captures/cost-prediction-20261101-v2')
def q(xs,p):
 xs=sorted(xs);u=(len(xs)-1)*p;i=int(u);return xs[i]*(1-u+i)+xs[min(i+1,len(xs)-1)]*(u-i)
def main():
 intervals=list(csv.DictReader((OUT/'intervals.csv').open()))
 traces=[];forecasts={}
 for model in ['imports','regime']:
  rows=[{**r,'cost':float(r['cpu_s']),'point':float(r['point']),'upper':float(r['upper'])}for r in intervals if r['model']==model]
  assert len(rows)==31 and len({r['module']for r in rows})==31
  forecasts[model]=rows;total=sum(r['cost']for r in rows)
  for fraction in [.1,.25,.5,.75,1.0]:
   budget=total*fraction
   for repeat in range(100):
    order=rows[:];random.Random(20261101+repeat).shuffle(order)
    for policy in ['fifo','predicted_cost','upper_admission','oracle']:
     work=order if policy=='fifo'else sorted(order,key=lambda r:r['cost']if policy=='oracle'else r['point'])
     remaining=budget;completed=0;interrupted=0;deferred=0;misses=0
     for row in work:
      if policy=='upper_admission'and row['upper']>remaining:
       deferred+=1;continue
      if row['cost']<=remaining+1e-9:
       remaining-=row['cost'];completed+=1;misses+=row['cost']>row['upper']
      else:
       interrupted+=1;remaining=0;break
     traces.append(dict(model=model,policy=policy,budget_fraction=fraction,repeat=repeat,cpu_budget=budget,
      completed=completed,interrupted=interrupted,deferred=deferred,cpu_spent=budget-remaining,
      observed_interval_misses=misses,completed_per_allocated_cpu_hour=completed/budget*3600,
      pass_at_1_completed_cost_subset=completed/len(rows),
      pass_at_k_greater_than_1='not identified: one proof per distinct library module'))
 summaries=[]
 for model in ['imports','regime']:
  for frac in [.1,.25,.5,.75,1.0]:
   for policy in ['fifo','predicted_cost','upper_admission','oracle']:
    sub=[r for r in traces if r['model']==model and r['budget_fraction']==frac and r['policy']==policy]
    summaries.append(dict(model=model,policy=policy,budget_fraction=frac,replays=len(sub),
     cpu_budget=sub[0]['cpu_budget'],mean_completed=statistics.mean(r['completed']for r in sub),
     arrival_p025_completed=q([r['completed']for r in sub],.025),arrival_p975_completed=q([r['completed']for r in sub],.975),
     mean_interruptions=statistics.mean(r['interrupted']for r in sub),mean_deferred=statistics.mean(r['deferred']for r in sub),
     mean_cpu_spent=statistics.mean(r['cpu_spent']for r in sub),
     mean_completed_per_allocated_cpu_hour=statistics.mean(r['completed_per_allocated_cpu_hour']for r in sub),
     pass_at_1_subset=statistics.mean(r['pass_at_1_completed_cost_subset']for r in sub),
     scope='offline observed-success subset; omitted11 costs and real multi-candidate pass@k unidentifiable'))
 for name,rs in [('simulation.csv',summaries),('simulation-replays.csv',traces)]:
  with(OUT/name).open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=rs[0]);w.writeheader();w.writerows(rs)
 # Native prototype has no old measured labels in its policy input.
 features={r['module']:r for r in csv.DictReader((OUT/'features-and-costs.csv').open())}
 plan_order=[r['module']for r in csv.DictReader(Path('/workspaces/repository/workloads/openai-math/build-planning-4eaee875/phaseA-targets.csv').open())if r['role']=='probability_sample']
 rmap={r['module']:r for r in forecasts['regime']}
 native=[dict(module=m,source=features[m]['source_path'],point=rmap[m]['point'],upper=rmap[m]['upper'],
  project=rmap[m]['project'],fold=int(rmap[m]['fold']))for m in plan_order if m in rmap]
 assert len(native)==31
 (OUT/'native-policy-plan.json').write_text(json.dumps(dict(candidates=native,cpu_budget_s=60,policies=['fifo','predicted_cost','upper_admission'],
  scope='OOF grouped-calibration forecasts only; old true costs not supplied to native policy; accepted IDs still observed natively'),indent=2))
 (OUT/'simulation-terminal.json').write_text(json.dumps(dict(status='complete',trace_replays=len(traces),summary_rows=len(summaries),
  scope='counterfactual CPU-work replay, not an actual run; separate native prototype plan B60'),indent=2))
if __name__=='__main__':main()
