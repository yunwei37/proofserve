from pathlib import Path
import os,json,gzip,shutil,datetime,tempfile
os.sched_setaffinity(0,{22,23});s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
groups=json.loads(gzip.decompress((e/'duplicate-preflight-groups.json.gz').read_bytes()));targets={x[0]for g in groups for x in g['paths']}
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  for fd in list((pr/'fd').iterdir())+[pr/'exe',pr/'cwd']:
   try:assert os.readlink(fd).removesuffix(' (deleted)')not in targets
   except OSError:pass
  for l in(pr/'maps').read_text().splitlines():
   a=l.split(None,5)
   if len(a)==6:assert a[5]not in targets
 except OSError:pass
def equal(a,b):
 with open(a,'rb')as f,open(b,'rb')as g:
  while True:
   x=f.read(1024*1024);y=g.read(1024*1024)
   if x!=y:return False
   if not x:return True
records=[];freed=0;before=shutil.disk_usage('/workspaces')._asdict()
for group in groups:
 reps=[]
 for x in group['paths']:
  p=Path(x[0]);st=p.stat()
  assert (st.st_dev,st.st_ino,st.st_mtime_ns)==(x[1],x[2],x[5])
  match=None
  for q in reps:
   qt=q.stat()
   if (st.st_mode,st.st_uid,st.st_gid)==(qt.st_mode,qt.st_uid,qt.st_gid)and equal(p,q):match=q;break
  if match is None:reps.append(p);continue
  tmp=Path('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030')/('dedup0279-'+str(os.getpid()))
  assert not tmp.exists()
  os.link(match,tmp);os.replace(tmp,p)
  if st.st_nlink==1:freed+=st.st_blocks*512
  records.append(dict(path=str(p),retained=str(match),bytes=st.st_size,old_inode=st.st_ino,old_nlink=st.st_nlink,old_mtime_ns=st.st_mtime_ns,mode=st.st_mode,exact_full_byte_comparison=True,lastlink_blocks_reclaimed=st.st_blocks*512 if st.st_nlink==1 else 0))
(e/'cleanup-identical-hardlinks.json.gz').write_bytes(gzip.compress(json.dumps(records).encode()))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),paths_preserved=len(records),raw_bytes_lost=0,tracked_touched=0,reclaimed_lastlink_blocks_bytes=freed,before=before,after=shutil.disk_usage('/workspaces')._asdict(),restore='Before future mutation of a retained historical path, copy its bytes into a distinct inode; restore original mtime from the per-path manifest if needed.')
(e/'cleanup-identical-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
