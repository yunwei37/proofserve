#!/usr/bin/env python3
"""E-core, bounded compilation/telemetry checks; no performance result."""
import os,json,sys,difflib
from pathlib import Path
from native_measurement import run,ROOT,SDK,environment
os.sched_setaffinity(0,set(range(8,16)))
BASE=ROOT.parent.parent;BOUNDARY=ROOT.parent/'boundary-v4'
assert(BOUNDARY/'qualified.json').is_file()
for name,args in [
 ('compile-lean',[SDK/'bin/lean','-o',ROOT/'AuditedStream.olean','-c',ROOT/'AuditedStream.c',ROOT/'AuditedStream.lean']),
 ('compile-native',[SDK/'bin/leanc','-O3','-o',ROOT/'audited-stream',ROOT/'AuditedStream.c'])]:
 result=run(name,args,180)
 if result['returncode']:raise SystemExit('actual preparation failure: '+name)
# Same native kernel path as the completed matrix; only telemetry differs.
before=(BOUNDARY/'AuditedStream.lean').read_text();after=(ROOT/'AuditedStream.lean').read_text()
(ROOT/'telemetry-source.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True))))
env=environment();env['LEAN_PATH']=str(BOUNDARY/'fixtures')+':'+env['LEAN_PATH']
env['DECOUPLED_MEMORY_PROFILE']='1';env['DECOUPLED_MEMORY_STEP']='1'
records=[]
for case,mutation,expected in [('positive','none',0),('corrupt','bvar',1)]:
 chosen=env.copy()
 if mutation!='none':chosen['DECOUPLED_MUTATE_MODULE']='DupB'
 result=run(case,[ROOT/'audited-stream','audit',mutation,'DupA','DupB'],60,False,env=chosen)
 es=[json.loads(x)for x in(ROOT/(result['key']+'.stdout')).read_text().splitlines()]
 valid=result['returncode']==expected
 if expected:valid=valid and any(e.get('event')=='reject'and e.get('module')=='DupB'for e in es)
 else:
  snaps=[e for e in es if e.get('event')=='memory_checkpoint']
  valid=valid and bool(snaps)and snaps[-1]['shared_kernel_declarations']>0 and'VmHWM:'in snaps[-1]['process_status']
 records.append(dict(case=case,returncode=result['returncode'],qualified=valid))
 if not valid:raise SystemExit('telemetry/native contract failed')
(ROOT/'measurement-qualified.json').write_text(json.dumps(dict(status='qualified',tests=records,
 scope='native checker semantic matrix in boundary-v4, changed telemetry separately qualified; not a full-library result'),indent=2))
print('measurement preparation qualified',flush=True)
