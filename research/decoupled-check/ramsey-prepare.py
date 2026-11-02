#!/usr/bin/env python3
"""Prepare the exact Ramsey subtree and an official producer namespace, not replay metadata."""
import os,json,tarfile,shutil
from pathlib import Path
os.sched_setaffinity(0,{8})
B=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
O=B/'whole-library-20261102';A=B/'ramsey-20261102';A.mkdir(exist_ok=True)
frame=json.loads((O/'frame.json').read_text())
targets=[v for v in frame if v['cohort']=='OAI.Combinatorics.Ramsey']
assert len(targets)==444
controls=['lean/ComparatorChallenges/AbhyankarSathaye.lean','lean/ComparatorChallenges/AffineBernstein.lean','lean/ComparatorChallenges/AlgorithmicThinTrees.lean','lean/OAI/Computability/BinPacking/Games/RepetitionUpper.lean']
wanted={v['path']:v['bytes']for v in targets}
for p in controls:wanted[p]=None
archive=Path('/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz')
done=set()
with tarfile.open(archive,'r|gz',stream=True)as tar:
 for member in tar:
  path=member.name.partition('/')[2]
  if not member.isfile()or path not in wanted:continue
  if wanted[path]is not None:assert member.size==wanted[path]
  dest=A/'sources'/path;dest.parent.mkdir(parents=True,exist_ok=True)
  with tar.extractfile(member)as inp,dest.open('wb')as out:shutil.copyfileobj(inp,out)
  done.add(path)
assert done==set(wanted)
(A/'ramsey-targets.json').write_text(json.dumps(targets,indent=2))
names={v['module']for v in targets}
external=sorted({q for v in targets for q in v['imports']if q not in names})
(A/'external-roots.json').write_text(json.dumps(external,indent=2))
old=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json')
providers=[Path(p)for p in json.loads(old.read_text())['lean_path'].split(':')if p]
providers=[p for p in providers if not any(q in str(p)for q in ['repair-v3/oleans','rellich4341-oleans','openai4341-oleans'])]
lib=A/'producer-ai';lib.mkdir(exist_ok=True)
(A/'external-roots.txt').write_text('\n'.join(external)+'\n')
# Keep exact official SDK/cache module providers for production. Never overlay
# rebuilt Init/Std/Lean/Lake parts; recompiled terms go only to check-lib.
for v in targets:
 for dep in v['imports']:
  if dep not in names:assert any(p.joinpath(*dep.split('.')).with_suffix('.olean').exists()for p in providers),dep
(A/'prepare.json').write_text(json.dumps(dict(source_pin='4eaee87548250b2682affda7d05d947c05554bae',
 targets=444,extracted_files=len(done),target_source_bytes=sum(v['bytes']for v in targets),
 external_roots=len(external),production_providers=list(map(str,providers)),
 protected_core_namespaces=['Init','Std','Lean','Lake'],timed=False),indent=2))
print((A/'prepare.json').read_text())
