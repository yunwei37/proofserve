#!/usr/bin/env python3
"""Planning estimates from retained previews and a READ-ONLY W cost snapshot.

These are not final checker timings or a whole-corpus verification measurement.
"""
import argparse,collections,csv,datetime,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[2]

def estimate(config,out):
 cfg=json.loads(config.read_text());out.mkdir(parents=True,exist_ok=True)
 preview=list(csv.DictReader((R/"checker/results/loaded-preview-cells.csv").open()))
 def median(prefix):
  return statistics.median(float(r["wall_s"])for r in preview if r["key"].startswith(prefix)and r["returncode"]=="0")
 policy=list(csv.DictReader((R/"checker/results/theorem-body-policy/closures.csv").open()))
 strict={r["dataset"]:r for r in policy if r["source"]=="e155-strict-context"}
 replacement={r["dataset"]:r for r in policy if r["source"]=="replacement-shared-checked"}
 plan=[]
 for d in ["math","grid","barrier"]:
  points=cfg.get("worker_points",{}).get(d,[1,2,4,8])
  for n in points:plan.append(dict(dataset=d,arm="native",workers=n,repeats=3,estimated_wall_s=3*median(f"{d}-P{n}-r"),basis="retained P-core loaded preview"))
  if d!="barrier":
   for arm in ["no-persistence","no-split-fallback"]:
    plan.append(dict(dataset=d,arm=arm,workers=8,repeats=3,estimated_wall_s=3*median(f"{d}-P8-{arm}-r"),basis="retained P-core loaded preview"))
   name="nat"if d=="math"else"grid"
   # Use the observed P2/E2 default-wall ratio as an uncertain hardware/load
   # conversion; assume NO extra strict speedup from 2 to 8 workers.
   scale=median(f"{d}-P2-r")/json.loads(replacement[name]["attempt_wall_s"])[0]
   plan.append(dict(dataset=d,arm="strict-theorem-bodies",workers=8,repeats=3,
    estimated_wall_s=3*sum(json.loads(strict[name]["attempt_wall_s"]))*scale,
    basis="historical E2 strict attempts times observed P2/E2 default-wall ratio; no 8-worker boost assumed"))
  for mode in ["default","fresh"]:
   val=median("math-official-"+mode+"-r")if d=="math"else(5 if mode=="default"else median(d+"-P1-r"))
   plan.append(dict(dataset=d,arm="official-"+mode,workers=8,repeats=3,estimated_wall_s=3*val,
    basis="actual retained Nat official control"if d=="math"else"planning proxy: 5s leaf or native-1worker closure"))
 plan.append(dict(dataset="math",arm="controls-and-interruption",workers=4,repeats=1,
  estimated_wall_s=30+2*median("math-P4-r"),basis="two full native P4 attempts plus 30s controls allowance"))
 seconds=sum(r["estimated_wall_s"]for r in plan)
 with(out/"matrix-plan.csv").open("w",newline="")as f:
  w=csv.DictWriter(f,fieldnames=list(plan[0]));w.writeheader();w.writerows(plan)
 manifest=json.loads(Path(cfg["manifest"]).read_text());by={r["module"]:r for r in manifest["modules"]}
 records=Path(cfg["census_terminal"]).parent/"records.jsonl"
 latest={};attempt_cpu=0
 with records.open()as f:
  for line in f:
   if not line.endswith("\n"):break
   row=json.loads(line)
   if row.get("record")!="result":continue
   attempt_cpu+=row.get("user_cpu_s",0)+row.get("system_cpu_s",0)
   if row.get("status")=="completed":latest[row["module"]]=row
 source_groups=collections.Counter("calculation"if r.get("decide_plus_kernel",0)>0 else"other"for r in by.values())
 groups=collections.defaultdict(lambda:dict(modules=0,compiler_user_cpu_s=0,compiler_system_cpu_s=0))
 for name,row in latest.items():
  kind="calculation"if by[name].get("decide_plus_kernel",0)>0 else"other"
  g=groups[kind+"_"+row["pool"]];g["modules"]+=1;g["compiler_user_cpu_s"]+=row["user_cpu_s"];g["compiler_system_cpu_s"]+=row["system_cpu_s"]
 calculation=[r for k,r in groups.items()if k.startswith("calculation_")]
 observed_calculation_n=sum(r["modules"]for r in calculation)
 observed_calculation_user=sum(r["compiler_user_cpu_s"]for r in calculation)
 projected_calculation_user=observed_calculation_user/observed_calculation_n*source_groups["calculation"]
 # The 75-94% kernel-user fraction was profiled only for selected computational
 # modules. Applying it to the census stratum is an explicit modeling assumption.
 # Include the static repeated import-loading envelope rather than claiming free imports.
 cost=dict(observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
   source_modules=len(by),completed_sources=len(latest),source_strata=dict(source_groups),observed_cost_strata=dict(groups),
   compiler_all_attempt_cpu_s=attempt_cpu,observed_calculation_user_cpu_s=observed_calculation_user,
   projected_calculation_user_cpu_s=projected_calculation_user,
   calculation_kernel_proxy_cpu_s_range=[.75*projected_calculation_user,.94*projected_calculation_user],
   proof_plus_repeated_loading_cpu_s_range=[.75*projected_calculation_user+4047413*.062,
                                          .94*projected_calculation_user+4047413*.231],
   caveats=["compiler CPU is not checker CPU; selected-module profile fractions are modeling assumptions",
            "completed strata are unfinished and order-biased; refresh after W finishes",
            "mixed P/E CPU seconds are retained separately above; no all-core wall speedup inferred",
            "the loading envelope uses the static 4,047,413-entry dependency-first model and old closure CPU/module rates; it may double-count proof work",
            "large-context memory and input hashing remain unmeasured; this range is not a capacity guarantee"])
 (out/"corpus-cost-plan.json").write_text(json.dumps(cost,indent=2)+"\n")
 result=dict(planning_only=True,estimated_matrix_s=seconds,with_20_percent_reserve_s=1.2*seconds,
   matrix_limit_s=21600,omitted_barrier_workers=[n for n in [1,2,4,8]if n not in cfg.get("worker_points",{}).get("barrier",[1,2,4,8])],
   native_commit="e000ed62",strict_is_new_release_measurement_not_historical_reuse=True,
   source_frame=str(cfg["manifest"]),corpus_cost_file="corpus-cost-plan.json")
 (out/"matrix-plan.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("config",type=Path);ap.add_argument("out",type=Path)
 a=ap.parse_args();estimate(a.config,a.out)
