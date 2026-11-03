from pathlib import Path
import os,importlib.util,json,shutil,subprocess
os.sched_setaffinity(0,{8})
B=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
P=B/"ramsey-20261102/cpu-profile";V=P/"source-v2"
spec=importlib.util.spec_from_file_location("n",B/"scale-study/falconer-project-20261101/native_project.py")
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=P
env=n.environment();env["LEAN_PATH"]=str(n.SDK/"lib/lean")
calls=[];old=P/"source-v1/CheckpointAuditCpu.c";generated=V/"CheckpointAuditCpu.c"
if old.exists():
 if not generated.exists():os.link(old,generated)
 reused=dict(source=str(old),original_key="clock-v1-compile-lean",returncode=0)
else:
 reused=None
 a=n.run("clock-v2-compile-lean",[n.SDK/"bin/lean","--root="+str(V),"-o",V/"CheckpointAuditCpu.olean","-c",generated,V/"CheckpointAuditCpu.lean"],180,False,env=env,cwd=V)
 calls.append(a)
 if a["returncode"]!=0:raise SystemExit(2)
cc=shutil.which("cc");assert cc
a=n.run("clock-v2-compile-clock",[cc,"-O3","-I"+str(n.SDK/"include"),"-c",V/"process-cpu-clock.c","-o",V/"process-cpu-clock.o"],180,False,env=env,cwd=V)
calls.append(a)
if a["returncode"]!=0:raise SystemExit(2)
b=n.run("clock-v2-link",[n.SDK/"bin/leanc","-O3","-o",P/"clock-audit-v2",generated,V/"process-cpu-clock.o"],180,False,env=env,cwd=V)
calls.append(b)
v=dict(complete=b["returncode"]==0,cells=calls,reused_lean_codegen=reused,system_c_compiler=subprocess.check_output([cc,"--version"],text=True).splitlines()[0],timed=False,native_qualification=False)
(P/"build-v2-terminal.json").write_text(json.dumps(v,indent=2))
raise SystemExit(0 if v["complete"]else 2)
