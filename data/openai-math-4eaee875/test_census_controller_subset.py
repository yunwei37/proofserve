#!/usr/bin/env python3
"""Dry preparation and closure guards; no compiler or cgroup is started."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import census_controller as controller

class SubsetPreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.manifest=self.root/"manifest.json"
        self.export=self.root/"environment.json"
        self.out=self.root/"must-not-exist"
        self.data=dict(source_revision="fixed",mathlib="fixed",lean="4.34.1",lean_binary=sys.executable,
            lean_options=["-DautoImplicit=false"],source_project_root=str(self.root),env={},
            modules=[dict(module="A",source=str(self.root/"A.lean"),root=str(self.root),deps=[],external=[])])
        self.export.write_text(json.dumps(dict(context_export_verified=True,package_versions_verified=True,
            source_revision="fixed",toolchain="4.34.1",project=str(self.root),native_compiler=sys.executable,
            native_environment=dict(LEAN_PATH=str(self.root)))))
    def tearDown(self):
        self.tmp.cleanup()
    def prepare(self,bounded=True):
        self.manifest.write_text(json.dumps(self.data))
        args=argparse.Namespace(manifest=self.manifest,environment_export=self.export,functional=False,
            execute=False,validate_subset=bounded,pool="22",out=self.out,commit="test-only")
        with contextlib.redirect_stdout(io.StringIO()) as capture:
            controller.run(args)
        self.assertFalse(self.out.exists())
        return json.loads(capture.getvalue())
    def test_default_stays_dry_and_preserves_full_pools(self):
        result=self.prepare(False)
        self.assertFalse(result["execute"])
        self.assertEqual(result["protocol"]["pools"],dict(P=list(range(8)),E=list(range(10,24))))
        self.assertNotIn("bounded_validation",result["protocol"])
    def test_subset_is_dry_nonmeasurement_with_e_core_only(self):
        result=self.prepare()
        self.assertFalse(result["execute"])
        self.assertTrue(result["protocol"]["bounded_validation"])
        self.assertFalse(result["protocol"]["cost_measurement"])
        self.assertEqual(result["protocol"]["pools"],dict(P=[],E=list(range(10,17))))
        self.assertEqual(result["protocol"]["threads"],8)
        self.assertEqual(result["protocol"]["validation_limits"]["workers"],1)
    def test_incomplete_closure_is_refused(self):
        self.data["modules"][0]["deps"]=["B"]
        with self.assertRaisesRegex(ValueError,"internal dependency closure"):
            self.prepare()
        self.assertFalse(self.out.exists())
    def test_oversized_subset_is_refused(self):
        row=self.data["modules"][0]
        self.data["modules"]=[dict(row,module=str(i))for i in range(2001)]
        with self.assertRaisesRegex(ValueError,"1..2000"):
            self.prepare()
        self.assertFalse(self.out.exists())

class ImportViewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.first=self.root/"first";self.first.mkdir()
        self.second=self.root/"second";self.second.mkdir()
        self.view=self.root/"view";self.view.mkdir()
    def tearDown(self):
        self.tmp.cleanup()
    def put(self,root,relative,data=b"fixture"):
        p=root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        return p
    def test_all_products_and_future_extensions_are_present(self):
        names=["Pkg/A.olean","Pkg/A.olean.private","Pkg/A.olean.server","Pkg/A.ir",
            "Pkg/A.ir.sig","Pkg/A.ilean","Pkg/A.c","Pkg/A.future-format","libhelper.so"]
        for n in names:self.put(self.first,n)
        expected,_=controller.inventory_imports([str(self.first)])
        self.assertEqual(set(expected),{Path(n)for n in names})
        result=controller.materialize_import_view(self.view,expected)
        self.assertTrue(result["passed"])
        self.assertEqual(result["checked_files"],len(names))
    def test_first_hit_is_retained_and_old_corpus_excluded(self):
        first=self.put(self.first,"Pkg/A.olean",b"first")
        self.put(self.second,"Pkg/A.olean",b"second")
        for n in ["OAI/X.olean","OAI.olean","ComparatorChallenges/X.ir","HodgeConjecture/X.c"]:
            self.put(self.first,n)
        expected,_=controller.inventory_imports([str(self.first),str(self.second)])
        self.assertEqual(expected,{Path("Pkg/A.olean"):first.resolve()})
    def test_partial_module_family_shadowing_is_refused(self):
        self.put(self.first,"Pkg/A.olean")
        self.put(self.second,"Pkg/A.ir")
        with self.assertRaisesRegex(ValueError,"partial module-family shadowing"):
            controller.inventory_imports([str(self.first),str(self.second)])
    def test_missing_extra_and_wrong_target_are_detected(self):
        self.put(self.first,"Pkg/A.olean");self.put(self.first,"Pkg/A.ir")
        expected,_=controller.inventory_imports([str(self.first)])
        controller.materialize_import_view(self.view,expected)
        (self.view/"Pkg/A.ir").unlink()
        self.put(self.view,"extra.file")
        (self.view/"Pkg/A.olean").unlink()
        wrong=self.put(self.second,"A.olean",b"wrong")
        (self.view/"Pkg/A.olean").symlink_to(wrong)
        result=controller.check_import_view(self.view,expected)
        self.assertFalse(result["passed"])
        self.assertEqual(result["missing"],["Pkg/A.ir"])
        self.assertEqual(result["extra"],["extra.file"])
        self.assertEqual(result["different"],["Pkg/A.olean"])
    def test_new_module_publication_uses_all_siblings(self):
        for name in ["A.olean","A.ir","A.ir.sig","A.olean.private","A.ilean","A.c","A.future"]:
            self.put(self.first,name)
        self.put(self.first,"B.ir")
        products=controller.module_products(self.first/"A.olean")
        self.assertEqual({p.name for p in products},{"A.olean","A.ir","A.ir.sig","A.olean.private","A.ilean","A.c","A.future"})
    def test_directory_alias_and_cycle_handling(self):
        sub=self.first/"Pkg";sub.mkdir()
        self.put(sub,"A.olean")
        (self.first/"Alias").symlink_to(sub,target_is_directory=True)
        expected,_=controller.inventory_imports([str(self.first)])
        self.assertEqual(set(expected),{Path("Pkg/A.olean"),Path("Alias/A.olean")})
        (sub/"cycle").symlink_to(self.first,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"cyclic import directory"):
            controller.inventory_imports([str(self.first)])

if __name__=="__main__":
    unittest.main()
