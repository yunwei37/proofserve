#!/usr/bin/env python3
"""Replay only actual whole-closure checker costs; never impute an unmeasured route."""
import os,csv,json,itertools,collections,statistics
from pathlib import Path
os.sched_setaffinity(0,{8})
REPO=Path('/workspaces/repository')
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/cost-classification-20261101')
def writecsv(name, rows):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def main():
 cells=list(csv.DictReader((REPO/'research/parallel-stream-check/full-cells.csv').open()))
 math=list(csv.DictReader((REPO/'research/parallel-stream-check/v14-math-cells.csv').open()))
 math=[r for r in math if r['variant']=='reference']
 plan=json.loads((ROOT/'native/plan.json').read_text())
 full={r['cohort']+'-'+r['variant']:r for r in cells}
 costs={j['id']:{}for j in plan['jobs']}
 for key in ['barrier','grid']:
  for mode,variant in [('serial','reference'),('parallel4','parallel')]:
   r=full[key+'-'+variant]
   assert r['complete']=='True' and r['accepted_set_equal_to_full_curve']=='True'
   costs[key][mode]=(float(r['whole_cpu_s']),float(r['whole_wall_s']))
 classes={r['id']:r['class']for r in plan['jobs']}
 rows=[]
 for m in math:
  costs['math']['serial']=(float(m['cpu_s']),float(m['wall_s']))
  for budget in [120,600,900,1200]:
   for permutation in itertools.permutations(classes):
    for policy in ['fifo','type_route','upper_admission']:
     rem=float(budget);done=[];cuts=[];deferred=[];wall=0.;waste=0.;used=0.
     for key in permutation:
      route='serial'if policy=='fifo'or classes[key]=='ordinary'else'parallel4'
      if policy=='upper_admission'and plan['type_upper_cpu_s'][classes[key]]>rem:
       deferred.append(key);continue
      cpu,w=costs[key][route]
      if cpu<=rem:
       done.append(key);used+=cpu;rem-=cpu;wall+=w
      else:
       cuts.append(key);waste+=rem;used+=rem;rem=0
       # Prefix wall cannot be linearly inferred from completed whole-process wall.
       wall=None;break
     rows.append(dict(budget_cpu_s=budget,math_repeat=m['repeat'],arrival='/'.join(permutation),
      policy=policy,completed=len(done),completed_ids='/'.join(done),interruptions=len(cuts),
      interrupted_ids='/'.join(cuts),admission_deferred=len(deferred),cpu_spent=used,
      discarded_root_cpu_s=waste,unused_budget_cpu_s=rem,
      wall_if_all_started_roots_completed_s=wall,
      complete_closure_routes_only=True,
      scope='counterfactual;18 arrival/math-repeat cases; single computational pair reused, not18 native repetitions'))
 writecsv('routing-replay.csv',rows)
 summary=[]
 for budget in [120,600,900,1200]:
  for policy in ['fifo','type_route','upper_admission']:
   rs=[r for r in rows if r['budget_cpu_s']==budget and r['policy']==policy]
   summary.append(dict(budget_cpu_s=budget,policy=policy,replay_cases=len(rs),
    completed_mean=statistics.mean(r['completed']for r in rs),
    completed_min=min(r['completed']for r in rs),completed_max=max(r['completed']for r in rs),
    interruptions_mean=statistics.mean(r['interruptions']for r in rs),
    discarded_root_cpu_mean=statistics.mean(r['discarded_root_cpu_s']for r in rs),
    unused_cpu_mean=statistics.mean(r['unused_budget_cpu_s']for r in rs),
    interval_scope='enumerated arrival/repeated-Mathlib range, not native repeated-computational uncertainty'))
 writecsv('routing-replay-summary.csv',summary)
if __name__=='__main__':main()
