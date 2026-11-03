from pathlib import Path
import os,subprocess,json,gzip,collections,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
protected=set(gzip.decompress((e/'cleanup-protected-tracked-paths.txt.gz').read_bytes()).decode().splitlines())
sizes=collections.defaultdict(list);cnt=0
for root in [b,r/'artifacts']:
 for dp,dn,fn in os.walk(root):
  dn[:]=[n for n in dn if n!='.git']
  for n in fn:
   p=Path(dp)/n
   if str(p)in protected or p.is_symlink():continue
   st=p.stat()
   if st.st_size>=4096:sizes[st.st_size].append((str(p),st.st_dev,st.st_ino,st.st_blocks*512,st.st_nlink,st.st_mtime_ns));cnt+=1
groups=[];potential=0
for size,rows in sizes.items():
 unique={}
 for x in rows:unique.setdefault((x[1],x[2]),x)
 rows=list(unique.values())
 if len(rows)<2:continue
 quick=collections.defaultdict(list)
 for x in rows:
  with open(x[0],'rb')as f:
   head=f.read(4096);f.seek(max(0,size-4096));tail=f.read(4096)
  quick[(head,tail)].append(x)
 for arr in quick.values():
  if len(arr)>1:groups.append(dict(bytes=size,paths=arr));potential+=sum(x[3]for x in arr[1:]if x[4]==1)
(e/'duplicate-preflight-groups.json.gz').write_bytes(gzip.compress(json.dumps(groups).encode()))
print('DUP_PREFLIGHT',dict(files=cnt,groups=len(groups),potential_reclaim=potential,GiB=potential/1024**3),flush=True)
print('TOP_GROUPS',[(g['bytes'],len(g['paths']),[x[0]for x in g['paths'][:2]])for g in sorted(groups,key=lambda g:g['bytes']*len(g['paths']),reverse=True)[:12]])
