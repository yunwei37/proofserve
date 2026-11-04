#!/usr/bin/env python3
"""Static planner and frozen-workflow artifact accounting controls; no Lean runs."""
import contextlib,importlib.util,io,json,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
plan=module("plan_full",R/"checker/bench/plan_full.py")
reduce=module("reduce_full",R/"checker/bench/summarize.py")
class Planning(unittest.TestCase):
 def test_diamond_and_context_root_files(self):
  with tempfile.TemporaryDirectory(prefix="planner-",dir="/workspaces/.agent-state/gpu-smt-captures")as td:
   d=Path(td);src=d/"source";src.mkdir()
   deps={"A":["Shared"],"B":["Shared"],"Shared":[],"Z":[]}
   rows=[]
   for n,ds in deps.items():
    f=src/(n+".lean");f.write_text("prelude\n"+"".join("import "+x+"\n"for x in ds)+"axiom p"+n+" : Prop\n")
    rows.append(dict(module=n,source=str(f),root=str(src),deps=ds,external=[]))
   manifest=d/"manifest.json";manifest.write_text(json.dumps(dict(modules=rows,lean_binary=str(d/"sdk/bin/lean"),env={"LEAN_PATH":""},source_revision="fixture")))
   with contextlib.redirect_stdout(io.StringIO()):plan.analyze(manifest,d/"plan",R)
   result=json.loads((d/"plan/summary.json").read_text());by={r["strategy"]:r for r in result["strategy_rows"]}
   self.assertEqual(result["unresolved_external_modules"],[])
   self.assertEqual(by["compiled_empty_assumption_order_1"]["sum_closure_modules"],5)
   self.assertEqual(by["dependency_completed_module_certificates_500"]["sum_closure_modules"],4)
   self.assertEqual((d/"plan/source-context-0-roots.txt").read_text().splitlines(),["A","B","Shared","Z"])
 def test_changed_child_identity_is_not_silently_merged(self):
  with tempfile.TemporaryDirectory(prefix="identity-",dir="/workspaces/.agent-state/gpu-smt-captures")as td:
   d=Path(td);(d/"identity.json").write_text(json.dumps(dict(roots=["X"],manifest=None)))
   for i,value in enumerate(["1","2"]):
    b=d/("batch-"+str(i));b.mkdir()
    (b/"certified.json").write_text(json.dumps(dict(input_identity=dict(inputs=[["same.olean",value]]))))
   with self.assertRaises(AssertionError):reduce.artifact_identity(d)
if __name__=="__main__":unittest.main()
