from pathlib import Path
import os,importlib.util,json
os.sched_setaffinity(0,{8})
B=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
P=B/"ramsey-20261102/cpu-profile";V=P/"source-v1"
spec=importlib.util.spec_from_file_location("n",B/"scale-study/falconer-project-20261101/native_project.py")
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=P
env=n.environment();env["LEAN_PATH"]=str(n.SDK/"lib/lean")
a=n.run("clock-v1-compile-lean",[n.SDK/"bin/lean","--root="+str(V),"-o",V/"CheckpointAuditCpu.olean","-c",V/"CheckpointAuditCpu.c",V/"CheckpointAuditCpu.lean"],180,False,env=env,cwd=V)
if a["returncode"]!=0:raise SystemExit(2)
b=n.run("clock-v1-compile-native",[n.SDK/"bin/leanc","-O3","-o",P/"clock-audit-v1",V/"CheckpointAuditCpu.c",V/"process-cpu-clock.c"],180,False,env=env,cwd=V)
(P/"build-v1-terminal.json").write_text(json.dumps(dict(complete=b["returncode"]==0,cells=[a,b],timed=False,native_qualification=False),indent=2))
raise SystemExit(0 if b["returncode"]==0 else 2)
