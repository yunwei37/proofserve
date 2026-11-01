"""Resume only the missing real Grid arm; do not rerun the preserved reference."""
import sys,json,time
from native import ROOT
import full
reference=ROOT/'grid-full-reference1-r1-summary.json'
ref=json.loads(reference.read_text())
r=ref['result']
assert ref['completed']and r['returncode']==0 and r['native_retired']and r['cgroup_retired']
assert ref['accepted_set_equal_to_same_input_curve']and len(ref['accepted'])==3793
assert r['wall_limit_s']==800 and r['affinity']==list(range(8))
assert not(ROOT/'grid-full-parallel4-r1-summary.json').exists()
try:
 sys.argv=[str(ROOT/'full.py'),'grid','parallel','4','1','800']
 full.main()
 par=json.loads((ROOT/'grid-full-parallel4-r1-summary.json').read_text())
 assert par['completed']and par['result']['native_retired']and par['result']['cgroup_retired']
 assert set(par['accepted'])==set(ref['accepted'])
 (ROOT/'grid-full-pair-results.json').write_text(json.dumps([ref,par],indent=2))
 (ROOT/'grid-full-pair-complete.json').write_text(json.dumps(dict(
  arms=2,accepted_ids=len(ref['accepted']),parity=True,
  resumed_after_controller_path_error=True,reference_reused_without_rerun=True,
  scope='two actual full native processes separated by disclosed controller-repair gap')))
finally:
 (ROOT/'grid-full-pair-resume-terminal.json').write_text(json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
