from pathlib import Path
import os,json,gzip,collections,shutil,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
protected=set(gzip.decompress((e/'cleanup-protected-tracked-paths.txt.gz').read_bytes()).decode().splitlines());groups={};rows=[]
for root in [b,r/'artifacts']:
 for dp,dn,fn in os.walk(root):
  dn[:]=[n for n in dn if n!='.git']
  for n in fn:
   p=Path(dp)/n
   if str(p)in protected or p.is_symlink():continue
   st=p.stat()
   if not 0<st.st_size<4096 or st.st_blocks==0:continue
   k=(st.st_size,st.st_mode,st.st_uid,st.st_gid,p.read_bytes())
   if k not in groups:groups[k]=(str(p),st.st_dev,st.st_ino);continue
   q,dev,ino=groups[k]
   if(st.st_dev,st.st_ino)==(dev,ino):continue
   rows.append(dict(path=str(p),retained=q,bytes=st.st_size,dev=st.st_dev,ino=st.st_ino,mtime_ns=st.st_mtime_ns,mode=st.st_mode,nlink=st.st_nlink,blocks=st.st_blocks*512))
(e/'small-identical-preflight.json.gz').write_bytes(gzip.compress(json.dumps(rows).encode()))
print(dict(unique_small_contents=len(groups),duplicate_paths=len(rows),potential_bytes=sum(x['blocks']for x in rows if x['nlink']==1)),flush=True)
