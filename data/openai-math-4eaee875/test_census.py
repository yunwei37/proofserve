#!/usr/bin/env python3
"""Runner lifecycle checks use a tiny executable control, never pretend Lean data."""
import csv
import gzip
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("census",HERE/"census.py")
census=importlib.util.module_from_spec(spec);spec.loader.exec_module(census)

class LedgerTests(unittest.TestCase):
    def test_partial_and_malformed_bytes_are_not_costs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"records"
            census.append(p,dict(record="result",module="A",cpu_s=2))
            with p.open("ab") as f:f.write(b'broken\n{"record":"result"')
            self.assertEqual([r["module"] for r in census.records(p)],["A"])
            self.assertIn(b"broken",p.read_bytes())

@unittest.skipUnless(os.name=="posix" and os.geteuid()==0,"requires existing writable development cgroups")
class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="census-control-",dir="/workspaces/.agent-state/gpu-smt-captures/workloads")
        self.root=Path(self.temp.name)
        self.fake=self.root/"compiler-control"
        self.fake.write_text("""#!/usr/bin/python3
import pathlib,sys,time,subprocess
source=pathlib.Path(sys.argv[-1]).read_text()
if 'WAIT' in source:time.sleep(2)
if 'FAIL' in source:sys.exit(1)
if 'SPAWN' in source:subprocess.Popen([sys.executable,'-c','import time;time.sleep(5)'])
for flag in ['-o','-i','-c']:
 p=pathlib.Path(sys.argv[sys.argv.index(flag)+1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'control')
""")
        self.fake.chmod(0o755)
        self.a=self.root/"A.lean";self.a.write_text("A")
        self.b=self.root/"B.lean";self.b.write_text("B")
        self.manifest=self.root/"manifest.json"
        self.out=self.root/"out"
        self.manifest.write_text(json.dumps(dict(source_revision=census.PIN,mathlib=census.MATHLIB,
            lean="4.34.1",lean_binary=str(self.fake),env=dict(LEAN_PATH=""),lean_options=[],
            modules=[dict(module="A",source=str(self.a),root=str(self.root),bytes=1,deps=[]),
                     dict(module="B",source=str(self.b),root=str(self.root),bytes=1,deps=["A"])])))
        cpus=sorted(os.sched_getaffinity(0)&set(range(8,24)))[:4]
        if len(cpus)<2:self.skipTest("two E cores unavailable")
        self.cmd=[sys.executable,str(HERE/"census.py"),"run","--manifest",str(self.manifest),
            "--out",str(self.out),"--cpus",",".join(map(str,cpus)),"--workers","2","--threads","1"]

    def tearDown(self):
        self.temp.cleanup()

    def run_control(self,code=0):
        p=subprocess.run(self.cmd,capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,code,p.stdout+p.stderr)
        return json.loads((self.out/"terminal.json").read_text())

    def test_dependency_order_durable_resume_and_partial_tail(self):
        t=self.run_control()
        rows=census.records(self.out/"records.jsonl")
        self.assertEqual([r["module"] for r in rows],["A","B"])
        self.assertTrue(all(r["status"]=="completed" and r["native_retired"] and r["cgroup_retired"] for r in rows))
        self.assertTrue(all(r["cpu_class"]=="E" and r["user_cpu_s"]>=0 for r in rows))
        original=(self.out/"records.jsonl").read_bytes()
        with (self.out/"records.jsonl").open("ab") as f:f.write(b'{"partial"')
        t=self.run_control()
        self.assertEqual(len(census.records(self.out/"records.jsonl")),2)
        self.assertTrue((self.out/"records.jsonl").read_bytes().startswith(original+b'{"partial"'))
        self.assertEqual(t["completed"],2)
        with gzip.open(self.out/"module-costs.csv.gz","rt") as f:
            self.assertEqual(len(list(csv.DictReader(f))),2)

    def test_failure_blocks_dependent_without_imputation(self):
        self.a.write_text("FAIL")
        m=json.loads(self.manifest.read_text());m["modules"][0]["bytes"]=4
        self.manifest.write_text(json.dumps(m))
        t=self.run_control(2)
        self.assertEqual((t["failed"],t["unreached"]),(1,1))
        rows=census.records(self.out/"records.jsonl")
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["status"],"native_failure")

    def test_unwaited_descendant_is_cleaned_and_not_completed(self):
        self.a.write_text("SPAWN")
        m=json.loads(self.manifest.read_text());m["modules"][0]["bytes"]=5
        self.manifest.write_text(json.dumps(m))
        self.run_control(2)
        rows=census.records(self.out/"records.jsonl")
        self.assertEqual(rows[0]["status"],"descendants_not_retired")
        self.assertTrue(rows[0]["cleanup_killed_leftover_descendants"])
        self.assertTrue(rows[0]["cgroup_retired"])

    def test_source_change_is_not_a_successful_resume(self):
        self.run_control()
        self.a.write_text("changed")
        p=subprocess.run(self.cmd,capture_output=True,text=True,timeout=10)
        self.assertNotEqual(p.returncode,0)
        self.assertIn("source changed",p.stderr)
        self.assertEqual(len(census.records(self.out/"records.jsonl")),2)

    def test_controller_death_preserves_unknown_cost_then_resumes(self):
        self.a.write_text("WAIT")
        m=json.loads(self.manifest.read_text());m["modules"][0]["bytes"]=4
        self.manifest.write_text(json.dumps(m))
        process=subprocess.Popen(self.cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        deadline=time.monotonic()+10
        lifecycle=self.out/"lifecycle.jsonl"
        while time.monotonic()<deadline:
            if lifecycle.exists() and "native_started" in lifecycle.read_text():break
            time.sleep(.01)
        else:self.fail("control native never started")
        process.kill();process.wait(timeout=5)
        process.stderr.close()
        self.assertEqual(process.returncode,-signal.SIGKILL)
        self.run_control()
        rows=census.records(self.out/"records.jsonl")
        interrupted=[r for r in rows if r["status"]=="interrupted_unknown_cost"]
        self.assertEqual(len(interrupted),1)
        self.assertEqual(interrupted[0]["user_cpu_s"],"")
        self.assertEqual([r["module"] for r in rows if r["status"]=="completed"],["A","B"])
        self.assertEqual(next(r for r in rows if r["module"]=="A" and r["status"]=="completed")["attempt"],2)

if __name__=="__main__":unittest.main()
