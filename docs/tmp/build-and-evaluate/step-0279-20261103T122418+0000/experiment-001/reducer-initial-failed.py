from pathlib import Path
import os,json,collections,statistics,csv,tarfile,time,resource,decimal,gzip,subprocess
os.sched_setaffinity(0,{22,23});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
ref=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/runs/barrier-full-reference1-r1/stdout')
workref=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103/runs/full-plain-P8-r1-before/stdout')
def events(p):
 with p.open()as f:
  for line in f:
   if line.startswith('{'):yield json.loads(line)
reference={x['module']:(x['constants'],x['imports'])for x in events(ref)if x.get('event')=='accept'}
wv={x['module']:(x['metrics']['checks'],x['metrics']['raw_HB'])for x in events(workref)if x.get('event')=='profile_module'}
assert len(reference)==len(wv)==4449
keys=['full-plain-m%d-P%d-r%d'%(m,n,k)for m in [0,1]for n in [1,2,4,8]for k in [1,2,3]]+['full-stat-m%d-P1-r1'%m for m in [0,1]]
freeze={ref,workref};identities=set();rows=[];pmu=[]
def resourcecheck(d,expected=None):
 c=json.loads((d/'command.json').read_text());v=json.loads((d/'result.json').read_text())
 assert c['argv']==v['argv']and c['affinity']==list(range(8))and c['cgroup_charged_memory_max_gib']==14 and c['own_rss_sample_stop_gib']==14
 assert not any(str(x).startswith('-M')for x in c['argv'])
 assert v['wait4_usage_complete']and v['native_retired']and not v['stop_reasons']and not Path(v['cgroup']).exists()
 assert all(int(z.split()[1])==0 for z in v['memory_events'].splitlines()if z.split()[0]in ['oom','oom_kill','oom_group_kill'])
 if expected is not None:assert v['returncode']==expected
 identities.add((int(v['pid']),str(v['birth'])))
 peak=0
 for line in(d/'memory.jsonl').read_text().splitlines():
  x=json.loads(line);peak=max(peak,x['rss_bytes']);identities.update((int(y['pid']),str(y['birth']))for y in x['processes'])
 assert peak==v['sampled_tree_peak_bytes']
 freeze.update(d/x for x in ['command.json','result.json','stdout','stderr','memory.jsonl'])
 return v
for key in keys:
 d=b/'runs'/key;v=resourcecheck(d,0);term=json.loads((b/(key+'-terminal.json')).read_text());assert term['state']=='complete'and term['cell']['argv']==v['argv'];freeze.add(b/(key+'-terminal.json'));freeze.add(b/(key+'-application.time'))
 m=int(key.split('-m')[1][0]);n=int(key.split('-P')[1].split('-')[0]);k=int(key.rsplit('r',1)[1]);heads={};accepted={};prof={};complete=[];cpu=0;markcpu=0;calls=0;after=[0]*5;ready=[0]*5;before=[0]*5
 for x in events(d/'stdout'):
  ev=x.get('event')
  if ev in ['accept','module_header']:
   dest=accepted if ev=='accept'else heads;assert x['module']not in dest;dest[x['module']]=(x['constants'],x['imports'])
  if ev=='complete':complete.append(x)
  if ev=='profile_module':
   a=x['metrics'];assert x['module']not in prof;prof[x['module']]=(a['checks'],a['raw_HB']);cpu+=a['kernel_cpu_ns'];p=x['persistence'];assert p['enabled']==bool(m)and not p['diagnostic'];calls+=p['calls'];markcpu+=p['window_thread_cpu_ns']
   for dst,src in [(before,'base_before'),(after,'base_after'),(ready,'after_enqueue')]:
    for i in range(5):dst[i]+=p[src][i]
 assert heads==accepted==reference and prof==wv and len(complete)==1
 assert complete[0]['constants']==425463 and complete[0]['skipped_unsafe_partial']==3595 and complete[0]['module_local_fallbacks']==0
 assert calls==18990 and before==[0,18990,0,0,0]
 assert after==ready==([18990,0,0,0,0]if m else [0,0,18990,0,0])
 rows.append(dict(key=key,arm='plain'if 'plain'in key else'stat',persistent=m,workers=n,repeat=k,wall_s=v['wall_s'],CPU_s=v['user_s']+v['system_s'],observer_CPU_s=cpu/1e9,marker_CPU_s=markcpu/1e9,sampled_RSS_B=v['sampled_tree_peak_bytes'],wait4_HWM_KiB=v['peak_rss_kib'],charged_peak_B=v['charged_peak_bytes'],checks=sum(z[0]for z in prof.values()),units=sum(z[1]for z in prof.values()),frontiers=calls))
 if 'stat'in key:
  f=b/(key+'-stat.json');freeze.add(f)
  for l in f.read_text().splitlines():
   q=json.loads(l);assert q['pcnt-running']==100;pmu.append(dict(persistent=m,event=q['event'],value=int(decimal.Decimal(q['counter-value'])),runtime=q['event-runtime'],pcnt=q['pcnt-running']))
# Controls are separately qualified, never included in performance denominators.
qual=json.loads((b/'qualification-terminal.json').read_text());assert qual['state']=='qualified'and len(qual['cells'])==13
control=[]
for c in qual['cells']:
 key=c['key'];v=resourcecheck(b/'runs'/key);ev=list(events(b/'runs'/key/'stdout'));text=(b/'runs'/key/'stdout').read_text()+(b/'runs'/key/'stderr').read_text()
 if key.endswith('-valid'):assert v['returncode']==0 and len([x for x in ev if x.get('event')=='accept'])==650 and any(x.get('event')=='complete'for x in ev)
 elif key.endswith('-bvar'):assert v['returncode']==1 and any(x.get('event')=='reject'and 'kernel_reject:c0:'in x.get('error','')for x in ev)
 elif key.endswith('-stale'):assert v['returncode']==1 and 'stale checked frontier'in text
 elif key.endswith('-duplicate'):assert v['returncode']==1 and 'base-index cover differs'in text
 else:assert key=='qual-official-import-probe'and v['returncode']==0 and len([x for x in ev if x.get('event')=='official_import_snapshot'])==2
 control.append(dict(key=key,rc=v['returncode'],wall_s=v['wall_s']))
for pid,birth in identities:
 try:
  z=Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split();assert z[19]!=birth,(pid,birth)
 except FileNotFoundError:pass
summary=[]
for m in [0,1]:
 for n in [1,2,4,8]:
  a=[x for x in rows if x['arm']=='plain'and x['persistent']==m and x['workers']==n];assert len(a)==3
  o=dict(persistent=m,workers=n)
  for met in ['wall_s','CPU_s','observer_CPU_s','marker_CPU_s','sampled_RSS_B']:
   vals=[x[met]for x in a];o[met+'_median']=statistics.median(vals);o[met+'_min']=min(vals);o[met+'_max']=max(vals)
  summary.append(o)
paired=[]
for k in [1,2,3]:
 lookup={(x['persistent'],x['workers']):x for x in rows if x['arm']=='plain'and x['repeat']==k}
 for met in ['CPU_s','observer_CPU_s']:
  off=lookup[0,8][met]-lookup[0,4][met];on=lookup[1,8][met]-lookup[1,4][met]
  paired.append(dict(repeat=k,metric=met,off_growth=off,on_growth=on,removed=off-on,removed_fraction=(off-on)/off))
def csvout(name,arr):
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]),lineterminator='\n');w.writeheader();w.writerows(arr)
for name,a in [('qualified-plain-and-P1stat.csv',rows),('plain-summary.csv',summary),('paired-growth.csv',paired),('P1-pmu.csv',pmu),('correctness-controls.csv',control)]:csvout(name,a)
freeze.update(b/n for n in ['cell.py','matrix.py','matrix-schedule.json','native.py','attribution.py','qualify.py','qualification-terminal.json','build_persistence.py','preparation.json'])
freeze.update((b/'source').iterdir())
for n in ['plan.md','source-and-scope.md','plain-results.md','stat-P1-intermediate.md','three-repeat-interaction.md']:
 freeze.add(r/'research/parallel-stream-check/persistent'/n)
with tarfile.open(e/'qualified-original-raw-source.tar.gz','w:gz')as tar:
 for p in sorted(freeze):tar.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
out=dict(root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,plain_cells=24,P1_stat_cells=2,qualified_controls=13,retired_actual_PID_births=len(identities),reference_modules=len(reference),checks=237863,units=3283925639,source_scope='same new executable flag0/1, original kernel; unsafe quiescence/coordinator/FFI trusted',overall32matrix_complete=False,archive_bytes=(e/'qualified-original-raw-source.tar.gz').stat().st_size)
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True);print('SUMMARY',json.dumps(summary));print('PAIRED',json.dumps(paired))
