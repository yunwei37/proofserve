from pathlib import Path
import json,csv,collections,statistics,math
def csvout(path,rows):
 if not rows:return
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read_events(path):
 return [json.loads(s) for s in path.read_text().splitlines() if s.startswith('{')]
def fit(rows):
 x=[1/r['workers'] for r in rows];y=[r['wall_s'] for r in rows]
 mx=statistics.mean(x);my=statistics.mean(y)
 p=sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x);s=my-p*mx
 residuals=[b-(s+p*a) for a,b in zip(x,y)]
 return dict(S_s=s,P_s=p,effective_serial_fraction=s/(s+p),RMSE_s=math.sqrt(statistics.mean(v*v for v in residuals)),
  points=[dict(workers=r['workers'],observed_s=r['wall_s'],predicted_s=s+p/r['workers'],residual_s=d) for r,d in zip(rows,residuals)],
  caveat='effective fit includes algorithm/observer overhead; not an inherent serial fraction; single-run points')
def analyze(point,out):
 out.mkdir(exist_ok=True,parents=True)
 full=[];cores=[];workers=[];phases=[]
 for phase in ['p12','p48','types','observer']:
  f=point/(phase+'-results.json')
  if not f.exists():continue
  for c in json.loads(f.read_text()):
   if c['returncode'] or not c.get('complete_events') or not c['accepted_set_equal_to_serial']:continue
   name=c['key'].removeprefix('full-');ev=read_events(point/'runs'/c['key']/'stdout')
   row=dict(name=name,workers=len(c['worker_pins']),profile=c['profile_enabled'],worker_pins=c['worker_pins'],
    coordinator_cpu=c['coordinator_cpu'],wall_s=c['wall_s'],CPU_s=c['user_s']+c['system_s'],
    peak_RSS_MiB=c['peak_rss_kib']/1024,accepted_modules=len(c['accepted_IDs']))
   full.append(row)
   if not c['profile_enabled']:continue
   dep=sum(int(e['read_ns'])+int(e['context_ns']) for e in ev if e.get('event')=='dependency_phase')/1e9
   mods=[e for e in ev if e.get('event')=='profile_module']
   plan=sum(int(e['plan_ns']) for e in mods)/1e9
   fallback=sum(int(e['fallback_ns']) for e in mods)/1e9
   dup=sum(int(e['wall_ns']) for e in ev if e.get('event')=='serial_duplicate_phase')/1e9
   union=sum(int(e['metrics']['kernel_union_ns']) for e in mods)/1e9
   batch=sum(int(e['metrics']['batch_wall_ns']) for e in mods)/1e9
   kernel_cpu=sum(int(e['metrics']['kernel_cpu_ns']) for e in mods)/1e9
   batch_cpu=sum(int(e['metrics']['batch_cpu_ns']) for e in mods)/1e9
   serial=dep+plan+fallback+dup;remaining=c['wall_s']-serial-union
   phases.append(dict(name=name,workers=row['workers'],read_context_s=dep,plan_s=plan,upstream_serial_kernel_s=fallback,
    serial_duplicate_s=dup,implementation_serial_s=serial,parallel_kernel_occupancy_s=union,
    overhead_residual_s=remaining,batch_wall_s=batch,batch_non_kernel_wall_s=batch-union,
    other_residual_s=remaining-(batch-union),kernel_CPU_s=kernel_cpu,batch_CPU_s=batch_cpu,
    batch_non_kernel_CPU_s=batch_cpu-kernel_cpu,process_wall_s=c['wall_s']))
   core=collections.defaultdict(lambda:collections.Counter())
   th=collections.defaultdict(lambda:collections.Counter())
   for m in mods:
    for w in m['metrics']['workers']:
     for key in ['checks','cpu_ns','raw_HB','narrow_checks','narrow_HB','within_check_migrations']:
      core[int(w['cpu'])][key]+=int(w[key]);th[(w['tid'],w['cpu'])][key]+=int(w[key])
   for cpu,counts in sorted(core.items()):
    seconds=counts['cpu_ns']/1e9
    cores.append(dict(name=name,cpu=cpu,core_type='P' if cpu<8 else 'E',checks=counts['checks'],kernel_CPU_s=seconds,
     raw_HB=counts['raw_HB'],checks_per_active_CPU_s=counts['checks']/seconds if seconds else None,
     HB_per_active_CPU_s=counts['raw_HB']/seconds if seconds else None,
     kernel_core_utilization=seconds/c['wall_s'],narrow_checks=counts['narrow_checks'],
     narrow_HB=counts['narrow_HB'],within_check_migrations=counts['within_check_migrations']))
   for (tid,cpu),counts in sorted(th.items()):
    workers.append(dict(name=name,TID=tid,cpu=cpu,core_type='P' if cpu<8 else 'E',**counts))
 csvout(out/'full-cells.csv',full);csvout(out/'phase-ledger.csv',phases)
 csvout(out/'per-core-throughput.csv',cores);csvout(out/'worker-placement.csv',workers)
 selected=[next((r for r in full if r['name']=='P'+str(n)),None) for n in [1,2,4,8]]
 if all(selected):(out/'fixed-serial-fit.json').write_text(json.dumps(fit(selected),indent=2))
 f=point/'det24-terminal.json'
 if f.exists():
  t=json.loads(f.read_text());ev=read_events(point/'runs/hardware-leaf/stdout');current=None
  units=[];curves=[];stats=[];by=collections.defaultdict(list)
  for e in ev:
   if e.get('event')=='curve_begin':current=(e['kind'],e['repeat'])
   elif e.get('event')=='unit_check':
    kind,rep=current;units.append(dict(kind=kind,repeat=rep,target=e['target'],HB=int(e['raw_HB']),CPU_ns=int(e['cpu_ns']),cpu=e['cpu'],TID=e['tid'],accepted=e['accept']))
   elif e.get('event')=='curve_cell':curves.append(e)
   elif e.get('event')=='profile_module' and e['module'].endswith('BarrierData41') and current is not None:stats.append(dict(kind=current[0],repeat=current[1],metrics=e['metrics']))
  for r in units:by[r['target']].append(r)
  ranges=[]
  for target,rr in sorted(by.items()):
   h=[r['HB'] for r in rr]
   ranges.append(dict(target=target,observations=len(rr),min_HB=min(h),max_HB=max(h),range_pct=100*(max(h)-min(h))/min(h)))
  summary=dict(state=t['state'],native_returncode=t['cells'][0]['returncode'],targets=len(by),observations=len(units),
   zero_range_targets=sum(r['range_pct']==0 for r in ranges),all_accepted=all(r['accepted'] for r in units),
   complete_coverage=len(by)==50 and all(len(rr)==9 and len({(r['kind'],r['repeat']) for r in rr})==9 for rr in by.values()),
   artifacts=json.loads((point/'hardware-artifacts.json').read_text()) if (point/'hardware-artifacts.json').exists() else None)
  csvout(out/'hardware-target-ranges.csv',ranges);csvout(out/'hardware-units.csv',units)
  csvout(out/'hardware-leaf-cells.csv',curves)
  med=[]
  for kind in ['p1','e1','mixed24']:
   rr=[e for e in curves if e['kind']==kind]
   if not rr:continue
   cpu=[sum(r['CPU_ns'] for r in units if r['kind']==kind and r['repeat']==rep)/1e9 for rep in range(3)]
   med.append(dict(kind=kind,median_wall_s=statistics.median(int(r['elapsed_ns'])/1e9 for r in rr),
    min_wall_s=min(int(r['elapsed_ns'])/1e9 for r in rr),max_wall_s=max(int(r['elapsed_ns'])/1e9 for r in rr),
    median_CPU_s=statistics.median(int(r['cpu_ns'])/1e9 for r in rr),sample50_kernel_CPU_median_s=statistics.median(cpu)))
  csvout(out/'hardware-leaf-summary.csv',med)
  if len(med)==3:summary['E_vs_P_sampled_kernel_work_rate']=med[0]['sample50_kernel_CPU_median_s']/med[1]['sample50_kernel_CPU_median_s']
  (out/'hardware-determinism.json').write_text(json.dumps(summary,indent=2))
 return full,phases
if __name__=='__main__':
 import sys
 rows,ph=analyze(Path(sys.argv[1]),Path(sys.argv[2]));print(json.dumps(dict(full_cells=len(rows),phase_rows=len(ph))))
