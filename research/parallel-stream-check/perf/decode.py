"""Offline CPU8-15 analysis; <=14GiB guard, serial relative to own native."""
import json,os,sys,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
assert str(P).startswith('/workspaces/.agent-state/gpu-smt-captures/')
assert set(os.sched_getaffinity(0))<=set(range(8,16))
import native as decode_guard
def main():
 key=sys.argv[1]
 assert key.startswith('full-record-') and '/' not in key
 terminal=P/(key+'-terminal.json')
 t=json.loads(terminal.read_text());assert t['state']=='complete'
 data=P/(key+'.perf.data');assert data.exists()
 out=P/('decode-'+key);assert not out.exists();out.mkdir()
 env=dict(os.environ,DEBUGINFOD_URLS='',PERF_ANALYSIS_OUT=str(out),PERF_NATIVE_TERMINAL=str(terminal))
 cmds=[
  ('attrs',['perf','evlist','-v','-i',str(data)]),
  ('read-times',['python3',str(P/'read_times.py'),str(data),str(out)]),
  ('inventory',['perf','report','--stdio','--stats','-i',str(data)]),
  ('thread-counters',['perf','report','--stdio','-T','-g','none','--no-children','--percent-limit','100','-i',str(data)]),
  ('samples',['perf','script','--demangle','--max-stack','512','-i',str(data),'-s',str(P/'perf_samples.py')])]
 for label,cmd in cmds:
  c=decode_guard.run('decode-'+key+'-'+label,cmd,1100,False,env)
  shutil.copyfile(P/'runs'/('decode-'+key+'-'+label)/'stdout',out/(label+'.txt'))
  if label=='read-times' and c['returncode']:
   print('AUX_READ_FIELDS_FAILED_PRESERVED',key,flush=True);continue
  if c['returncode'] or c['stop_reasons'] or not c['cgroup_retired']:
   raise RuntimeError('decode incomplete; preserve outputs')
 print('DECODE_COMPLETE',key,flush=True)
if __name__=='__main__':main()
