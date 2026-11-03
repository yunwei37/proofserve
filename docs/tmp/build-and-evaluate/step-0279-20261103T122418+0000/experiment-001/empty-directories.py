from pathlib import Path
import os,json,gzip,datetime,shutil
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
rows=[];freed=0
for root in [b,r/'artifacts']:
 for dp,dn,fn in os.walk(root,topdown=False):
  p=Path(dp)
  if p==root or '.git'in p.parts:continue
  if not any(p.iterdir()):
   st=p.stat();assert p.resolve().is_relative_to(root.resolve());p.rmdir();freed+=st.st_blocks*512
   rows.append(dict(path=str(p),blocks=st.st_blocks*512,mode=st.st_mode,mtime_ns=st.st_mtime_ns,reason='empty retired intermediate directory after verified file cleanup; no data files removed'))
(e/'cleanup-empty-directories.json.gz').write_bytes(gzip.compress(json.dumps(rows).encode()))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),removed_empty_directories=len(rows),reclaimed_directory_blocks_bytes=freed,disk=shutil.disk_usage('/workspaces')._asdict());(e/'cleanup-empty-directories-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
