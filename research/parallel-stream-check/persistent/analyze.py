import csv,json,statistics,sys,collections
from pathlib import Path
from decimal import Decimal
def write(p,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator=chr(10));w.writeheader();w.writerows(rows)
def main():
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 schedule=json.loads((root/'matrix-schedule.json').read_text())
 keys={'full-'+arm+'-m'+str(mode)+'-P'+str(n)+'-'+rep for arm,mode,n,rep in schedule}
 rows=[];pmus=[]
 for key in sorted(keys):
  path=root/(key+'-terminal.json')
  if not path.exists():continue
  t=json.loads(path.read_text());c=t.get('cell')or{}
  if not c:
   rows.append(dict(key=key,state=t['state']));continue
  mark=c.get('persistence',{})
  row=dict(key=key,state=t['state'],workers=c['workers'],persistent=c['persistent'],
   arm=c['arm'],repeat=c['repeat'],wall_s=c['wall_s'],user_s=c['user_s'],system_s=c['system_s'],
   CPU_s=c['user_s']+c['system_s'],cgroup_CPU_s=c.get('cgroup_usage_s'),
   original_check_observer_CPU_s=c['kernel_CPU_ns']/1e9,
   mark_window_wall_s=mark.get('window_wall_ns',0)/1e9,
   mark_window_CPU_s=mark.get('window_thread_cpu_ns',0)/1e9,
   frontier_calls=mark.get('calls',0),sampled_peak_GiB=c['sampled_tree_peak_bytes']/1024**3,
   ru_maxrss_peak_GiB=c['peak_rss_kib']/1024**2,charged_peak_GiB=c['charged_peak_bytes']/1024**3,
   accepted_count=len(c['accepted_IDs']),accepted_equal=c['accepted_set_equal_to_reference'],
   checks=c['checks'],allocation_units=c['allocation_units'],work_equal=c['work_equal_to_frozen_reference'])
  if 'application_time'in c:
   a=c['application_time']
   row.update(application_wall_s=float(a['wall_s']),application_CPU_s=float(a['user_s'])+float(a['system_s']))
  rows.append(row)
  stat=root/(key+'-stat.json')
  if stat.exists():
   for line in stat.read_text().splitlines():
    if line.strip():
     s=json.loads(line)
     pmus.append(dict(key=key,workers=c['workers'],persistent=c['persistent'],event=s['event'],
      count=s['counter-value'],percent_running=s.get('pcnt-running'),
      scope='whole command user-mode stat; not exact original-check interval'))
 summary=[]
 groups=collections.defaultdict(list)
 for row in rows:
  if row.get('state')=='complete'and row.get('arm')=='plain':groups[row['workers'],row['persistent']].append(row)
 metrics=['wall_s','CPU_s','application_CPU_s','cgroup_CPU_s','original_check_observer_CPU_s',
 'mark_window_wall_s','mark_window_CPU_s','sampled_peak_GiB','ru_maxrss_peak_GiB','charged_peak_GiB']
 for (n,mode),rr in sorted(groups.items()):
  entry=dict(workers=n,persistent=mode,complete_repetitions=len(rr),expected_repetitions=3,
   interpretation='observed median/range; incomplete groups are not final; no confidence interval')
  for m in metrics:
   vv=[float(x[m])for x in rr if x.get(m)is not None]
   if vv:entry.update({m+'_median':statistics.median(vv),m+'_min':min(vv),m+'_max':max(vv)})
  summary.append(entry)
 comparisons=[]
 for n in [1,2,4,8]:
  lookup={x['persistent']:x for x in summary if x['workers']==n}
  if len(lookup)!=2:continue
  off=lookup[False];on=lookup[True]
  for m in metrics:
   k=m+'_median'
   if k in off and k in on and off[k]:
    comparisons.append(dict(workers=n,metric=m,off_repetitions=off['complete_repetitions'],
     on_repetitions=on['complete_repetitions'],off_median=off[k],on_median=on[k],
     relative_change=on[k]/off[k]-1,scope='same executable plain; partial groups explicit'))
 write(out/'cells.csv',rows);write(out/'plain-summary.csv',summary)
 write(out/'plain-on-off.csv',comparisons);write(out/'stat-counters.csv',pmus)
 (out/'status.json').write_text(json.dumps(dict(returned=len(rows),expected=32,
  complete=sum(x['state']=='complete'for x in rows),pending=sorted(keys-{x['key']for x in rows})),indent=2))
 print(json.dumps(dict(returned=len(rows),expected=32,complete=sum(x['state']=='complete'for x in rows))))
if __name__=='__main__':main()
