from pathlib import Path
import os,time,json,csv,gzip,tarfile,subprocess,statistics,datetime,collections,resource
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v16')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0267-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-stream-bytes-root-step.txt').write_text(str(s)+'\n')
for n in ['docs/user-instruction.md','docs/questions-for-author.md','docs/research-status.md','docs/research-plan.md','research/README.md','docs/novelty-20261101.md','docs/paper/main.tex']:
 p=r/n;(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress(p.read_bytes()))
terminal=json.loads((b/'determinism-terminal.json').read_text());assert terminal['state']=='complete'and terminal['error']is None and len(terminal['cells'])==1
launch=json.loads((b/'determinism-launch.json').read_text());d=b/'runs/barrier-determinism';native=json.loads((d/'result.json').read_text());command=json.loads((d/'command.json').read_text())
assert native['returncode']==0 and native['wait4_usage_complete']and not native['stop_reasons']and not Path(native['cgroup']).exists()
assert command['affinity']==list(range(16))and not any(str(v).startswith('-M')for v in command['argv'])
events=[json.loads(v)for v in (d/'stdout').read_text().splitlines()if v.startswith('{')]
assert not any(v.get('event')=='reject'for v in events)
head=[v for v in events if v.get('event')=='module_header'];acc=[v for v in events if v.get('event')=='accept'];complete=[v for v in events if v.get('event')=='complete']
refp=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/barrier-full-reference1-r1-summary.json');ref=set(json.loads(refp.read_text())['accepted'])
assert len(head)==len(acc)==len(ref)==4449 and {v['module']for v in acc}==ref and len(complete)==1
assert complete[0]['constants']==425463 and complete[0]['skipped_unsafe_partial']==3595 and complete[0]['module_local_fallbacks']==0
graph={v['module']:(v['imports'],v['constants'])for v in head};assert graph=={v['module']:(v['imports'],v['constants'])for v in acc}
pending=['OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'];seen=set()
while pending:
 n=pending.pop()
 if n in seen:continue
 seen.add(n);pending.extend(graph[n][0])
assert seen==ref
current=None;units=[];curves=[];snapshots=[];order=[]
for v in events:
 tag=v.get('event')
 if tag=='curve_begin':current=(int(v['kind'].removeprefix('parallel')),int(v['repeat']));order.append(current)
 elif tag=='unit_check':
  assert current is not None and v['accept'] is True
  units.append(dict(workers=current[0],repeat=current[1],target=v['target'],raw_HB=int(v['raw_HB']),CPU_ns=int(v['cpu_ns']),TID=str(v['tid'])))
 elif tag=='curve_cell':
  assert(int(v['workers']),int(v['repeat']))==current and v['accept']is True and v['jobs']==3425 and v['waves']==6
  curves.append(dict(workers=current[0],repeat=current[1],wall_s=int(v['elapsed_ns'])/1e9,CPU_s=int(v['cpu_ns'])/1e9))
 elif tag=='snapshot':
  assert v['checked_substitutions']==3425 and v['parts']==1 and v['extension_entries_revalidated']is False
  snapshots.append(v)
expected=[(w,rep)for rep in range(3)for w in([1,4,8,16]if rep%2==0 else[16,8,4,1])]
assert order==expected and len(curves)==len(snapshots)==12 and len(units)==1200
groups=collections.defaultdict(list)
for v in units:groups[v['target']].append(v)
assert len(groups)==100
old=list(csv.DictReader((r/'research/reproducible-verdict/census-results-v12/target-heartbeats.csv').open()))
barrier=sorted(v['target']for v in old if v['module']=='BarrierData41');assert len(barrier)==1320
selected={barrier[i*(len(barrier)-1)//99]for i in range(100)};assert set(groups)==selected
ranges=[]
for target,rr in sorted(groups.items()):
 assert len(rr)==12 and {(v['workers'],v['repeat'])for v in rr}==set(expected)
 vals=[v['raw_HB']for v in rr];assert min(vals)>0 and min(vals)==max(vals)
 ranges.append(dict(target=target,observations=12,min_raw_HB=min(vals),max_raw_HB=max(vals),range_pct=0.0))
paircount=0
for target,rr in groups.items():
 dd={(v['workers'],v['repeat']):v for v in rr}
 for rep in range(3):
  for workers in [4,8,16]:assert dd[(1,rep)]['raw_HB']==dd[(workers,rep)]['raw_HB'];paircount+=1
original=Path(json.loads((r/'research/parallel-stream-check/extended-results/original-serialization-comparison.json').read_text())['input'])
baseline=original.read_bytes();assert len(baseline)==9160440
artifactrows=[]
for v in snapshots:
 p=Path(v['file']);assert p.parent==b/'barrier-checked-output'
 data=p.read_bytes();assert data==baseline
 artifactrows.append(dict(path=str(p),bytes=len(data),equal_original=True,substitutions=v['checked_substitutions'],parts=v['parts']))
assert len({v['path']for v in artifactrows})==12
identities={(int(launch['pid']),str(launch['birth'])),(int(native['pid']),str(native['birth']))}
mem=[json.loads(v)for v in(d/'memory.jsonl').read_text().splitlines()]
for v in mem:
 for p in v['processes']:identities.add((int(p['pid']),str(p['birth'])))
assert max(v['rss_bytes']for v in mem)==native['sampled_tree_peak_bytes']
retired=[]
for pid,birth in sorted(identities):
 p=Path('/proc')/str(pid)/'stat';now=p.read_text().split(') ')[1].split()[19]if p.exists()else None;assert now!=birth
 retired.append(dict(pid=pid,birth=birth,current_birth=now))
m=dict(v.split()for v in native['memory_events'].splitlines());assert int(m['oom'])==int(m['oom_kill'])==0
summary=[]
for workers in [1,4,8,16]:
 cc=[v for v in curves if v['workers']==workers];uu=[v for v in units if v['workers']==workers]
 totals=[sum(v['CPU_ns']for v in uu if v['repeat']==rep)/1e9 for rep in range(3)]
 summary.append(dict(workers=workers,median_leaf_wall_s=statistics.median(v['wall_s']for v in cc),median_leaf_CPU_s=statistics.median(v['CPU_s']for v in cc),median_sampled100_call_CPU_s=statistics.median(totals),sampled_TID_unions=';'.join(str(len({v['TID']for v in uu if v['repeat']==rep}))for rep in range(3))))
for name,data in [('units.csv',units),('target-ranges.csv',ranges),('leaf-summary.csv',summary),('artifact-byte-comparisons.csv',artifactrows),('retired-identities.csv',retired)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
freeze=[b/n for n in ['determinism-launch.json','determinism-terminal.json','determinism-artifacts.json','determinism-controller.log','extended.py','native.py','source/ParallelCore.lean','source/ParallelStream.lean','source/checked_commit.c']]
freeze+=[d/n for n in ['command.json','result.json','memory.jsonl','stdout','stderr']]
freeze+=[r/n for n in ['research/parallel-stream-check/step018.md','research/parallel-stream-check/step018-audit.md','research/parallel-stream-check/extended-results/parallel-determinism.md','research/parallel-stream-check/extended-results/original-serialization-comparison.json']]
freeze.append(refp)
with tarfile.open(e/'stream-raw-source-and-owner-reports.tar.gz','w:gz')as tar:
 for p in freeze:
  if p.exists():tar.add(p,arcname=str(p).removeprefix('/workspaces/'))
j=dict(targets=100,observations=1200,pairs=paircount,per_target_range_P95_pct=0,per_target_range_max_pct=0,all_sampled_targets_in_old_Barrier_census=True,artifacts=12,artifact_bytes=9160440,artifact_equal_original=True,graph_modules=4449,leaf_jobs=3425,leaf_waves=6,identities=len(retired),controller_wall_s=terminal['wall_s'],native_wall_s=native['wall_s'],native_CPU_s=native['user_s']+native['system_s'],wait4_RSS_KiB=native['peak_rss_kib'],sampled_RSS_B=native['sampled_tree_peak_bytes'],charged_peak_B=native['charged_peak_bytes'],leaf_summary=summary,leaf_median_wall_ratio=summary[0]['median_leaf_wall_s']/summary[-1]['median_leaf_wall_s'],sampled_call_CPU_ratio=summary[-1]['median_sampled100_call_CPU_s']/summary[0]['median_sampled100_call_CPU_s'],raw_gzip_bytes=(e/'stream-raw-source-and-owner-reports.tar.gz').stat().st_size,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_root_native=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n');print('STEP',s);print(json.dumps(j))
