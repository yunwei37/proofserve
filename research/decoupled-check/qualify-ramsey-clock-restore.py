from pathlib import Path
import os,json,re,importlib.util
B=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031");A=B/"ramsey-20261102";P=A/"cpu-profile"
assert sorted(os.sched_getaffinity(0))==list(range(8))
assert json.loads((P/"qualification-v2-terminal.json").read_text())["complete"]
spec=importlib.util.spec_from_file_location("n",B/"scale-study/falconer-project-20261101/native_project.py")
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=P
env=n.environment();env["LEAN_PATH"]=str(P)+":"+str(A)+":"+str(A/"check-lib")
for key in ["DECOUPLED_CHECKPOINT_INPUT","DECOUPLED_CHECKPOINT_OUTPUT","DECOUPLED_CHECKPOINT_MODULE","DECOUPLED_SEGMENT_MODULES","DECOUPLED_MUTATE_MODULE"]:env.pop(key,None)
def read(c):
 return [json.loads(l)for l in(P/(c["key"]+".stdout")).read_text().splitlines()if l.startswith("{")]
prefix="ClockCompatibilityPrefixV2";chosen=env.copy()
chosen.update(DECOUPLED_CHECKPOINT_OUTPUT=str(P/(prefix+".olean")),DECOUPLED_CHECKPOINT_MODULE=prefix,DECOUPLED_SEGMENT_MODULES="1")
a=n.run("clock-restore-v2-original-prefix",[A/"checkpoint-audit","audit","none","Init.Prelude"],120,True,env=chosen)
es=read(a);first={v["module"]for v in es if v.get("event")=="accept"}
assert a["returncode"]==0 and first=={"Init.Prelude"}and any(v.get("event")=="checkpoint"for v in es)
root="Mathlib.Data.Nat.Basic";graph={v["module"]:v["imports"]for v in json.loads((A/"frame.json").read_text())}
expected=set()
def visit(m):
 if m in expected:return
 expected.add(m)
 for q in graph[m]:visit(q)
visit(root);chosen=env.copy();chosen["DECOUPLED_CHECKPOINT_INPUT"]=prefix
b=n.run("clock-restore-v2-valid",[P/"clock-audit-v2","audit","none",root],120,True,env=chosen)
bs=read(b);accepted={v["module"]for v in bs if v.get("event")=="accept"}
done=next((v for v in reversed(bs)if v.get("event")=="complete"),None)
timings=[v for v in bs if v.get("event")=="module_cpu"]
positive=b["returncode"]==0 and first|accepted==expected and done is not None and done["modules"]==len(expected)and len(timings)==len(accepted)
errors=[];c=None;negative=False
if positive:
 chosen["DECOUPLED_MUTATE_MODULE"]=root
 c=n.run("clock-restore-v2-bad",[P/"clock-audit-v2","audit","bvar",root],120,True,env=chosen)
 errors=[v.get("error","")for v in read(c)if v.get("event")=="reject"and v.get("module")==root]
 negative=c["returncode"]==1 and any(re.search(r"(?i)(bound variable|de.?bruijn|bvar)",v)for v in errors)
v=dict(complete=bool(positive and negative),original_prefix_accepted=sorted(first),expected_modules=len(expected),clock_suffix_accepted=len(accepted),native_union_equal=first|accepted==expected,cpu_events=len(timings),positive=bool(positive),negative=bool(negative),errors=errors,complete_event=done,cells=[a,b]+([c]if c else[]),primary_modified=False,full_corpus_equality_tested=False)
(P/"restore-v2-terminal.json").write_text(json.dumps(v,indent=2));print(json.dumps(v),flush=True)
raise SystemExit(0 if v["complete"]else 2)
