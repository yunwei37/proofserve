# Untimed, serial E-core build; reuses SDK and immutable fd1e9be runtime sources.
import os,json
from native import ROOT,SDK,run,environment
os.sched_setaffinity(0,set(range(8,16)))
e=environment();e['LEAN_PATH']=str(ROOT)+':'+str(SDK/'lib/lean')
source=ROOT/'source'
commands=[
 [SDK/'bin/lean','--root='+str(source),'-o',ROOT/'ParallelCore.olean','-c',ROOT/'ParallelCore.c',source/'ParallelCore.lean'],
 ['cc','-O2','-I'+str(SDK/'include'),'-c',source/'checked_commit.c','-o',ROOT/'checked_commit.o'],
 ['cc','-O2','-I'+str(SDK/'include'),'-c',source/'placement_profile.c','-o',ROOT/'placement_profile.o'],
 ['cc','-O2','-I'+str(SDK/'include'),'-c',source/'persistence.c','-o',ROOT/'persistence.o'],
 [SDK/'bin/lean','--root='+str(source),'-c',ROOT/'ParallelStream.c',source/'ParallelStream.lean'],
 [SDK/'bin/leanc','-O2','-o',ROOT/'parallel-stream',ROOT/'ParallelStream.c',ROOT/'ParallelCore.c',ROOT/'checked_commit.o',ROOT/'placement_profile.o',ROOT/'persistence.o'],
 [SDK/'bin/lean','--root='+str(source),'-c',ROOT/'PersistenceProbe.c',source/'PersistenceProbe.lean'],
 [SDK/'bin/leanc','-O2','-o',ROOT/'persistence-probe',ROOT/'PersistenceProbe.c',ROOT/'ParallelCore.c',ROOT/'checked_commit.o',ROOT/'placement_profile.o',ROOT/'persistence.o']]
cells=[]
for i,argv in enumerate(commands):
 c=run('build-persistence-'+str(i),argv,180,False,e);cells.append(c)
 (ROOT/'build-results.json').write_text(json.dumps(cells,indent=2))
 if c['returncode']:raise RuntimeError('build failed; preserve step'+str(i))
print('BUILD_COMPLETE',flush=True)
