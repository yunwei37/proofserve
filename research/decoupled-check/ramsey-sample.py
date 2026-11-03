#!/usr/bin/env python3
"""Five size strata, four original-kernel references per retained-prefix stratum."""
import argparse,csv,importlib.util,json,os,statistics,subprocess,time
from pathlib import Path
R=Path("/workspaces/repository");D=R/"research/decoupled-check";OWN=D
B=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
A=B/"ramsey-20261102";S=A/"size-sample";LOCK=str(B.parent/"pcore.lock")
def plan():return json.loads((A/"size-sample-plan.json").read_text())
def module():
 spec=importlib.util.spec_from_file_location("m",A/"ramsey-run-v3.py")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def rows():
 p=S/"results.jsonl"
 return [json.loads(t)for t in p.read_text().splitlines()]if p.exists()else[]
def worker(i):
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 v=plan()["selected"][i];m=module();n=m.native();n.ROOT=S
 e=n.environment();e["LEAN_PATH"]=str(A/"check-lib")
 c=n.run("sample-"+str(i).zfill(2),[m.F.parent/"measurement-v1/audited-stream","one","none",v["module"]],1400,True,env=e)
 es=[json.loads(line)for line in(S/(c["key"]+".stdout")).read_text().splitlines()if line.startswith("{")]
 ids=[q["module"]for q in es if q.get("event")=="accept"]
 good=c["returncode"]==0 and ids==[v["module"]]and not any(q.get("event")=="reject"for q in es)
 with(S/"results.jsonl").open("a")as f:
  f.write(json.dumps(dict(v,cell=c,accepted=ids,valid=good))+"\n");f.flush();os.fsync(f.fileno())
 return 0 if good else 2
def report():
 out=[]
 for v in rows():
  c=v["cell"];cpu=c["user_s"]+c["system_s"]
  out.append(dict(module=v["module"],stratum=v["stratum"],bytes=v["bytes"],descriptive_group=v["descriptive_group"],source_cpu_s=v["source_cpu_s"],check_cpu_s=cpu,source_wall_s=v["source_wall_s"],check_wall_s=c["wall_s"],cpu_ratio=cpu/v["source_cpu_s"]if v["valid"]else"",wall_ratio=c["wall_s"]/v["source_wall_s"]if v["valid"]else"",valid=v["valid"],returncode=c["returncode"],peak_rss_kib=c["peak_rss_kib"],raw_key=c["key"]))
 if out:
  with(D/"ramsey-sample-costs.csv").open("w",newline="")as f:
   w=csv.DictWriter(f,fieldnames=out[0],lineterminator="\n");w.writeheader();w.writerows(out)
 good=[v for v in out if v["valid"]]
 s=dict(selected=20,returned=len(out),accepted=len(good),failed=len(out)-len(good),cpu_s=sum(v["check_cpu_s"]for v in out),complete=len(out)==20,eligible=190,full_population=444,full_closure=False)
 if good:
  ratios=[v["cpu_ratio"]for v in good]
  s.update(median_cpu_ratio=statistics.median(ratios),min_cpu_ratio=min(ratios),max_cpu_ratio=max(ratios),pooled_cpu_ratio=sum(v["check_cpu_s"]for v in good)/sum(v["source_cpu_s"]for v in good))
 (D/"ramsey-sample-summary.json").write_text(json.dumps(s,indent=2)+"\n")
 txt="# Ramsey retained-prefix size-stratified module-local sample\n\nReview: 自审.\n\n"+json.dumps(s,indent=2)+"\n\n"
 txt+="Seed20261103: four uniformly without-replacement targets from each source-byte quintile of190 completed targets. This dependency-ordered prefix is not a random sample of444: it contains Construction prerequisites and some finite certificates before downstream CycleClique certificates/patterns/Main. The254 missing targets are unobserved. Size is not a proof-cost model. K10 is supplemental, excluded from random-sample summaries.\n\nEach separate original4.34.1 module-local checker trusts imports as the existing reference does; startup/import are inside CPU clocks. Source emits olean/ilean/C. These are **not full-closure streaming ratios** and cannot share the Falconer6.31% or matched Mathlib8.95% denominator. Nonzero rc, timeout and OOM remain visible. No further Ramsey source is built.\n"
 (D/"ramsey-sample-result.md").write_text(txt)
 for name in ["ramsey-progress.md","whole-library-progress.md"]:
  p=D/name;t=p.read_text();marker="<!-- retained-prefix-sample -->"
  if marker in t:t=t[:t.index(marker)].rstrip()
  p.write_text(t+"\n\n"+marker+"\nProduction stopped190/444; full stream0/444,0CPUh. Size sample **"+str(len(good))+"/20 accepted**, **"+str(s["failed"])+" failures**, **"+format(s["cpu_s"]/3600,".6f")+" referenceCPUh**. [Sample](ramsey-sample-result.md).\n")
 return s
def queue():
 os.sched_setaffinity(0,{8});S.mkdir(exist_ok=True)
 for i in range(20):
  if any(v["module"]==plan()["selected"][i]["module"]for v in rows()):continue
  locks=Path("/proc/locks").read_text()
  with(S/("task-"+str(i)+".log")).open("x")as f:
   p=subprocess.Popen(["flock",LOCK,"taskset","-c","0-7","timeout","--signal=TERM","--kill-after=10","1500","python3","-u",str(Path(__file__).resolve()),"worker",str(i)],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   (S/("task-"+str(i)+".submission.json")).write_text(json.dumps(dict(pid=p.pid,locks_before=locks),indent=2));rc=p.wait()
  report();publish()
  if rc:break
 s=report();(S/"terminal.json").write_text(json.dumps(s,indent=2))

def publish():
 files=['research/decoupled-check/'+n for n in ['ramsey-sample.py','ramsey-sample-plan.json','ramsey-sample-costs.csv','ramsey-sample-summary.json','ramsey-sample-result.md','ramsey-progress.md','whole-library-progress.md']if(OWN/n).exists()]
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=R,text=True).strip()=='main'
 subprocess.run(['git','add','--']+files,cwd=R,check=True)
 if subprocess.run(['git','diff','--cached','--quiet','--']+files,cwd=R).returncode!=0:
  s=json.loads((D/'ramsey-sample-summary.json').read_text());a=subprocess.check_output(['git','show','-s','--format=%an%n%ae','58ab893'],cwd=R,text=True).splitlines()
  title=f'Ramsey module-local sample: {s["accepted"]}/20 accepted; full production stopped'
  subprocess.run(['git','-c','user.name='+a[0],'-c','user.email='+a[1],'commit','--only','-m',title,'--']+files,cwd=R,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 for i in range(3):
  try:
   subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=R,check=True)
   subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R,check=True)
   subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=R,check=True);return
  except subprocess.CalledProcessError as e:
   if'merge-base'in e.cmd or i==2:raise
   time.sleep(5*(i+1))

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("op",choices=["worker","queue","report"]);p.add_argument("i",nargs="?",type=int);a=p.parse_args()
 if a.op=="worker":raise SystemExit(worker(a.i))
 elif a.op=="queue":queue()
 else:print(json.dumps(report()))
