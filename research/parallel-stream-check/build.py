"""Untimed E-core qualification build; launch only after own native run retires."""
import os,shutil,json
from pathlib import Path
from native import run,SDK,ROOT,environment
os.sched_setaffinity(0,set(range(8,16)))
source=ROOT/'source'
assets=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets/all-envelope')
prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
e=environment();e.update(LEAN_PATH=str(ROOT)+':'+str(assets)+':'+str(assets.parent/'overlay-complete-v2')+':'+prep['lean_path'],
 PARALLEL_PREPARED_OUT=str(assets))
commands=[
 [SDK/'bin/lean','--root='+str(source),'-o',ROOT/'ParallelCore.olean','-c',ROOT/'ParallelCore.c',source/'ParallelCore.lean'],
 ['cc','-O2','-I'+str(SDK/'include'),'-c',source/'checked_commit.c','-o',ROOT/'checked_commit.o'],
 [SDK/'bin/lean','--root='+str(source),'-c',ROOT/'ParallelStream.c',source/'ParallelStream.lean'],
 [SDK/'bin/leanc','-O2','-o',ROOT/'parallel-stream',ROOT/'ParallelStream.c',ROOT/'ParallelCore.c',ROOT/'checked_commit.o'],
 [SDK/'bin/lean','--root='+str(assets),'-o',assets/'EnvelopeStreamBase.olean',assets/'EnvelopeStreamBase.lean'],
 [SDK/'bin/lean','--root='+str(source),source/'PrepareChunks.lean']]
for i,c in enumerate(commands):
 result=run('build-'+str(i),c,180,False,e)
 if result['returncode']:raise RuntimeError('build failed '+str(i))
shutil.copy2(assets.parent/'envelope/reference.olean',assets/'reference.olean')
for suffix in ['.server','.private']:
 p=Path(str(assets.parent/'envelope/reference.olean')+suffix)
 if p.exists():shutil.copy2(p,str(assets/'reference.olean')+suffix)
(ROOT/'build-qualified.json').write_text(json.dumps(dict(binary=str(ROOT/'parallel-stream'),
 schemas=len(json.loads((assets/'schemas.json').read_text())['specs']),
 prepared_payload='untrusted; not a kernel acceptance result')))
