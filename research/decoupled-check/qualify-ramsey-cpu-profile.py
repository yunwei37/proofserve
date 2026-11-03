from pathlib import Path
import os,json,importlib.util,re
B=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
A=B/"ramsey-20261102";P=A/"cpu-profile"
assert sorted(os.sched_getaffinity(0))==list(range(8))
assert json.loads((P/"build-v1-terminal.json").read_text())["complete"]
spec=importlib.util.spec_from_file_location("n",B/"scale-study/falconer-project-20261101/native_project.py")
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=P
e=n.environment();e["LEAN_PATH"]=str(A)+":"+str(A/"check-lib")
for key in ["DECOUPLED_CHECKPOINT_INPUT","DECOUPLED_CHECKPOINT_OUTPUT","DECOUPLED_CHECKPOINT_MODULE","DECOUPLED_SEGMENT_MODULES","DECOUPLED_MUTATE_MODULE"]:
 e.pop(key,None)
records=[]
for label,binary in [("base",A/"checkpoint-audit"),("clock",P/"clock-audit-v1")]:
 for corruption in [False,True]:
  chosen=e.copy();mod="Mathlib.Data.Nat.Basic"if corruption else"Init.Prelude"
  if corruption:chosen["DECOUPLED_MUTATE_MODULE"]=mod
  key="clock-v1-"+label+("-bad"if corruption else"-valid")
  c=n.run(key,[binary,"one"if corruption else"audit","bvar"if corruption else"none",mod],120,True,env=chosen)
  events=[]
  for line in(P/(c["key"]+".stdout")).read_text().splitlines():
   if line.startswith("{"):events.append(json.loads(line))
  errs=[v.get("error","")for v in events if v.get("event")=="reject"and v.get("module")==mod]
  accepted=[v["module"]for v in events if v.get("event")=="accept"]
  timings=[v for v in events if v.get("event")=="module_cpu"]
  good=(c["returncode"]==1 and bool(errs)and any(re.search(r"(?i)(bound variable|de.?bruijn|bvar)",s)for s in errs))if corruption else(c["returncode"]==0 and accepted==[mod])
  if label=="clock"and not corruption:good=good and len(timings)==1 and int(timings[0]["exclusive_process_cpu_ns"])>=0
  records.append(dict(label=label,corruption=corruption,module=mod,cell=c,accepted=accepted,errors=errs,module_cpu=timings,qualified=bool(good)))
  if not good:break
 if not records[-1]["qualified"]:break
v=dict(complete=len(records)==4 and all(v["qualified"]for v in records),records=records,primary_modified=False,production_speed_claim=False)
(P/"qualification-v1-terminal.json").write_text(json.dumps(v,indent=2));print(json.dumps(v),flush=True)
raise SystemExit(0 if v["complete"]else 2)
