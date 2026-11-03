"""Untimed metadata estimate only; available artifacts are not the whole source frame."""
import sys,os,json,time
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);assert not out.exists()
sys.path.insert(0,str(root))
from attribution import runtime
paths=[Path(s)for s in runtime(1,list(range(8)),[0],0,False)['LEAN_PATH'].split(':')]
found={}
for base in paths:
 for current,ds,fs in os.walk(base):
  for name in fs:
   if not name.endswith('.olean'):continue
   f=Path(current)/name;mod='.'.join(f.relative_to(base).with_suffix('').parts)
   if mod in found:continue
   sizes=[q.stat().st_size for suffix in ['','.server','.private']if(q:=Path(str(f)+suffix)).exists()]
   found[mod]=dict(path=str(f),bytes=sum(sizes),parts=len(sizes))
ids=[]
for s in(root/'runs/full-plain-m0-P8-r1/stdout').open():
 if s.startswith('{'):
  x=json.loads(s)
  if x.get('event')=='accept':ids.append(x['module'])
assert all(m in found for m in ids)
groups={}
for prefix in ['Mathlib','OAI','Init','Std','Lean']:
 names=[m for m in found if m==prefix or m.startswith(prefix+'.')]
 groups[prefix]=dict(available_modules=len(names),logical_artifact_bytes=sum(found[m]['bytes']for m in names),
  artifact_parts=sum(found[m]['parts']for m in names))
snap=dict(utc=time.strftime('%FT%TZ',time.gmtime()),
 scope='current available compiled search path; not proof of complete source-library build',
 closure=dict(modules=len(ids),logical_artifact_bytes=sum(found[m]['bytes']for m in ids),
  artifact_parts=sum(found[m]['parts']for m in ids)),compiled_available=groups,
 search_path=list(map(str,paths)),
 caveat='W builds may add artifacts; on-disk logical bytes are not live anonymous memory or a memory bound')
out.write_text(json.dumps(snap,indent=2));print(json.dumps(snap))
