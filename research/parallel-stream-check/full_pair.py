"""One bounded paired task; two equal-budget cold Barrier arms, never concurrent."""
import os,sys,json,time
from native import ROOT
import full
os.sched_setaffinity(0,set(range(8)))
label=sys.argv[1]if len(sys.argv)>1 else 'barrier'
assert label in ['barrier','grid']
deadline=time.monotonic()+1700
records=[]
try:
 for mode,workers in [('reference',1),('parallel',4)]:
  if deadline-time.monotonic()<810:
   raise RuntimeError('insufficient complete arm budget; arm not started')
  sys.argv=[str(ROOT/'full.py'),label,mode,str(workers),'1','800']
  try:full.main()
  finally:
   (ROOT/(label+'-full-'+mode+str(workers)+'-r1-terminal.json')).write_text(
    json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
  record=json.loads((ROOT/(label+'-full-'+mode+str(workers)+'-r1-summary.json')).read_text())
  records.append(record)
  (ROOT/label+'-full-pair-results.json').write_text(json.dumps(records,indent=2))
 if set(records[0]['accepted'])!=set(records[1]['accepted']):
  raise RuntimeError('actual full-cohort acceptance difference')
 (ROOT/label+'-full-pair-complete.json').write_text(json.dumps(dict(arms=2,accepted_ids=len(records[0]['accepted']),parity=True)))
finally:
 (ROOT/label+'-full-pair-terminal.json').write_text(json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
