#!/usr/bin/env python3
"""Per-stratum half-cost quota plug-in; n=2 bootstrap is a diagnostic, not a CI."""
import collections, csv, itertools, json, math, os
from pathlib import Path
os.sched_setaffinity(0, set(range(8,16)))
root=Path(__file__).resolve().parents[2]
out=root/"workloads/openai-math/half-cost-quota-source32"
out.mkdir(exist_ok=True)
def read(p): return list(csv.DictReader(p.open()))
def write(name,rs):
 with (out/name).open("w",newline="") as f:
  w=csv.DictWriter(f,list(rs[0]),lineterminator="\n");w.writeheader();w.writerows(rs)
frame=read(root/"workloads/openai-math/noM-hard19-source32/sample-costs.csv")
groups=collections.defaultdict(list);audit=[]
N={";".join(r[k] for k in ("size_percentile_bin","import_depth_bin","has_decide_kernel")):int(r["population_modules"]) for r in read(root/"workloads/openai-math/build-planning-4eaee875/strata.csv")}
for r in frame:
 if r["status"]!="completed_cost":continue
 raw=json.loads(Path(r["source_file"]).read_text().splitlines()[int(r["source_line"])-1])
 y=raw["user_cpu_s"]+raw["system_cpu_s"]
 assert raw["status"]=="compile_ok" and raw["source_exact"] and raw["lean_memory_option_MiB"]==0
 assert raw["native_retired"] and raw["cgroup_retired"] and raw["pcore_lock"]
 assert math.isclose(y,float(r["cpu_s"]),rel_tol=1e-12)
 groups[r["stratum"]].append(y)
 audit.append(dict(module=r["module"],stratum=r["stratum"],status=raw["status"],CPU_s=y,wall_s=raw["wall_s"],actual_self_wall_s=raw["actual_self_wall_s"],censored=False,source_file=r["source_file"],source_line=r["source_line"]))
assert len(frame)==42 and len(audit)==32
rows=[]
for h,ys in sorted(groups.items()):
 if len(ys)!=2:continue
 lo,hi=sorted(ys);n=N[h];k=n*(lo+hi)/(4*hi)
 rows.append(dict(stratum=h,population_modules=n,smaller_CPU_s=lo,larger_CPU_s=hi,stratum_CPU_h=n*(lo+hi)/7200,half_cost_equivalent_modules=k,rounded_half_cost_modules=math.ceil(k),census=n==2))
assert len(rows)==15 and sum(r["population_modules"] for r in rows)==104632
write("per-stratum.csv",rows);write("completed-source-audit.csv",audit)
noncensus=[r for r in rows if not r["census"]];census=[r for r in rows if r["census"]]
reference=[];fractional=[]
for flags in itertools.product((0,1),repeat=len(noncensus)):
 ks=[r["half_cost_equivalent_modules"] for r in census]+[r["half_cost_equivalent_modules"] if distinct else r["population_modules"]/2 for r,distinct in zip(noncensus,flags)]
 reference.append(sum(math.ceil(k) for k in ks));fractional.append(sum(ks))
def quantile(xs,p):
 xs=sorted(xs);q=(len(xs)-1)*p;i=int(q);return xs[i]+(xs[min(i+1,len(xs)-1)]-xs[i])*(q-i)
point=sum(r["rounded_half_cost_modules"] for r in rows)
assert point==33971 and min(reference)==point and quantile(reference,.025)>point
summary=dict(observed_original_costs=32,missing_original_draws=10,complete_strata=15,conditional_modules=104632,full_frame_modules=sum(N.values()),fractional_half_quota_modules=sum(r["half_cost_equivalent_modules"] for r in rows),rounded_per_cell_half_quota_modules=point,conditional_fraction=point/104632,
 bootstrap_draws=len(reference),bootstrap_method="exact ordinary within-cell n2 resampling; true N2 census held fixed; equal-cost outcomes collapsed with multiplicity",bootstrap_integer_95_reference=[quantile(reference,.025),quantile(reference,.975)],bootstrap_fractional_95_reference=[quantile(fractional,.025),quantile(fractional,.975)],
 population_confidence_interval="unknown; reference is NOT a population CI",reference_excludes_point=True,
 no_assumption_conditional_integer_quota_range=[len(rows),sum(math.ceil(r["population_modules"]/2) for r in rows)],
 no_assumption_full_integer_quota_range=[len(N),sum(math.ceil(n/2) for n in N.values())],
 whole_library_actual_half_cost_quota="unknown",
 estimand="sum of per-stratum half-CPU quotas; differs from globally minimal count for half total CPU")
(out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
O=root/"research/decoupled-check"; finals=read(O/"falconer-final-costs.csv")
source_falconer=0.
for r in read(O/"falconer-source-costs.csv"):
 cell=json.loads((Path(r["source_cell_root"])/(r["source_cell"]+".result.json")).read_text())
 assert cell["returncode"]==0 and cell["measured"] and cell["affinity"]==list(range(8))
 assert not any(x.startswith("-M") for x in cell["args"])
 source_falconer+=cell["user_s"]+cell["system_s"]
cal=read(root/"workloads/openai-math/cost_staircase/calibration.csv")
mathbuild=next(float(r["source_CPU_s"]) for r in cal if r["calibration"]=="math")
grid=next(float(r["CPU_factor"]) for r in cal if r["calibration"]=="compute-grid")
factors={r["cohort"]:float(r["cpu_s"])/(source_falconer if r["cohort"]=="Falconer" else mathbuild) for r in finals}
write("O-complete-CPU-ratios.csv",[dict(cohort=r["cohort"],modules=r["modules"],segments=r["segments"],build_CPU_s=source_falconer if r["cohort"]=="Falconer" else mathbuild,check_CPU_s=r["cpu_s"],CPU_check_over_build=factors[r["cohort"]],complete=r["complete"],evidence="research/decoupled-check/falconer-final-costs.csv",scope="complete selected closure, not all source frame") for r in finals])
model=[]
for r in rows:
 for anchor,f in factors.items():
  positive=r["stratum"].endswith(";1")
  factor=grid if positive else f
  model.append(dict(stratum=r["stratum"],population_modules=r["population_modules"],source_CPU_h=r["stratum_CPU_h"],ordinary_anchor=anchor,marker_positive=positive,CPU_factor=factor,modeled_check_CPU_h=r["stratum_CPU_h"]*factor,
   protocol="historical unsegmented Grid transfer" if positive else "latest complete segmented "+anchor+" transfer",measured_target_check=False))
write("per-stratum-check-transfer.csv",model)
print(json.dumps(summary));print(json.dumps(factors))
