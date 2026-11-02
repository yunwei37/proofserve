import os,json
from pathlib import Path
from native import run,ROOT,SDK,environment
os.sched_setaffinity(0,set(range(8,16)))
e=environment();e['LEAN_PATH']=str(ROOT)+':'+str(SDK/'lib/lean')
source=ROOT/'source'
commands=[
 [SDK/'bin/lean','--root='+str(source),'-o',ROOT/'ParallelCore.olean','-c',ROOT/'ParallelCore.c',source/'ParallelCore.lean'],
 ['cc','-O2','-I'+str(SDK/'include'),'-c',source/'checked_commit.c','-o',ROOT/'checked_commit.o'],
 ['cc','-O2','-I'+str(SDK/'include'),'-c',source/'placement_profile.c','-o',ROOT/'placement_profile.o'],
 [SDK/'bin/lean','--root='+str(source),'-c',ROOT/'ParallelStream.c',source/'ParallelStream.lean'],
 [SDK/'bin/leanc','-O2','-o',ROOT/'parallel-stream',ROOT/'ParallelStream.c',ROOT/'ParallelCore.c',ROOT/'checked_commit.o',ROOT/'placement_profile.o']]
cells=[]
for i,c in enumerate(commands):
 r=run('build-'+str(i),c,180,False,e);cells.append(r)
 (ROOT/'extended-build.json').write_text(json.dumps(cells,indent=2))
 if r['returncode']:raise RuntimeError('build failed '+str(i))
