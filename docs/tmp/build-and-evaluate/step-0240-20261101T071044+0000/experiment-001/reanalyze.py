from pathlib import Path
import os,json,gzip,time,resource,csv,subprocess,datetime,math
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0240-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-pooled-grid-paper-step.txt').write_text(str(s)+'\n')
def freeze(q,name):
 b=Path(q).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(b,mtime=0));return b
def live(pid,birth):
 f=Path('/proc')/str(pid)/'stat'
 return f.exists() and f.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
p=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v12');m=r/'research/parallel-stream-check'
for f in ['step005.md','step005-audit.md','certificate-native-controls.json','prepared-targets.csv','resource-failure.md','protocol.md','CertificateControl.lean.in']:
 freeze(m/f,'published-'+f)
for f in ['ParallelCore.lean','ParallelStream.lean','checked_commit.c']:
 freeze(p/'source'/f,'frozen-v12-'+f)
for f in ['certificate-controls-qualified.json','certificate-control-results.json','run-certificate-controls.py','grid-r1-launch.json','grid-r1-terminal.json','grid-stream-r1-summary.json','curve.py','native.py']:
 freeze(p/f,'raw-v12-'+f)
freeze(p/'certificate-control-source/CertificateControls.lean','native-control-source.lean')
packet=[]
for key,expected in [('certificate-good-all',0),('certificate-bad-input',1),('certificate-bad-chunk',1),('grid-stream-r1',0)]:
 d=p/'runs'/key;z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
 assert z['argv']==cmd['argv'] and not any(a.startswith('-M') for a in z['argv'])
 assert z['returncode']==expected and z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons']
 assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
 assert z['affinity']==list(range(8)) and z['cgroup_charged_memory_max_gib']==14 and z['wait4_usage_complete']
 assert all(int(x.split()[1])==0 for x in z['memory_events'].splitlines())
 assert z['measured']==(key=='grid-stream-r1')
 events=[json.loads(x) for x in (d/'stdout').read_text().splitlines() if x.startswith('{')]
 packet.append(dict(key=key,result=z,command=cmd,events=events))
 for f in ['stdout','stderr','memory.jsonl']:freeze(d/f,key+'-'+f)
controls=packet[:3];good=controls[0]['events'];work=next(x for x in good if x['event']=='chunk_work')
selected=list(csv.DictReader((m/'prepared-targets.csv').open()))
assert len(selected)==10 and len({x['original_name'] for x in selected})==10
assert set(work['constants'])=={x['original_name'] for x in selected}
assert all(float(x['profile_cpu_s'])>=1 for x in selected)
assert work['parents']==10 and work['children']==80 and work['workers']==8 and work['axioms']==['propext'] and not work['sorry']
assert next(x for x in good if x['event']=='control_accept')['selected_targets']==10
for x in controls[1:]:
 ev=next(z for z in x['events'] if z['event']=='control_reject');assert 'kernel_reject:' in ev['error'] and 'loose bound variables' in ev['error']
grid=packet[3];curves=[x for x in grid['events'] if x['event']=='curve_cell']
assert [x['kind'] for x in curves]==['serial','parallel1','parallel2','parallel4','parallel8']
assert all(x['accept'] and x['module']=='OAI.Analysis.PlanarPacking.Grid' and x['retained_certificate_regions']==0 for x in curves)
assert all(x['jobs']==7898 and x['waves']==8 and x['route']=='parallel' for x in curves[1:])
headers={x['module']:x for x in grid['events'] if x['event']=='module_header'}
accepts=[x['module'] for x in grid['events'] if x['event']=='accept']
assert len(accepts)==len(set(accepts))==len(headers)==3793 and set(accepts)==set(headers)
todo=['OAI.Analysis.PlanarPacking.Grid'];seen=set()
while todo:
 n=todo.pop()
 if n in seen:continue
 seen.add(n);assert n in headers;todo.extend(headers[n]['imports'])
assert seen==set(headers)
done=next(x for x in grid['events'] if x['event']=='complete')
assert done['modules']==3793 and done['constants']==382707 and done['skipped_unsafe_partial']==3554 and done['module_local_fallbacks']==0
assert not any(x.get('event')=='reject' for x in grid['events'])
src=(p/'source/ParallelStream.lean').read_text()
assert 'let env ← s.checked.replay insertMap' in src and 'sameConstant expected actual' in src
assert 'let t0 ← IO.monoNanosNow' in src and 'let c1 ← processNs' in src
assert len(curves)==5
launch=json.loads((p/'grid-r1-launch.json').read_text());assert not live(launch['pid'],launch['birth'])
rows=[]
for x in curves:
 rows.append(dict(kind=x['kind'],workers=x['workers'],incremental_wall_s=int(x['elapsed_ns'])/1e9,process_CPU_s=int(x['cpu_ns'])/1e9,jobs=x['jobs'],waves=x['waves']))
base=rows[0]
for x in rows:
 x['serial_to_trial_wall_ratio']=base['incremental_wall_s']/x['incremental_wall_s']
 x['CPU_change_percent']=100*(x['process_CPU_s']/base['process_CPU_s']-1)
j=dict(certificates=dict(selected=10,checked_children=80,merged_parents=10,actual_input_CI_matches_selector=True,axioms=['propext'],sorry=False,negative_controls=['corrupt incoming original proof','corrupt prepared child'],scope='trusted imported prefix; root-ready dependencies rechecked; no independent complete closure or gain'),grid=dict(curves=rows,complete_native_processes=1,repetitions_per_mode=1,accepted_closure_modules=3793,entries=382707,unsafe_partial_excluded=3554,whole_process_wall_s=grid['result']['wall_s'],whole_process_CPU_s=grid['result']['user_s']+grid['result']['system_s'],cgroup_CPU_s=grid['result']['cgroup_usage_s'],sampled_RSS_bytes=grid['result']['sampled_tree_peak_bytes'],charged_peak_bytes=grid['result']['charged_peak_bytes'],cap_GiB=14,all_native_identities_and_scopes_retired=True,scope='one prefix checked once, five ordered incremental target trials include planning/check/CI audit; full process includes prefix and all five, not cold single-mode speedup',additional_implementation_TCB=True),root_analysis_s=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native_runs=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
(e/'native-packet.json.gz').write_bytes(gzip.compress(json.dumps(packet).encode(),mtime=0))
with(e/'Grid-incremental-trials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('STEP',s,'GRID',json.dumps(j['grid']),'ROOT',j['root_analysis_s'],j['root_analysis_maxrss_kib'])
