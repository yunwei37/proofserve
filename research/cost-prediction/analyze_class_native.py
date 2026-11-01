#!/usr/bin/env python3
"""Reduce a completed native classification policy matrix, preserving all exits."""
import os,csv,json,statistics
from pathlib import Path
os.sched_setaffinity(0,{8})
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/cost-classification-20261101')
def csvwrite(name, rows):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
def events(path):
 rows=[]
 for line in path.read_text().splitlines():
  if line.startswith('{'):
   try:rows.append(json.loads(line))
   except ValueError:pass
 return rows
def main():
 p=ROOT/'native';terminal=json.loads((p/'terminal.json').read_text())
 assert terminal['status']=='complete',terminal
 sums=json.loads((p/'policy-summary.json').read_text())
 rows=[json.loads(s)for s in(p/'native-results.jsonl').read_text().splitlines()]
 assert len(sums)==9 and {r['policy']for r in sums}=={'fifo','type_route','upper_admission'}
 assert len(rows)==terminal['native_calls']
 # Only native reference IDs from the same original artifact path qualify parity.
 prior=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/runs/math-reference-0/stdout')
 expected={e['module']for e in events(prior)if e.get('event')=='accept'}
 assert len(expected)==1330
 for r in rows:
  assert r['native_retired']
  if r['accepted']:
   out=p/f"r{r['repeat']}-{r['policy']}"/r['job']/'stdout'
   actual={e['module']for e in events(out)if e.get('event')=='accept'}
   if r['job']=='math':assert actual==expected
  else:assert r['budget_interruption'],r
 csvwrite('native-classification-batches.csv',[{k:('/'.join(v)if isinstance(v,list)else v)for k,v in x.items()}for x in sums])
 csvwrite('native-classification-calls.csv',[{k:v for k,v in r.items()if k not in ['memory_events','cpu_stat','complete_event','stop_reasons']}for r in rows])
 summary=[]
 for policy in ['fifo','type_route','upper_admission']:
  rs=[r for r in sums if r['policy']==policy]
  assert len(rs)==3 and {r['repeat']for r in rs}=={0,1,2}
  row=dict(policy=policy,native_batches=3,budget_cpu_s=120)
  for key in ['completed','interruptions','discarded_root_cpu_s','total_cpu_s','unused_budget_cpu_s','actual_budget_excess_cpu_s','wall_s']:
   values=[r[key]for r in rs]
   row.update({key+'_mean':statistics.mean(values),key+'_min':min(values),key+'_max':max(values)})
  row['range_scope']='three cyclic-arrival batches, rotated policy order; descriptive range, not population CI'
  summary.append(row)
 csvwrite('native-classification-summary.csv',summary)
 (ROOT/'native-audit.json').write_text(json.dumps(dict(
  status='complete_self_review',native_calls=len(rows),policy_cells=len(sums),
  root_accepts=sum(r['accepted']for r in rows),
  operational_interruptions=sum(r['budget_interruption']for r in rows),
  complete_math_ID_set_matches_native_reference=True,
  max_charged_peak_bytes=max(r['charged_peak_bytes']for r in rows),
  max_sampled_RSS_bytes=max(r['sampled_tree_peak_bytes']for r in rows),
  all_children_retired=all(r['native_retired']for r in rows),
  semantics='native accepted completed roots only; skipped/interrupted never called false',
  novelty='no new cost-sensitive classification or checker parallelism claim'),indent=2))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
