#!/usr/bin/env python3
"""Three in-memory bad-proof controls after full source/reference coverage."""
from pathlib import Path
import os,json,re,importlib.util
A=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103")
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 spec=importlib.util.spec_from_file_location("m",A/"subexponential-run-resume-v2.py")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 assert m.state()["phase"]=="complete","primary not retired/complete"
 frame=json.loads((A/"frame.json").read_text())
 candidates=[v for v in frame if v["target"]and re.search(r"(?m)^\s*(?:private\s+)?theorem\s",Path(v["source"]).read_text())]
 chosen=sorted(candidates,key=lambda v:(Path(v["source"]).stat().st_size,v["module"]))[:3];assert len(chosen)==3
 n=m.native();out=[]
 for i,v in enumerate(chosen):
  e=n.environment();e["LEAN_PATH"]=str(A/"check-lib");e["DECOUPLED_MUTATE_MODULE"]=v["module"]
  c=n.run("negative-control-"+str(i),[m.F.parent/"measurement-v1/audited-stream","one","bvar",v["module"]],120,True,env=e)
  es,bad=m.events(c["key"]);reject=[q for q in es if q.get("event")=="reject"and q.get("module")==v["module"]]
  valid=c["returncode"]==1 and not bad and bool(reject)and"loose bound variables"in reject[0].get("error","")
  out.append(dict(module=v["module"],cell=c,valid=valid,reject=reject))
  if not valid:break
 terminal=dict(complete=len(out)==3 and all(v["valid"]for v in out),rejected=sum(v["valid"]for v in out),controls=out,mutation="first theorem proof -> loose bound variable in memory; no source/olean edit")
 (A/"negative-controls-terminal.json").write_text(json.dumps(terminal,indent=2));print(json.dumps(terminal,indent=2),flush=True)
 return 0 if terminal["complete"]else 2
if __name__=="__main__":raise SystemExit(main())
