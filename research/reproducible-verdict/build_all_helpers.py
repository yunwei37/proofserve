from pathlib import Path
import os,json
import native
P=Path(__file__).resolve().parent
os.sched_setaffinity(0,set(range(8,16)))
commands=[
 [native.SDK/'bin/lean','--root='+str(P),'-o',P/'AllHelpers.olean','-c',P/'AllHelpers.c',P/'AllHelpers.lean'],
 ['cc','-O2','-I'+str(native.SDK/'include'),'-c',P/'thread_cpu.c','-o',P/'thread_cpu.o'],
 [native.SDK/'bin/leanc','-rdynamic','-O2','-o',P/'all-helpers',P/'AllHelpers.c',P/'thread_cpu.o']]
records=[]
for i,c in enumerate(commands):
 r=native.run('build-'+str(i),c,180,False);records.append(r)
 if r['returncode']:break
(P/'build-terminal.json').write_text(json.dumps(dict(complete=len(records)==3 and all(x['returncode']==0 for x in records),cells=records),indent=2))
