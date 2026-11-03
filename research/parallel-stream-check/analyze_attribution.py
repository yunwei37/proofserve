from pathlib import Path
import json,csv,collections,statistics,math,re
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
 full=[];cores=[];workers=[];phases=[];module_work={}
 for phase in ['p12','p48','types','observer','placement']:
  f=point/(phase+'-results.json')
  if not f.exists():continue
  for c in json.loads(f.read_text()):
   if (c['returncode'] or not c.get('complete_events') or not c['accepted_set_equal_to_serial']
    or len(c['accepted_IDs'])!=4449 or len(set(c['accepted_IDs']))!=4449
    or not c.get('native_retired') or not c.get('cgroup_retired') or c.get('stop_reasons')):continue
   name=c['key'].removeprefix('full-');ev=read_events(point/'runs'/c['key']/'stdout')
   requested=int(re.match(r'^[PEM](\d+)',name).group(1))
   assert not c['worker_pins'] or len(c['worker_pins'])==requested
   row=dict(name=name,workers=requested,profile=c['profile_enabled'],worker_pins=c['worker_pins'],
    coordinator_cpu=c['coordinator_cpu'],wall_s=c['wall_s'],CPU_s=c['user_s']+c['system_s'],
    peak_RSS_MiB=c['peak_rss_kib']/1024,accepted_modules=len(c['accepted_IDs']))
   full.append(row)
   if not c['profile_enabled']:continue
   dep=sum(int(e['read_ns'])+int(e['context_ns']) for e in ev if e.get('event')=='dependency_phase')/1e9
   mods=[e for e in ev if e.get('event')=='profile_module']
   module_work[name]={e['module']:e['metrics'] for e in mods if e['metrics']['checks']>0}
   plan=sum(int(e['plan_ns']) for e in mods)/1e9
   fallback=sum(int(e['fallback_ns']) for e in mods)/1e9
   dup=sum(int(e['wall_ns']) for e in ev if e.get('event')=='serial_duplicate_phase')/1e9
   union=sum(int(e['metrics']['kernel_union_ns']) for e in mods)/1e9
   batch=sum(int(e['metrics']['batch_wall_ns']) for e in mods)/1e9
   kernel_cpu=sum(int(e['metrics']['kernel_cpu_ns']) for e in mods)/1e9
   span=sum(int(e['metrics']['sum_wave_max_cpu_ns']) for e in mods)/1e9
   batch_cpu=sum(int(e['metrics']['batch_cpu_ns']) for e in mods)/1e9
   serial=dep+plan+fallback+dup;remaining=c['wall_s']-serial-union
   phases.append(dict(name=name,workers=row['workers'],read_context_s=dep,plan_s=plan,upstream_serial_kernel_s=fallback,
    upstream_serial_kernel_CPU_s=sum(int(e['fallback_cpu_ns']) for e in mods)/1e9,
    ordinary_checks=sum(int(e['metrics']['checks']) for e in mods),
    ordinary_raw_HB=sum(int(e['metrics']['raw_HB']) for e in mods),
    serial_duplicate_s=dup,implementation_serial_s=serial,parallel_kernel_occupancy_s=union,
    overhead_residual_s=remaining,batch_wall_s=batch,batch_non_kernel_wall_s=batch-union,
    other_residual_s=remaining-(batch-union),kernel_CPU_s=kernel_cpu,batch_CPU_s=batch_cpu,
    batch_non_kernel_CPU_s=batch_cpu-kernel_cpu,wave_span_proxy_s=span,kernel_parallelism_proxy=kernel_cpu/span if span else None,process_wall_s=c['wall_s']))
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
 comparisons=[];changed=[]
 if 'P1' in module_work:
  base=module_work['P1']
  for name,rows in module_work.items():
   if name=='P1':continue
   shared=base.keys()&rows.keys();different=[]
   for module in shared:
    a=base[module];b=rows[module]
    if a['raw_HB']!=b['raw_HB']:
     different.append(module);changed.append(dict(name=name,module=module,baseline_HB=a['raw_HB'],current_HB=b['raw_HB'],
      delta_HB=b['raw_HB']-a['raw_HB']))
   comparisons.append(dict(name=name,matched_modules=len(shared),module_count_equal=set(base)==set(rows),
    changed_module_HB_counts=len(different),total_baseline_HB=sum(base[k]['raw_HB'] for k in shared),
    total_current_HB=sum(rows[k]['raw_HB'] for k in shared)))
 csvout(out/'aggregate-work-comparisons.csv',comparisons)
 if changed:csvout(out/'changed-module-work.csv',sorted(changed,key=lambda r:abs(r['delta_HB']),reverse=True)[:100])
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
  # Compare actual serialized bytes with original input as well as other trials.
  reference=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets/overlay-complete-v2/OAI/MathematicalPhysics/Transonic/Certificates/BarrierData41.olean')
  if reference.exists():
   original=reference.read_bytes()
   artifacts=sorted((point/'hardware-leaf-output').glob('*.olean'))
   summary['original_olean_bytes']=len(original)
   summary['original_olean_reference']=str(reference)
   summary['all_olean_equal_to_original']=len(artifacts)==9 and all(f.read_bytes()==original for f in artifacts)
  else:
   summary['all_olean_equal_to_original']=None
   summary['original_reference_status']='not found; no original-byte equality claim'
  summary['allocation_budget_scope']='per-target observed allocation deltas; native kernel poll units unobserved'
  # Target by target calibration avoids a per-core aggregate being presented as
  # a universal capacity. The same sampled names appear in all nine trials.
  calibrated=[]
  for target,rr in sorted(by.items()):
   values={}
   for kind in ['p1','e1','mixed24']:
    costs=[r['CPU_ns']/1e9 for r in rr if r['kind']==kind]
    if costs:values[kind]=statistics.median(costs)
   if len(values)==3:
    calibrated.append(dict(target=target,P1_CPU_median_s=values['p1'],E1_CPU_median_s=values['e1'],
     M24_CPU_median_s=values['mixed24'],E_to_P_work_rate=values['p1']/values['e1'],
     mixed_to_P_CPU_ratio=values['mixed24']/values['p1']))
  csvout(out/'hardware-target-costs.csv',calibrated)
  (out/'hardware-determinism.json').write_text(json.dumps(summary,indent=2))
 return full,phases

def supplements(point,out,full,phases):
 inventory=[]
 for phase in ['p12','p48','types','observer','placement']:
  f=point/(phase+'-terminal.json')
  inventory.append(dict(phase=phase,terminal=json.loads(f.read_text())['state'] if f.exists() else 'not_terminal',
   results_present=(point/(phase+'-results.json')).exists()))
 (out/'analysis-status.json').write_text(json.dumps(dict(phase_inventory=inventory,
  complete_full_cells=len(full),scope='completed native cells only; unfinished cells excluded, not failures'),indent=2))
 by_full={r['name']:r for r in full};by_phase={r['name']:r for r in phases}
 per_module=[]
 for name in by_phase:
  for m in read_events(point/'runs'/('full-'+name)/'stdout'):
   if m.get('event')!='profile_module':continue
   mm=m['metrics']
   assert sum(w['checks'] for w in mm['workers'])==mm['checks']
   assert sum(w['cpu_ns'] for w in mm['workers'])==mm['kernel_cpu_ns']
   assert sum(w['raw_HB'] for w in mm['workers'])==mm['raw_HB']
   span=mm['sum_wave_max_cpu_ns']/1e9;work=mm['kernel_cpu_ns']/1e9
   per_module.append(dict(name=name,module=m['module'],checks=mm['checks'],raw_HB=mm['raw_HB'],
    waves=mm['waves'],frontier_span_s=span,work_span_proxy=work/span if span else None,
    kernel_union_s=mm['kernel_union_ns']/1e9,kernel_CPU_s=work,
    batch_non_kernel_wall_s=(mm['batch_wall_ns']-mm['kernel_union_ns'])/1e9,
    batch_non_kernel_CPU_s=(mm['batch_cpu_ns']-mm['kernel_cpu_ns'])/1e9))
 csvout(out/'module-phases.csv',per_module)
 p1=[r for r in per_module if r['name']=='P1' and r['checks']]
 if p1:
  work=sum(r['kernel_CPU_s'] for r in p1);buckets=[]
  for low,high in [(1,2),(2,4),(4,8),(8,float('inf'))]:
   rr=[r for r in p1 if r['work_span_proxy']>=low-1e-10 and r['work_span_proxy']<high]
   cpu=sum(r['kernel_CPU_s'] for r in rr)
   buckets.append(dict(proxy_from=low,proxy_to=high if math.isfinite(high) else 'inf',
    modules=len(rr),CPU_s=cpu,CPU_share_pct=100*cpu/work,frontier_span_s=sum(r['frontier_span_s'] for r in rr)))
  csvout(out/'P1-work-span-distribution.csv',buckets)
  csvout(out/'P1-top-span-modules.csv',sorted(p1,key=lambda r:r['frontier_span_s'],reverse=True)[:30])
 pair_rows=[];delta_rows=[];module_delta=[]
 pairs=[('P1','P2'),('P2','P4'),('P4','P8'),('P8','E16'),('P8','M24'),
  ('P8','P8-noProfile'),('M24','M24-noProfile'),
  ('P8-noProfile','P8-unpinned'),('M24-noProfile','M24-unpinned'),
  ('P8-unpinned','M24-unpinned')]
 terms=['read_context_s','plan_s','upstream_serial_kernel_s','serial_duplicate_s',
  'parallel_kernel_occupancy_s','batch_non_kernel_wall_s','other_residual_s']
 for left,right in pairs:
  if left not in by_full or right not in by_full:continue
  a=by_full[left];b=by_full[right];delta=b['wall_s']-a['wall_s']
  pair_rows.append(dict(baseline=left,condition=right,wall_delta_s=delta,
   wall_change_pct=100*(b['wall_s']/a['wall_s']-1),CPU_delta_s=b['CPU_s']-a['CPU_s'],
   CPU_change_pct=100*(b['CPU_s']/a['CPU_s']-1),
   note='one fixed-order observation per full configuration; not a confidence interval'))
  if left in by_phase and right in by_phase:
   da=by_phase[left];db=by_phase[right]
   for key in terms:
    d=db[key]-da[key]
    delta_rows.append(dict(baseline=left,condition=right,term=key,delta_s=d,
     signed_share_of_net_wall_delta_pct=100*d/delta if delta else None))
   assert math.isclose(sum(db[k]-da[k] for k in terms),delta,abs_tol=1e-6)
   aa={r['module']:r for r in per_module if r['name']==left}
   bb={r['module']:r for r in per_module if r['name']==right}
   ranked=[]
   for module in aa.keys()&bb.keys():
    row=dict(baseline=left,condition=right,module=module)
    for key in ['kernel_union_s','kernel_CPU_s','batch_non_kernel_wall_s','batch_non_kernel_CPU_s']:
     row['delta_'+key]=bb[module][key]-aa[module][key]
    ranked.append(row)
   module_delta.extend(sorted(ranked,key=lambda x:abs(x['delta_kernel_union_s'])+
    abs(x['delta_batch_non_kernel_wall_s']),reverse=True)[:30])
 csvout(out/'condition-comparisons.csv',pair_rows)
 csvout(out/'signed-phase-deltas.csv',delta_rows)
 csvout(out/'top-module-deltas.csv',module_delta)

if __name__=='__main__':
 import sys
 rows,ph=analyze(Path(sys.argv[1]),Path(sys.argv[2]));supplements(Path(sys.argv[1]),Path(sys.argv[2]),rows,ph);print(json.dumps(dict(full_cells=len(rows),phase_rows=len(ph))))
