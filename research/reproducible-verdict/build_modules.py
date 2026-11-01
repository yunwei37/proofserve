from pathlib import Path
import os,json
import native
P=Path(__file__).resolve().parent
os.sched_setaffinity(0,set(range(8,16)))
commands=[
 [native.SDK/'bin/lean','--root='+str(P),'-o',P/'ModuleProbe.olean','-c',P/'ModuleProbe.c',P/'ModuleProbe.lean'],
 ['cc','-O2','-I'+str(native.SDK/'include'),'-c',P/'thread_cpu.c','-o',P/'thread_cpu.o'],
 [native.SDK/'bin/leanc','-rdynamic','-O2','-o',P/'module-probe',P/'ModuleProbe.c',P/'thread_cpu.o']]
records=[]
for i,argv in enumerate(commands):
 r=native.run('build-v4-'+str(i),argv,180,False);records.append(r)
 if r['returncode']:break
(P/'build-v4-terminal.json').write_text(json.dumps(dict(complete=len(records)==3 and all(x['returncode']==0 for x in records),cells=records),indent=2))
