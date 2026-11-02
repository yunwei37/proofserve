#!/usr/bin/env python3
"""Describe completed source draws; keep population assumptions separate."""
import argparse
import collections
import csv
import json
import math
import os
from pathlib import Path
import statistics

os.sched_setaffinity(0,set(range(8,16)))
ROOT=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--frame",type=Path,default=ROOT/"workloads/openai-math/noM-hard19-source32/sample-costs.csv")
ap.add_argument("--out",type=Path,default=Path(__file__).with_suffix(""))
a=ap.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
def read(p):return list(csv.DictReader(p.open()))
def write(name,rows):
 with (a.out/name).open("w",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
frame=read(a.frame)
assert len(frame)==42 and len({r["module"]for r in frame})==42
strata={";".join(r[k]for k in ["size_percentile_bin","import_depth_bin","has_decide_kernel"]):int(r["population_modules"])
 for r in read(ROOT/"workloads/openai-math/build-planning-4eaee875/strata.csv")}
members=collections.defaultdict(list)
completed={}
for r in frame:
 members[r["stratum"]].append(r["module"])
 if r["status"]!="completed_cost":continue
 z=json.loads(Path(r["source_file"]).read_text().splitlines()[int(r["source_line"])-1])
 assert z["status"]=="compile_ok" and z["source_exact"] and z["native_retired"] and z["cgroup_retired"]
 assert z["lean_memory_option_MiB"]==0 and z["threads"]==8 and z["pcore_lock"] and not z["profiled"]
 assert z["compilation_outputs"]=="olean_ilean_c" and z["heartbeat_budget"]=="authored_or_native_default"
 completed[r["module"]]=dict(module=r["module"],stratum=r["stratum"],CPU_s=z["user_cpu_s"]+z["system_cpu_s"],
   source_bytes=Path(z["args"][-1]).stat().st_size,source_file=r["source_file"],source_line=r["source_line"])
assert all(len(ms)==2 for ms in members.values())
complete={h for h,ms in members.items() if all(m in completed for m in ms)}
domain=lambda h:"certificate_proxy"if h.endswith(";1")else"ordinary_proxy"
observed=[dict(x,weight=1.,observed=True)for x in completed.values()]
conditional=[dict(x,weight=strata[x["stratum"]]/2,observed=True)for x in completed.values()if x["stratum"]in complete]
groups={
 "selected_completed_draws":observed,
 "complete_strata_HT_distribution":conditional}
costlimits={d:(min(x["CPU_s"]for x in completed.values()if domain(x["stratum"])==d),
 max(x["CPU_s"]for x in completed.values()if domain(x["stratum"])==d))for d in ["ordinary_proxy","certificate_proxy"]}
for which,index in [("missing_class_min_assumption",0),("missing_class_max_assumption",1)]:
 atoms=[]
 for r in frame:
  m,h=r["module"],r["stratum"];known=m in completed
  x=completed[m]if known else dict(module=m,stratum=h,CPU_s=costlimits[domain(h)][index],source_bytes="",source_file="",source_line="")
  atoms.append(dict(x,weight=strata[h]/2,observed=known))
 groups[which]=atoms
def tail(atoms,fraction,key="CPU_s"):
 mass=fraction*sum(x["weight"]for x in atoms)
 cost=0.
 for x in sorted(atoms,key=lambda r:(r[key],r["module"]),reverse=True):
  take=min(mass,x["weight"]);cost+=take*x["CPU_s"];mass-=take
  if mass<=1e-10:break
 return cost/sum(x["weight"]*x["CPU_s"]for x in atoms)
def weighted_quantile(atoms,p):
 threshold=p*sum(x["weight"]for x in atoms);mass=0.
 for x in sorted(atoms,key=lambda r:r["CPU_s"]):
  mass+=x["weight"]
  if mass+1e-10>=threshold:return x["CPU_s"]
 raise AssertionError("quantile")
def r7(vals,p):
 vals=sorted(vals);x=(len(vals)-1)*p;i=math.floor(x);j=math.ceil(x)
 return vals[i]+(vals[j]-vals[i])*(x-i)
summary=[];tailpoints=[];curves=[]
for name,atoms in groups.items():
 mass=sum(x["weight"]for x in atoms);total=sum(x["weight"]*x["CPU_s"]for x in atoms)
 selected=name=="selected_completed_draws";assumed=name.startswith("missing_")
 scope=("unweighted selected completed draws; not a population sample distribution"if selected else
 "hypothetical missing draw costs; NOT observed population or confidence bounds"if assumed else
 "HT empirical distribution conditional on complete strata only; nonlinear tail estimates, no confidence guarantee")
 summary.append(dict(scope=name,cost_atoms=len(atoms),observed_atoms=sum(x["observed"]for x in atoms),represented_module_mass=mass,CPU_s=total,
  median_CPU_s=r7([x["CPU_s"]for x in atoms],.5)if selected else weighted_quantile(atoms,.5),
  P90_CPU_s=r7([x["CPU_s"]for x in atoms],.9)if selected else weighted_quantile(atoms,.9),max_observed_or_assumed_CPU_s=max(x["CPU_s"]for x in atoms),
  quantile_definition="R7 sample interpolation"if selected else"left inverse of weighted empirical CDF",
  interval="not estimated; 2draws/cell and 10missingdraws",interpretation=scope))
 for p in [.01,.05,.1,.2,.5,1.]:
  k=math.ceil(p*len(atoms))if selected else""
  indiv=sorted(atoms,key=lambda r:r["CPU_s"],reverse=True)[:k]if selected else[]
  tailpoints.append(dict(scope=name,top_module_fraction=p,cost_share=tail(atoms,p),
   boundary_rule="fractional boundary atom; linear interpolation, not observed submodule execution",
   actual_integer_top_k=k,actual_integer_fraction=k/len(atoms)if selected else"",
   actual_integer_cost_share=sum(x["CPU_s"]for x in indiv)/total if selected else"",interpretation=scope))
 mass_c=cost_c=0.
 curves.append(dict(scope=name,top_module_fraction=0.,cost_share=0.,atoms_included=0,interpretation=scope))
 for rank,x in enumerate(sorted(atoms,key=lambda r:r["CPU_s"],reverse=True),1):
  mass_c+=x["weight"];cost_c+=x["weight"]*x["CPU_s"]
  curves.append(dict(scope=name,top_module_fraction=mass_c/mass,cost_share=cost_c/total,atoms_included=rank,interpretation=scope))
 assert math.isclose(curves[-1]["top_module_fraction"],1)and math.isclose(curves[-1]["cost_share"],1)
size_rows=[];size_curves=[]
for name in ["selected_completed_draws","complete_strata_HT_distribution"]:
 atoms=groups[name];mass=sum(x["weight"]for x in atoms);cost=sum(x["weight"]*x["CPU_s"]for x in atoms)
 for fraction in [.01,.05,.1,.2,.5,1.]:
  size_rows.append(dict(scope=name,top_source_byte_fraction=fraction,
   native_CPU_share_in_largest_source_files=tail(atoms,fraction,"source_bytes"),
   native_CPU_share_in_most_expensive_files=tail(atoms,fraction),
   scope_note="source bytes and nativeCPU order differ; conditional descriptive association, not predictive policy evidence"))
 mass_c=cost_c=0.
 size_curves.append(dict(scope=name,largest_source_fraction=0.,native_CPU_share=0.))
 for x in sorted(atoms,key=lambda r:(r["source_bytes"],r["module"]),reverse=True):
  mass_c+=x["weight"];cost_c+=x["weight"]*x["CPU_s"]
  size_curves.append(dict(scope=name,largest_source_fraction=mass_c/mass,native_CPU_share=cost_c/cost))
write("source-size-vs-cost.csv",size_rows)
write("source-size-cost-curve.csv",size_curves)
ordered=sorted(completed.values(),key=lambda r:r["CPU_s"],reverse=True)
write("source-draws.csv",[dict(rank=i+1,**x,complete_cell=x["stratum"]in complete,original_weight=strata[x["stratum"]]/2)for i,x in enumerate(ordered)])
write("distribution-summary.csv",summary);write("top-cost-shares.csv",tailpoints);write("concentration-curve.csv",curves)
assert math.isclose(sum(x["CPU_s"]for x in completed.values()),817.179526,rel_tol=1e-12)
assert math.isclose(sum(x["weight"]*x["CPU_s"]for x in conditional)/3600,174.25123012819444,rel_tol=1e-12)
receipt=dict(source_frame=str(a.frame),source_costs=len(completed),original_draws=42,missing_draws=42-len(completed),complete_strata=len(complete),conditional_modules=sum(strata[h]for h in complete),population_modules=sum(strata.values()),original_weights_preserved=True,tail_quantities_are_nonlinear=True,
 unweighted_minimum_integer_module_fraction=1/len(completed),whole_library_tail_concentration_established=False,intervals_established=False,
 construction_CPU_is_not_checked_closure_CPU=True,no_native_run=True,checks="all4curves end1; sums match source32and15-cell estimator")
(a.out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt))
for x in summary:print(json.dumps(x))
for x in tailpoints:
 if x["top_module_fraction"]in [.01,.05,.1]:print(json.dumps(x))
