"""One finite continuation after actual prior controller retirement.
Not a service/scheduler; no other lane/run is resumed.
"""
import os,sys,time,json,subprocess,contextlib,fcntl
from pathlib import Path
CAP=Path('/workspaces/.agent-state/gpu-smt-captures')
P=CAP/'parallel-stream-wall-20261103'
H=CAP/'parallel-stream-wall-hybrid-20261103'
B=CAP/'parallel-stream-barrier-corrected-20261103'
SDK=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
def main():
 assert json.loads((P/'matrix-terminal.json').read_text())['complete']
 built=json.loads((H/'extended-build-fixed2.json').read_text())
 assert len(built)==5 and all(c['returncode']==0 and c['native_retired']and c['cgroup_retired']for c in built)
 os.sched_setaffinity(0,set(range(8,16)))
 sys.path.insert(0,str(H));import native
 fixture=H/'fixtures'
 fixture_result=json.loads((H/'runs/build-complex-fixture-fixed/result.json').read_text())
 assert fixture_result['returncode']==0 and fixture_result['native_retired']
 # Same executable, corrected default mark; split flag is the only arm variable.
 sys.path.insert(0,str(P));import importlib.util
 spec=importlib.util.spec_from_file_location('wall_matrix',P/'matrix-v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 # Its ROOT/run/reader refer to H instead of P; unmodified original records retained.
 m.ROOT=H;m.run=native.run
 for split in[0,1]:
  for n in[1,8]:
   for bad in[False,True]:
    key='complex-control-s'+str(split)+'-P'+str(n)+('-bad'if bad else'')
    ee=m.runtime('math',n,True);ee['LEAN_PATH']=str(fixture)+':'+ee['LEAN_PATH'];ee['PARALLEL_SPLIT_COMPLEX']=str(split)
    if bad:ee['DECOUPLED_MUTATE_MODULE']='ComplexControl'
    m.launch(key,[H/'parallel-stream','parallel','bvar'if bad else'none','ComplexControl'],ee,2,bad)
 reference=json.loads((P/'diagnostic-terminal.json').read_text())['accepted_IDs']
 specs=[("diagnostic",1,True,[0,1])]+[("plain",rep,False,[1,0]if rep==2 else[0,1])for rep in[1,2,3]]
 for arm,rep,profile,order in specs:
  for split in order:
   key='hybrid-'+arm+'-P8-s'+str(split)+'-r'+str(rep)
   ee=m.runtime('barrier',8,profile,H/(key+'.jsonl')if profile else None);ee['PARALLEL_SPLIT_COMPLEX']=str(split)
   c=m.launch(key,[H/'parallel-stream','parallel','none',m.BARRIER],ee,4449)
   assert c['accepted_IDs']==reference
 # Old process-per-frontier program: original upstream replay/export/import/audit.
 native.ROOT=B;(B/'tmp').mkdir(exist_ok=True)
 ee=native.environment();ee['LEAN_PATH']=str(SDK/'lib/lean')
 commands=[
 ['cc','-O2','-I'+str(SDK/'include'),'-c',B/'source/checked_commit.c','-o',B/'checked_commit.o'],
 [SDK/'bin/lean','--root='+str(B/'source'),'-c',B/'ParallelReplay.c',B/'source/ParallelReplay.lean'],
 [SDK/'bin/leanc','-O2','-o',B/'parallel-replay',B/'ParallelReplay.c',B/'checked_commit.o']]
 for i,cmd in enumerate(commands):
  with(B/'build.log').open('a')as log,contextlib.redirect_stdout(log):c=native.run('build-'+str(i),cmd,180,False,ee)
  assert c['returncode']==0
 subprocess.run(['python3','-u',str(B/'driver.py')],cwd=B,check=True)
 (H/'continuation-terminal.json').write_text(json.dumps(dict(complete=True)))
if __name__=='__main__':main()
