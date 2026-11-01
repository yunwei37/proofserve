from pathlib import Path
import os,json,gzip,time,resource,csv,subprocess,datetime,math
os.sched_setaffinity(0,{22,23});begin=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0243-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-envelope-cold-paper-step.txt').write_text(str(s)+'\n')
def freeze(q,name):
 b=Path(q).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(b,mtime=0));return b
def live(pid,birth):
 q=Path('/proc')/str(pid)/'stat'
 return q.exists() and q.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
p=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14');d=p/'runs/envelope-stream-r1';m=r/'research/parallel-stream-check'
for f in ['result.json','command.json','stdout','stderr','memory.jsonl']:freeze(d/f,'native-'+f)
for f in ['envelope-stream-r1-summary.json','envelope-r1-launch.json','envelope-r1-terminal.json','curve.py','native.py']:freeze(p/f,'raw-'+f)
for f in ['envelope-stream-results.md','step011.md','step011-audit.md','selection-scope.md','compute-completeness.json']:
 freeze(m/f,'published-'+f)
z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
assert z['argv']==cmd['argv'] and z['returncode']==0 and z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons'] and z['wait4_usage_complete']
assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
assert z['affinity']==list(range(8)) and z['cgroup_charged_memory_max_gib']==14 and not any(x.startswith('-M') for x in z['argv'])
assert z['wall_s']<1680 and all(int(x.split()[1])==0 for x in z['memory_events'].splitlines())
assert z['sampled_tree_peak_bytes']<14*1024**3 and z['peak_rss_kib']*1024>14*1024**3 and z['peak_rss_kib']*1024<16*1024**3
launch=json.loads((p/'envelope-r1-launch.json').read_text());assert not live(launch['pid'],launch['birth'])
events=[json.loads(x) for x in(d/'stdout').read_text().splitlines()if x.startswith('{')]
curves=[x for x in events if x.get('event')=='curve_cell']
assert [x['kind'] for x in curves]==['serial','parallel1','parallel2','parallel4','parallel8','chunk1','chunk2','chunk4','chunk8']
target='OAI.Analysis.Triangular.Envelope.EnvelopePsiB'
assert all(x['accept'] and x['module']==target for x in curves)
headers={x['module']:x for x in events if x.get('event')=='module_header'};accepted=[x['module'] for x in events if x.get('event')=='accept']
assert len(accepted)==len(set(accepted))==len(headers)==10752 and set(accepted)==set(headers)
assert headers[target]['constants']==110
todo=[target];seen=set()
while todo:
 name=todo.pop()
 if name in seen:continue
 seen.add(name);assert name in headers;todo.extend(headers[name]['imports'])
assert seen==set(headers)
done=next(x for x in events if x.get('event')=='complete');assert done['modules']==10752 and done['constants']==785706 and done['skipped_unsafe_partial']==4444 and done['module_local_fallbacks']==0
prior=r/'docs/tmp/build-and-evaluate/step-0241-20261101T080929+0000/experiment-001'
for f in ['ParallelCore.lean','ParallelStream.lean','checked_commit.c']:
 b=freeze(p/'source'/f,'frozen-v14-'+f);assert b==gzip.decompress((prior/('frozen-v14-'+f+'.gz')).read_bytes())
src=(p/'source/ParallelStream.lean').read_text();core=(p/'source/ParallelCore.lean').read_text()
assert 'expected.name==actual.name && expected.type==actual.type' in src and 'expected.levelParams==actual.levelParams' in src and 'sameConstant expected actual' in src
assert 'unless sameConstant original bundle.reference' in core and 'thm with value' in core
assert "PARALLEL_WORKERS='4'" in (p/'curve.py').read_text()
names={x['original_name']for x in csv.DictReader((m/'prepared-targets.csv').open())};assert len(names)==10
pending=[];rows=[];allchildren=0;allparents=0
for ev in events:
 if ev.get('event')=='chunk_work':pending.append(ev)
 if ev.get('event')!='curve_cell':continue
 row=dict(kind=ev['kind'],workers=ev['workers'],wall_s=int(ev['elapsed_ns'])/1e9,CPU_s=int(ev['cpu_ns'])/1e9,jobs=ev['jobs'],waves=ev['waves'])
 if ev['kind'].startswith('chunk'):
  k=int(ev['kind'][5:]);assert sum(x['parents']for x in pending)==10 and sum(x['children']for x in pending)==10*k
  assert {v for x in pending for v in x['constants']}==names
  assert all(x['axioms']==['propext'] and not x['sorry'] for x in pending)
  row.update(checked_children=10*k,checked_parent_merges=10)
  allchildren+=10*k;allparents+=10
 else:assert not pending;row.update(checked_children=0,checked_parent_merges=0)
 assert ev['jobs']==(0 if ev['kind']=='serial' else 110)
 rows.append(row);pending=[]
assert not pending and allchildren==150 and allparents==40
assert not any(x.get('event')=='reject' for x in events)
b=rows[0];decl=next(x for x in rows if x['kind']=='parallel8');chunk=next(x for x in rows if x['kind']=='chunk8')
metrics=dict(chunk8_over_declaration8_wall_ratio=decl['wall_s']/chunk['wall_s'],chunk8_vs_decl8_wall_reduction_percent=100*(1-chunk['wall_s']/decl['wall_s']),chunk8_vs_decl8_CPU_increase_percent=100*(chunk['CPU_s']/decl['CPU_s']-1),chunk8_over_serial_wall_ratio=b['wall_s']/chunk['wall_s'],chunk8_vs_serial_CPU_increase_percent=100*(chunk['CPU_s']/b['CPU_s']-1),declaration8_over_serial_wall_ratio=b['wall_s']/decl['wall_s'])
anc=[x for x in events if x.get('event')=='kernel_work' and x.get('module','').endswith('.WaveExpData')]
j=dict(curves=rows,metrics=metrics,complete_processes=1,observations_per_mode=1,verified_prefix_modules=10751,closure_modules=10752,input_entries=785706,unsafe_partial_exclusions=4444,leaf_entries=110,rewritten_parents=10,aggregate_children_across_four_k=150,aggregate_merges_across_four_k=40,axiom_scope='transformed parents union propext; not whole-repository axiom audit',prefix_workers=4,full_process_wall_s=z['wall_s'],full_native_CPU_s=z['user_s']+z['system_s'],full_cgroup_CPU_s=z['cgroup_usage_s'],sum_incremental_leaf_wall_s=sum(x['wall_s']for x in rows),nontrial_residual_wall_s=z['wall_s']-sum(x['wall_s']for x in rows),wait4_max_RSS_KiB=z['peak_rss_kib'],sampled_tree_peak_bytes=z['sampled_tree_peak_bytes'],charged_peak_bytes=z['charged_peak_bytes'],sample_stop_and_charged_cap_GiB=14,native_share_GiB=16,wait4_peak_exceeds_sample_stop_but_not_sampled=True,all_native_identities_scopes_controller_retired=True,WaveExpData_aggregate_events=anc,source_equal_prior_qualified_v14=True,scope='cold prefix plus nine ordered incremental leaf trials, not a single-configuration whole-closure speedup or whole-cohort serial parity',new_native_runs=0,root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
with(e/'incremental-curves.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('STEP',s,'METRICS',json.dumps(metrics),'WHOLE',j['full_process_wall_s'],j['full_cgroup_CPU_s'],'LEAF',j['sum_incremental_leaf_wall_s'],'RESIDUAL',j['nontrial_residual_wall_s'],'ROOT',j['root_analysis_s'],j['root_analysis_maxrss_kib'])
