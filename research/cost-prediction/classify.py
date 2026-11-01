#!/usr/bin/env python3
"""Source-only regime label, independently evaluated on existing kernel traces."""
import os,csv,json,gzip,random,collections,math
from pathlib import Path
os.sched_setaffinity(0,{8})
REPO=Path('/workspaces/repository')
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/cost-classification-20261101')
FEATURES=Path('/workspaces/.agent-state/gpu-smt-captures/cost-prediction-20261101-v2/features-and-costs.csv')
def writecsv(name, rows):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def q(xs,p):
 xs=sorted(xs);x=(len(xs)-1)*p;i=int(x)
 return xs[i]*(1-x+i)+xs[min(i+1,len(xs)-1)]*(x-i)
def main():
 features={r['module']:r for r in csv.DictReader(FEATURES.open())}
 primary={r['module']for r in csv.DictReader((REPO/'research/cost-prediction/primary42-features.csv').open())}
 dynamic=list(csv.DictReader((REPO/'research/chunked-kernel-check/declaration-distribution.csv').open()))
 wpath=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-cost-regimes-20261101-v3/all-module-labels.csv.gz')
 with gzip.open(wpath,'rt') as f:
  wlabels={r['module']:r for r in csv.DictReader(f)if r['module'] in features}
 overlaps=[]
 for m,w in wlabels.items():
  ours=features[m]['regime']=='1';theirs=w['explicit_any']=='True'
  overlaps.append(dict(module=m,primary42=m in primary,our_class=int(ours),W_source_proxy=int(theirs),agree=ours==theirs))
 writecsv('W-agreement.csv',overlaps)
 rows=[]
 for d in dynamic:
  f=features[d['module']]
  total=float(d['all_kernel_call_cpu_s']);compute=float(d['decision_call_cpu_s'])
  rows.append(dict(module=d['module'],project=f['project'],primary42=d['module']in primary,
   source_bytes=int(f['source_bytes']),explicit_markers=int(f['explicit_kernel_sites']),
   density=float(f['kernel_density_kib']),predicted_certificate=f['regime']=='1',
   decision_cpu_s=compute,kernel_call_cpu_s=total,decision_cpu_share=compute/total,
   dynamic_certificate=compute/total>=.5,compiler_cpu_s=float(f['compiler_cpu_s']),
   raw_trace=d['raw'],scope='separate original-kernel replay CPU; not compiler phase fraction'))
 writecsv('classification-rows.csv',rows)
 summaries=[]
 rng=random.Random(20261101)
 for scope in ['primary29','purposeful2','all31']:
  subset=[r for r in rows if scope=='all31' or r['primary42']==(scope=='primary29')]
  for threshold in [.25,.5,.75]:
   vals=[dict(r,truth=r['decision_cpu_share']>=threshold)for r in subset]
   counter=collections.Counter((r['truth'],r['predicted_certificate'])for r in vals)
   errors=[r for r in vals if r['truth']!=r['predicted_certificate']]
   groups=collections.defaultdict(list)
   for r in vals:groups[r['project']].append(r)
   names=sorted(groups);stats=[]
   for _ in range(2000):
    sample=[r for name in rng.choices(names,k=len(names))for r in groups[name]]
    e=[r for r in sample if r['truth']!=r['predicted_certificate']]
    stats.append((1-len(e)/len(sample),sum(r['kernel_call_cpu_s']for r in e)/sum(r['kernel_call_cpu_s']for r in sample)))
   summaries.append(dict(scope=scope,truth_threshold=threshold,n=len(vals),projects=len(names),
    TP=counter[True,True],FN=counter[True,False],FP=counter[False,True],TN=counter[False,False],
    accuracy=1-len(errors)/len(vals),accuracy_ci_low=q([s[0]for s in stats],.025),accuracy_ci_high=q([s[0]for s in stats],.975),
    misclassified_kernel_cpu_s=sum(r['kernel_call_cpu_s']for r in errors),
    all_kernel_cpu_s=sum(r['kernel_call_cpu_s']for r in vals),
    kernel_cpu_weighted_error=sum(r['kernel_call_cpu_s']for r in errors)/sum(r['kernel_call_cpu_s']for r in vals),
    kernel_weighted_error_ci_low=q([s[1]for s in stats],.025),kernel_weighted_error_ci_high=q([s[1]for s in stats],.975),
    exposed_compiler_cpu_s=sum(r['compiler_cpu_s']for r in errors),all_compiler_cpu_s=sum(r['compiler_cpu_s']for r in vals),
    exposed_compiler_cpu_fraction=sum(r['compiler_cpu_s']for r in errors)/sum(r['compiler_cpu_s']for r in vals),
    CI='2000 project-block resamples of observed panel; not full-corpus or training uncertainty',
    cost_scope='CPU on mislabeled modules; not extra CPU caused by selecting a checker'))
 writecsv('classification-summary.csv',summaries)
 (ROOT/'classification-terminal.json').write_text(json.dumps(dict(status='complete',native_launched=False,
  W_overlaps=len(overlaps),W_disagreements=sum(not r['agree']for r in overlaps),
  primary42_W_overlap=sum(r['primary42']for r in overlaps),dynamic_panel=len(rows),
  primary_dynamic=sum(r['primary42']for r in rows),primary_unobserved=42-sum(r['primary42']for r in rows),
  independent_truth='decision-shaped helper share >=.5 within measured original-kernel replay',
  classifier='preexisting fixed source explicit-marker density >0; no fitting',
  W_agreement_scope='same proxy definition/scanner lineage, not independent truth'),indent=2))
 print((ROOT/'classification-terminal.json').read_text())
if __name__=='__main__':main()
