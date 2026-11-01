#!/usr/bin/env python3
"""Fixed log-ridge, grouped validation and calibration; stdlib only."""
import os,csv,json,math,random,collections
from pathlib import Path
os.sched_setaffinity(0,{8})
OUT=Path('/workspaces/.agent-state/gpu-smt-captures/cost-prediction-20261101-v2')
SEED=20261101
def quantile(xs,p):
 if not xs:return None
 v=sorted(xs);u=(len(v)-1)*p;i=int(u);return v[i]*(1-u+i)+v[min(i+1,len(v)-1)]*(u-i)
def inv(A):
 n=len(A);a=[row[:]+[float(i==j)for j in range(n)]for i,row in enumerate(A)]
 for k in range(n):
  pivot=max(range(k,n),key=lambda i:abs(a[i][k]))
  a[k],a[pivot]=a[pivot],a[k]
  if abs(a[k][k])<1e-12:raise ArithmeticError('singular model')
  z=a[k][k];a[k]=[v/z for v in a[k]]
  for i in range(n):
   if i!=k:
    z=a[i][k]
    if z:a[i]=[u-z*v for u,v in zip(a[i],a[k])]
 return [r[n:]for r in a]
def dot(a,b):return sum(u*v for u,v in zip(a,b))
def fit(X,y,ids):
 p=len(X[0]);A=[[0.0]*p for _ in range(p)];b=[0.0]*p
 for k in ids:
  x=X[k];v=y[k]
  for i in range(p):
   b[i]+=x[i]*v
   for j in range(i+1):A[i][j]+=x[i]*x[j]
 for i in range(p):
  for j in range(i):A[j][i]=A[i][j]
  if i:A[i][i]+=1.0
 I=inv(A);return [dot(row,b)for row in I],I
def safeexp(z):return math.exp(min(700,max(-700,z)))
def feats(r,name):
 L=lambda k:math.log1p(float(r[k]))
 x=[1.]
 if name=='constant':return x
 x += [L('source_bytes')]
 if name=='bytes':return x
 x += [L(k)for k in ['direct_imports','transitive_files','closure_source_bytes','import_depth']]
 if name=='imports':return x
 x += [L(k)for k in ['source_declarations','max_numeral_digits','max_range_literal']]
 x += [float(r[k])for k in ['goal_eq_fraction','goal_quant_fraction','goal_arith_fraction','goal_logic_fraction']]
 if name=='regime':
  z=float(r['regime']);x += [z,L('kernel_density_kib'),z*L('source_bytes'),z*L('source_declarations')]
 return x
def folds(rows,grouped):
 groups=collections.defaultdict(list)
 for i,r in enumerate(rows):groups[r['project']if grouped else r['module']].append(i)
 names=list(groups);rng=random.Random(SEED);rng.shuffle(names);names.sort(key=lambda k:-len(groups[k]))
 result=[[]for _ in range(5)]
 for name in names:
  j=min(range(5),key=lambda j:len(result[j]));result[j]+=groups[name]
 return [sorted(v)for v in result if v]
def errors(rows,pred):
 out=[]
 for r,p in zip(rows,pred):
  t=float(r['_actual'])
  out.append(dict(module=r['module'],project=r['project'],regime=r['regime'],actual=t,pred=p,
   ape=abs(p-t)/t,factor=max(p/t,t/p),log_abs=abs(math.log(p/t))))
 return out
def metric(vals):
 return dict(n=len(vals),median_ape=quantile([v['ape']for v in vals],.5),
  p90_ape=quantile([v['ape']for v in vals],.9),
  median_factor=quantile([v['factor']for v in vals],.5),
  p90_factor=quantile([v['factor']for v in vals],.9))
def bootstrap(vals,reps):
 groups=collections.defaultdict(list)
 for v in vals:groups[v['project']].append(v)
 names=sorted(groups)
 if len(names)<2:return dict(projects=len(names),median_ci_low=None,median_ci_high=None,p90_ci_low=None,p90_ci_high=None,bootstrap_replicates=0)
 rng=random.Random(SEED);med=[];p90=[]
 for _ in range(reps):
  sample=[v for k in rng.choices(names,k=len(names))for v in groups[k]]
  a=[v['ape']for v in sample];med.append(quantile(a,.5));p90.append(quantile(a,.9))
 return dict(projects=len(names),median_ci_low=quantile(med,.025),median_ci_high=quantile(med,.975),
  p90_ci_low=quantile(p90,.025),p90_ci_high=quantile(p90,.975),bootstrap_replicates=reps)
def writecsv(path,rows):
 if not rows:return
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def main():
 data=list(csv.DictReader((OUT/'features-and-costs.csv').open()))
 data=[r for r in data if r['unresolved_imports']=='0']
 cohorts=[
 ('primary31_cpu',[dict(r,_actual=r['compiler_cpu_s'])for r in data if r['primary_completed']=='True']),
 ('ai_measured_cpu',[dict(r,_actual=r['compiler_cpu_s'])for r in data if r['ai_module']=='True'and r['compiler_cpu_s']]),
 ('all_measured_cpu',[dict(r,_actual=r['compiler_cpu_s'])for r in data if r['compiler_cpu_s']]),
 ('kernel_component_wall',[dict(r,_actual=r['kernel_replay_wall_s'])for r in data if r['kernel_replay_wall_s']]),
 ]
 summaries=[];predictions=[];interval_rows=[];validation=[]
 for cohort,rows in cohorts:
  rows=[r for r in rows if float(r['_actual'])>0]
  y=[math.log(float(r['_actual']))for r in rows];n=len(rows);allids=list(range(n))
  print('cohort',cohort,n,flush=True)
  for model in ['constant','bytes','imports','static','regime']:
   X=[feats(r,model)for r in rows];beta,I=fit(X,y,allids)
   loo=[]
   for i,x in enumerate(X):
    fitted=dot(x,beta);h=dot(x,[dot(row,x)for row in I])
    if 1-h<1e-8:
     b,_=fit(X,y,[j for j in allids if j!=i]);loo.append(safeexp(dot(x,b)))
    else:loo.append(safeexp(y[i]-(y[i]-fitted)/(1-h)))
   # Check exact PRESS against independently refitted real rows, no label tuning.
   worst=0
   for i in sorted({0,n//2,n-1}):
    b,_=fit(X,y,[j for j in allids if j!=i]);actual=safeexp(dot(X[i],b))
    worst=max(worst,abs(actual-loo[i])/max(actual,1e-300))
   assert worst<1e-5,(cohort,model,worst)
   validation.append(dict(cohort=cohort,model=model,PRESS_max_relative_difference=worst))
   schemes=[('loo_module',loo)]
   for grouped in [False,True]:
    fs=folds(rows,grouped);p=[None]*n
    for test in fs:
     ts=set(test);train=[i for i in allids if i not in ts];b,_=fit(X,y,train)
     for i in test:p[i]=safeexp(dot(X[i],b))
    schemes.append(('project_5fold'if grouped else'5fold',p))
   # Extra project leave-one-out for the small AI cohorts only.
   if n<=300:
    p=[None]*n
    for group in sorted({r['project']for r in rows}):
     test=[i for i,r in enumerate(rows)if r['project']==group];ts=set(test)
     train=[i for i in allids if i not in ts]
     if len(train)<2:continue
     b,_=fit(X,y,train)
     for i in test:p[i]=safeexp(dot(X[i],b))
    if all(v is not None for v in p):schemes.append(('leave_project_out',p))
   for scheme,p in schemes:
    vals=errors(rows,p)
    for domain in ['all','ordinary_proxy','certificate_proxy']:
     subset=[v for v in vals if domain=='all'or(v['regime']=='1')==(domain=='certificate_proxy')]
     if not subset:continue
     summaries.append(dict(cohort=cohort,model=model,validation=scheme,domain=domain,
      **metric(subset),**bootstrap(subset,500 if n<=300 else 200),
      ci_scope='project-block resampling of fixed OOF errors; not training/corpus/per-instance uncertainty'))
    if cohort in ['primary31_cpu','ai_measured_cpu']or model=='regime':
     for v in vals:predictions.append(dict(cohort=cohort,model=model,validation=scheme,**v))
   if cohort=='primary31_cpu'and model in ['imports','regime']:
    # Outer group-folds; calibration projects are disjoint from fitted/test projects.
    for fold,test in enumerate(folds(rows,True)):
     ts=set(test);outer=[i for i in allids if i not in ts]
     groups=collections.defaultdict(list)
     for i in outer:groups[rows[i]['project']].append(i)
     names=sorted(groups);random.Random(SEED+fold).shuffle(names)
     cal=[]
     while names and len(cal)<math.ceil(.4*len(outer))and len(names)>2:cal+=groups[names.pop()]
     cs=set(cal);train=[i for i in outer if i not in cs]
     b,_=fit(X,y,train)
     residual=sorted(y[i]-dot(X[i],b)for i in cal)
     rank=math.ceil((len(cal)+1)*.9)
     q=residual[rank-1]if 1<=rank<=len(residual)else float('inf')
     for i in test:
      point=safeexp(dot(X[i],b));upper=max(point,safeexp(dot(X[i],b)+q))if math.isfinite(q)else float('inf')
      interval_rows.append(dict(model=model,fold=fold,module=rows[i]['module'],project=rows[i]['project'],regime=rows[i]['regime'],
       cpu_s=float(rows[i]['_actual']),point=point,upper=upper,covered=float(rows[i]['_actual'])<=upper,
       train_n=len(train),calibration_n=len(cal),test_n=len(test),finite_upper=math.isfinite(upper),
       bound_scope='empirical heldout upper; no exchangeability/per-instance/corpus guarantee'))
  writecsv(OUT/'errors.csv',summaries);writecsv(OUT/'predictions.csv',predictions)
  writecsv(OUT/'intervals.csv',interval_rows);writecsv(OUT/'numeric-validation.csv',validation)
 (OUT/'fit-terminal.json').write_text(json.dumps(dict(status='complete',cohorts=[(k,len(r))for k,r in cohorts],summaries=len(summaries),
  PRESS_refit_checks=len(validation),no_Lean_launched=True,models_and_seeds_fixed_before_fitting=True),indent=2))
 print((OUT/'fit-terminal.json').read_text(),flush=True)
if __name__=='__main__':main()
