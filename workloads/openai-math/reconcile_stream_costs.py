#!/usr/bin/env python3
"""Recompute the currently available same-closure O CPU comparison; no Lean."""
import argparse
import csv
import gzip
import json
import math
import os
from pathlib import Path

os.sched_setaffinity(0,set(range(8,16)))
ROOT=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--out",type=Path,required=True)
a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
O=ROOT/"research/decoupled-check"
source=list(csv.DictReader((O/"falconer-source-costs.csv").open()))
source_CPU=source_wall=0.
for row in source:
 cell=json.loads((Path(row["source_cell_root"])/(row["source_cell"]+".result.json")).read_text())
 assert cell["returncode"]==0 and cell["measured"] and cell["affinity"]==list(range(8))
 assert not any(x.startswith("-M")for x in cell["args"])
 assert math.isclose(cell["user_s"],float(row["source_user_s"]),rel_tol=1e-12)
 assert math.isclose(cell["system_s"],float(row["source_system_s"]),rel_tol=1e-12)
 source_CPU+=cell["user_s"]+cell["system_s"];source_wall+=cell["wall_s"]
raw=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101")
segments=[json.loads(p.read_text())for p in sorted((raw/"checkpoint-recheck-v2").glob("segment-*-terminal.json"))]
assert len(segments)==27
check_CPU=sum(x["cell"]["user_s"]+x["cell"]["system_s"]for x in segments)
check_wall=sum(x["cell"]["wall_s"]for x in segments)
for x in segments:
 assert x["cell"]["returncode"]==0 and x["cell"]["affinity"]==list(range(8))
 assert not any(t.startswith("-M")for t in x["cell"]["args"])
e=json.loads((O/"falconer-paper-evidence.json").read_text())
assert math.isclose(check_CPU,e["check_cpu_sum_s"],rel_tol=1e-12)
assert math.isclose(check_wall,e["check_wall_sum_s"],rel_tol=1e-12)
assert math.isclose(source_wall,e["source_wall_sum_s"],rel_tol=1e-12)
# W's static frame is immutable source metadata; do not infer it from the Oclosure.
labels=ROOT/"workloads/openai-math/cost-regimes-noM/receipt.json"
inventory=Path(json.loads(labels.read_text())["all_module_labels_gzip"])
W={x["module"]for x in csv.DictReader(gzip.open(inventory,"rt"))}
ids={x["module"]for x in source};assert len(ids)==13205
inter=ids&W
cal=list(csv.DictReader((ROOT/"workloads/openai-math/cost_staircase/calibration.csv").open()))
anchors=[float(x["CPU_factor"])for x in cal if x["calibration"]in ["math","ordinary-oai"]]
rows=[]
for clock,build,check in [("CPU",source_CPU,check_CPU),("summed_native_elapsed",source_wall,check_wall)]:
 rows.append(dict(observed_input="complete Falconer closure, not whole openai/math",clock=clock,modules=len(ids),
  W_internal_modules=len(inter),external_to_W_frame=len(ids-W),build_s=build,check_s=check,
  build_h=build/3600,check_h=check/3600,check_over_build=check/build,
  CPU_ratio_inside_old_ordinary_anchor_envelope=min(anchors)<=check_CPU/source_CPU<=max(anchors),
  source_rows_verified=len(source),stream_segments=len(segments),
  verification_scope="O reported full parity; W rechecked cost arithmetic/raw sourceCPU only"))
with(a.out/"O-cost-reconciliation.csv").open("w",newline="")as f:
 w=csv.DictWriter(f,rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
receipt=dict(raw_source_cells_checked=len(source),raw_stream_segment_cells=27,O_complete_modules=len(ids),
 W_fullframe_modules=len(W),W_intersection=len(inter),external_to_Wframe=len(ids-W),
 mathematical_acceptance_parity_source="research/decoupled-check/falconer-paper-evidence.json; reported by O, not newly replayed by W",
 whole163097stream_complete_evidence_available=False,new_native_run=False)
(a.out/"O-cost-reconciliation-audit.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(rows))
