#!/usr/bin/env python3
"""Finite completion of this one corpus point: three native controls and report."""
from pathlib import Path
import json,os,select,subprocess,time
R=Path("/workspaces/repository");D=R/"research/decoupled-check"
A=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103")
def main():
 os.sched_setaffinity(0,{8})
 v=json.loads((A/"resume-submission.json").read_text());p=Path("/proc",str(v["pid"]))
 if p.exists()and(p/"stat").read_text().split(") ")[1].split()[19]==v["birth"]:
  fd=os.pidfd_open(v["pid"]);select.select([fd],[],[]);os.close(fd)
 state=json.loads((A/"state.json").read_text())
 if state["phase"]!="complete":
  (A/"post-run-terminal.json").write_text(json.dumps(dict(complete=False,reason="primary did not complete; no additional native calls",phase=state["phase"]),indent=2));return
 expected={v["module"]for v in json.loads((A/"frame.json").read_text())}
 assert set(state["stream_ids"])==expected and expected<=set(state["oracle_ids"])
 locks=Path("/proc/locks").read_text()
 cmd=["flock",str(A.parent.parent/"pcore.lock"),"taskset","-c","0-7","timeout","--signal=TERM","--kill-after=10","600","python3","-u",str(A/"negative-controls-v1.py")]
 with(A/"negative-controls-task.log").open("x")as f:
  p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  (A/"negative-controls-submission.json").write_text(json.dumps(dict(pid=p.pid,args=cmd,locks_before=locks),indent=2));rc=p.wait()
 if rc:
  (A/"post-run-terminal.json").write_text(json.dumps(dict(complete=False,reason="native negative controls failed",returncode=rc),indent=2));return
 subprocess.run(["taskset","-c","8","python3",str(A/"complete-analysis-v1.py")],check=True)
 controls=json.loads((A/"negative-controls-terminal.json").read_text())
 (D/"subexponential-negative-controls.json").write_text(json.dumps(controls,indent=2)+"\n")
 m=json.loads((D/"subexponential-complete-metrics.json").read_text())
 for name in ["subexponential-progress.md","whole-library-progress.md"]:
  p=D/name;t=p.read_text()
  t+=f"\n## Completed SubexponentialSAT result and controls\n\nReview: 自审.3977source targets/10744dependencies/14721closure modules accepted; exact stream/reference/frame sets equal. Native checker{m['checker_cpu_h']:.6f}CPUh. Full-source CPU ratio{m['full_cpu_ratio']:.6%}; excluding retained dependency source work{m['incremental_cpu_ratio']:.6%}. Three malformed proofs rejected. These directory scopes do not turn historical partial whole-library data into a complete163097-module run. [Complete result](subexponential-complete-result.md), [risk review](subexponential-risk-review.md).\n"
  p.write_text(t)
 names=["subexponential-complete-metrics.json","subexponential-component-costs.csv","subexponential-complete-result.md","subexponential-risk-review.json","subexponential-risk-review.md","subexponential-negative-controls.json","subexponential-progress.md","whole-library-progress.md","subexponential-post-run.py"]
 files=["research/decoupled-check/"+n for n in names]
 assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=R,text=True).strip()=="main"
 subprocess.run(["git","diff","--check","--"]+files,cwd=R,check=True);subprocess.run(["git","add","--"]+files,cwd=R,check=True)
 a=subprocess.check_output(["git","show","-s","--format=%an%n%ae","58ab893"],cwd=R,text=True).splitlines()
 subprocess.run(["git","-c","user.name="+a[0],"-c","user.email="+a[1],"commit","--only","-m",f"Complete3977-target SubexponentialSAT: {m['full_cpu_ratio']:.2%} CPU ratio; three bad proofs rejected","--"]+files,cwd=R,check=True)
 subprocess.run(["git","pull","--rebase","--no-autostash","origin","main"],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 subprocess.run(["git","-c","credential.helper="+helper,"fetch","origin","main"],cwd=R,check=True);subprocess.run(["git","merge-base","--is-ancestor","origin/main","HEAD"],cwd=R,check=True);subprocess.run(["git","-c","credential.helper="+helper,"push","origin","main"],cwd=R,check=True)
 (A/"post-run-terminal.json").write_text(json.dumps(dict(complete=True,metrics=m),indent=2))
if __name__=="__main__":main()
