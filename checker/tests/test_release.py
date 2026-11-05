#!/usr/bin/env python3
"""Offline phase selection, source accounting and honest partial coverage controls."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("release",ROOT/"bench/release.py")
release=importlib.util.module_from_spec(spec);spec.loader.exec_module(release)

class Release(unittest.TestCase):
 def test_explicit_user_stop_allows_only_retired_partial_handoff(self):
  with tempfile.TemporaryDirectory()as td:
   d=Path(td)
   (d/"stop").write_text(json.dumps(dict(user_stop_words="stop the census",segment2_launched=False)))
   (d/"supervisor").write_text(json.dumps(dict(returncode=-2)))
   (d/"launch").write_text(json.dumps(dict(pid=999999999,birth="12",cgroup=str(d/"absent"))))
   cfg=dict(census_stop_record=str(d/"stop"),census_supervisor_terminal=str(d/"supervisor"),census_launch=str(d/"launch"))
   result=release.require_retired_census(cfg)
   self.assertTrue(result["operator_stopped"]);self.assertFalse(result["complete"])
   with patch.object(release,"birth",lambda pid:"12"),self.assertRaises(RuntimeError):
    release.require_retired_census(cfg)
   (d/"stop").write_text(json.dumps(dict(user_stop_words="stop",segment2_launched=True)))
   with self.assertRaises(RuntimeError):release.require_retired_census(cfg)

 def test_complete_traversal_with_real_build_failure_is_not_partial_census(self):
  with tempfile.TemporaryDirectory()as td:
   d=Path(td);terminal=d/"outcomes.json";launch=d/"launch.json"
   launch.write_text(json.dumps(dict(pid=999999999,birth="12",cgroup=str(d/"absent"))))
   value=dict(full_census=True,stop=None,complete=False,total_source_units=3,
              successful=["A"],failed=["Bad"],configuration_units=[],blocked=[dict(module="Dependent",status="blocked")])
   terminal.write_text(json.dumps(value));cfg=dict(census_terminal=str(terminal),census_launch=str(launch))
   self.assertEqual(release.require_retired_census(cfg),value)
   value["blocked"][0]["status"]="not_attempted";terminal.write_text(json.dumps(value))
   with self.assertRaises(RuntimeError):release.require_retired_census(cfg)
   value["blocked"][0]["status"]="blocked";value["stop"]="deadline";terminal.write_text(json.dumps(value))
   with self.assertRaises(RuntimeError):release.require_retired_census(cfg)
 def test_retired_outcome_never_overrides_live_controller(self):
  with tempfile.TemporaryDirectory()as td:
   d=Path(td);(d/"outcomes").write_text(json.dumps(dict(full_census=True,stop=None,complete=True)))
   (d/"launch").write_text(json.dumps(dict(pid=1,birth="9",cgroup=str(d/"absent"))))
   with patch.object(release,"birth",lambda pid:"9"),self.assertRaises(RuntimeError):
    release.require_retired_census(dict(census_terminal=str(d/"outcomes"),census_launch=str(d/"launch")))
 def test_stopped_corpus_reports_exact_subset_and_pending_context(self):
  with tempfile.TemporaryDirectory()as td:
   d=Path(td);b=d/"whole-state/batch-0";b.mkdir(parents=True)
   (b/"certified.json").write_text(json.dumps(dict(receipt=dict(accepted=["A","Dependency"],axioms=["a"]))))
   pending=[dict(module="OAI",context_status="not_completed")]
   j=release.corpus_coverage(d,["A","B","OAI"],pending,[])
   self.assertIsNone(j["verified_source_units"])
   self.assertEqual(j["checkpoint_accepted_source_units"],1)
   self.assertEqual(j["missing_source_units"],["B","OAI"])
   self.assertFalse(j["inputs_revalidated_this_invocation"])
   self.assertEqual(j["status"],"incomplete")
   self.assertEqual(j["pending_contexts"],pending)
   (d/"whole-state/receipt.json").write_text(json.dumps(dict(accepted=["A","B","OAI"],axioms=["a"])))
   stale=release.corpus_coverage(d,["A","B","OAI"],[],[])
   self.assertEqual(stale["status"],"incomplete")
   self.assertIsNone(stale["verified_source_units"])
   current=release.corpus_coverage(d,["A","B","OAI"],[],[],True)
   self.assertEqual(current["status"],"complete")
   self.assertEqual(current["verified_source_units"],3)
if __name__=="__main__":unittest.main()
