"""Read-only complete diagnostic analysis; per-run denominators only."""
import json,csv,collections,statistics
from pathlib import Path
CAP=Path('/workspaces/.agent-state/gpu-smt-captures')
P=CAP/'parallel-stream-wall-20261103'
OUT=Path(__file__).resolve().parent
def union(intervals):
 ans=[]
 for a,b in sorted(intervals):
  if ans and a<=ans[-1][1]:ans[-1][1]=max(ans[-1][1],b)
  else:ans.append([a,b])
 return ans
def overlap(intervals,a,b):
 return sum(max(0,min(y,b)-max(x,a))for x,y in intervals)
def analyze(raw=P,key="diagnostic",out=OUT,trace=None):
 P=Path(raw);OUT=Path(out);OUT.mkdir(parents=True,exist_ok=True)
 t=json.loads((P/(key+"-terminal.json")).read_text());assert t['qualified']
 ev=[json.loads(s)for s in(P/'runs'/key/'stdout').read_text().splitlines()if s.startswith('{')]
 assert sum(x.get('event')=='accept'for x in ev)==4449
 metrics={x['module']:x for x in ev if x.get('event')=='profile_module'}
 rows=[];module_rows=[];ph=collections.Counter();cur=None;waves=[];weights={}
 def finish():
  nonlocal cur,waves,weights
  if cur is None:return
  nodes=cur['nodes'];names={x['index']:x['name']for x in nodes}
  assert len(weights)==len(nodes),(cur['module'],len(weights),len(nodes))
  # Exact local DAG longest path under measured threadCPU node weights.
  dist={}
  for wave in waves:
   for idx,a,b,cpu in wave['jobs']:
    deps=nodes[idx]['dependencies']
    assert all(d in dist for d in deps)
    dist[idx]=cpu+max([dist[d]for d in deps]+[0])
  actual_span=max(dist.values(),default=0)
  m=metrics[cur['module']]['metrics']
  module_rows.append(dict(module=cur['module'],checks=len(nodes),waves=len(waves),
    kernel_cpu_s=sum(weights.values())/1e9,dag_span_s=actual_span/1e9,
    barrier_span_s=sum(max([j[3]for j in w['jobs']]+[0])for w in waves)/1e9,
    batch_s=int(m['batch_wall_ns'])/1e9))
  cur=None;waves=[];weights={}
 for line in(Path(trace) if trace else P/'barrier-wave-trace.jsonl').open():
  x=json.loads(line)
  if x['event']=='plan':finish();cur=x
  elif x['event']=='wave':
   assert cur is not None
   wave=x;waves.append(wave)
   q=wave['phase_ns'];assert q==sorted(q)
   intervals=union((j[1],j[2])for j in wave['jobs'])
   for idx,a,b,cpu in wave['jobs']:
    assert idx not in weights;weights[idx]=cpu
   kernel=sum(b-a for a,b in intervals)
   # Exclusive partition, handles one-worker checking before gate release.
   phases=dict(mark=q[1]-q[0],
     launch_no_kernel=q[2]-q[1]-overlap(intervals,q[1],q[2]),
     join_no_kernel=q[3]-q[2]-overlap(intervals,q[2],q[3]),
     validate=q[4]-q[3],commit=q[5]-q[4],kernel_active=kernel)
   # Kernel begins after marker and all tasks joined before validation.
   assert overlap(intervals,q[0],q[1])==0
   assert overlap(intervals,q[3],q[5])==0
   assert sum(phases.values())==q[5]-q[0]
   ph.update(phases)
   heavy=max(wave['jobs'],key=lambda j:j[3],default=None)
   rows.append(dict(module=cur['module'],wave_id=wave['id'],width=wave['width'],
     measured_window_s=(q[5]-q[0])/1e9,kernel_active_s=kernel/1e9,
     max_job_cpu_s=(heavy[3]if heavy else 0)/1e9,
     sum_job_cpu_s=sum(j[3]for j in wave['jobs'])/1e9,
     heaviest=cur['nodes'][heavy[0]]['name']if heavy else'',
     **{k+'_s':v/1e9 for k,v in phases.items()if k!='kernel_active'}))
 finish()
 total=collections.Counter()
 for x in ev:
  if x.get('event')=='dependency_phase':
   total['read_s']+=int(x['read_ns'])/1e9;total['context_s']+=int(x['context_ns'])/1e9
  elif x.get('event')=='profile_module':
   total['plan_s']+=int(x['plan_ns'])/1e9;total['fallback_s']+=int(x['fallback_ns'])/1e9
   total['batch_s']+=int(x['metrics']['batch_wall_ns'])/1e9
   total['checks']+=int(x['metrics']['checks']);total['units']+=int(x['metrics']['raw_HB'])
  elif x.get('event')=='serial_duplicate_phase':total['duplicate_s']+=int(x['wall_ns'])/1e9
 total['wall_s']=t['wall_s']
 total['unassigned_s']=t['wall_s']-sum(total[k]for k in['read_s','context_s','plan_s','fallback_s','batch_s','duplicate_s'])
 total.update({k+'_s':v/1e9 for k,v in ph.items()})
 total['batch_observer_tail_s']=total['batch_s']-sum(ph.values())/1e9
 total['dag_span_s']=sum(x['dag_span_s']for x in module_rows)
 total['barrier_span_s']=sum(x['barrier_span_s']for x in module_rows)
 total['fixed_outside_batch_s']=t['wall_s']-total['batch_s']
 total['conditional_current_barrier_floor_s']=total['fixed_outside_batch_s']+total['barrier_span_s']
 total['conditional_current_local_DAG_floor_s']=total['fixed_outside_batch_s']+total['dag_span_s']
 bins=collections.defaultdict(lambda:collections.Counter())
 for r in rows:
  width=r['width'];k='0'if width==0 else'1'if width==1 else'2–8'if width<=8 else'9–32'if width<=32 else'33–128'if width<=128 else'>128'
  b=bins[k];b['waves']+=1;b['jobs']+=width
  for f in['measured_window_s','max_job_cpu_s','sum_job_cpu_s','kernel_active_s']:b[f]+=r[f]
 for name,data in [('diagnostic-modules.csv',module_rows),('wave-width-bins.csv',[dict(width=k,**v)for k,v in bins.items()]),('heaviest-waves.csv',sorted(rows,key=lambda r:-r['measured_window_s'])[:40])]:
  with(OUT/name).open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 (P/(key+'-wave-analysis.json')).write_text(json.dumps(rows))
 (OUT/'diagnostic-summary.json').write_text(json.dumps(dict(total=total,method='C interval clocks; fixed measured service costs; local module DAG, serial module order retained'),indent=2))
 print(json.dumps(total,indent=2));print('BINS',dict(bins))
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument("--raw",default=str(P));a.add_argument("--key",default="diagnostic")
 a.add_argument("--out",default=str(OUT));a.add_argument("--trace")
 args=a.parse_args();analyze(args.raw,args.key,args.out,args.trace)
