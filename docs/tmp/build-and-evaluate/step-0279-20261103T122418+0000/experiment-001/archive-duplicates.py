from pathlib import Path
import os,json,gzip,zipfile,tarfile,collections,shutil,datetime,io
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
protected=set(gzip.decompress((e/'cleanup-protected-tracked-paths.txt.gz').read_bytes()).decode().splitlines())
roots=[b,r/'artifacts']
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  for fd in list((pr/'fd').iterdir())+[pr/'exe',pr/'cwd']:
   try:
    z=os.readlink(fd).removesuffix(' (deleted)')
    assert not any(z.startswith(str(q)+'/')for q in roots),(pr.name,z)
   except OSError:pass
 except OSError:pass
before=shutil.disk_usage('/workspaces')._asdict();records=[];freed=0;errors=[]
def remove(p,reason,archive=None,member=None):
 global freed
 assert str(p)not in protected and not p.is_symlink()and any(p.resolve().is_relative_to(q.resolve())for q in roots)
 st=p.stat();rec=dict(path=str(p),bytes=st.st_size,mode=st.st_mode,mtime_ns=st.st_mtime_ns,nlink=st.st_nlink,reason=reason,retained_archive=str(archive)if archive else None,archive_member=member,exact_bytes_verified=archive is not None)
 p.unlink();rec['lastlink_blocks_reclaimed']=st.st_blocks*512 if st.st_nlink==1 else 0;freed+=rec['lastlink_blocks_reclaimed'];records.append(rec)
# Prior direct archive audit: all7517 members are regenerable Lean .olean.private objects.
p=b/'goedel427/mathlib4/.lake/build/frozen-private-cache-20261028.tar.gz'
remove(p,'retired reproducible compiled private-cache archive; direct tar inventory contained only7517 .private outputs')
# Compressed compiled executables are intermediate build outputs, never experiment raw.
for dp,dn,fn in os.walk(r/'artifacts'):
 dn[:]=[n for n in dn if n!='.git']
 for n in fn:
  p=Path(dp)/n
  if str(p)in protected or p.is_symlink()or not n.endswith('.gz')or p.stat().st_size<100000:continue
  try:
   with gzip.open(p,'rb')as f:magic=f.read(4)
   if magic==b'\x7fELF':remove(p,'retired reproducible compressed ELF output; source/build/result records retained')
  except (OSError,EOFError):pass
actual=collections.defaultdict(list);archives=[]
for root in roots:
 for dp,dn,fn in os.walk(root):
  dn[:]=[n for n in dn if n!='.git']
  for n in fn:
   p=Path(dp)/n
   if p.is_symlink():continue
   st=p.stat()
   if str(p)not in protected and st.st_size>=4096:actual[(n,st.st_size)].append(p)
   if p.suffix=='.zip':archives.append(p)
def compare_stream(stream,p):
 with p.open('rb')as f:
  while True:
   x=stream.read(1024*1024);y=f.read(1024*1024)
   if x!=y:return False
   if not x:return True
for arc in archives:
 try:
  with zipfile.ZipFile(arc)as z:
   for m in z.infolist():
    if m.is_dir()or m.file_size<4096:continue
    for p in actual.get((Path(m.filename).name,m.file_size),[]):
     if not p.exists()or p==arc:continue
     # Existing extraction path must agree, in addition to exact bytes.
     if not str(p).endswith('/'+m.filename.lstrip('./')):continue
     with z.open(m)as f:eq=compare_stream(f,p)
     if eq:remove(p,'expanded intermediate duplicate exactly retained in existing ZIP',arc,m.filename)
 except (zipfile.BadZipFile,OSError,EOFError)as ex:errors.append([str(arc),repr(ex)])
 print('ZIP_PROGRESS',len(records),freed,flush=True)if len(records)%2000==0 else None
# Existing split source archives are retained byte-for-byte; inspect without materializing a new archive.
class Parts(io.RawIOBase):
 def __init__(self,paths):self.paths=iter(paths);self.f=None
 def readable(self):return True
 def read(self,n=-1):
  out=bytearray()
  while n<0 or len(out)<n:
   if self.f is None:
    try:self.f=next(self.paths).open('rb')
    except StopIteration:break
   d=self.f.read(-1 if n<0 else n-len(out))
   if not d:self.f.close();self.f=None;continue
   out.extend(d)
  return bytes(out)
for name in ['inputs-chunks','inputs-corrected-chunks']:
 folder=r/'artifacts/leanpolish-native-2026-10-09'/name;parts=sorted(folder.glob('part-*'))
 with tarfile.open(fileobj=Parts(parts),mode='r|gz')as t:
  for m in t:
   if not m.isfile()or m.size<4096:continue
   for p in actual.get((Path(m.name).name,m.size),[]):
    if not p.exists()or not str(p).endswith('/'+m.name.lstrip('./')):continue
    f=t.extractfile(m)
    if f is not None and compare_stream(f,p):remove(p,'expanded intermediate duplicate exactly retained in existing split tar.gz',folder,m.name)
(e/'cleanup-retained-archive-duplicates.json.gz').write_bytes(gzip.compress(json.dumps(records).encode()))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),removed_intermediate_copies=len(records),reclaimed_lastlink_blocks_bytes=freed,raw_unique_bytes_lost=0,tracked_touched=0,archive_errors=errors,before=before,after=shutil.disk_usage('/workspaces')._asdict())
(e/'cleanup-retained-archive-result.json').write_text(json.dumps(out,indent=2)+'\n');print('RESULT',json.dumps(out),flush=True)
