#!/usr/bin/env python3
"""Read-only W/O file-frame join and qualified existing artifact candidates."""
import argparse
import csv
import datetime
import gzip
import json
import os
from pathlib import Path

os.sched_setaffinity(0,set(range(8,16)))
ROOT=Path(__file__).resolve().parents[2]
B=Path("/workspaces/.agent-state/gpu-smt-captures")
O=B/"decoupled-check-20261031/whole-library-20261102"
W=B/"workloads"
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--out",type=Path,required=True)
a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
def write(n,rs):
 if not rs:return
 with(a.out/n).open("w",newline="")as f:
  q=csv.DictWriter(f,list(rs[0]),lineterminator="\n");q.writeheader();q.writerows(rs)
labels=Path(json.loads((ROOT/"workloads/openai-math/cost-regimes-noM/receipt.json").read_text())["all_module_labels_gzip"])
wl=list(csv.DictReader(gzip.open(labels,"rt")))
of=json.loads((O/"frame.json").read_text());wp={r["path"]:r for r in wl};op={r["path"]:r for r in of}
assert len(wl)==len(wp)==len(of)==len(op)==163097
assert wp.keys()==op.keys()
aliases=[dict(path=p,W_frozen_module=wp[p]["module"],O_native_module=op[p]["module"],W_frozen_stratum=wp[p]["stratum"],source_unit_match=True)for p in wp if wp[p]["module"]!=op[p]["module"]]
write("three-name-differences.csv",aliases)
sample=[r for r in csv.DictReader((ROOT/"workloads/openai-math/build-planning-4eaee875/phaseA-targets.csv").open())if r["role"]=="probability_sample"]
assert len(sample)==42
sample_ids={r["module"]for r in sample};alias_ids={r["W_frozen_module"]for r in aliases}
assert not sample_ids.intersection(alias_ids)
# Read a single atomic Ostate snapshot; no write/import/restart of Oinputs.
s=json.loads((O/"all-state.json").read_text());accepted=set(s["accepted"]);Oids={r["module"]for r in of}
prep=json.loads((O/"prepared.json").read_text());front=json.loads((O/"external-frontier-analysis.json").read_text())
candidates={}
for ledger in sorted(W.glob("*/results.jsonl")):
 for no,line in enumerate(ledger.read_text().splitlines(),1):
  z=json.loads(line)
  if not(z.get("status")=="compile_ok"and z.get("source_exact")and z.get("native_retired")and z.get("cgroup_retired")
   and z.get("lean_memory_option_MiB")==0 and z.get("heartbeat_budget")=="authored_or_native_default"
   and z.get("compilation_outputs")=="olean_ilean_c"and z.get("threads")==8 and z.get("pcore_lock")):continue
  path=z.get("path")
  if path not in op:continue
  expected=op[path]["module"];parts=Path(z["raw"])/"artifacts"
  olean=parts/(expected.split(".")[-1]+".olean")
  if not olean.exists():continue
  # Immutable producer-copy candidate, not mutable shared-cache identity.
  candidates[expected]=dict(module=expected,source_path=path,W_collection_module=z["module"],producer_olean=str(olean),
   source_ledger=str(ledger),source_line=no,producer_raw=z["raw"],native_retired=True,
   already_available_in_O_lib=O.joinpath("lib",*expected.split(".")).with_suffix(".olean").is_file(),
   accepted_in_O_state=expected in accepted,
   scope="candidate for Oowner; not imported or kernel-qualified by this analysis")
write("existing-W-artifact-candidates.csv",sorted(candidates.values(),key=lambda r:r["module"]))
summary=dict(observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_pin=prep["source_revision"],
 W_source_files=len(wp),O_source_files=len(op),same_source_path_units=len(wp),
 exact_module_id_intersection=len({r["module"]for r in wl}&Oids),name_differences=len(aliases),
 original42_sample_name_differences=0,frozen_strata_and_weights_changed=False,
 O_state_snapshot_status=s["status"],O_state_snapshot_terminal=s["terminal"],
 O_accepted_source_ids=len(accepted&Oids),O_accepted_external_ids=len(accepted-Oids),
 O_source_failures=len(s["source_failures"]),O_blocked_records=len(s["blocked"]),
 unresolved_provider_names=len(front["unresolved_external_imports"]),source_reachability_to_missing_providers=front["affected_source_count"],
 external_frontier_scope="static potential reachability, not native compile failure or kernel rejection",
 O_initial_available_source_artifacts=prep["initial_available_source_artifacts"],
 O_initial_missing_source_artifacts=prep["initial_missing_source_artifacts"],
 W_existing_exact_source_artifact_candidates=len(candidates),
 candidate_missing_from_O_lib=sum(not r["already_available_in_O_lib"]for r in candidates.values()),
 artifact_candidate_scope="collection-qualified producer copies; O must import/qualify via its owner; no Ofiles changed",
 whole_library_CPU_result_complete=False,modifications_to_O_or_active_W=0,
 source_cost_warning="Omissinginputproduction emits oleanonly; Wsourcecost draws emit olean+ilean+C; keep production and kernelchecking CPU separate")
(a.out/"alignment-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary));print(json.dumps(aliases))
