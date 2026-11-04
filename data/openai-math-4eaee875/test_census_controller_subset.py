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

if __name__=="__main__":
    unittest.main()
