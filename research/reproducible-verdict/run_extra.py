"""Frozen budget ladder and scoped input-cache controls; one finite locked task."""
from pathlib import Path
import json,os,time,mmap,ctypes
import native
ROOT=Path(__file__).resolve().parent
def residency(path):
 size=path.stat().st_size
 with path.open('r+b')as f:
  mapping=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_COPY)
  vec=(ctypes.c_ubyte*((size+4095)//4096))()
  address=ctypes.addressof(ctypes.c_char.from_buffer(mapping))
  ret=ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(address),ctypes.c_size_t(size),vec)
  if ret:raise OSError(ctypes.get_errno(),"mincore")
  bits=[int(x)&1 for x in vec];mapping.close()
 return dict(pages=len(bits),resident=sum(bits))
def run(label,threads=1,limit=180):
 env=native.environment();env['LEAN_NUM_THREADS']=str(threads)
 return native.run(label,[native.SDK/'bin/lean','-j'+str(threads),
   '--run',ROOT/'Probe.lean',ROOT/(label+'.json')],limit=limit,measured=True,env=env)
def main():
 records=[];cache=[]
 try:
  for threads in [1,8]:
   result=run('ladder-j'+str(threads),threads)
   records.append(result)
   if result['returncode']:raise RuntimeError("ladder interrupted")
  for repeat in [0,1,2]:
   for mode in (['cold','warm']if repeat!=1 else ['warm','cold']):
    label=f'cache-r{repeat}-{mode}'
    path=ROOT/(label+'.json')
    before=residency(path)
    if mode=='cold':
     with path.open('rb')as f:
      os.fsync(f.fileno())
      os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    else:path.read_bytes()
    treated=residency(path)
    result=run(label)
    after=residency(path)
    cache.append(dict(label=label,before=before,treated=treated,after=after,
      scope="only this request input JSON, not globally cold SDK or Mathlib pages"))
    records.append(result)
    if result['returncode']:raise RuntimeError("cache cell interrupted")
  state='complete'
 except BaseException as e:
  records.append(dict(error=repr(e)));state='partial'
 (ROOT/'extra-terminal.json').write_text(json.dumps(dict(state=state,cells=records,cache=cache),indent=2))
 return 0 if state=='complete'else 1
if __name__=='__main__':raise SystemExit(main())
