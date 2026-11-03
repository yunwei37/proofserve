from pathlib import Path
import os,json,gzip,tarfile,collections,shutil,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
protected=set(gzip.decompress((e/'cleanup-protected-tracked-paths.txt.gz').read_bytes()).decode().splitlines())
actual=collections.defaultdict(list);archives=[]
for root in [b,r/'artifacts']:
 for dp,dn,fn in os.walk(root):
  dn[:]=[n for n in dn if n!='.git']
  for n in fn:
   p=Path(dp)/n
   if p.is_symlink():continue
   st=p.stat()
   if str(p)not in protected and st.st_size>=4096:actual[(n,st.st_size)].append(p)
   if n.endswith('.tar.gz'):archives.append(p)
records=[];errors=[];freed=0;before=shutil.disk_usage('/workspaces')._asdict()
with(e/'cleanup-tar-duplicates.jsonl').open('w')as log:
 for arc in archives:
  try:
   with tarfile.open(arc,'r|gz')as tar:
    for m in tar:
     if not m.isfile()or m.size<4096:continue
     paths=[p for p in actual.get((Path(m.name).name,m.size),[])if p.exists()and p!=arc and str(p).endswith('/'+m.name.lstrip('./'))]
     if not paths:continue
     handles=[p.open('rb')for p in paths];same=[True]*len(paths);source=tar.extractfile(m)
     try:
      while True:
       x=source.read(1024*1024)
       for i,h in enumerate(handles):
        if h.read(len(x))!=x:same[i]=False
       if not x:break
     finally:
      for h in handles:h.close()
     for p,eq in zip(paths,same):
      if not eq:continue
      assert str(p)not in protected and not p.is_symlink()
      st=p.stat();rec=dict(path=str(p),archive=str(arc),member=m.name,bytes=st.st_size,mode=st.st_mode,mtime_ns=st.st_mtime_ns,exact_bytes_verified=True,lastlink_blocks_reclaimed=st.st_blocks*512 if st.st_nlink==1 else 0)
      p.unlink();freed+=rec['lastlink_blocks_reclaimed'];records.append(rec);log.write(json.dumps(rec)+'\n');log.flush()
  except (tarfile.TarError,OSError,EOFError)as ex:errors.append([str(arc),repr(ex)])
  print('TAR_PROGRESS',arc.name,len(records),freed,flush=True)
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),expanded_duplicate_files=len(records),reclaimed_lastlink_blocks_bytes=freed,unique_raw_bytes_lost=0,tracked_deleted=0,errors=errors,before=before,after=shutil.disk_usage('/workspaces')._asdict())
(e/'cleanup-tar-result.json').write_text(json.dumps(out,indent=2)+'\n');print('RESULT',json.dumps(out),flush=True)
