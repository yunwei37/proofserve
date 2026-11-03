"""Semantic boundaries of the static audit; no Lean, network or build required."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("audit", Path(__file__).with_name("audit.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class AuditTests(unittest.TestCase):
    def project(self, base):
        p = Path(base)
        (p / "lakefile.toml").write_text('name = "demo"\ndefaultTargets = ["Demo"]\n[[lean_lib]]\nname = "Demo"\n')
        (p / "Demo.lean").write_text("import Demo.Used\n")
        (p / "Demo").mkdir()
        (p / "Demo/Used.lean").write_text('theorem ok : True := by trivial\n')
        (p / "Demo/Omitted.lean").write_text('example : True := by decide +kernel\n')
        return p

    def test_default_roots_follow_imports_not_directory(self):
        with tempfile.TemporaryDirectory() as d:
            r = audit.audit(self.project(d))
            self.assertEqual(r["coverage"]["omitted_modules"], ["Demo.Omitted"])
            self.assertEqual(r["lexical_counts"]["decide_plus_kernel"], 1)
            self.assertIsNone(r["modules"][0]["cost"])
            self.assertEqual(r["compiled_evidence"]["status"], "unavailable")

    def test_globs_include_or_exclude_root(self):
        modules = {"D": {}, "D.A": {}, "DD": {}}
        t = dict(roots=["D"], globs=["D.+"])
        self.assertEqual(audit.roots_for(t, modules), {"D.A"})
        t["globs"] = ["D.*"]
        self.assertEqual(audit.roots_for(t, modules), {"D", "D.A"})

    def test_executable_lake_is_unknown_not_zero_omissions(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            (p / "lakefile.toml").unlink()
            (p / "lakefile.lean").write_text("import Lake\nopen Lake DSL\n@[default_target]\nlean_lib Demo\n")
            r = audit.audit(p)
            self.assertEqual(r["coverage"]["status"], "unknown")
            self.assertIsNone(r["coverage"]["omitted_modules"])
            r = audit.audit(p, ["Demo"])
            self.assertEqual(r["coverage"]["status"], "explicit_import_roots")
            self.assertEqual(r["coverage"]["omitted_modules"], ["Demo.Omitted"])

    def test_comments_strings_nested_comments_do_not_count(self):
        r = audit.lexical('-- decide +kernel\n/- decide /- bv_decide -/ simp -/\n'
                          'def s := "decide +kernel"\nexample : True := by decide +kernel\n')
        self.assertEqual(r["counts"]["decide"], 1)
        self.assertEqual(r["counts"]["decide_plus_kernel"], 1)
        self.assertEqual(r["counts"]["bv_decide"], 0)

    def test_character_literal_quote(self):
        self.assertEqual(audit.lexical('def c : Char := \'"\'\n')['counts']['decide'], 0)

    def test_custom_target_and_broken_source_are_not_covered(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            (p / "lakefile.toml").write_text('name="demo"\ndefaultTargets=["custom"]\n')
            self.assertIsNone(audit.audit(p)["coverage"]["omitted_modules"])
            (p / "Demo/Omitted.lean").write_text("/- unterminated")
            self.assertTrue(audit.audit(p)["errors"])

    def test_source_root_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            with (p / "lakefile.toml").open("a") as f:
                f.write('srcDir = "../outside"\n')
            with self.assertRaises(ValueError):
                audit.audit(p)

    def test_costs_require_matching_source_and_finite_nonnegative_values(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            digest = next(x for x in audit.audit(p)["modules"] if x["module"] == "Demo")["source_digest_blake2b"]
            f = p / "costs.csv"
            with f.open("w", newline="") as out:
                w = csv.writer(out)
                w.writerow(["module", "source_digest_blake2b", "status", "user_cpu_s", "system_cpu_s", "wall_s"])
                w.writerow(["Demo", digest, "accepted", 2, .5, 1])
                w.writerow(["Demo.Used", "wrong", "accepted", 2, 0, 1])
            r = audit.audit(p, cost_log=f)
            self.assertEqual(r["modules"][0]["cost"]["cpu_s"], 2.5)
            self.assertEqual(len(r["cost_errors"]), 1)

    def test_receipt_is_not_source_derived_axioms(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            f = p / "receipt.json"
            f.write_text(json.dumps({"unrecognized": True}))
            r = audit.audit(p, receipt=f)
            self.assertEqual(r["compiled_evidence"]["status"], "supplied_uninterpreted")
            self.assertNotIn("axioms", r)

if __name__ == "__main__":
    unittest.main()
