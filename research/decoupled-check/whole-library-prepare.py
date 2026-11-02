#!/usr/bin/env python3
"""Untimed pinned-input preparation; never counts source inventory as accepted terms."""
import csv,gzip,json,os,re,tarfile,shutil,graphlib
from pathlib import Path
os.sched_setaffinity(0,{8})
R=Path('/workspaces/repository')
B=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
F=B/'scale-study/falconer-project-20261101'
O=B/'whole-library-20261102'
INV=R/'workloads/openai-math/static-4eaee875'
GROUPS=['OAI.Combinatorics.Ramsey','OAI.Analysis.MutuallyUnbiased','OAI.Analysis.PlanarPacking','OAI.MathematicalPhysics.Transonic','OAI.Algorithms.SubexponentialSAT']
def atomic(p,v):
 t=p.with_suffix('.pending')
 with t.open('w')as f:json.dump(v,f,indent=2);f.flush();os.fsync(f.fileno())
 t.replace(p)
def name(path,roots):
 root=max((x for x in roots if path.startswith(x+'/')),key=len)
 return path[len(root)+1:-5].replace('/','.')
def main():
 O.mkdir(exist_ok=True)
 if(O/'prepared.json').exists():print('already prepared');return
 meta=json.loads((INV/'upstream-metadata.json').read_text())
 roots=['lean']+['lean/'+x for x in re.findall(r'srcDir\s*:=\s*"([^"]+)"',meta['lean/lakefile.lean'])]
 inventory=list(csv.DictReader(gzip.open(INV/'files.csv.gz','rt')))
 bypath={x['path']:x for x in inventory}
 rows={name(x['path'],roots):dict(module=name(x['path'],roots),path=x['path'],bytes=int(x['size']),
       source_root=max((q for q in roots if x['path'].startswith(q+'/')),key=len))for x in inventory}
 assert len(rows)==len(inventory)==163097
 for m,v in rows.items():
  v['cohort']=next((g for g in GROUPS if m==g or m.startswith(g+'.')),'remainder');v['imports']=[]
 with gzip.open(INV/'content/imports.csv.gz','rt')as f:
  for x in csv.DictReader(f):rows[x['module']]['imports'].append(x['imports'])
 order=list(graphlib.TopologicalSorter({m:{q for q in x['imports']if q in rows}for m,x in rows.items()}).static_order())
 atomic(O/'frame.json',[rows[m]for m in order])
 count=0;source=O/'sources'
 archive=Path('/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz')
 with tarfile.open(archive,'r|gz',stream=True)as tar:
  for member in tar:
   if not member.isfile():continue
   path=member.name.partition('/')[2]
   if path not in bypath:continue
   assert member.size==int(bypath[path]['size'])
   dest=source/path;dest.parent.mkdir(parents=True,exist_ok=True)
   if dest.exists():assert dest.stat().st_size==member.size
   else:
    temp=dest.with_suffix('.partial')
    with tar.extractfile(member)as inp,temp.open('wb')as out:shutil.copyfileobj(inp,out)
    temp.replace(dest)
   count+=1
   if count%10000==0:print('extracted',count,flush=True)
 assert count==163097
 old=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json')
 providers=[Path(p)for p in json.loads(old.read_text())['lean_path'].split(':')if p]
 providers=[p for p in providers if not any(x in str(p)for x in ['repair-v3/oleans','rellich4341-oleans','openai4341-oleans'])]
 providers=list(dict.fromkeys(providers+[B/'constructed/lib',F/'constructed/lib']))
 lib=O/'lib';lib.mkdir(exist_ok=True)
 linked=[]
 for provider in providers:
  n=0
  for root,dirs,files in os.walk(provider):
   for file in files:
    if not file.endswith(('.olean','.olean.server','.olean.private','.ir')):continue
    src=Path(root)/file;dest=lib/src.relative_to(provider);dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():dest.unlink() # Owned overlay link only; providers stay immutable.
    os.link(src,dest);n+=1
  linked.append(dict(path=str(provider),links=n))
 def available(m):return lib.joinpath(*m.split('.')).with_suffix('.olean').exists()
 ready={m for m in rows if available(m)}
 external=sorted({q for x in rows.values()for q in x['imports']if q not in rows and not available(q)})
 shutil.copy2(F/'checkpoint-recheck-v2/checkpoint-audit',O/'checkpoint-audit')
 shutil.copyfile(F/'checkpoint-recheck-v2/CheckpointAudit.lean',O/'CheckpointAudit.lean')
 runner=(F/'native_project.py').read_text()
 assert '12*1024**3-256*1024**2'in runner
 (O/'native_whole.py').write_text(runner.replace('12*1024**3-256*1024**2','12*1024**3-512*1024**2'))
 (O/'initial-artifact-modules.txt').write_text('\n'.join(sorted(ready))+'\n')
 atomic(O/'prepared.json',dict(source_revision='4eaee87548250b2682affda7d05d947c05554bae',
   source_modules=len(rows),source_files_extracted=count,source_bytes=sum(int(x['size'])for x in inventory),
   initial_available_source_artifacts=len(ready),initial_missing_source_artifacts=len(rows)-len(ready),
   unresolved_external_imports=external,providers=linked,free_bytes=shutil.disk_usage(O).free))
 print(json.dumps(json.loads((O/'prepared.json').read_text()),indent=2),flush=True)
if __name__=='__main__':main()
