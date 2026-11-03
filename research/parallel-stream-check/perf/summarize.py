"""Summarize native/PMU strata without borrowing historical denominators."""
import collections,csv,json,sys
from pathlib import Path
def write(p,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator=chr(10));w.writeheader();w.writerows(rows)
def report_threads(path):
 text=path.read_text();headers=[x for x in text.splitlines() if x.startswith('#    PID')]
 if len(headers)!=1:raise ValueError('expected actual report-Ttable')
 names=headers[0].lstrip('#').split()
 return [dict(zip(names,map(int,x.split()))) for x in text.splitlines()
  if x.strip() and x.split()[0].isdigit() and len(x.split())==len(names)]
def main():
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 times=[];stats=[];threads=[];cats=[];scopes=[];problems=[]
 for f in sorted(root.glob('full-*-terminal.json')):
  t=json.loads(f.read_text());c=t.get('cell');key=f.name.removesuffix('-terminal.json')
  if not c or t['state']!='complete':
   problems.append(dict(key=key,state=t['state']));continue
  base=dict(key=key,workers=c['workers'],arm=c['arm'],repeat=c['repeat'])
  if (c['ordinary_checks'],c['ordinary_allocation_units'])!=(237863,3283925639):
   raise ValueError('frozen full ordinary work differs')
  native=dict(base,wall_s=c['wall_s'],user_s=c['user_s'],system_s=c['system_s'],
   cpu_s=c['user_s']+c['system_s'],sampled_tree_peak_bytes=c['sampled_tree_peak_bytes'],
   charged_peak_bytes=c['charged_peak_bytes'],accepted_count=c['accepted_count'],
   accepted_reference_equal=c['accepted_set_equal_to_reference'],
   checks=c['ordinary_checks'],allocation_units=c['ordinary_allocation_units'])
  native.update({'application_'+k:v for k,v in c.get('application_time',{}).items()})
  native.update({k:c.get(k) for k in ['cgroup_usage_s','cgroup_user_s','cgroup_system_s']})
  metrics=collections.Counter()
  with (root/'runs'/key/'stdout').open() as g:
   for line in g:
    if line.startswith('{'):
     e=json.loads(line)
     if e.get('event')=='profile_module':
      for name in ['kernel_cpu_ns','kernel_union_ns','batch_cpu_ns','batch_wall_ns']:
       metrics[name]+=e['metrics'].get(name,0)
  native.update({k.removesuffix('_ns')+'_s':v/1e9 for k,v in metrics.items()});times.append(native)
  sf=root/(key+'-stat.json')
  if sf.exists():
   for line in sf.read_text().splitlines():
    if line.strip():
     e=json.loads(line);v=e.get('counter-value','')
     stats.append(dict(base,event=e.get('event'),counter_value=v,
      pcnt_running=e.get('pcnt-running'),event_runtime=e.get('event-runtime'),
      scope='whole command; not original-kernel interval'))
  d=root/('decode-'+key)
  tf=d/'thread-counters.txt'
  if tf.exists():
   workers=set(c['observed_worker_TIDs']);trs=report_threads(tf)
   for r in trs:
    threads.append(dict(base,**r,observed_original_check_worker=r['TID'] in workers,
     scope='thread lifetime, not just original-check interval',
     IPC=r['cpu_core/instructions,period=0/u']/r['cpu_core/cpu-cycles/u'] if r['cpu_core/cpu-cycles/u'] else None,
     retired_L3_misses_per_kinsn=1000*r['cpu_core/mem_load_retired.l3_miss,period=0/u']/r['cpu_core/instructions,period=0/u'] if r['cpu_core/instructions,period=0/u'] else None))
   if workers-set(r['TID'] for r in trs):problems.append(dict(key=key,state='missing worker READcounts'))
  cat=d/'category-thread-periods.csv'
  if cat.exists():
   with cat.open() as g:
    cats.extend(dict(base,**r) for r in csv.DictReader(g))
  sf=d/'scope-periods.csv'
  if sf.exists():
   with sf.open() as g:
    scopes.extend(dict(base,**r) for r in csv.DictReader(g))
 write(out/'native-timings.csv',times);write(out/'stat-counters.csv',stats)
 write(out/'record-thread-counters.csv',threads);write(out/'sample-category-threads.csv',cats)
 write(out/'sample-scopes.csv',scopes)
 aggregated=collections.Counter()
 for r in cats:
  aggregated[(r['key'],r['workers'],r['event'],r['scope'],r['category'])]+=int(r['sampled_period'])
 write(out/'category-by-workers.csv',[dict(key=k[0],workers=k[1],event=k[2],scope=k[3],category=k[4],
  sampled_cycles=v,interpretation='exclusive sampled family; inlined RC not fully resolved')
  for k,v in sorted(aggregated.items())])
 brackets=[]
 for n in [1,2,4,8]:
  ts=[r for r in times if r['workers']==n]
  plains=[r for r in ts if r['arm']=='plain']
  if len(plains)!=2:continue
  lo=min(r['wall_s'] for r in plains);hi=max(r['wall_s'] for r in plains)
  for r in ts:
   if r['arm']!='plain':
    brackets.append(dict(workers=n,arm=r['arm'],instrumented_wall_s=r['wall_s'],
     ordinary_min_s=lo,ordinary_max_s=hi,
     relative_to_plain_min=r['wall_s']/lo-1,relative_to_plain_max=r['wall_s']/hi-1,
     interpretation='observed bracket, not CI; perf and ordinary times kept separate'))
 write(out/'perf-overhead-brackets.csv',brackets)
 (out/'analysis-status.json').write_text(json.dumps(dict(complete_native_points=len(times),problems=problems,
  expected_native_points=16,raw=str(root),sampling_scope='period-weighted estimates; unresolved inline RC retained'),indent=2))
if __name__=='__main__':main()
