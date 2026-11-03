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

    def receipt(self, status="complete"):
        return dict(schema_version=1, status=status, accepted=["Demo"], rejected=[],
            roots=["Demo"], axioms=["propext"], lean_version="Lean (version 4.34.1, ...)",
            module_set_hash=42, module_set_hash_algorithm="lean4.34.1-hash64-noncryptographic",
            workers=2, cpu_ns=2000000000, wall_ns=1500000000,
            cumulative_segment_cpu_ns=4000000000, trusted_local_checkpoints=True)

    def test_v1_receipt_complete_vs_prefix_axioms(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            f = p / "receipt.json"
            f.write_text(json.dumps(self.receipt()))
            r = audit.audit(p, receipt=f)["compiled_evidence"]
            self.assertEqual(r["status"], "reported_complete")
            self.assertEqual(r["axioms"], ["propext"])
            self.assertEqual(r["axioms_scope"], "complete_checked_closure")
            self.assertEqual(r["invocation_cpu_s"], 2)
            self.assertEqual(r["cumulative_segment_cpu_s"], 4)
            self.assertIn("not established", r["source_binding"])
            f.write_text(json.dumps(self.receipt("incomplete")))
            self.assertEqual(audit.audit(p, receipt=f)["compiled_evidence"]["axioms_scope"],
                             "last_successful_prefix_only")

    def test_v1_receipt_rejects_contradictory_or_bad_clock(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.project(d)
            f = p / "receipt.json"
            r = self.receipt()
            r["rejected"] = [{"error": "bad proof"}]
            f.write_text(json.dumps(r))
            with self.assertRaises(ValueError):
                audit.audit(p, receipt=f)
            r = self.receipt()
            r["cpu_ns"] = -1
            f.write_text(json.dumps(r))
            with self.assertRaises(ValueError):
                audit.audit(p, receipt=f)

    def test_raw_string_and_unicode_import(self):
        r = audit.lexical('def s := r#"literal " decide +kernel "#\nimport Δοκιμή.Test\n')
        self.assertEqual(r["counts"]["decide_plus_kernel"], 0)
        self.assertEqual(r["imports"], ["Δοκιμή.Test"])

if __name__ == "__main__":
    unittest.main()
