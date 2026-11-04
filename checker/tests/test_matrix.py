#!/usr/bin/env python3
"""Pure harness failure/retry controls. Native calls and leases are STUBBED.
No stub result is exported as scientific or native-qualification evidence.
"""
import contextlib,importlib.util,io,json,os,sys,tempfile,time,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
class MatrixRetry(unittest.TestCase):
 def test_failed_native_attempt_is_preserved_and_retry_is_fresh(self):
  original_cwd=Path.cwd();original_argv=list(sys.argv)
  with tempfile.TemporaryDirectory(prefix="matrix-harness-",dir="/workspaces/.agent-state/gpu-smt-captures")as td:
   d=Path(td);project=d/"project";project.mkdir();overlay=d/"overlay"
   roots={"math":"Mathlib.Data.Nat.Basic","grid":"OAI.Analysis.PlanarPacking.Grid","barrier":"OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41"}
   for n in roots.values():
    f=overlay/Path(*n.split(".")).with_suffix(".olean");f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b"fixture")
   fake=types.ModuleType("guard");fake.ROOT=d;fake.SDK=d/"sdk";fake.ACTIVE=None;fake.environment=lambda:dict(os.environ)
   fail_once=[True]
   def run(key,argv,limit,measured,env):
    out=d/"runs"/key;out.mkdir(parents=True)
    name=next((n for n in roots if key.startswith(n)),"math")
    state=Path(argv[argv.index("--checkpoint-dir")+1])if"--checkpoint-dir"in argv else None
    code=0
    if key=="grid-P2-r1"and fail_once[0]:code=124;fail_once[0]=False
    if key.startswith("bad-real-prefix"):code=1
    if key=="math-interrupt":
     state.mkdir(parents=True,exist_ok=True);(state/"segment-0.json").write_text("{}")
     cg=d/"fake-cgroup";cg.mkdir();fake.ACTIVE=(cg,0);time.sleep(.08);fake.ACTIVE=None;code=137
    if state:
     state.mkdir(parents=True,exist_ok=True)
     (state/"identity.json").write_text(json.dumps(dict(inputs=[[str(overlay/(roots[name]+".olean")),"1"]],manifest=None,roots=[roots[name]])))
    receipt=dict(status="complete",execution_path="proofserve-parallel",accepted=[roots[name]],axioms=["fixtureAxiom"],module_set_hash="1",workers=1,segments=[dict(segment=0,reused=key=="math-resume")])
    stdout=json.dumps(receipt)if state and code==0 else""
    if key.startswith("bad-real-prefix"):stdout="kernel_reject: Mathlib.Data.Nat.Basic"
    (out/"stdout").write_text(stdout);(out/"stderr").write_text("")
    result=dict(returncode=code,wall_s=1,user_s=1,system_s=0,peak_rss_kib=1,sampled_tree_peak_bytes=1,native_retired=True,cgroup_retired=True,cgroup_usage_s=1,cgroup_user_s=1,cgroup_system_s=0,charged_peak_bytes=1)
    (out/"result.json").write_text(json.dumps(result));return result
   fake.run=run
   cfg=dict(raw=str(d),project=str(project),binary=str(d/"fake-binary"),lease=str(d/"unit-only.lock"),overlay=str(overlay),commit="stub-only-not-scientific")
   config=d/"config.json";config.write_text(json.dumps(cfg))
   try:
    with patch.dict(sys.modules,{"guard":fake}):
     matrix=load("matrix_unit",ROOT/"bench/matrix.py")
     with patch.object(matrix.os,"sched_setaffinity",lambda *args:None),patch.object(matrix.fcntl,"flock",lambda *args:None),contextlib.redirect_stdout(io.StringIO()):
      sys.argv=["matrix.py",str(config)]
      with self.assertRaises(RuntimeError):matrix.main()
      cfg["retry_failed"]=True;config.write_text(json.dumps(cfg));matrix.main()
     failures=json.loads((d/"failed-cells.json").read_text());self.assertEqual(len(failures),1)
     self.assertEqual(failures[0]["returncode"],124)
     rows=json.loads((d/"completed.json").read_text());self.assertEqual(len(rows),71)
     retried=next(r for r in rows if r["key"]=="grid-P2-r1")
     self.assertEqual(retried["run_key"],"grid-P2-r1-attempt-2")
     self.assertEqual(Path(retried["state_directory"]).name,retried["run_key"])
     self.assertTrue((d/"runs/grid-P2-r1/result.json").exists())
     reducer=load("matrix_reducer_unit",ROOT/"bench/summarize.py")
     sys.argv=["summarize.py",str(d),str(d/"summary")]
     with contextlib.redirect_stdout(io.StringIO()):reducer.main()
     self.assertTrue((d/"summary/fixed-failed-attempts.csv").exists())
   finally:os.chdir(original_cwd);sys.argv=original_argv
if __name__=="__main__":unittest.main()
