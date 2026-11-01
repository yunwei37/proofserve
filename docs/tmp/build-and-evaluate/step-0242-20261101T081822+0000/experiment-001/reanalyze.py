from pathlib import Path
import os,json,gzip,time,resource,subprocess,csv,datetime
os.sched_setaffinity(0,{22,23});begin=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0242-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-barrier-stream-paper-step.txt').write_text(str(s)+'\n')
def freeze(q,name):
 b=Path(q).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(b,mtime=0));return b
def live(pid,birth):
 q=Path('/proc')/str(pid)/'stat'
 return q.exists() and q.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
p=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14');d=p/'runs/barrier-stream-r1'
for f in ['result.json','command.json','stdout','stderr','memory.jsonl']:freeze(d/f,'native-'+f)
for f in ['barrier-stream-r1-summary.json','barrier-r1-launch.json','barrier-r1-terminal.json','curve.py','native.py']:freeze(p/f,'raw-'+f)
z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
assert z['argv']==cmd['argv'] and z['returncode']==0 and z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons'] and z['wait4_usage_complete']
assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
assert z['affinity']==list(range(8)) and z['measured'] and z['cgroup_charged_memory_max_gib']==14
assert not any(x.startswith('-M') for x in z['argv'])
assert all(int(l.split()[1])==0 for l in z['memory_events'].splitlines())
launch=json.loads((p/'barrier-r1-launch.json').read_text());assert not live(launch['pid'],launch['birth'])
events=[json.loads(l) for l in (d/'stdout').read_text().splitlines() if l.startswith('{')]
curves=[x for x in events if x.get('event')=='curve_cell'];assert [x['kind'] for x in curves]==['serial','parallel1','parallel2','parallel4','parallel8']
target='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
assert all(x['accept'] and x['module']==target and x['retained_certificate_regions']==0 for x in curves)
assert all(x['jobs']==3425 and x['waves']==6 and x['route']=='parallel' for x in curves[1:])
headers={x['module']:x for x in events if x.get('event')=='module_header'};accepted=[x['module'] for x in events if x.get('event')=='accept']
assert len(accepted)==len(set(accepted))==len(headers)==4449 and set(accepted)==set(headers)
todo=[target];seen=set()
while todo:
 n=todo.pop()
 if n in seen:continue
 seen.add(n);assert n in headers;todo.extend(headers[n]['imports'])
assert seen==set(headers)
done=next(x for x in events if x.get('event')=='complete');assert done['modules']==4449
assert not any(x.get('event') in ['reject','chunk_work'] for x in events)
# This source is exactly the source qualified and frozen in rootstep0241.
prior=r/'docs/tmp/build-and-evaluate/step-0241-20261101T080929+0000/experiment-001'
for f in ['ParallelCore.lean','ParallelStream.lean','checked_commit.c']:
 b=freeze(p/'source'/f,'frozen-v14-'+f);assert b==gzip.decompress((prior/('frozen-v14-'+f+'.gz')).read_bytes())
rows=[dict(kind=x['kind'],workers=x['workers'],wall_s=int(x['elapsed_ns'])/1e9,CPU_s=int(x['cpu_ns'])/1e9,jobs=x['jobs'],waves=x['waves']) for x in curves]
for x in rows:
 x['serial_to_wall_ratio']=rows[0]['wall_s']/x['wall_s'];x['CPU_increase_percent']=100*(x['CPU_s']/rows[0]['CPU_s']-1)
j=dict(curves=rows,complete_processes=1,repeats_per_mode=1,verified_prefix_modules=4448,closure_modules=4449,closure_complete_event=done,full_process_wall_s=z['wall_s'],full_process_CPU_s=z['user_s']+z['system_s'],cgroup_CPU_s=z['cgroup_usage_s'],sampled_RSS_bytes=z['sampled_tree_peak_bytes'],charged_peak_bytes=z['charged_peak_bytes'],cap_GiB=14,all_identities_scopes_retired=True,source_equal_prior_qualified_v14=True,additional_implementation_TCB=True,scope='five ordered incremental target trials share one independently checked prefix; complete process includes prefix and all five, not cold-mode or old fragment-pipeline speedup',root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native_runs=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
with(e/'incremental-curves.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('STEP',s,'RESULT',json.dumps(j))
