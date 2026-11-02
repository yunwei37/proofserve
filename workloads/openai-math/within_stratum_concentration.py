#!/usr/bin/env python3
"""Within-stratum tail plug-ins and cost-cover counts, with resolution limits."""
import argparse
import collections
import csv
import json
import math
import os
from pathlib import Path

os.sched_setaffinity(0,set(range(8,16)))
ROOT=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--frame",type=Path,default=ROOT/"workloads/openai-math/noM-hard19-source32/sample-costs.csv")
ap.add_argument("--out",type=Path,default=Path(__file__).with_suffix(""))
a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
def read(p):return list(csv.DictReader(p.open()))
def write(name,rows):
 with(a.out/name).open("w",newline="")as f:
  w=csv.DictWriter(f,list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
frame=read(a.frame)
strata={";".join(x[k]for k in ["size_percentile_bin","import_depth_bin","has_decide_kernel"]):int(x["population_modules"])
 for x in read(ROOT/"workloads/openai-math/build-planning-4eaee875/strata.csv")}
members=collections.defaultdict(list);observed={}
for x in frame:
 members[x["stratum"]].append(x["module"])
 if x["status"]=="completed_cost":
  z=json.loads(Path(x["source_file"]).read_text().splitlines()[int(x["source_line"])-1])
  assert z["status"]=="compile_ok" and z["source_exact"] and z["lean_memory_option_MiB"]==0
  assert z["pcore_lock"] and z["native_retired"] and z["cgroup_retired"]
  observed[x["module"]]=z["user_cpu_s"]+z["system_cpu_s"]
assert len(frame)==42 and all(len(v)==2 for v in members.values())
complete={h for h,ms in members.items()if all(m in observed for m in ms)}
def tail(atoms,p):
 mass=p*sum(n for y,n in atoms);part=0.
 for y,n in sorted(atoms,reverse=True):
  take=min(n,mass);part+=y*take;mass-=take
  if mass<=1e-10:break
 return part/sum(y*n for y,n in atoms)
def count_for_cost(atoms,p=.5):
 remaining=p*sum(y*n for y,n in atoms);mass=0.
 for y,n in sorted(atoms,reverse=True):
  take=min(n,remaining/y);mass+=take;remaining-=y*take
  if remaining<=1e-7:return mass
 raise AssertionError("uncoveredcost")
rows=[];parts=[]
for h,N in strata.items():
 values=[observed[m]for m in members[h]if m in observed];done=len(values)==2
 row=dict(stratum=h,population_modules=N,planned_draws=2,completed_draws=len(values),complete=done,census_if_complete=N==2,
  requested_within_top_fraction=.1,minimum_observed_integer_fraction=.5 if done else"",
  original_inverse_probability_weight=N/2,smaller_CPU_s=min(values)if done else"",larger_CPU_s=max(values)if done else"",
  fractional_top10_cost_share=tail([(y,1)for y in values],.1)if done else"",
  actual_larger_observed_half_share=max(values)/sum(values)if done else"",
  estimated_stratum_CPU_h=N*sum(values)/2/3600 if done else"",
  cost_of_stratum_top10_equivalent_modules_h=N*.1*max(values)/3600 if done else"",
  scope="n2 empirical interpolation; true populationtail unknown except census"if done else"incomplete; no tail imputation")
 rows.append(row)
 if done:parts.append(row)
write("stratum-tail.csv",rows)
T=sum(x["estimated_stratum_CPU_h"]for x in parts)
cpu_weighted=sum(x["cost_of_stratum_top10_equivalent_modules_h"]for x in parts)/T
N=sum(x["population_modules"]for x in parts)
module_weighted=sum(x["population_modules"]*x["fractional_top10_cost_share"]for x in parts)/N
assert math.isclose(cpu_weighted,sum(x["estimated_stratum_CPU_h"]*x["fractional_top10_cost_share"]for x in parts)/T,rel_tol=1e-12)
summary=[dict(scope="complete_strata_only",complete_strata=len(parts),population_modules=N,total_estimated_CPU_h=T,
 union_of_each_stratum_fraction=.1,selected_equivalent_module_mass=.1*N,
 union_selected_estimated_CPU_h=sum(x["cost_of_stratum_top10_equivalent_modules_h"]for x in parts),
 CPU_weighted_within10_cost_share=cpu_weighted,module_weighted_average_within10_share=module_weighted,
 true_population_tail_established=False,confidence_interval="unknown",scope_note="weights correct known sampling proportions; n2 resolution and missingstrata remain")]
write("within-tail-summary.csv",summary)
atoms=[(y,1)for y in observed.values()]
weighted=[(observed[m],strata[h]/2)for h in complete for m in members[h]]
class_min=min(y for m,y in observed.items()if next(x["stratum"]for x in frame if x["module"]==m).endswith(";0"))
class_max=max(y for m,y in observed.items()if next(x["stratum"]for x in frame if x["module"]==m).endswith(";0"))
groups={"actual_selected32":atoms,"conditional_complete_strata_HT":weighted}
for label,value in [("missing_ordinary_min_assumption",class_min),("missing_ordinary_max_assumption",class_max)]:
 assert all(x["stratum"].endswith(";0")for x in frame if x["module"]not in observed)
 groups[label]=[(observed.get(x["module"],value),strata[x["stratum"]]/2)for x in frame]
cover=[]
for name,vs in groups.items():
 fractional=count_for_cost(vs);integer=math.ceil(fractional)
 cover.append(dict(scope=name,represented_modules=sum(n for y,n in vs),source_CPU_h=sum(y*n for y,n in vs)/3600,
  target_cost_share=.5,fractional_modules_for_half_cost=fractional,rounded_up_module_count=integer,
  fractional_count_fraction=fractional/sum(n for y,n in vs),rounded_count_fraction=integer/sum(n for y,n in vs),actual_named_modules_available=name=="actual_selected32",
  interpretation="observed minimal integer count in selected32"if name=="actual_selected32"else"model-equivalent modules, not known actual identities or a full-library measurement"))
write("modules-for-half-cost.csv",cover)
ranked=sorted(observed,key=lambda m:observed[m],reverse=True)
k=math.ceil(count_for_cost(atoms))
named=[dict(rank=i+1,module=m,CPU_s=observed[m],cumulative_CPU_s=sum(observed[z]for z in ranked[:i+1]),scope="actual selected32 only")for i,m in enumerate(ranked[:k])]
write("actual-half-cost-modules.csv",named)
# Constructed identifiability examples, never benchmark data.
controls=[]
for name,pair in [("equal_pair",[1.,1.]),("extreme_pair",[1.,1e12])]:
 controls.append(dict(case=name,observed_draws=2,population_modules=2,sample_interpolated_top10_share=tail([(y,1)for y in pair],.1),
  complete_population_top10_share=tail([(y,1)for y in pair],.1),scope="analytic fractional-curve control; not native measurements"))
pair=[1.,10.]
for label,pop in [("same_pair_near_uniform",[1.,10.]+[5.5]*998),("same_pair_hidden_hotspot",[1.,10.,1e12]+[1.]*997)]:
 controls.append(dict(case=label,observed_draws=2,population_modules=1000,sample_interpolated_top10_share=tail([(y,1)for y in pair],.1),
  complete_population_top10_share=tail([(y,1)for y in pop],.1),scope="constructed compatible completion; NOT empirical data or realistic cost prediction"))
assert math.isclose(controls[0]["sample_interpolated_top10_share"],.1)
assert .199999<controls[1]["sample_interpolated_top10_share"]<=.2
assert controls[2]["complete_population_top10_share"]<.11 and controls[3]["complete_population_top10_share"]>.99
write("resolution-and-identifiability-controls.csv",controls)
# Complete measured AI subtree: no within-project sampling/response weights.
labels=Path(json.loads((ROOT/"workloads/openai-math/cost-regimes-noM/receipt.json").read_text())["all_module_labels_gzip"])
import gzip
W={x["module"]:x for x in csv.DictReader(gzip.open(labels,"rt"))}
O=ROOT/"research/decoupled-check"
census=[]
for row in read(O/"falconer-source-costs.csv"):
 m=row["module"]
 if m not in W:continue
 assert m.startswith("OAI.MeasureTheory.Falconer.")
 cell=json.loads((Path(row["source_cell_root"])/(row["source_cell"]+".result.json")).read_text())
 assert cell["returncode"]==0 and cell["measured"] and cell["affinity"]==list(range(8))
 assert not any(x.startswith("-M")for x in cell["args"])
 y=cell["user_s"]+cell["system_s"]
 assert math.isclose(y,float(row["source_user_s"])+float(row["source_system_s"]),rel_tol=1e-12)
 census.append(dict(module=m,stratum=W[m]["stratum"],CPU_s=y,source_cell_root=row["source_cell_root"],source_cell=row["source_cell"]))
assert len(census)==2461 and len({x["module"]for x in census})==2461
groups=collections.defaultdict(list)
for row in census:groups[row["stratum"]].append(row)
census_strata=[];census_total=sum(x["CPU_s"]for x in census)
for h,rs in sorted(groups.items()):
 ys=[x["CPU_s"]for x in rs];n=len(ys);k=math.ceil(.1*n);cost=sum(ys)
 census_strata.append(dict(stratum=h,actual_project_modules=n,source_CPU_s=cost,
  fractional_within10_cost_share=tail([(y,1)for y in ys],.1),integer_top_k=k,integer_top_k_fraction=k/n,
  integer_top_k_cost_share=sum(sorted(ys,reverse=True)[:k])/cost,
  weight_scope="actual project stratum size; not global source-frame weights",census=True))
write("falconer-census-strata.csv",census_strata)
census_tails=[]
for fraction in [.01,.05,.1]:
 vs=[(x["CPU_s"],1)for x in census];k=math.ceil(fraction*len(vs))
 census_tails.append(dict(scope="complete measured Falconer AI subtree",actual_modules=len(census),
  requested_top_fraction=fraction,fractional_cost_share=tail(vs,fraction),
  actual_integer_top_k=k,actual_integer_fraction=k/len(vs),
  actual_integer_cost_share=sum(sorted((x["CPU_s"]for x in census),reverse=True)[:k])/census_total))
write("falconer-census-tails.csv",census_tails)
fractional_census_count=count_for_cost([(x["CPU_s"],1)for x in census]);kc=math.ceil(fractional_census_count)
csorted=sorted(census,key=lambda x:x["CPU_s"],reverse=True)
write("falconer-actual-half-cost-modules.csv",[dict(rank=i+1,**x)for i,x in enumerate(csorted[:kc])])
census_summary=dict(actual_project_modules=len(census),source_CPU_s=census_total,
 strata=len(groups),source_file_population_complete=True,whole_openai_math_population_complete=False,
 union_within10_CPU_share=sum(x["source_CPU_s"]*x["fractional_within10_cost_share"]for x in census_strata)/census_total,
 union_integer_top_counts=sum(x["integer_top_k"]for x in census_strata),
 union_integer_top_CPU_share=sum(x["source_CPU_s"]*x["integer_top_k_cost_share"]for x in census_strata)/census_total,
 actual_modules_for_half_cost=kc,CPU_share_at_that_integer=sum(x["CPU_s"]for x in csorted[:kc])/census_total,
 original_capture_single_observation=True,project_selection_uncertainty="purposeful ordinary project; not random whole-library coverage")
(a.out/"falconer-census-summary.json").write_text(json.dumps(census_summary,indent=2)+"\n")
receipt=dict(source_frame=str(a.frame),observed_original_costs=len(observed),complete_strata=len(complete),missing_original_draws=42-len(observed),
 all_strata_have_two_planned_draws=True,population_modules=sum(strata.values()),conditional_modules=N,
 no_assumption_global_count_min=1,no_assumption_global_count_universal_nonsharp_max=math.ceil(sum(strata.values())/2),
 full_library_actual_half_cost_count="unknown",full_library_within10_cost_share="unknown",
 current_n2_plugin_bound=[.1,.2],bounds_scope="algebraic bound on interpolation estimator, NOT true populationtail",
 no_native_run=True,checks="same withinshare under two contrarypopulationcompletions; CPUweights equation; observed and HT totals")
(a.out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(census_summary));print(json.dumps(summary));print(json.dumps(cover));print(json.dumps(controls));print(json.dumps(receipt))
