from pathlib import Path
import os,json,collections,csv,gzip,tarfile,time,resource,re,decimal,subprocess
os.sched_setaffinity(0,{22,23});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103');s=Path(Path('/workspaces/.agent-state/gpu-smt-persistence-pmu-memory-root-step.txt').read_text().strip());e=s/'experiment-001'
prior=r/'docs/tmp/build-and-evaluate/step-0279-20261103T122418+0000/experiment-001'
freeze=set();source_equal=[]
with tarfile.open(prior/'qualified-original-raw-source.tar.gz','r:gz')as old:
 for name in ['source/ParallelCore.lean','source/ParallelStream.lean','source/persistence.c','source/checked_commit.c','source/placement_profile.c','cell.py','matrix.py','native.py','attribution.py']:
  p=b/name;member=str(p).removeprefix('/workspaces/');assert old.extractfile(member).read()==p.read_bytes(),name;freeze.add(p);source_equal.append(name)
ref=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/runs/barrier-full-reference1-r1/stdout')
wvref=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103/runs/full-plain-P8-r1-before/stdout')
def events(p):
 with p.open()as f:
  for l in f:
   if l.startswith('{'):yield json.loads(l)
reference={x['module']:(x['constants'],x['imports'])for x in events(ref)if x.get('event')=='accept'}
work={x['module']:(x['metrics']['checks'],x['metrics']['raw_HB'])for x in events(wvref)if x.get('event')=='profile_module'}
assert len(reference)==len(work)==4449;freeze|={ref,wvref}
keys=['full-stat-m%d-P%d-r1'%(m,n)for m in [0,1]for n in [2,4,8]]+['full-plain-m%d-P8-memory-r1'%m for m in [0,1]]
identities=set();resources=[];memory={}
for key in keys:
 p=b/'runs'/key;c=json.loads((p/'command.json').read_text());v=json.loads((p/'result.json').read_text());t=json.loads((b/(key+'-terminal.json')).read_text())
 assert c['argv']==v['argv']==t['cell']['argv']and t['state']=='complete'and v['returncode']==0
 assert c['affinity']==list(range(8))and c['wall_limit_s']==1100 and c['cgroup_charged_memory_max_gib']==14 and c['own_rss_sample_stop_gib']==14
 assert not any(str(a).startswith('-M')for a in c['argv'])
 assert v['wait4_usage_complete']and v['native_retired']and not v['stop_reasons']and not Path(v['cgroup']).exists()
 assert all(int(z.split()[1])==0 for z in v['memory_events'].splitlines()if z.split()[0]in ['oom','oom_kill','oom_group_kill'])
 identities.add((int(v['pid']),str(v['birth'])));peak=0
 for l in(p/'memory.jsonl').read_text().splitlines():
  a=json.loads(l);peak=max(peak,a['rss_bytes']);identities.update((int(z['pid']),str(z['birth']))for z in a['processes'])
 assert peak==v['sampled_tree_peak_bytes']
 m=int(key.split('-m')[1][0]);n=int(key.split('-P')[1].split('-')[0]);heads={};accept={};profiles={};completed=[];calls=0;pre=[0]*5;post=[0]*5;ready=[0]*5
 cumulative_checks=units=modules=entries=frontiers=0;last=None;checkpoints=[]
 for x in events(p/'stdout'):
  ev=x.get('event')
  if ev in ['module_header','accept']:
   dst=heads if ev=='module_header'else accept;assert x['module']not in dst;dst[x['module']]=(x['constants'],x['imports'])
   if ev=='accept':modules+=1;entries+=x['constants'];last=x['module']
  if ev=='profile_module':
   a=x['metrics'];assert x['module']not in profiles;profiles[x['module']]=(a['checks'],a['raw_HB']);q=x['persistence'];assert q['enabled']==bool(m)and not q['diagnostic']
   cumulative_checks+=a['checks'];units+=a['raw_HB'];frontiers+=q['calls'];calls+=q['calls']
   for dst,k in [(pre,'base_before'),(post,'base_after'),(ready,'after_enqueue')]:
    for i in range(5):dst[i]+=q[k][i]
  if ev=='complete':completed.append(x)
  if ev=='memory_checkpoint':
   assert 'memory'in key and x['modules']==modules and x['input_entries']==entries
   row=dict(modules=modules,last_module=last,input_entries=entries,checks=cumulative_checks,units=units,frontiers=frontiers)
   for line in x['smaps_rollup'].splitlines():
    if ':'not in line:continue
    label,value=line.split(':',1);values=value.split()
    if len(values)==2 and values[1]=='kB':row[label+'_bytes']=int(values[0])*1024
   assert row['Swap_bytes']==0;checkpoints.append(row)
 assert heads==accept==reference and profiles==work and len(completed)==1
 assert completed[0]['constants']==425463 and completed[0]['skipped_unsafe_partial']==3595 and completed[0]['module_local_fallbacks']==0
 assert calls==18990 and pre==[0,18990,0,0,0]and post==([18990,0,0,0,0]if m else[0,18990,0,0,0])and ready==([18990,0,0,0,0]if m else[0,0,18990,0,0])
 if 'memory'in key:
  assert len(checkpoints)==4449 and checkpoints[-1]['last_module']=='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
  memory[m]=checkpoints;launch=b/('aux-memory-m%d-P8-launch.json'%m);a=json.loads(launch.read_text());assert a['argv'][:2]==['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock'];identities.add((int(a['pid']),str(a['birth'])));freeze.add(launch);freeze.add(b/(key+'-auxiliary-config.json'))
 resources.append(dict(key=key,returncode=v['returncode'],wall_s=v['wall_s'],user_s=v['user_s'],system_s=v['system_s'],CPU_s=v['user_s']+v['system_s'],HWM_KiB=v['peak_rss_kib'],sampled_RSS_B=v['sampled_tree_peak_bytes'],charged_peak_B=v['charged_peak_bytes']))
 freeze.update(p/n for n in ['command.json','result.json','stdout','stderr','memory.jsonl']);freeze.add(b/(key+'-terminal.json'));freeze.add(b/(key+'-application.time'))
# Full primary completion is lineage: root0279 already qualified26; this step adds remaining6.
terminal=json.loads((b/'matrix-terminal.json').read_text());assert terminal['state']=='all32_complete_requires_review'and len(terminal['rows'])==32
assert len({x['key']for x in terminal['rows']})==32 and all(x['wrapper_rc']==0 and x['state']=='complete'for x in terminal['rows'])
for name in ['matrix-launch.json','matrix-active.json']:
 a=json.loads((b/name).read_text());identities.add((int(a['pid']),str(a['birth'])));freeze.add(b/name)
freeze.add(b/'matrix-terminal.json')
for pid,birth in identities:
 try:assert Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[19]!=birth,(pid,birth)
 except FileNotFoundError:pass
# Decode each actual stat JSON independently; preserve raw selector semantics.
pmu=[]
for m in [0,1]:
 for n in [1,2,4,8]:
  p=b/('full-stat-m%d-P%d-r1-stat.json'%(m,n));a=[json.loads(l)for l in p.read_text().splitlines()];assert len(a)==7 and all(x['pcnt-running']==100 for x in a)
  assert len({x['event']for x in a})==7
  for x in a:pmu.append(dict(persistent=m,workers=n,event=x['event'],value=int(decimal.Decimal(x['counter-value'])),running_pct=x['pcnt-running'],event_runtime=x['event-runtime']))
  freeze.add(p)
lookup={(x['persistent'],x['workers'],x['event']):x['value']for x in pmu};evnames=[x['event']for x in pmu[:7]]
effects=[]
for n in [1,2,4,8]:
 for event in evnames:
  a=lookup[0,n,event];z=lookup[1,n,event];effects.append(dict(workers=n,event=event,off=a,persistent=z,change_pct=100*(z/a-1)))
scaling=[]
for m in [0,1]:
 for event in evnames:
  a=lookup[m,4,event];z=lookup[m,8,event];scaling.append(dict(persistent=m,event=event,P4=a,P8=z,change_pct=100*(z/a-1)))
deltas=[]
for a,z in zip(memory[0],memory[1]):
 for k in ['modules','last_module','input_entries','checks','units','frontiers']:assert a[k]==z[k],k
 row={k:a[k]for k in ['modules','last_module','input_entries','checks','units','frontiers']}
 for k in ['Rss_bytes','Pss_bytes','Anonymous_bytes','Private_Dirty_bytes','Private_Clean_bytes']:
  row[k+'_off']=a[k];row[k+'_on']=z[k];row[k+'_delta']=z[k]-a[k]
 deltas.append(row)
def write(name,rows):
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
for name,a in [('new-native-scopes.csv',resources),('all-eight-stat-raw.csv',pmu),('stat-treatment-effects.csv',effects),('stat-P4-P8-scaling.csv',scaling),('aligned-memory-all-boundaries.csv',deltas)]:write(name,a)
freeze.update(b/n for n in ['auxiliary.py','memory_analysis.py'])
for n in ['stat-results.md','memory-results.md','auxiliary-plan.md','source-and-scope.md']:freeze.add(r/'research/parallel-stream-check/persistent'/n)
# Source checkpoint hook and semantics are frozen/read; no new binary or toolchain copy.
source=(b/'source/ParallelStream.lean').read_text();assert 'DECOUPLED_MEMORY_PROFILE'in source and 'smaps_rollup'in source
(e/'checkpoint-source.lean.gz').write_bytes(gzip.compress(source.encode()))
with tarfile.open(e/'new-qualified-raw-source.tar.gz','w:gz')as tar:
 for p in sorted(freeze):tar.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
out=dict(root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_stat_native_cells=6,prior_root0279_qualified_primary_cells=26,total_primary_cells_qualified=32,separate_memory_native_cells=2,stat_readings=56,all_running_pct=100,modules_per_native=4449,checks=237863,allocation_units=3283925639,source_exactly_matches_root0279=source_equal,retired_actual_PID_births=len(identities),memory_boundaries_aligned=len(deltas),memory_final=deltas[-1],anonymous_delta_min_B=min(x['Anonymous_bytes_delta']for x in deltas),anonymous_delta_max_B=max(x['Anonymous_bytes_delta']for x in deltas),archive_bytes=(e/'new-qualified-raw-source.tar.gz').stat().st_size,native_reruns=0)
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n');print('ANALYSIS',json.dumps(out),flush=True);print('P8_EFFECTS',json.dumps([x for x in effects if x['workers']==8]));print('SCALING',json.dumps(scaling))
