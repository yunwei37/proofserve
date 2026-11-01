"""Private-inode cold/warm runtime input test, never host drop_caches.

Preparatory copying/advice is outside native timing, but the whole finite task
owns the shared P-core lock. Source/runtime bytes are not rebuilt or modified.
"""
from pathlib import Path
import os,json,time,shutil,sys,mmap,ctypes
import native
ROOT=Path(__file__).resolve().parent
def needed(p):
 n=p.name
 return ".olean"in n or n.endswith(".ir")or ".so"in n
def residency(path):
 size=path.stat().st_size
 if not size:return (0,0)
 with path.open('r+b')as f:
  m=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_COPY)
  pages=(size+4095)//4096;v=(ctypes.c_ubyte*pages)()
  address=ctypes.addressof(ctypes.c_char.from_buffer(m))
  if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(address),ctypes.c_size_t(size),v):
   raise OSError(ctypes.get_errno(),"mincore")
  resident=sum(x&1 for x in v);m.close()
 return pages,resident
def prepare():
 inputs=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/inputs.json').read_text())
 source_sdk=native.SDK
 original=[Path(x)for x in inputs['LEAN_PATH'].split(':')if'mathlib4341'in x]
 sdk=ROOT/'runtime/sdk';sdk.mkdir(parents=True,exist_ok=False)
 (sdk/'bin').mkdir();(sdk/'lib').mkdir()
 shutil.copyfile(source_sdk/'bin/lean',sdk/'bin/lean')
 shutil.copymode(source_sdk/'bin/lean',sdk/'bin/lean')
 files=[sdk/'bin/lean'];pairs=[]
 for p in (source_sdk/'lib').rglob('*'):
  if p.is_file()and needed(p):pairs.append((p,sdk/'lib'/p.relative_to(source_sdk/'lib')))
 lean_path=[]
 for i,root in enumerate(original):
  dest=ROOT/'runtime'/f'import{i}';dest.mkdir()
  lean_path.append(str(dest))
  for p in root.rglob('*'):
   if p.is_file()and needed(p):pairs.append((p,dest/p.relative_to(root)))
 for source,target in pairs:
  target.parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(source,target);files.append(target)
  # Different inode is necessary: advice must not evict another lane's input.
  if source.stat().st_dev==target.stat().st_dev and source.stat().st_ino==target.stat().st_ino:
   raise RuntimeError('runtime copy unexpectedly shares source inode')
 (ROOT/'runtime-files.json').write_text(json.dumps(list(map(str,files))))
 env=native.environment()
 env.update(LEAN_SYSROOT=str(sdk),LEAN_PATH=':'.join(lean_path+[str(sdk/'lib/lean')]))
 (ROOT/'runtime-prepared.json').write_text(json.dumps(dict(files=len(files),
   bytes=sum(p.stat().st_size for p in files),source_sdk=str(source_sdk),
   copied_sdk=str(sdk),copied_imports=lean_path),indent=2))
 return sdk,files,env
def treat(files,kind):
 pages=resident=0
 for p in files:
  with p.open('rb')as f:
   if kind=='cold':
    os.fsync(f.fileno())
    os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
   else:
    while f.read(8*1024*1024):pass
  n,r=residency(p);pages+=n;resident+=r
 return dict(pages=pages,resident=resident,fraction=resident/max(1,pages))
def main():
 begin=time.monotonic();records=[];conditions=[]
 try:
  sdk,files,env=prepare()
  for rep in [0,1]:
   for threads in [1,8]:
    for kind in (['cold','warm']if rep==0 else['warm','cold']):
     left=int(1690-(time.monotonic()-begin))
     if left<30:raise RuntimeError('finite group budget exhausted')
     label=f'private-r{rep}-j{threads}-{kind}'
     inputs=[ROOT/'Probe.lean',ROOT/(label+'.json')]
     condition=treat(files+inputs,kind)
     condition.update(label=label,scope='private SDK/lib and Mathlib runtime inputs; system libc/page tables not globally evicted')
     conditions.append(condition)
     (ROOT/'cache-conditions.json').write_text(json.dumps(conditions,indent=2))
     env['LEAN_NUM_THREADS']=str(threads)
     result=native.run(label,[sdk/'bin/lean','-j'+str(threads),'--run',
        ROOT/'Probe.lean',ROOT/(label+'.json')],limit=min(180,left),measured=True,env=env)
     records.append(result)
     if result['returncode']:raise RuntimeError('private runtime native cell failed')
  state='complete'
 except BaseException as error:
  records.append(dict(error=repr(error)));state='partial'
 (ROOT/'private-terminal.json').write_text(json.dumps(dict(state=state,cells=records,
   conditions=conditions,wall_s=time.monotonic()-begin),indent=2))
 return 0 if state=='complete'else 1
if __name__=='__main__':raise SystemExit(main())
