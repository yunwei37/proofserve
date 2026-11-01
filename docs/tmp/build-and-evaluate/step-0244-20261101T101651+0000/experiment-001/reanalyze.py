from pathlib import Path
import os,json,gzip,time,resource,csv,subprocess,datetime
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0244-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-full-closures-paper-step.txt').write_text(str(s)+'\n')
def freeze(p,name):
 data=Path(p).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(data,mtime=0));return data
def live(pid,birth):
 p=Path('/proc')/str(pid)/'stat'
 try:return p.read_text().rsplit(')',1)[1].split()[19]==str(birth)
 except FileNotFoundError:return False
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14');m=r/'research/parallel-stream-check'
for name in ['full.py','full_pair.py','full_grid_pair.py','finish_grid_pair.py','native.py','barrier-full-pair-launch.json','barrier-full-pair-terminal.json','barrier-full-pair-complete.json','grid-full-pair-launch.json','grid-full-pair-resume-launch.json','grid-full-pair-resume-terminal.json','grid-full-pair-complete.json','grid-full-pair-controller.log','grid-full-pair-resume-controller.log','grid-r1-launch.json']:
 freeze(b/name,'raw-'+name)
for name in ['full-barrier-results.md','full-grid-results.md','grid-repaired-results.md','full-cells.csv','full-pairs.csv','step012.md','step013.md','step014.md','step015.md','correctness.md']:
 if (m/name).exists():freeze(m/name,'published-'+name)
prior=r/'docs/tmp/build-and-evaluate/step-0241-20261101T080929+0000/experiment-001'
for f in ['ParallelCore.lean','ParallelStream.lean','checked_commit.c']:
 data=freeze(b/'source'/f,'frozen-v14-'+f)
 assert data==gzip.decompress((prior/('frozen-v14-'+f+'.gz')).read_bytes())
for name in ['barrier-full-pair-launch.json','grid-full-pair-launch.json','grid-full-pair-resume-launch.json','grid-r1-launch.json']:
 launch=json.loads((b/name).read_text());assert not live(launch['pid'],launch['birth'])
driver=(b/'full.py').read_text()
assert all("e.pop(option,None)" in driver for x in [0])
for option in ['PARALLEL_CURVE_MODULES','PARALLEL_CHUNK_ASSETS','PARALLEL_CHUNK_ASSETS_CURVE','DECOUPLED_MEMORY_PROFILE']:assert option in driver
assert "if mode=='chunk':e['PARALLEL_CHUNK_ASSETS']" in driver
# None of these four arms selects chunk mode.
keys=['barrier-full-reference1-r1','barrier-full-parallel4-r1','grid-full-reference1-r1','grid-full-parallel4-r1','grid-stream-r1']
results={};events={};accepts={};rows=[];identities=set()
for key in keys:
 d=b/'runs'/key
 for f in ['result.json','command.json','stdout','stderr','memory.jsonl']:freeze(d/f,key+'-'+f)
 freeze(b/(key+'-summary.json'),key+'-summary.json')
 z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
 assert z['argv']==cmd['argv'] and z['returncode']==0 and z['native_retired'] and z['cgroup_retired'] and z['wait4_usage_complete']
 assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists() and not z['stop_reasons']
 assert z['affinity']==list(range(8)) and z['cgroup_charged_memory_max_gib']==14 and z['own_rss_sample_stop_gib']==14
 assert not any(x.startswith('-M')for x in z['argv'])
 assert z['wall_limit_s']==(1680 if key=='grid-stream-r1'else 800)
 assert all(int(x.split()[1])==0 for x in z['memory_events'].splitlines())
 assert z['charged_peak_bytes']<14*1024**3 and z['sampled_tree_peak_bytes']<14*1024**3
 mem=[json.loads(x)for x in(d/'memory.jsonl').read_text().splitlines()]
 assert max(x['rss_bytes']for x in mem)==z['sampled_tree_peak_bytes']
 for x in mem:
  for item in x['processes']:
   ident=(item['pid'],item['birth']);identities.add(ident);assert not live(*ident)
 ev=[json.loads(x)for x in(d/'stdout').read_text().splitlines()if x.startswith('{')]
 done=[x for x in ev if x.get('event')=='complete'];assert len(done)==1
 ac=[x for x in ev if x.get('event')=='accept'];ids=[x['module']for x in ac]
 n=4449 if key.startswith('barrier') else 3793
 assert len(ids)==len(set(ids))==n and done[0]['modules']==n
 assert done[0]['constants']==(425463 if key.startswith('barrier')else 382707)
 assert done[0]['skipped_unsafe_partial']==(3595 if key.startswith('barrier')else 3554)
 headers={x['module']:x for x in ac};root=z['argv'][-1];todo=[root];seen=set()
 while todo:
  name=todo.pop()
  if name in seen:continue
  seen.add(name);assert name in headers;todo.extend(headers[name]['imports'])
 assert seen==set(ids)
 summary=json.loads((b/(key+'-summary.json')).read_text())
 assert set(summary['accepted'])==set(ids) and summary['completed']
 if key!='grid-stream-r1':
  assert not any(x.get('event')=='curve_cell'for x in ev)
  assert summary['scope']=='one_full_cold_closure_single_configuration' and not summary['chunk_rewrite_enabled']
  assert summary['accepted_set_equal_to_same_input_curve']
 assert not any(x.get('event')=='reject'for x in ev)
 accepts[key]=headers;results[key]=z;events[key]=ev
 rows.append(dict(key=key,wall_s=z['wall_s'],wait4_CPU_s=z['user_s']+z['system_s'],cgroup_CPU_s=z['cgroup_usage_s'],wait4_maxrss_kib=z['peak_rss_kib'],sampled_RSS_bytes=z['sampled_tree_peak_bytes'],charged_peak_bytes=z['charged_peak_bytes'],accepted=n,native_limit_s=z['wall_limit_s'],all_native_retired=True))
pairs=[]
for label in ['barrier','grid']:
 a=label+'-full-reference1-r1';p=label+'-full-parallel4-r1';aa=accepts[a];pp=accepts[p]
 assert set(aa)==set(pp)
 for name in aa:
  assert aa[name]['imports']==pp[name]['imports'] and aa[name]['constants']==pp[name]['constants']
 old=json.loads((b/(label+'-stream-r1-summary.json')).read_text())
 assert set(old['accepted'])==set(aa)
 za=results[a];zp=results[p]
 pairs.append(dict(cohort=label,modules=len(aa),reference_wall_s=za['wall_s'],parallel4_wall_s=zp['wall_s'],wall_ratio=za['wall_s']/zp['wall_s'],wall_reduction_percent=100*(1-zp['wall_s']/za['wall_s']),cgroup_CPU_increase_percent=100*(zp['cgroup_usage_s']/za['cgroup_usage_s']-1),wait4_CPU_increase_percent=100*((zp['user_s']+zp['system_s'])/(za['user_s']+za['system_s'])-1),interrupted_pair=label=='grid'))
grid_complete=json.loads((b/'grid-full-pair-complete.json').read_text())
assert grid_complete['resumed_after_controller_path_error'] and grid_complete['reference_reused_without_rerun']
curve=[x for x in events['grid-stream-r1']if x.get('event')=='curve_cell']
assert [x['kind']for x in curve]==['serial','parallel1','parallel2','parallel4','parallel8']
gridrows=[]
for x in curve:
 assert x['accept'] and x['module']=='OAI.Analysis.PlanarPacking.Grid'
 assert x['jobs']==(0 if x['kind']=='serial'else 7898) and x['waves']==(0 if x['kind']=='serial'else 8)
 gridrows.append(dict(kind=x['kind'],wall_s=int(x['elapsed_ns'])/1e9,CPU_s=int(x['cpu_ns'])/1e9))
metrics=dict(grid8_incremental_ratio=gridrows[0]['wall_s']/gridrows[-1]['wall_s'],grid8_CPU_increase_percent=100*(gridrows[-1]['CPU_s']/gridrows[0]['CPU_s']-1),grid8_CPU_wall=gridrows[-1]['CPU_s']/gridrows[-1]['wall_s'])
for name,rs in [('complete-native-cells.csv',rows),('complete-pairs.csv',pairs),('grid-v14-incremental.csv',gridrows)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]),lineterminator='\n');w.writeheader();w.writerows(rs)
# The native clock ends at wait4. Post-wait sampler join/cgroup removal is verified, not charged to this wall clock.
assert 'wall_s=time.monotonic()-begin' in (b/'native.py').read_text()
j=dict(pairs=pairs,grid_incremental=gridrows,grid_metrics=metrics,full_native_cells=4,additional_incremental_processes=1,unique_sampled_PID_births=len(identities),root_new_native_runs=0,full_clock='Popen-to-wait4 wall; excludes outer queue/setup and subsequent sampler/cgroup cleanup',CPU_ledger='cgroup usage preferred; complete wait4 user+system separately retained',cgroup_CPU_wait4_agreement_max_abs_s=max(abs(z['cgroup_usage_s']-z['user_s']-z['system_s'])for z in results.values()),root_analysis_s=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'step':str(s),**j},indent=2))
