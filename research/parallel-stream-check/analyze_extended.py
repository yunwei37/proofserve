from pathlib import Path
import csv,json,collections,statistics,math
def writecsv(path,rows):
 if not rows:return
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def analyze(point,out):
 out.mkdir(parents=True,exist_ok=True)
 if (point/'scaling-terminal.json').exists():
  t=json.loads((point/'scaling-terminal.json').read_text())
  rows=[];phase_rows=[]
  for c in t['cells']:
   ev=[json.loads(line) for line in (point/'runs'/c['key']/'stdout').read_text().splitlines() if line.startswith('{')]
   durations=collections.defaultdict(float);counts=collections.Counter()
   for event in ev:
    if event.get('event')=='kernel_work':
     durations[event['path']]+=int(event['elapsed_ns'])/1e9;counts[event['path']]+=1
   measured_sum=sum(durations.values())
   for route,seconds in durations.items():
    phase_rows.append(dict(workers=int(c['key'].split('j')[-1]),route=route,modules=counts[route],
     wall_s=seconds,process_wall_fraction=seconds/c['wall_s']))
   phase_rows.append(dict(workers=int(c['key'].split('j')[-1]),route='outside_recorded_kernel_work',modules=0,
    wall_s=c['wall_s']-measured_sum,process_wall_fraction=(c['wall_s']-measured_sum)/c['wall_s']))
   workers=int(c['key'].split('j')[-1])
   rows.append(dict(workers=workers,P_cores=8,E_cores=workers-8,allowed_cpus=','.join(map(str,c['affinity'])),
    wall_s=c['wall_s'],user_s=c['user_s'],system_s=c['system_s'],CPU_s=c['user_s']+c['system_s'],
    mean_cores=(c['user_s']+c['system_s'])/c['wall_s'],peak_RSS_MiB=c['peak_rss_kib']/1024,
    accepted_modules=len(c.get('accepted_IDs',[])),same_accepted_set=c.get('accepted_set_equal_to_serial'),
    returncode=c['returncode'],native_retired=c['native_retired'],cgroup_retired=c.get('cgroup_retired',False)))
  if rows:
   base=next((r for r in rows if r['workers']==8),None)
   if base:
    for r in rows:r['speedup_vs_8P']=base['wall_s']/r['wall_s'];r['CPU_ratio_vs_8P']=r['CPU_s']/base['CPU_s']
   writecsv(out/'heterogeneous-scaling.csv',rows)
   writecsv(out/'scaling-paths.csv',phase_rows)
  (out/'scaling-status.json').write_text(json.dumps(dict(state=t['state'],error=t['error'],cells=len(rows)),indent=2))
 if (point/'determinism-terminal.json').exists():
  t=json.loads((point/'determinism-terminal.json').read_text())
  source=point/'runs/barrier-determinism/stdout'
  current=None;units=[];curves=[];snapshots=[]
  for line in source.read_text().splitlines():
   if not line.startswith('{'):continue
   r=json.loads(line);event=r.get('event')
   if event=='curve_begin':current=(int(r['kind'].removeprefix('parallel')),r['repeat'])
   elif event=='unit_check':
    if current is None:raise ValueError('unit outside curve')
    units.append(dict(workers=current[0],repeat=current[1],target=r['target'],raw_HB=int(r['raw_HB']),
     CPU_ns=int(r['cpu_ns']),TID=r['tid'],accepted=r['accept']))
   elif event=='curve_cell':curves.append(r)
   elif event=='snapshot':snapshots.append(r)
  groups=collections.defaultdict(list)
  for r in units:groups[r['target']].append(r)
  coverage=[]
  for target,rr in sorted(groups.items()):
   if len(rr)!=12 or len({(r['workers'],r['repeat']) for r in rr})!=12:
    raise ValueError('incomplete deterministic target '+target)
   h=[r['raw_HB'] for r in rr]
   z=dict(target=target,observations=12,min_raw_HB=min(h),max_raw_HB=max(h),
    range_pct=100*(max(h)-min(h))/min(h) if min(h) else None,all_accepted=all(r['accepted'] for r in rr))
   for j in [1,4,8,16]:
    hh=[r['raw_HB'] for r in rr if r['workers']==j];z['j'+str(j)+'_min']=min(hh);z['j'+str(j)+'_max']=max(hh)
   coverage.append(z)
  ranges=sorted(r['range_pct'] for r in coverage if r['range_pct'] is not None)
  status=dict(state=t['state'],error=t['error'],targets=len(groups),observations=len(units),curves=len(curves),
   zero_range_targets=sum(r['range_pct']==0 for r in coverage),
   P95_range_pct=ranges[math.ceil(.95*len(ranges))-1] if ranges else None,max_range_pct=max(ranges) if ranges else None,
   all_accepted=bool(units) and all(r['accepted'] for r in units),complete_coverage=len(groups)==100 and len(units)==1200 and len(curves)==12,snapshot_events=len(snapshots),
   artifacts=json.loads((point/'determinism-artifacts.json').read_text()) if (point/'determinism-artifacts.json').exists() else None)
  (out/'determinism-status.json').write_text(json.dumps(status,indent=2))
  writecsv(out/'parallel-target-heartbeats.csv',coverage)
  writecsv(out/'parallel-observations.csv',units)
  writecsv(out/'resident-leaf-cells.csv',[dict(workers=r['workers'],repeat=r['repeat'],wall_s=int(r['elapsed_ns'])/1e9,
    CPU_s=int(r['cpu_ns'])/1e9,jobs=r['jobs'],waves=r['waves'],route=r['route']) for r in curves])
  writecsv(out/'checked-artifacts.csv',snapshots)
 return 'analysis complete'
if __name__=='__main__':
 import sys
 print(analyze(Path(sys.argv[1]),Path(sys.argv[2])))
