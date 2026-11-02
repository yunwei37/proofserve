#!/usr/bin/env python3
"""Conditional cost staircase: measured calibration, explicit transfer assumptions."""
import argparse
import collections
import csv
import json
import math
import os
from pathlib import Path
import statistics
import sys

os.sched_setaffinity(0, set(range(8, 16)))
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FRAME=ROOT/"workloads/openai-math/noM-original-c-suffix48/sample-costs.csv"
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--frame",type=Path,default=DEFAULT_FRAME)
ap.add_argument("--out",type=Path,default=Path(__file__).with_suffix(""))
args=ap.parse_args()
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0, str(ROOT/"workloads/openai-math"))
from estimate_paired_replay_costs import total_part
sys.path.insert(0, "/workspaces/.agent-state/gpu-smt-captures/workloads/statistics-python-deps")
from scipy.stats import t, norm

def read(p):
    return list(csv.DictReader(p.open()))

def write(n, rows):
    with (OUT/n).open("w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def interval(parts, nonnegative=True):
    total = sum(x[0] for x in parts)
    v = sum(x[1] for x in parts)
    den = sum(x[1]**2/(x[2]-1) for x in parts if x[1] > 0)
    df = v*v/den if den else math.inf
    crit = float(t.ppf(.975, df)) if math.isfinite(df) else float(norm.ppf(.975))
    margin = crit*math.sqrt(v)
    return total, max(0., total-margin) if nonnegative else total-margin, total+margin, v, df

BRAW = Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
plan = json.loads((BRAW/"cohort-plan.json").read_text())
raw = [json.loads(s) for s in (BRAW/"measured.jsonl").open()]
calibrations = []
o = {}
for name, spec in plan["cases"].items():
    wanted = set(spec["modules"])
    builds = [x for x in raw if x["operation"] == "build" and x["module"] in wanted]
    assert {x["module"] for x in builds if x["returncode"] == 0} == wanted
    stream = next(x for x in reversed(raw) if x["operation"] == "matched_stream" and x["cohort"] == name)
    assert stream["closure_complete"] and stream["returncode"] == 0
    bcpu = sum(x["user_s"]+x["system_s"] for x in builds)
    bwall = sum(x["wall_s"] for x in builds)
    qcpu = stream["user_s"]+stream["system_s"]
    o[name] = dict(cpu=qcpu/bcpu, wall=stream["wall_s"]/bwall)
    calibrations.append(dict(calibration=name,comparison="stream_over_build",
        source_CPU_s=bcpu,method_CPU_s=qcpu,CPU_factor=o[name]["cpu"],
        source_wall_s=bwall,method_wall_s=stream["wall_s"],wall_factor=o[name]["wall"],
        evidence=str(BRAW/"measured.jsonl"),scope="complete selected closure; shared base included; not a regime population ratio"))
mrows = {x["variant"]:x for x in read(ROOT/"research/parallel-stream-check/v14-math-summary.csv")}
math_cpu = float(mrows["parallel8"]["cpu_s_median"])/float(mrows["reference"]["cpu_s_median"])
math_wall = float(mrows["parallel8"]["wall_s_median"])/float(mrows["reference"]["wall_s_median"])
grow = next(x for x in read(ROOT/"research/parallel-stream-check/full-pairs.csv") if x["cohort"] == "grid")
compute_cpu, compute_wall = float(grow["cpu_ratio"]), 1/float(grow["speedup"])
erows = {x["variant"]:x for x in read(ROOT/"research/parallel-stream-check/compute-cells.csv")
         if x["module"] == "OAI.Analysis.Triangular.Envelope.EnvelopePsiB"}
envelope = "OAI.Analysis.Triangular.Envelope.EnvelopePsiB"
epcpu = float(erows["parallel8"]["cpu_s"])/float(erows["serial"]["cpu_s"])
epwall = float(erows["parallel8"]["wall_s"])/float(erows["serial"]["wall_s"])
ecpu = float(erows["chunk8"]["cpu_s"])/float(erows["parallel8"]["cpu_s"])
ewall = float(erows["chunk8"]["wall_s"])/float(erows["parallel8"]["wall_s"])
for name,b,m,evidence,scope in [
    ("math_parallel8",mrows["reference"],mrows["parallel8"],"research/parallel-stream-check/v14-math-summary.csv","ratio of three-repeat medians; complete Nat.Basic closure"),
    ("grid_parallel4",dict(cpu_s_median=1,wall_s_median=1),dict(cpu_s_median=compute_cpu,wall_s_median=compute_wall),"research/parallel-stream-check/full-pairs.csv","one full-closure pair; CPU rises, wall falls"),
    ("envelope_parallel8",dict(cpu_s_median=erows["serial"]["cpu_s"],wall_s_median=erows["serial"]["wall_s"]),dict(cpu_s_median=erows["parallel8"]["cpu_s"],wall_s_median=erows["parallel8"]["wall_s"]),"research/parallel-stream-check/compute-cells.csv","same-process leaf after fixed checked prefix; not complete closure"),
    ("envelope_chunk8",dict(cpu_s_median=erows["parallel8"]["cpu_s"],wall_s_median=erows["parallel8"]["wall_s"]),dict(cpu_s_median=erows["chunk8"]["cpu_s"],wall_s_median=erows["chunk8"]["wall_s"]),"research/parallel-stream-check/compute-cells.csv","ten qualified >=1 CPU second goals; payload/merges included; generation excluded")
]:
    calibrations.append(dict(calibration=name,comparison="method_over_reference",source_CPU_s=float(b["cpu_s_median"]),method_CPU_s=float(m["cpu_s_median"]),
        CPU_factor=float(m["cpu_s_median"])/float(b["cpu_s_median"]),source_wall_s=float(b["wall_s_median"]),method_wall_s=float(m["wall_s_median"]),
        wall_factor=float(m["wall_s_median"])/float(b["wall_s_median"]),evidence=evidence,scope=scope))
write("calibration.csv",calibrations)

strata = {}
for x in read(ROOT/"workloads/openai-math/build-planning-4eaee875/strata.csv"):
    h = ";".join(x[k] for k in ["size_percentile_bin","import_depth_bin","has_decide_kernel"])
    strata[h] = int(x["population_modules"])
frame = read(args.frame)
members = collections.defaultdict(list)
source = {}
for x in frame:
    members[x["stratum"]].append(x["module"])
    if x["status"] == "completed_cost":
        row = json.loads(Path(x["source_file"]).read_text().splitlines()[int(x["source_line"])-1])
        assert row["status"] == "compile_ok" and row["lean_memory_option_MiB"] == 0
        assert row["source_exact"] and row["compilation_outputs"] == "olean_ilean_c"
        source[x["module"]] = dict(cpu=row["user_cpu_s"]+row["system_cpu_s"],wall=row["wall_s"])
complete = [h for h, ms in members.items() if all(m in source for m in ms)]
assert len(frame)==42 and len({x["module"] for x in frame})==42
assert all(len(v)==2 for v in members.values())
covered_scope=f"covered{len(complete)}_conditional"
domain = lambda h: "certificate_proxy" if h.endswith(";1") else "ordinary_proxy"
covered = {d:sum(strata[h] for h in complete if domain(h)==d) for d in ["certificate_proxy","ordinary_proxy"]}
population = {d:sum(N for h,N in strata.items() if domain(h)==d) for d in covered}
large = {x["module"]:int(x["large_decision_count_ge1s_cpu"]) for x in read(ROOT/"research/chunked-kernel-check/declaration-distribution.csv")}
scenarios = {
 "NatBasic_Grid_closure_transfer": {"ordinary_proxy":"math","certificate_proxy":"compute-grid"},
 "NearPin_Amplitudes_closure_transfer": {"ordinary_proxy":"ordinary-oai","certificate_proxy":"compute-amplitudes"}
}

def factors(m, d, metric, scenario):
    b = o[scenarios[scenario][d]][metric]
    p = (epcpu if metric=="cpu" else epwall) if m==envelope else (
        math_cpu if metric=="cpu" else math_wall) if d=="ordinary_proxy" else (
        compute_cpu if metric=="cpu" else compute_wall)
    chunk = (ecpu if metric=="cpu" else ewall) if m==envelope else 1.
    return [1., b, b*p, b*p*chunk]

modules = []
for row in frame:
    m,h = row["module"],row["stratum"];d = domain(h)
    for scenario in scenarios:
        for metric in ["cpu","wall"]:
            fs = factors(m,d,metric,scenario)
            values = [source[m][metric]*f for f in fs] if m in source else [""]*4
            modules.append(dict(module=m,stratum=h,regime=d,scenario=scenario,clock="CPU_s" if metric=="cpu" else "native_elapsed_s",
                inclusion_weight=strata[h]/2,complete_stratum=h in complete,observed_source=m in source,
                a_build=values[0],b_stream_model=values[1],c_parallel_model=values[2],d_chunk_model=values[3],
                measured_ge1s_goals=large.get(m,"unprofiled"),chunk_applied=m==envelope,
                value_scope="a measured; b/c/d transferred model, not per-module replay measurements"))
write("module-staircase.csv",modules)

summaries=[];marginals=[]
for scenario in scenarios:
 for scope in [covered_scope,"full_frame_class_mean_projection"]:
  scales = {d:1. if scope==covered_scope else population[d]/covered[d] for d in covered}
  for dom in ["all","ordinary_proxy","certificate_proxy"]:
   hs=[h for h in complete if dom=="all" or domain(h)==dom]
   for metric in ["cpu","wall"]:
    def parts(stage, difference=False):
     pp=[]
     for h in hs:
      vals=[]
      for m in members[h]:
       fs=factors(m,domain(h),metric,scenario)
       f=fs[stage]-fs[2] if difference else fs[stage]
       vals.append(source[m][metric]*f*scales[domain(h)])
      pp.append(total_part(strata[h],vals))
     return pp
    abase=interval(parts(0))[0];cbase=interval(parts(2))[0]
    for i,stage in enumerate(["a_build","b_serial_stream","c_parallel_stream","d_plus_qualified_chunk"]):
     estimate,lo,hi,var,df=interval(parts(i))
     R=estimate/abase
     residual=[]
     for h in hs:
      vals=[source[m][metric]*(factors(m,domain(h),metric,scenario)[i]-R)*scales[domain(h)] for m in members[h]]
      residual.append(total_part(strata[h],vals))
     rb=interval([(0,v/abase**2,n) for _,v,n in residual],False)
     summaries.append(dict(scenario=scenario,scope=scope,domain=dom,clock="CPU_h" if metric=="cpu" else "serial_native_elapsed_h_model_not_makespan",
       stage=stage,estimate_h=estimate/3600,nominal95_low_h=lo/3600,nominal95_high_h=hi/3600,df=df,
       over_build=R,over_build_nominal95_low=max(0,R+rb[1]),over_build_nominal95_high=R+rb[2],
       actual_covered_modules=sum(strata[h] for h in hs),target_frame_modules=sum(population.values()) if dom=="all" else population[dom],
       interval_scope="source sampling only; fixed transfer factors; selection/nonresponse/calibration/model uncertainty excluded",
       whole_library_measurement=False))
    delta,lo,hi,_,df=interval(parts(3,True),False)
    marginals.append(dict(scenario=scenario,scope=scope,domain=dom,clock=metric,
       d_minus_c_h=delta/3600,nominal95_low_h=lo/3600,nominal95_high_h=hi/3600,df=df,
       relative_to_c=delta/cbase,relative_to_a=delta/abase,
       meaning="CPU overhead" if metric=="cpu" else "modeled reduction in summed module durations, not measured library makespan",
       qualified_chunk_modules=1,other_ge1s_module_not_qualified="OAI.NumberTheory.DirichletL.Cusp.ResiduesModThree"))
write("conditional-staircase.csv",summaries)
write("chunk-marginal.csv",marginals)
# Sensitivity: varying computation share/coverage is not a new confidence interval.
sensitivity=[]
covered_CPU=sum(strata[h]/2*source[m]["cpu"] for h in complete for m in members[h])
covered_compute_CPU=sum(strata[h]/2*source[m]["cpu"] for h in complete if domain(h)=="certificate_proxy" for m in members[h])
for p in [0.,covered_compute_CPU/covered_CPU,.5,1.]:
 for f in [0.,.1,1.]:
  saving=p*f*(1-ewall)
  sensitivity.append(dict(compute_share_at_c=p,qualified_chunk_fraction_of_compute_at_c=f,
      idealized_c_to_d_elapsed_reduction=saving,CPU_fractional_increase=p*f*(ecpu-1),
      interpretation="hypothetical c-stage shares; covered source-build share is not measured c-stage prevalence"))
write("chunk-share-sensitivity.csv",sensitivity)
receipt=dict(source_frame=str(args.frame),original_costs=len(source),planned=42,complete_strata=len(complete),total_strata=21,
 covered_modules=sum(strata[h] for h in complete),population_modules=sum(strata.values()),
 missing_population_modules=sum(strata[h] for h in strata if h not in complete),
 no_new_native_run=True,no_M=True,source_regime_is_proxy=True,
 no_full_library_measurement=True,calibration_uncertainty_in_CI=False,
 chunk_preparation_CPU_h="unknown; eligibility/support generation not timed in selected leaf curves",
 chunk_hardware_memory="Envelope combined process peak14.0187GiB; not a whole-library memory proof",
 full_frame_projection_assumption="unobserved modules have same within-class mean as complete-cell domain; not established",
 external_dependency_cost="not separately identified; selected closure transfer mixes base/dependencies; no additional shared-base CPU invented")
(OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt))
for x in summaries:
 if x["scenario"]=="NatBasic_Grid_closure_transfer" and x["domain"]=="all":print(json.dumps(x))
for x in marginals:
 if x["scenario"]=="NatBasic_Grid_closure_transfer" and x["domain"]=="all":print(json.dumps(x))
