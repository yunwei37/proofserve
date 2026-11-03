#!/usr/bin/env python3
"""Same three bad theorem bodies rejected by restored stream and module-local replay."""
from pathlib import Path
import os,json,re,importlib.util
A=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103")
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 spec=importlib.util.spec_from_file_location("m",A/"subexponential-run-resume-v2.py")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 assert m.state()["phase"]=="complete"
 frame=json.loads((A/"frame.json").read_text())
 ledger=[json.loads(l)for l in(A/"ledger.jsonl").read_text().splitlines()]
 final=next(v for v in reversed(ledger)if v["operation"]=="stream"and v["valid"])
 assert final["previous"],"complete14721-node point must have a certified predecessor"
 # These roots were absent from the predecessor, so a mutation cannot hide
 # behind a module already marked visited by the restored checkpoint.
 tail=set(final["accepted"])
 candidates=[v for v in frame if v["target"]and v["module"]in tail and re.search(r"(?m)^\s*(?:private\s+)?theorem\s",Path(v["source"]).read_text())]
 chosen=sorted(candidates,key=lambda v:(Path(v["source"]).stat().st_size,v["module"]))[:3];assert len(chosen)==3
 n=m.native();out=[]
 for i,v in enumerate(chosen):
  pair=dict(module=v["module"],certified_predecessor=final["previous"],modes=[])
  for mode in ["one","audit"]:
   e=n.environment();e["LEAN_PATH"]=str(A)+":"+str(A/"check-lib");e["DECOUPLED_MUTATE_MODULE"]=v["module"]
   for key in ["DECOUPLED_CHECKPOINT_OUTPUT","DECOUPLED_CHECKPOINT_MODULE","DECOUPLED_SEGMENT_MODULES","DECOUPLED_CHECKPOINT_INPUT"]:e.pop(key,None)
   if mode=="audit":
    e["DECOUPLED_CHECKPOINT_INPUT"]=final["previous"];binary=A/"checkpoint-audit"
   else:binary=m.F.parent/"measurement-v1/audited-stream"
   c=n.run("negative-control-"+str(i)+"-"+mode,[binary,mode,"bvar",v["module"]],120,True,env=e)
   es,bad=m.events(c["key"]);reject=[q for q in es if q.get("event")=="reject"]
   valid=c["returncode"]==1 and not bad and any("loose bound variables"in q.get("error","")for q in reject)and not any(q.get("event")=="accept"and q.get("module")==v["module"]for q in es)
   pair["modes"].append(dict(mode=mode,cell=c,valid=valid,reject=reject))
   if not valid:break
  pair["valid"]=len(pair["modes"])==2 and all(q["valid"]for q in pair["modes"]);out.append(pair)
  if not pair["valid"]:break
 terminal=dict(complete=len(out)==3 and all(v["valid"]for v in out),rejected=sum(v["valid"]for v in out),
 native_rejection_processes=sum(q["valid"]for v in out for q in v["modes"]),controls=out,
 mutation="first theorem proof -> loose bound variable in memory, same root in original module-local and certified-prefix-restored stream; no source/olean edits")
 (A/"negative-controls-terminal.json").write_text(json.dumps(terminal,indent=2));print(json.dumps(terminal,indent=2),flush=True)
 return 0 if terminal["complete"]else 2
if __name__=="__main__":raise SystemExit(main())
