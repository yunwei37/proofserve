from pathlib import Path
import os,json,time,resource,tarfile,gzip,csv,statistics,collections,subprocess
os.sched_setaffinity(0,{22,23});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-wall-hybrid-20261103');p=b.parent/'parallel-stream-wall-20261103'
s=Path(Path('/workspaces/.agent-state/gpu-smt-hybrid-source40-root-step.txt').read_text().strip());e=s/'experiment-001'
def events(f):
 for l in f.open():
  if l.startswith('{'):yield json.loads(l)
ref=b.parent/'parallel-stream-check-v14/runs/barrier-full-reference1-r1/stdout'
rg={x['module']:(x['constants'],x['imports'])for x in events(ref)if x.get('event')=='accept'};assert len(rg)==4449
inputs={ref,b/'after_matrix-v4.py',b/'native.py',p/'matrix-v2.py',b/'continuation-v4.log',b/'continuation-v4-launch.json',b/'extended-build-fixed2.json',b/'fixtures/ComplexControl.lean'}
for n in ['ParallelStream.lean','checked_commit.c','placement_profile.c']:
 assert(b/'source'/n).read_bytes()==(p/'source'/n).read_bytes();inputs.add(b/'source'/n)
inputs.add(b/'source/ParallelCore.lean')
rows=[];ids=set();works={};profiles={};parts=[];ordered=None
def retired(pid,birth):
 try:assert Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[19]!=str(birth),(pid,birth)
 except FileNotFoundError:pass
 ids.add((int(pid),str(birth)))
keys=['complex-control-s'+str(z)+'-P'+str(n)+bad for z in[0,1]for n in[1,8]for bad in['','-bad']]
keys += ['hybrid-'+arm+'-P8-s'+str(z)+'-r'+str(rep)for arm,reps in[('diagnostic',[1]),('plain',[1,2,3])]for rep in reps for z in[0,1]]
for key in keys:
 q=b/'runs'/key;c=json.loads((q/'command.json').read_text());v=json.loads((q/'result.json').read_text());t=json.loads((b/(key+'-terminal.json')).read_text())
 assert all(t[k]==z for k,z in v.items())and t['qualified']
 assert c['argv']==v['argv']and c['affinity']==list(range(8))and c['wall_limit_s']==1100 and c['own_rss_sample_stop_gib']==c['cgroup_charged_memory_max_gib']==14
 assert not any(str(a).startswith('-M')for a in c['argv'])
 bad=key.endswith('-bad')
 assert v['returncode']==int(bad)and v['wait4_usage_complete']and v['native_retired']and v['cgroup_retired']and not v['stop_reasons']and not Path(v['cgroup']).exists()
 assert all(int(x.split()[1])==0 for x in v['memory_events'].splitlines()if x.split()[0]in['oom','oom_kill','oom_group_kill'])
 retired(v['pid'],v['birth']);peak=0
 for l in(q/'memory.jsonl').open():
  x=json.loads(l);assert x['rss_bytes']==sum(y['rss']for y in x['processes']);peak=max(peak,x['rss_bytes'])
  for y in x['processes']:retired(y['pid'],y['birth'])
 assert peak==v['sampled_tree_peak_bytes']
 ev=list(events(q/'stdout'));acc=[x for x in ev if x.get('event')=='accept'];graph={x['module']:(x['constants'],x['imports'])for x in acc};comp=[x for x in ev if x.get('event')=='complete'];rej=[x for x in ev if x.get('event')=='reject']
 if key.startswith('hybrid'):
  assert len(acc)==len(graph)==4449 and graph==rg and len(comp)==1 and not rej and not(q/'stderr').read_bytes()
  assert comp[0]['constants']==425463 and comp[0]['skipped_unsafe_partial']==3595 and comp[0]['module_local_fallbacks']==0
  if ordered is None:ordered=[x['module']for x in acc]
  assert ordered==[x['module']for x in acc]==t['accepted_IDs']
  assert {x['module']:(x['constants'],x['imports'])for x in ev if x.get('event')=='module_header'}==graph
  split=int(key.split('-s')[1][0]);work={x['module']:(x['path'],x['jobs'],x['waves'])for x in ev if x.get('event')=='kernel_work'}
  assert len(work)==4449
  if split in works:assert works[split]==work
  works[split]=work
  if 'diagnostic'in key:
   prof={x['module']:x for x in ev if x.get('event')=='profile_module'};assert len(prof)==4449
   profiles[split]=prof
   phases={k:sum(int(x.get(k,0))for x in prof.values())/1e9 for k in['fallback_ns','plan_ns']}
   for k in['batch_wall_ns','checks','raw_HB','waves']:
    phases[k]=sum(int(x['metrics'][k])for x in prof.values())/(1e9 if k.endswith('_ns')else 1)
   for k in['read_ns','context_ns']:phases[k]=sum(x[k]for x in ev if x.get('event')=='dependency_phase')/1e9
   phases['duplicates_s']=sum(x['wall_ns']for x in ev if x.get('event')=='serial_duplicate_phase')/1e9
   phases['unassigned_s']=v['wall_s']-sum(phases[k]for k in['fallback_ns','plan_ns','batch_wall_ns','read_ns','context_ns','duplicates_s'])
   phases.update(split=split,wall_s=v['wall_s'],CPU_s=v['user_s']+v['system_s']);parts.append(phases)
   if split:part=[x for x in ev if x.get('event')=='complex_partition']
  else:assert not any(x.get('event')in['profile_module','dependency_phase','complex_partition']for x in ev)
 else:
  assert [x['module']for x in acc]==(['Init.Prelude']if bad else['Init.Prelude','ComplexControl'])
  if bad:assert len(rej)==1 and not comp and 'loose bound variables'in rej[0]['error']and 'loose bound variables'in(q/'stderr').read_text()
  else:assert len(comp)==1 and not rej and not(q/'stderr').read_bytes()
 rows.append(dict(key=key,wall_s=v['wall_s'],CPU_s=v['user_s']+v['system_s'],user_s=v['user_s'],system_s=v['system_s'],HWM_KiB=v['peak_rss_kib'],sampled_RSS_B=peak,charged_peak_B=v['charged_peak_bytes'],returncode=v['returncode'],PID=v['pid'],birth=v['birth']))
 inputs.update(q/n for n in['command.json','result.json','stdout','stderr','memory.jsonl']);inputs.add(b/(key+'-terminal.json'))
assert len(part)==1231 and all(x['remaining_plannable']for x in part)
parttot={k:sum(x[k]for x in part)for k in['original_constants','ordinary_parallel_constants','serial_constants','prefix_ordinary','inductives','constructors','recursors','quotients']}
assert parttot['ordinary_parallel_constants']==168713 and parttot['serial_constants']==14932
assert {x['module']for x in part}=={k for k,v in works[0].items()if v[0]=='upstream_complex_or_cycle'}
assert sum(x['metrics']['checks']for x in profiles[0].values())==237863 and sum(x['metrics']['checks']for x in profiles[1].values())==406576
# Same ordinary modules preserve observed check/HB work; newly covered checks remain a distinct vector.
for mod,v in works[0].items():
 if v[0]=='parallel':
  assert works[1][mod]==v
  assert tuple(profiles[0][mod]['metrics'][k]for k in['checks','raw_HB'])==tuple(profiles[1][mod]['metrics'][k]for k in['checks','raw_HB'])
summary=[]
for split in[0,1]:
 rr=[x for x in rows if x['key'].startswith('hybrid-plain')and '-s'+str(split)+'-'in x['key']]
 z=dict(split=split)
 for k in['wall_s','CPU_s','HWM_KiB','sampled_RSS_B','charged_peak_B']:
  z[k+'_median']=statistics.median(x[k]for x in rr);z[k+'_min']=min(x[k]for x in rr);z[k+'_max']=max(x[k]for x in rr)
 summary.append(z)
for name,data in[('sixteen-hybrid-control-processes.csv',rows),('hybrid-three-repeat-summary.csv',summary),('diagnostic-phase-reconciliation.csv',parts)]:
 with(e/name).open('w',newline='')as f:w=csv.DictWriter(f,list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
for n in['complex-prefix-plain-results.md','complex-prefix-plain-effect.json','complex-prefix-plain-repeats.csv','complex-prefix-diagnostic.md','complex-prefix-bounds.json','analyze_waves.py']:
 inputs.add(r/'research/parallel-stream-check/wall-ceiling'/n)
for n in['step073.md','step073-audit.md','step074.md','step074-audit.md']:inputs.add(r/'research/parallel-stream-check'/n)
for x in b.glob('hybrid-diagnostic*.jsonl'):inputs.add(x)
with tarfile.open(e/'hybrid-raw-source.tar.gz','w:gz')as tf:
 for x in sorted(inputs):tf.add(x,arcname=str(x).removeprefix('/workspaces/'),recursive=False)
count=payload=0
with tarfile.open(e/'hybrid-raw-source.tar.gz','r:gz')as tf:
 for x in tf:
  data=tf.extractfile(x).read();assert len(data)==x.size;count+=1;payload+=len(data)
with gzip.open(e/'hybrid-raw-source.tar.gz','rb')as f:
 while f.read(1024*1024):pass
z=dict(summary=summary,wall_ratio=summary[0]['wall_s_median']/summary[1]['wall_s_median'],wall_reduction_percent=100*(1-summary[1]['wall_s_median']/summary[0]['wall_s_median']),CPU_change_percent=100*(summary[1]['CPU_s_median']/summary[0]['CPU_s_median']-1),same_repeat_ratios=[next(x['wall_s']for x in rows if x['key']=='hybrid-plain-P8-s0-r'+str(i))/next(x['wall_s']for x in rows if x['key']=='hybrid-plain-P8-s1-r'+str(i))for i in[1,2,3]],routes={str(k):dict(collections.Counter(x[0]for x in v.values()))for k,v in works.items()},partition_counts=parttot,phases=parts,retired_PID_births=len(ids),cgroups_absent=16,controller_retirement_claimed=False,archive_members=count,archive_payload_B=payload,archive_B=(e/'hybrid-raw-source.tar.gz').stat().st_size,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native=0)
(e/'reanalysis.json').write_text(json.dumps(z,indent=2)+'\n');print(json.dumps(z,indent=2))
