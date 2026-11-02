#!/usr/bin/env python3
"""Missing-original-draw stress scenarios; no invented confidence bounds."""
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
DEFAULT_FRAME=ROOT/"workloads/openai-math/noM-original-c-suffix48/sample-costs.csv"
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--frame",type=Path,default=DEFAULT_FRAME)
ap.add_argument("--out",type=Path,default=Path(__file__).with_suffix(""))
args=ap.parse_args()
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
def read(p):return list(csv.DictReader(p.open()))
def write(n,rows):
 with (OUT/n).open("w",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),lineterminator="\n")
  w.writeheader();w.writerows(rows)

frame=read(args.frame)
assert len(frame)==42 and len({x["module"] for x in frame})==42
strata={";".join(x[k] for k in ["size_percentile_bin","import_depth_bin","has_decide_kernel"]):int(x["population_modules"])
 for x in read(ROOT/"workloads/openai-math/build-planning-4eaee875/strata.csv")}
D=lambda h:"certificate_proxy" if h.endswith(";1") else "ordinary_proxy"
known={};missing=[];byclass=collections.defaultdict(list)
for x in frame:
 h=x["stratum"];d=D(h)
 if x["status"]=="completed_cost":
  a=json.loads(Path(x["source_file"]).read_text().splitlines()[int(x["source_line"])-1])
  assert a["status"]=="compile_ok" and a["lean_memory_option_MiB"]==0 and a["source_exact"]
  cost=a["user_cpu_s"]+a["system_cpu_s"]
  known[x["module"]]=(h,cost)
  byclass[d].append(cost)
 else:
  missing.append(dict(module=x["module"],stratum=h,domain=d,weight=strata[h]/2))
assert len(known)+len(missing)==42
assert all(byclass[d] for d in ["ordinary_proxy","certificate_proxy"])
cal={x["calibration"]:float(x["CPU_factor"]) for x in read(ROOT/"workloads/openai-math/cost_staircase/calibration.csv")}
ranges={"ordinary_proxy":(cal["ordinary-oai"],cal["math"]),
        "certificate_proxy":(cal["compute-amplitudes"],cal["compute-grid"])}
complete={x["stratum"] for x in frame if sum(y["status"]=="completed_cost" for y in frame if y["stratum"]==x["stratum"])==2}
coveredmean={}
for d in ranges:
 total=sum(strata[h]*y/2 for h,y in known.values() if h in complete and D(h)==d)
 N=sum(strata[h] for h in complete if D(h)==d)
 coveredmean[d]=total/N
stats={d:dict(min=min(v),median=statistics.median(v),max=max(v),covered_mean=coveredmean[d]) for d,v in byclass.items()}
rules={
 "zero_missing_cost":{d:0. for d in stats},
 "observed_class_min":{d:s["min"] for d,s in stats.items()},
 "observed_class_median":{d:s["median"] for d,s in stats.items()},
 "covered_domain_mean":{d:s["covered_mean"] for d,s in stats.items()},
 "observed_class_max":{d:s["max"] for d,s in stats.items()},
 "ten_times_class_max":{d:10*s["max"] for d,s in stats.items()},
 "ordinary_tail_stress":{d:(10*s["max"] if d=="ordinary_proxy" else s["min"]) for d,s in stats.items()},
 "certificate_tail_stress":{d:(10*s["max"] if d=="certificate_proxy" else s["min"]) for d,s in stats.items()},
 "nominal_budgeted_8cores_x1200s_work":{d:9600. for d in stats}}
draws=[]
for x in missing:
 for rule,assumption in rules.items():
  y=assumption[x["domain"]]
  draws.append(dict(**x,scenario=rule,assumed_native_CPU_s=y,weighted_contribution_h=x["weight"]*y/3600,
   scope="hypothetical missing draw; not an observation or imputation adopted for primary estimate"))
write("missing-draw-scenarios.csv",draws)
table=[]
for rule,assumption in rules.items():
 source={}
 for dom in ["ordinary_proxy","certificate_proxy","all"]:
  ds=list(stats) if dom=="all" else [dom]
  K=sum(strata[h]*y/2 for h,y in known.values() if D(h) in ds)
  M=sum(x["weight"]*assumption[x["domain"]] for x in missing if x["domain"] in ds)
  kl=sum(strata[h]*y/2*ranges[D(h)][0] for h,y in known.values() if D(h) in ds)
  kh=sum(strata[h]*y/2*ranges[D(h)][1] for h,y in known.values() if D(h) in ds)
  ml=sum(x["weight"]*assumption[x["domain"]]*ranges[x["domain"]][0] for x in missing if x["domain"] in ds)
  mh=sum(x["weight"]*assumption[x["domain"]]*ranges[x["domain"]][1] for x in missing if x["domain"] in ds)
  source[dom]=K+M
  table.append(dict(scenario=rule,domain=dom,known_draws=sum(D(h) in ds for h,y in known.values()),
   missing_draws=sum(x["domain"] in ds for x in missing),known_source_point_h=K/3600,assumed_missing_source_point_h=M/3600,
   full_source_point_h=(K+M)/3600,stream_transfer_low_anchor_h=(kl+ml)/3600,
   stream_transfer_high_anchor_h=(kh+mh)/3600,stream_no_saving_on_missing_h=(kh+M)/3600,
   stream_twice_source_on_missing_h=(kh+2*M)/3600,
   missing_checker_over_source_break_even=(K+M-kh)/M if M else "",
   computational_source_share="",scope="scenario endpoint, NOT confidence/guaranteed bounds; stream uses fixed O closure-ratio transfer",
   budget_changes_estimand=rule.startswith("nominal_budgeted")))
 for x in table[-3:]:x["computational_source_share"]=source["certificate_proxy"]/source["all"]
write("source-vs-stream-scenarios.csv",table)
# The known terms are algebraically lower for a future nonnegative-cost HT point,
# not a lower confidence bound on the finite population.
K=sum(strata[h]*y/2 for h,y in known.values())/3600
W=sum(x["weight"] for x in missing)
if args.frame.resolve()==DEFAULT_FRAME.resolve():
 assert math.isclose(K,165.1879359965278,rel_tol=1e-10)
 assert math.isclose(W/3600,10.842083333333333,rel_tol=1e-12)
assert math.isclose(K,sum(strata[h]*cost/2/3600 for h,cost in known.values()),rel_tol=1e-12)
for row in table:
 if row["domain"]=="all":
  children=[x for x in table if x["scenario"]==row["scenario"] and x["domain"]!="all"]
  for col in ["full_source_point_h","stream_transfer_low_anchor_h","stream_transfer_high_anchor_h","stream_no_saving_on_missing_h"]:
   assert math.isclose(row[col],sum(x[col] for x in children),rel_tol=1e-12)
write("assumed-cost-levels.csv",[dict(domain=d,observed_draws=len(byclass[d]),observed_min_CPU_s=s["min"],
 observed_median_CPU_s=s["median"],observed_max_CPU_s=s["max"],covered_domain_mean_CPU_s=s["covered_mean"],
 missing_draws=sum(x["domain"]==d for x in missing),missing_inverse_probability_weight=sum(x["weight"] for x in missing if x["domain"]==d),
 stream_low_anchor=ranges[d][0],stream_high_anchor=ranges[d][1]) for d,s in stats.items()])
receipt=dict(source_frame=str(args.frame),source_draws_known=len(known),missing_original_draws=len(missing),known_HT_terms_CPU_h=K,
 future_complete_sample_point_algebraic_floor_h=K,actual_completed_HT_point_upper="unbounded without missing-cost assumptions",
 population_CPU_confidence_lower="unknown",population_CPU_confidence_upper="unknown",
 missing_draws_plus_one_CPU_second_total_h=W/3600,
 scenario_count=len(rules),rows=len(table),class_sum_checks=9,
 stream_ratios_are_assumptions_for_unmeasured_modules=True,
 nominal_budget_scenario_changes_to_budgeted_work_not_successful_full_build=True,no_native_run=True)
(OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt))
for x in table:
 if x["domain"]=="all":print(json.dumps(x))
