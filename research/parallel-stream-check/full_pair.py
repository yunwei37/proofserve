"""One bounded task: equal-budget cold closure arms, never concurrent."""
import sys,json,time
from native import ROOT
import full
label=sys.argv[1]if len(sys.argv)>1 else 'barrier'
assert label in ['barrier','grid']
prefix=f"{label}-full-pair"
deadline=time.monotonic()+1700
records=[]
try:
 for mode,workers in [('reference',1),('parallel',4)]:
  if deadline-time.monotonic()<810:
   raise RuntimeError('insufficient complete arm budget; arm not started')
  sys.argv=[str(ROOT/'full.py'),label,mode,str(workers),'1','800']
  try:full.main()
  finally:
   (ROOT/f"{label}-full-{mode}{workers}-r1-terminal.json").write_text(
    json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
  record=json.loads((ROOT/f"{label}-full-{mode}{workers}-r1-summary.json").read_text())
  records.append(record)
  (ROOT/f"{prefix}-results.json").write_text(json.dumps(records,indent=2))
 if set(records[0]['accepted'])!=set(records[1]['accepted']):
  raise RuntimeError('actual full-cohort acceptance difference')
 (ROOT/f"{prefix}-complete.json").write_text(json.dumps(dict(arms=2,accepted_ids=len(records[0]['accepted']),parity=True)))
finally:
 (ROOT/f"{prefix}-terminal.json").write_text(json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
