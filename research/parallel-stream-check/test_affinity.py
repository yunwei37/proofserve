import unittest
from unittest.mock import patch
import native
class PassedGuard(Exception):pass
class NoFiles:
 def __truediv__(self,name):raise PassedGuard()
class MeasurementAffinity(unittest.TestCase):
 def check(self,affinity,env,passes):
  with patch.object(native,'ROOT',NoFiles()),patch.object(native.os,'sched_getaffinity',return_value=set(affinity)):
   with self.assertRaises(PassedGuard if passes else AssertionError):
    native.run('guard-only',['/bin/true'],measured=True,env=env)
 def test_old_explicit_environment_keeps_pcore_default(self):
  self.check(range(8),{'PATH':'/usr/bin'},True)
 def test_explicit_heterogeneous_footprint(self):
  self.check(range(24),{'PARALLEL_ALLOWED_CPUS':str(list(range(24)))},True)
 def test_mismatched_actual_affinity(self):
  self.check(range(8),{'PARALLEL_ALLOWED_CPUS':str(list(range(24)))},False)
 def test_no_environment_keeps_pcore_default(self):
  self.check(range(8),None,True)
if __name__=='__main__':unittest.main()
