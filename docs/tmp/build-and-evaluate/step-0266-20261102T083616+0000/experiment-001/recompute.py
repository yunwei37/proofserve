from pathlib import Path
import os,json,csv,gzip,tarfile,datetime,time,resource,subprocess,collections
os.sched_setaffinity(0,{22,23});start=time.monotonic()
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v16')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0266-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-heterogeneous-root-step.txt').write_text(str(s)+'\n')
for n in ['docs/user-instruction.md','docs/questions-for-author.md','docs/research-status.md','docs/research-plan.md','research/README.md','docs/novelty-20261101.md','docs/paper/main.tex','docs/idea-story.md']:
 p=r/n
 if p.exists():(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress(p.read_bytes()))
t=json.loads((b/'scaling-terminal.json').read_text());launch=json.loads((b/'scaling-launch.json').read_text())
assert t['state']=='complete'and t['error']is None and len(t['cells'])==4
refp=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/barrier-full-reference1-r1-summary.json')
ref=json.loads(refp.read_text());reference=set(ref['accepted']);assert len(reference)==4449
identities={(int(launch['pid']),str(launch['birth']))};rows=[];graphs=[];paths=[];freeze=[refp]
for n in ['scaling-launch.json','scaling-terminal.json','scaling-results.json','scaling-controller.log','native.py','extended.py','affinity-snapshots.jsonl','qualification-launch.json','qualification-terminal.json','extended-qualified.json','extended-build.json','extended-build-r1.json','build_extended.py']:
 p=b/n
 if p.exists():freeze.append(p)
freeze+=list((b/'source').glob('*'))
for i,c in enumerate(t['cells']):
 workers=[8,12,16,24][i];key='barrier-full-j'+str(workers);d=b/'runs'/key
 assert c['key']==key
 result=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
 assert result['returncode']==0 and result['wait4_usage_complete']and not result['stop_reasons']
 assert result['affinity']==list(range(workers))and cmd['wall_limit_s']==500
 assert not any(str(a).startswith('-M')for a in cmd['argv'])
 assert not Path(result['cgroup']).exists()
 events=[json.loads(v)for v in (d/'stdout').read_text().splitlines()if v.startswith('{')]
 assert not any(v.get('event')=='reject'for v in events)
 acc=[v for v in events if v.get('event')=='accept'];head=[v for v in events if v.get('event')=='module_header'];complete=[v for v in events if v.get('event')=='complete']
 assert len(acc)==len(head)==4449 and len({v['module']for v in acc})==4449
 assert {v['module']for v in acc}==reference==set(c['accepted_IDs'])
 assert len(complete)==1 and complete[0]['constants']==425463 and complete[0]['skipped_unsafe_partial']==3595 and complete[0]['module_local_fallbacks']==0
 graph={v['module']:(v['imports'],v['constants'])for v in head}
 assert graph=={v['module']:(v['imports'],v['constants'])for v in acc}
 graphs.append(graph)
 root='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41';seen=set();pending=[root]
 while pending:
  n=pending.pop()
  if n in seen:continue
  seen.add(n);assert n in graph;pending.extend(graph[n][0])
 assert seen==reference
 identities.add((int(result['pid']),str(result['birth'])))
 mem=[json.loads(v)for v in (d/'memory.jsonl').read_text().splitlines()]
 for v in mem:
  for p in v['processes']:identities.add((int(p['pid']),str(p['birth'])))
 assert max(v['rss_bytes']for v in mem)==result['sampled_tree_peak_bytes']
 ev=dict(v.split()for v in result['memory_events'].splitlines());assert int(ev['oom'])==int(ev['oom_kill'])==0
 counts=collections.Counter();dur=collections.defaultdict(float)
 for v in events:
  if v.get('event')=='kernel_work':
   counts[v['path']]+=1;dur[v['path']]+=int(v['elapsed_ns'])/1e9
 assert sum(counts.values())==4449
 cpu=result['user_s']+result['system_s']
 rows.append(dict(workers=workers,P_cores=8,E_cores=workers-8,wall_s=result['wall_s'],wait4_CPU_s=cpu,cgroup_CPU_s=result['cgroup_usage_s'],wait4_RSS_KiB=result['peak_rss_kib'],sampled_tree_RSS_B=result['sampled_tree_peak_bytes'],charged_peak_B=result['charged_peak_bytes'],accepted=4449))
 for route,seconds in dur.items():paths.append(dict(workers=workers,route=route,modules=counts[route],wall_s=seconds))
 paths.append(dict(workers=workers,route='outside_recorded_kernel_work',modules=0,wall_s=result['wall_s']-sum(dur.values())))
 for n in ['command.json','result.json','stdout','stderr','memory.jsonl']:freeze.append(d/n)
assert all(g==graphs[0]for g in graphs)
retired=[]
for pid,birth in sorted(identities):
 p=Path('/proc')/str(pid)/'stat';current=p.read_text().split(') ')[1].split()[19]if p.exists()else None
 assert current!=birth,(pid,birth)
 retired.append(dict(pid=pid,birth=birth,current_birth=current))
for name,data in [('curve.csv',rows),('paths.csv',paths),('retired-identities.csv',retired)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
for n in ['research/parallel-stream-check/extended-plan.md','research/parallel-stream-check/step016.md','research/parallel-stream-check/step016-audit.md','research/parallel-stream-check/step017.md','research/parallel-stream-check/step017-audit.md','research/parallel-stream-check/extended-results/heterogeneous-scaling.md']:
 freeze.append(r/n)
with tarfile.open(e/'raw-source-and-owner-reports.tar.gz','w:gz')as tar:
 for p in freeze:
  assert p.is_file()
  tar.add(p,arcname=str(p).removeprefix('/workspaces/'))
j=dict(cells=rows,wall_increase_percent=100*(rows[-1]['wall_s']/rows[0]['wall_s']-1),CPU_increase_percent=100*(rows[-1]['wait4_CPU_s']/rows[0]['wait4_CPU_s']-1),controller_wall_s=t['wall_s'],native_wall_sum_s=sum(v['wall_s']for v in rows),native_CPU_sum_s=sum(v['wait4_CPU_s']for v in rows),identities=len(retired),same_graphs=True,entries=425463,excluded_unsafe_partial=3595,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,raw_gzip_bytes=(e/'raw-source-and-owner-reports.tar.gz').stat().st_size,new_root_native=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print('STEP',s);print(json.dumps(j))
