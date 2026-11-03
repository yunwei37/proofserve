from pathlib import Path
import importlib.util,os,json
A=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102")
assert sorted(os.sched_getaffinity(0))==list(range(8))
spec=importlib.util.spec_from_file_location("m",A/"ramsey-run-v3.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
mod="OAI.Combinatorics.Ramsey.CycleClique.Construction.CertificatesK10"
s=m.state();assert mod in s["built"]
assert mod not in s["oracle_ids"],"do not duplicate an already qualified reference"
n=m.native();e=n.environment();e["LEAN_PATH"]=str(A/"check-lib")
c=n.run("oracle-early-k10",[m.F.parent/"measurement-v1/audited-stream","one","none",mod],1400,True,env=e)
es,bad=m.events(c["key"]);ids=[v["module"]for v in es if v.get("event")=="accept"]
good=c["returncode"]==0 and not bad and ids==[mod]
m.append(dict(operation="oracle",cell=c,valid=good,accepted=ids,requested=[mod],advanced_before_source_complete=True))
if good:
 s["oracle_ids"]=sorted(set(s["oracle_ids"])|set(ids));s["tasks"]+=1
 m.atomic(A/"state.json",s)
m.atomic(A/"early-reference-k10-terminal.json",dict(complete=good,cell=c,accepted=ids,source_progress_preserved=True))
print("EARLY_REFERENCE_TERMINAL",good,flush=True)
raise SystemExit(0 if good else 2)
