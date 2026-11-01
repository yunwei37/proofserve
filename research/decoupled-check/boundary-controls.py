#!/usr/bin/env python3
"""Bounded native controls for cross-module context boundaries.
Invoked only under the shared P-core lock; no production files are mutated.
"""
import os,json,sys,time
from pathlib import Path
from native_audit import run,ROOT,SDK,environment
assert sorted(os.sched_getaffinity(0))==list(range(8))
source=ROOT/'AuditedStream.lean'
records=[]
def checked(key,cmd,limit=120,env=None,cwd=None):
 r=run(key,cmd,limit,False,env=env,cwd=cwd);records.append(r)
 if r['returncode']:raise RuntimeError('native preparation failed: '+key)
 return r
def main():
 checked('compile-lean',[SDK/'bin/lean','-o',ROOT/'AuditedStream.olean','-c',ROOT/'AuditedStream.c',source],180)
 checked('compile-native',[SDK/'bin/leanc','-O3','-o',ROOT/'audited-stream',ROOT/'AuditedStream.c'],180)
 fixtures={
 'DupA':'namespace Shared\ntheorem t : True := True.intro\nend Shared\n',
 'DupB':'namespace Shared\ntheorem t : True := True.intro\nend Shared\n',
 'ExtraA':'namespace Shared\ntheorem externalProof : True := True.intro\nend Shared\n',
 'ExtraB':'namespace LocalB\ntheorem result : True := True.intro\nend LocalB\n',
 'DefA':'namespace Shared\ndef f : Nat := 0\nend Shared\n',
 'DefB':'namespace Shared\ndef f : Nat := 1\nend Shared\n',
 'PrivateA':'private theorem helper : True := True.intro\ntheorem privateA : True := helper\n',
 'PrivateB':'private theorem helper : True := True.intro\ntheorem privateB : True := helper\n',
 }
 directory=ROOT/'fixtures';directory.mkdir(exist_ok=True)
 env=environment();env['LEAN_PATH']=str(directory)+':'+env['LEAN_PATH']
 for mod,text in fixtures.items():
  file=directory/(mod+'.lean');file.write_text(text)
  checked('fixture-'+mod,[SDK/'bin/lean','--root='+str(directory),'-o',directory/(mod+'.olean'),file],60,env=env,cwd=directory)
 cases=[
 ('ordinary-duplicates','none',None,['DupA','DupB'],dict(one=0,naive=0,audit=0)),
 ('corrupt-duplicate','bvar','DupB',['DupA','DupB'],dict(one=1,naive=0,audit=1)),
 ('unimported-sibling','sibling','ExtraB',['ExtraA','ExtraB'],dict(one=1,naive=0,audit=1)),
 ('conflicting-definitions','none',None,['DefA','DefB'],dict(one=0,naive=1,audit=0)),
 ('private-names','none',None,['PrivateA','PrivateB'],dict(one=0,naive=0,audit=0)),
 ]
 result=[]
 for name,mutation,target,roots,expected in cases:
  chosen=env.copy()
  if target:chosen['DECOUPLED_MUTATE_MODULE']=target
  for mode in ['one','naive','audit']:
   r=run(name+'-'+mode,[ROOT/'audited-stream',mode,mutation]+roots,90,False,env=chosen)
   events=[json.loads(x)for x in(ROOT/(r['key']+'.stdout')).read_text().splitlines()if x.startswith('{')]
   result.append(dict(case=name,mode=mode,expected_exit=expected[mode],actual_exit=r['returncode'],
     qualified=(r['returncode']==0)==(expected[mode]==0),
     accept=[e['module']for e in events if e.get('event')=='accept'],
     reject=[e['module']for e in events if e.get('event')=='reject'],
     fallbacks=[e for e in events if e.get('context')=='module_local']))
   # Nonzero expected is a native rejection, not an unconstrained crash.
   if expected[mode] and not any(e.get('event')=='reject'for e in events):
    result[-1]['qualified']=False
 (ROOT/'boundary-results.json').write_text(json.dumps(result,indent=2))
 if not all(x['qualified']for x in result):raise RuntimeError('boundary result differs; retain actual evidence')
 (ROOT/'qualified.json').write_text(json.dumps(dict(status='qualified',cases=len(cases),native_runs=len(result),
  scope='small synthetic sibling-context controls; not full AI library parity or performance'),indent=2))
if __name__=='__main__':
 try:main()
 finally:
  (ROOT/'control-terminal.json').write_text(json.dumps(dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
    qualified=(ROOT/'qualified.json').exists(),native_records=len(records)),indent=2))
