"""Evidence-integrity tests, separate from native semantic qualification."""
import unittest,copy
from replay import bundle,compare,key
class ReceiptTests(unittest.TestCase):
 def setUp(self):
  self.req=dict(id="a",mode="sync",observer="off",budget=3,target="t",code="theorem t : True := by trivial")
  self.row=dict(self.req,verdict="accepted",command_raw_heartbeats=[123],axioms=[],new_axioms=[],
    theorem_present=True,errors=[],warnings=[],accounting="sync")
 def make(self,row=None):
  return bundle([self.req],[self.row if row is None else row],dict(semantics=dict(version="4.34.1")),dict(returncode=0,native_retired=True))
 def test_counter_divergence_not_hidden(self):
  a=self.make();r=copy.deepcopy(self.row);r['command_raw_heartbeats']=[124]
  self.assertEqual(compare(a,self.make(r))['differences'][0]['field'],'command_raw_heartbeats')
 def test_interruption_keeps_missing(self):
  a=bundle([self.req],[],{},dict(returncode=124));self.assertEqual(a['missing'],[self.req])
 def test_no_sorry_acceptance(self):
  for field,value in [('axioms',['sorryAx']),('new_axioms',['newAxiom']),('errors',['bad']),('theorem_present',False)]:
   r=copy.deepcopy(self.row);r[field]=value
   with self.assertRaises(ValueError):self.make(r)
 def test_duplicate_and_unbound(self):
  with self.assertRaises(ValueError):bundle([self.req,self.req],[],{}, {})
  r=copy.deepcopy(self.row);r['id']='b'
  with self.assertRaises(ValueError):self.make(r)
 def test_replay_exact_and_version_different(self):
  a=self.make();self.assertEqual(compare(a,a)['differences'],[])
  b=copy.deepcopy(a);b['environment']['semantics']['version']='different'
  self.assertFalse(compare(a,b)['same_declared_semantics'])
 def test_no_total_work_claim(self):
  self.assertIn('NOT a global',self.make()['budget_scope'])
if __name__=='__main__':unittest.main()
