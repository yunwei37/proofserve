from pathlib import Path
import os,json,gzip,zipfile,tarfile,collections,shutil,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
protected=set(gzip.decompress((e/'cleanup-protected-tracked-paths.txt.gz').read_bytes()).decode().splitlines());actual=set();archives=[]
for root in [b,r/'artifacts']:
 for dp,dn,fn in os.walk(root):
  dn[:]=[n for n in dn if n!='.git']
  for n in fn:
   p=Path(dp)/n
   if p.is_symlink():continue
   st=p.stat()
   if str(p)not in protected and 0<st.st_size<4096:actual.add(str(p))
   if n.endswith(('.zip','.tar.gz')):archives.append(p)
records=[];errors=[];freed=0
def matched(p,data,arc,member,log):
 global freed
 if p.read_bytes()!=data:return
 st=p.stat();assert str(p)not in protected and not p.is_symlink()
 rec=dict(path=str(p),archive=str(arc),member=member,bytes=st.st_size,mode=st.st_mode,mtime_ns=st.st_mtime_ns,exact_bytes_verified=True,lastlink_blocks_reclaimed=st.st_blocks*512 if st.st_nlink==1 else 0)
 p.unlink();freed+=rec['lastlink_blocks_reclaimed'];records.append(rec);log.write(json.dumps(rec)+'\n')
with(e/'cleanup-small-archive-duplicates-direct.jsonl').open('w')as log:
 for arc in archives:
  try:
   if arc.suffix=='.zip':
    with zipfile.ZipFile(arc)as z:
     for m in z.infolist():
      if m.is_dir()or not 0<m.file_size<4096:continue
      paths=[p for p in {arc.parent/Path(m.filename.lstrip('./')),arc.parent.parent/Path(m.filename.lstrip('./')),r/Path(m.filename.lstrip('./')),b/Path(m.filename.lstrip('./'))}if str(p)in actual and p.exists()and p.stat().st_size==m.file_size]
      if paths:
       data=z.read(m)
       for p in paths:matched(p,data,arc,m.filename,log)
   else:
    with tarfile.open(arc,'r|gz')as t:
     for m in t:
      if not m.isfile()or not 0<m.size<4096:continue
      paths=[p for p in {arc.parent/Path(m.name.lstrip('./')),arc.parent.parent/Path(m.name.lstrip('./')),r/Path(m.name.lstrip('./')),b/Path(m.name.lstrip('./'))}if str(p)in actual and p.exists()and p.stat().st_size==m.size]
      if paths:
       data=t.extractfile(m).read()
       for p in paths:matched(p,data,arc,m.name,log)
  except (zipfile.BadZipFile,tarfile.TarError,OSError,EOFError)as ex:errors.append([str(arc),repr(ex)])
initial=[json.loads(l)for l in(e/'cleanup-small-archive-duplicates.jsonl').read_text().splitlines()]
freed+=sum(x['lastlink_blocks_reclaimed']for x in initial)
print('DIRECT_ARCHIVE_DONE',len(records),flush=True)
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),expanded_small_duplicate_files=len(records)+len(initial),reclaimed_lastlink_blocks_bytes=freed,unique_raw_lost=0,tracked_deleted=0,errors=errors,disk=shutil.disk_usage('/workspaces')._asdict())
(e/'cleanup-small-archive-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
