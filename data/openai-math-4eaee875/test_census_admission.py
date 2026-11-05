import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from census_admission import Policy,Ready,GIB,deferred_closure
class AdmissionTests(unittest.TestCase):
    def engine(self,values):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        cg=Path(self.tmp.name);(cg/"memory.current").write_text(str(sum(v for n,v in values)))
        live={}
        for i,(n,v)in enumerate(values):
            q=cg/str(i);q.mkdir();(q/"memory.current").write_text(str(v));live[i]=dict(cg=q,meta=dict(module=n))
        return SimpleNamespace(cg=cg,live=live)
    def test_headroom_stops_admission_without_RSS(self):
        p=Policy([]);e=self.engine([("A.B.C.x",GIB)])
        self.assertFalse(p.decide("D.E.F.x",e,11*GIB)["allowed"])
    def test_risk_metadata_does_not_apply_a_family_cap(self):
        rows=[dict(module="OAI.N.P.A.x",status="failure",interruption="cgroup_memory_oom",cgroup_peak=12*GIB)]
        p=Policy(rows);e=self.engine([("OAI.N.P.A.a",GIB),("OAI.N.P.B.b",GIB)])
        z=p.decide("OAI.N.P.C.c",e,40*GIB)
        self.assertTrue(z["risky_root"]);self.assertTrue(z["allowed"])
        self.assertTrue(p.decide("Other.N.P.x",e,40*GIB)["allowed"])
    def test_ready_keeps_lexical_order_among_feasible_families(self):
        r=Ready()
        for x in ["A.B.x","A.B.y","C.D.x"]:r.push(x)
        n,s=r.take(lambda n:True,lambda n:dict(allowed=not n.startswith("A.")))
        self.assertEqual(n,"C.D.x")
        n,s=r.take(lambda n:True,lambda n:dict(allowed=True));self.assertEqual(n,"A.B.x")
    def test_cancelled_transition_is_not_memory_failure(self):
        p=Policy([dict(module="A.B.x",status="failure",interruption="controller_interrupted",cgroup_peak=GIB)])
        self.assertEqual(p.failures["A.B.x"],0);self.assertFalse(p.risky)
    def test_first_and_second_resource_failures_are_counted(self):
        p=Policy([])
        row=dict(module="A.B.x",status="failure",interruption="memory_reserve",cgroup_peak=GIB)
        p.observe(row);self.assertEqual(p.failures["A.B.x"],1)
        p.observe(row);self.assertEqual(p.failures["A.B.x"],2)
    def test_defer_descendants_but_preserve_completed_and_running(self):
        pending={"Risk.A.x","Risk.A.y","Safe.Child","Safe.Other"}
        active={"Risk.A.y"};children={"Risk.A.x":{"Safe.Child"},"Safe.Child":{"Safe.Other"}}
        found=deferred_closure("Risk.A",pending,active,children)
        self.assertEqual(set(found),{"Risk.A.x","Safe.Child","Safe.Other"})
        self.assertEqual(found["Safe.Child"],"Risk.A.x")
        self.assertNotIn("Risk.A.y",found)
        self.assertNotIn("Risk.A.done",found)
if __name__=="__main__":unittest.main()
