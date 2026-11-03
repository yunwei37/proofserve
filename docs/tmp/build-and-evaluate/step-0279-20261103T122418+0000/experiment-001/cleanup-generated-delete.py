from pathlib import Path
import os,json,gzip,collections,shutil,datetime,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
rows=json.loads(gzip.decompress((e/'cleanup-generated-candidates.json.gz').read_bytes()));targets={x['path']for x in rows}
roots=[Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery').resolve(),(r/'artifacts').resolve()]
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  for fd in list((pr/'fd').iterdir())+[pr/'exe',pr/'cwd']:
   try:assert os.readlink(fd).removesuffix(' (deleted)')not in targets,(pr.name,str(fd))
   except OSError:pass
  for line in(pr/'maps').read_text().splitlines():
   a=line.split(None,5)
   if len(a)==6:assert a[5]not in targets,(pr.name,a[5])
 except OSError:pass
before=shutil.disk_usage('/workspaces')._asdict();reclaimed=0;deleted=[]
with(e/'cleanup-generated-deleted.jsonl').open('w')as log:
 for x in rows:
  p=Path(x['path']);assert any(p.resolve().is_relative_to(z)for z in roots)and not p.is_symlink()
  st=p.stat();assert (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)==(x['dev'],x['ino'],x['bytes'],x['mtime_ns']),str(p)
  lastlink=st.st_nlink==1;p.unlink()
  if lastlink:reclaimed+=st.st_blocks*512
  log.write(json.dumps(dict(path=str(p),bytes=st.st_size,blocks=st.st_blocks*512,lastlink=lastlink,reason=x['reason']))+'\n')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deleted_files':len(rows),'lastlink_reclaimed_blocks_bytes':reclaimed,'before':before,'after':shutil.disk_usage('/workspaces')._asdict(),'raw_source_archives_deleted':0,'tracked_files_deleted':0,'active_conflicts':0}
(e/'cleanup-generated-result.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
