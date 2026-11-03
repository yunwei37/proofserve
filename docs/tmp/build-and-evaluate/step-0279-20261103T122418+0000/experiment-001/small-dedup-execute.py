from pathlib import Path
import os,json,gzip,shutil,datetime
os.sched_setaffinity(0,{22,23});s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001';rows=json.loads(gzip.decompress((e/'small-identical-preflight.json.gz').read_bytes()))
targets={x['path']for x in rows}
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  for fd in list((pr/'fd').iterdir())+[pr/'exe',pr/'cwd']:
   try:assert os.readlink(fd).removesuffix(' (deleted)')not in targets
   except OSError:pass
 except OSError:pass
freed=0;done=0
with(e/'small-identical-completed.jsonl').open('w')as log:
 for x in rows:
  p=Path(x['path']);q=Path(x['retained']);st=p.stat()
  assert(st.st_dev,st.st_ino,st.st_mtime_ns)==(x['dev'],x['ino'],x['mtime_ns'])
  assert p.read_bytes()==q.read_bytes()and not p.is_symlink()
  tmp=Path('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030')/('small-dedup0279-'+str(os.getpid()));assert not tmp.exists();os.link(q,tmp);os.replace(tmp,p)
  saved=st.st_blocks*512 if st.st_nlink==1 else 0;freed+=saved;done+=1
  log.write(json.dumps(dict(x,reclaimed_lastlink_blocks_bytes=saved))+'\n')
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),paths_preserved=done,reclaimed_lastlink_blocks_bytes=freed,unique_bytes_lost=0,tracked_touched=0,disk=shutil.disk_usage('/workspaces')._asdict())
(e/'small-identical-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
