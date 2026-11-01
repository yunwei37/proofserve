"""Controller integration regression only: no Lean, kernel or timing evidence."""
import sys,types,runpy,json
from pathlib import Path
def check(base):
 source=Path(__file__).with_name('full_pair.py')
 for label in ['grid','barrier']:
  root=base/label;root.mkdir(parents=True)
  calls=[]
  native=types.ModuleType('native');native.ROOT=root
  fake=types.ModuleType('full')
  def invoke():
   cohort,mode,workers,repeat,budget=sys.argv[1:]
   calls.append((cohort,mode,workers,budget))
   key=f"{cohort}-full-{mode}{workers}-r1"
   (root/f"{key}-summary.json").write_text(json.dumps(dict(
    result=dict(key='synthetic_controller_control_not_a_measurement'),
    accepted=['fixture.module'],completed=True,synthetic_controller_only=True)))
  fake.main=invoke
  sys.modules['native']=native;sys.modules['full']=fake
  sys.argv=[str(source),label]
  runpy.run_path(str(source),run_name='__main__')
  assert calls==[(label,'reference','1','800'),(label,'parallel','4','800')]
  assert json.loads((root/f"{label}-full-pair-complete.json").read_text())['parity']
  assert(root/f"{label}-full-pair-results.json").exists()
  assert(root/f"{label}-full-pair-terminal.json").exists()
if __name__=='__main__':
 check(Path(sys.argv[1]))
