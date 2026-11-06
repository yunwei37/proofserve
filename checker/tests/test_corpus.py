import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'bench'))
from corpus import AdmissionDrain
class AdmissionDrainTest(unittest.TestCase):
 def test_existing_batch_drains_without_new_admission(self):
  d=AdmissionDrain(100,900)
  self.assertEqual(d.step(99,[1,2,3],[2],1),[])
  self.assertEqual(d.step(100,[1,2,3],[2],1),[('freeze',2)])
  self.assertEqual(d.step(101,[1,2,3],[],1),[])
  self.assertEqual(d.step(110,[1,2],[],1),[('kill','admission_deadline_drained')])
 def test_grace_is_absolute_not_reset_by_progress(self):
  d=AdmissionDrain(100,900)
  d.step(100,[1,2,3],[2],1)
  self.assertEqual(d.step(999,[1,2,3],[],1),[])
  self.assertEqual(d.step(1000,[1,2,3],[],1),[('kill','admission_deadline_drain_expired')])
 def test_missing_or_ambiguous_coordinator_does_not_run_past_deadline(self):
  for candidates in [[],[2,3]]:
   d=AdmissionDrain(100)
   self.assertEqual(d.step(100,[1,2,3],candidates,1),[('kill','admission_deadline_no_unique_coordinator')])
 def test_completed_stop_does_not_send_more_signals(self):
  d=AdmissionDrain(100);d.step(100,[1],[],1)
  self.assertEqual(d.step(200,[1,2],[2],1),[])
if __name__=='__main__':unittest.main()
