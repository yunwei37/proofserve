from pathlib import Path
import os,json,time,resource,tarfile,gzip,csv,statistics,collections,subprocess
os.sched_setaffinity(0,{22,23});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-wall-20261103');s=Path(Path('/workspaces/.agent-state/gpu-smt-grid-source39-root-step.txt').read_text().strip());e=s/'experiment-001'
def events(p):
 with p.open()as f:
  for l in f:
   if l.startswith('{'):yield json.loads(l)
old=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/runs/grid-full-reference1-r1/stdout')
reference={x['module']:(x['constants'],x['imports'])for x in events(old)if x.get('event')=='accept'};assert len(reference)==3793
frozen=['source/ParallelCore.lean','source/ParallelStream.lean','source/checked_commit.c','source/placement_profile.c','matrix-v2.py','native.py']
with tarfile.open(r/'docs/tmp/build-and-evaluate/step-0283-20261103T162836+0000/experiment-001/qualified-math-raw-source.tar.gz','r:gz')as tf:
 for n in frozen:assert(b/n).read_bytes()==tf.extractfile(str(b/n).removeprefix('/workspaces/')).read(),n
matrix=json.loads((b/'matrix-terminal.json').read_text());assert matrix['complete']
inputs={old,b/'matrix-terminal.json',b/'controller-v2.log',b/'build.py',b/'extended-build.json'}|{b/n for n in frozen}
rows=[];ids=set();ordered=None;workref=None
def retired(pid,birth):
 try:assert Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[19]!=str(birth),(pid,birth)
 except FileNotFoundError:pass
 ids.add((int(pid),str(birth)))
for rep in [1,2,3]:
 for arm in ['reference','parallel1','parallel4','parallel8']:
  key='grid-'+arm+'-r'+str(rep);p=b/'runs'/key;c=json.loads((p/'command.json').read_text());v=json.loads((p/'result.json').read_text());t=json.loads((b/(key+'-terminal.json')).read_text())
  assert all(t[k]==z for k,z in v.items());assert c['argv']==v['argv']and c['affinity']==list(range(8))and c['wall_limit_s']==1100 and c['own_rss_sample_stop_gib']==c['cgroup_charged_memory_max_gib']==14
  assert not any(str(a).startswith('-M')for a in c['argv'])
  assert v['returncode']==0 and t['qualified']and v['wait4_usage_complete']and v['native_retired']and v['cgroup_retired']and not v['stop_reasons']and not Path(v['cgroup']).exists()
  assert all(int(x.split()[1])==0 for x in v['memory_events'].splitlines()if x.split()[0]in['oom','oom_kill','oom_group_kill'])
  retired(v['pid'],v['birth']);peak=0
  for line in(p/'memory.jsonl').read_text().splitlines():
   a=json.loads(line);assert a['rss_bytes']==sum(x['rss']for x in a['processes']);peak=max(peak,a['rss_bytes'])
   for x in a['processes']:retired(x['pid'],x['birth'])
  assert peak==v['sampled_tree_peak_bytes']and not(p/'stderr').read_bytes()
  ev=list(events(p/'stdout'));acc=[x for x in ev if x.get('event')=='accept'];graph={x['module']:(x['constants'],x['imports'])for x in acc}
  assert len(acc)==len(graph)==3793 and graph==reference
  if ordered is None:ordered=[x['module']for x in acc]
  assert ordered==[x['module']for x in acc]==t['accepted_IDs']
  complete=[x for x in ev if x.get('event')=='complete'];assert len(complete)==1 and complete[0]['modules']==3793 and complete[0]['constants']==382707 and complete[0]['skipped_unsafe_partial']==3554
  assert not any(x.get('event')in['reject','profile_module','dependency_phase']for x in ev)
  if arm!='reference':
   heads={x['module']:(x['constants'],x['imports'])for x in ev if x.get('event')=='module_header'};assert heads==graph and complete[0]['module_local_fallbacks']==0
   work={x['module']:(x['path'],x['jobs'],x['waves'])for x in ev if x.get('event')=='kernel_work'};assert len(work)==3793
   if workref is None:workref=work
   assert work==workref
  rows.append(dict(key=key,arm=arm,repeat=rep,wall_s=v['wall_s'],CPU_s=v['user_s']+v['system_s'],user_s=v['user_s'],system_s=v['system_s'],HWM_KiB=v['peak_rss_kib'],sampled_RSS_B=peak,charged_peak_B=v['charged_peak_bytes']))
  inputs.update(p/n for n in ['command.json','result.json','stdout','stderr','memory.jsonl']);inputs.add(b/(key+'-terminal.json'))
retired(5528,'68581')
summary=[]
for arm in ['reference','parallel1','parallel4','parallel8']:
 a=[x for x in rows if x['arm']==arm];q=dict(arm=arm,repeats=3)
 for m in ['wall_s','CPU_s']:q.update({m+'_median':statistics.median(x[m]for x in a),m+'_min':min(x[m]for x in a),m+'_max':max(x[m]for x in a)})
 q['ratio_of_wall_medians']=summary[0]['wall_s_median']/q['wall_s_median']if summary else 1
 summary.append(q)
for name,data in [('twelve-grid-processes.csv',rows),('grid-three-repeat-summary.csv',summary)]:
 with(e/name).open('w',newline='')as f:w=csv.DictWriter(f,list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
for n in ['corrected-grid-results.md','corrected-stream-repeats.csv','corrected-stream-summary.csv','hardware-observation.json','plan.md','matrix.py','summarize.py']:
 inputs.add(r/'research/parallel-stream-check/wall-ceiling'/n)
for n in ['step071.md','step071-audit.md']:inputs.add(r/'research/parallel-stream-check'/n)
with tarfile.open(e/'grid-raw-source.tar.gz','w:gz')as tf:
 for p in sorted(inputs):tf.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
members=payload=0
with tarfile.open(e/'grid-raw-source.tar.gz','r:gz')as tf:
 for m in tf:
  data=tf.extractfile(m).read();assert len(data)==m.size;members+=1;payload+=len(data)
with gzip.open(e/'grid-raw-source.tar.gz','rb')as f:
 while f.read(1024*1024):pass
p4=summary[2];p8=summary[3];base=summary[0]
out=dict(summary=summary,source_equal_root0283=frozen,originals=3793,entries=382707,exclusions=3554,ordinary_jobs=sum(x[1]for x in workref.values()),waves=sum(x[2]for x in workref.values()),routes=dict(collections.Counter(x[0]for x in workref.values())),retired_PID_births=len(ids),cgroups_absent=12,CPU4_increase_percent=100*(p4['CPU_s_median']/base['CPU_s_median']-1),CPU8_increase_percent=100*(p8['CPU_s_median']/base['CPU_s_median']-1),wall4to8_reduction_percent=100*(1-p8['wall_s_median']/p4['wall_s_median']),CPU4to8_increase_percent=100*(p8['CPU_s_median']/p4['CPU_s_median']-1),same_repeat_4_ratios=[next(x['wall_s']for x in rows if x['arm']=='reference'and x['repeat']==i)/next(x['wall_s']for x in rows if x['arm']=='parallel4'and x['repeat']==i)for i in[1,2,3]],same_repeat_8_ratios=[next(x['wall_s']for x in rows if x['arm']=='reference'and x['repeat']==i)/next(x['wall_s']for x in rows if x['arm']=='parallel8'and x['repeat']==i)for i in[1,2,3]],matrix_terminal=matrix,kernel=os.uname().release,archive_members=members,archive_payload_B=payload,archive_B=(e/'grid-raw-source.tar.gz').stat().st_size,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native=0)
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
