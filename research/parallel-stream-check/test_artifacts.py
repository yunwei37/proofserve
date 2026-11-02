import tempfile,unittest
from pathlib import Path
from extended import compare_artifacts
class ArtifactOutcome(unittest.TestCase):
 def test_complete_byte_mismatch_is_a_measurement_outcome(self):
  root=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v16/tmp')
  with tempfile.TemporaryDirectory(dir=root) as name:
   folder=Path(name)
   for i in range(12):(folder/(str(i)+'.olean')).write_bytes(b'a')
   self.assertTrue(compare_artifacts(folder)[0]['all_equal'])
   (folder/'7.olean').write_bytes(b'b')
   self.assertFalse(compare_artifacts(folder)[0]['all_equal'])
if __name__=='__main__':unittest.main()
