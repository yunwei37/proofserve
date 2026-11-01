#!/usr/bin/env python3
"""Rebuild the declared three-root plan from static labels and retained route costs."""
import os,csv,json,argparse
from pathlib import Path
os.sched_setaffinity(0,{8})
REPO=Path('/workspaces/repository')
BASE=Path('/workspaces/.agent-state/gpu-smt-captures')
def make_plan():
 features={r['module']:r for r in csv.DictReader((BASE/'cost-prediction-20261101-v2/features-and-costs.csv').open())}
 jobs=[]
 for key,module,count in [
  ('math','Mathlib.Data.Nat.Basic',1330),
  ('barrier','OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41',4449),
  ('grid','OAI.Analysis.PlanarPacking.Grid',3793)]:
  feature=features[module]
  kind='certificate'if int(feature['explicit_kernel_sites'])>0 else 'ordinary'
  jobs.append(dict(id=key,module=module,modules=count,**{'class':kind}))
 full=list(csv.DictReader((REPO/'research/parallel-stream-check/full-cells.csv').open()))
 math=list(csv.DictReader((REPO/'research/parallel-stream-check/v14-math-cells.csv').open()))
 ordinary=max(float(x['cpu_s'])for x in math if x['variant']=='reference')
 certificate=max(float(x['whole_cpu_s'])for x in full if x['variant']=='parallel')
 prep=json.loads((BASE/'profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 return dict(jobs=jobs,budget_cpu_s=120,policies=['fifo','type_route','upper_admission'],
  type_upper_cpu_s={'ordinary':ordinary,'certificate':certificate},
  calibration='previous matched checker full-closure measurements on these same three roots; not unseen-input bound',
  lean_path=str(BASE/'parallel-stream-assets/overlay-complete-v2')+':'+prep['lean_path'],
  sysroot='/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux',
  child_memory_bytes=int(11.5*2**30),parent_reserve_bytes=512*2**20,
  code_reference='O stream-check; M frozen v14 8c62fc3, no chunk rewrite',
  scope='three selected complete-closure roots, not31 individual proof candidates')
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--out',type=Path,required=True)
 args=parser.parse_args()
 # Never overwrite or mutate the plan currently collecting.
 with args.out.open('x')as f:json.dump(make_plan(),f,indent=2)
if __name__=='__main__':main()
