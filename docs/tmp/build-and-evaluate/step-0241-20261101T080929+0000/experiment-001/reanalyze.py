from pathlib import Path
import os,json,gzip,time,resource,subprocess,csv,statistics,math,datetime
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-repaired-math-paper-step.txt').read_text().strip());e=s/'experiment-001'
def freeze(q,name):
 b=Path(q).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(b,mtime=0));return b
def live(pid,birth):
 f=Path('/proc')/str(pid)/'stat'
 return f.exists() and f.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
p=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14');m=r/'research/parallel-stream-check'
for f in ['v14-math-results.md','v14-math-cells.csv','v14-math-summary.csv','v14-math-completeness.json','v14-native-controls.json','step007.md','step008.md','worker-start.md','correctness.md']:
 freeze(m/f,'published-'+f)
for f in ['matrix-results.json','matrix-complete.json','matrix-terminal.json','matrix-launch.json','run.py','native.py','source-change.json','controls-qualified.json','certificate-controls-qualified.json']:
 freeze(p/f,'raw-v14-'+f)
for f in ['ParallelCore.lean','ParallelStream.lean','checked_commit.c']:
 freeze(p/'source'/f,'frozen-v14-'+f)
assert json.loads((p/'matrix-complete.json').read_text())['cells']==18
launch=json.loads((p/'matrix-launch.json').read_text());assert not live(launch['pid'],launch['birth'])
records=json.loads((p/'matrix-results.json').read_text());assert len(records)==18
variants=['reference','audited','parallel1','parallel2','parallel4','parallel8']
assert {x['key'] for x in records}=={f'math-{v}-{rep}' for v in variants for rep in range(3)}
base_set=set(records[0]['accepted']);assert len(base_set)==1330
packet=[];rows=[];controls=json.loads((m/'v14-native-controls.json').read_text())
for x in records:
 d=p/'runs'/x['key'];z=json.loads((d/'result.json').read_text());c=json.loads((d/'command.json').read_text())
 assert x['argv']==z['argv']==c['argv'] and x['wall_s']==z['wall_s']
 assert z['returncode']==0 and z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons'] and z['wait4_usage_complete']
 assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
 assert z['affinity']==list(range(8)) and z['measured'] and z['cgroup_charged_memory_max_gib']==14
 assert not any(a.startswith('-M') for a in z['argv']) and z['argv'][-1]=='Mathlib.Data.Nat.Basic'
 assert all(int(line.split()[1])==0 for line in z['memory_events'].splitlines())
 stdout=freeze(d/'stdout',x['key']+'-stdout').decode();freeze(d/'stderr',x['key']+'-stderr');freeze(d/'memory.jsonl',x['key']+'-memory.jsonl')
 events=[json.loads(l) for l in stdout.splitlines() if l.startswith('{')]
 accepted=[q['module'] for q in events if q.get('event')=='accept'];assert len(accepted)==len(set(accepted))==1330 and set(accepted)==base_set
 done=[q for q in events if q.get('event')=='complete'];assert len(done)==1
 assert done[0]['modules']==1330 and done[0]['constants']==132484 and done[0]['skipped_unsafe_partial']==2269
 kind=x['key'][5:].rsplit('-',1)[0];rep=int(x['key'].rsplit('-',1)[1])
 work=[q for q in events if q.get('event')=='kernel_work']
 if kind.startswith('parallel'):
  counts={name:sum(int(q.get(name,0)) for q in work if q.get('path')=='parallel') for name in ['jobs','waves']}
  assert len([q for q in work if q.get('path')=='parallel'])==858 and counts=={'jobs':55255,'waves':3616}
  assert len([q for q in work if q.get('path')=='upstream_complex_or_cycle'])==472 and done[0]['module_local_fallbacks']==0
  assert not any(q.get('event')=='chunk_work' for q in events)
 rows.append(dict(variant=kind,repeat=rep,wall_s=z['wall_s'],CPU_s=z['user_s']+z['system_s'],RSS_KiB=z['peak_rss_kib'],sampled_RSS_bytes=z['sampled_tree_peak_bytes'],charged_peak_bytes=z['charged_peak_bytes'],cgroup_CPU_s=z['cgroup_usage_s']))
 packet.append(dict(key=x['key'],result=z,command=c,complete=done[0],accepted=accepted))
# Repaired-version control receipts, kept separate from timings.
controlpacket=[]
assert len(controls['ordinary'])==20 and len(controls['certificate'])==3
for q in controls['ordinary']:
 key=q['key'];d=p/'runs'/key;z=json.loads((d/'result.json').read_text())
 assert q['qualified'] and z['returncode']==(0 if q['expected_accept'] else 1)
 assert z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons'] and not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
 txt=(d/'stdout').read_text();ev=[json.loads(x) for x in txt.splitlines() if x.startswith('{')]
 assert any(x.get('event')=='reject' for x in ev)==(not q['expected_accept'])
 controlpacket.append(dict(key=key,result=z,events=ev))
for key,rc in [('certificate-good-all',0),('certificate-bad-input',1),('certificate-bad-chunk',1)]:
 d=p/'runs'/key;z=json.loads((d/'result.json').read_text());ev=[json.loads(x) for x in(d/'stdout').read_text().splitlines()if x.startswith('{')]
 assert z['returncode']==rc and z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons'] and not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
 if rc:assert any(x.get('event')=='control_reject' and 'kernel_reject' in x.get('error','') for x in ev)
 else:assert any(x.get('event')=='chunk_work' and x['parents']==10 and x['children']==80 and x['axioms']==['propext'] and not x['sorry'] for x in ev)
 controlpacket.append(dict(key=key,result=z,events=ev))
assert "ORAW/'constructed/lib'" in (p/'run.py').read_text() and 'ORAW/' in (p/'run.py').read_text()
med={v:dict(wall_s=statistics.median(x['wall_s'] for x in rows if x['variant']==v),CPU_s=statistics.median(x['CPU_s'] for x in rows if x['variant']==v),minimum_wall_s=min(x['wall_s'] for x in rows if x['variant']==v),maximum_wall_s=max(x['wall_s'] for x in rows if x['variant']==v)) for v in variants}
pairs=[next(x['wall_s'] for x in rows if x['variant']=='reference' and x['repeat']==rep)/next(x['wall_s'] for x in rows if x['variant']=='parallel8' and x['repeat']==rep) for rep in range(3)]
metrics=dict(wall_median_ratio=med['reference']['wall_s']/med['parallel8']['wall_s'],wall_reduction_percent=100*(1-med['parallel8']['wall_s']/med['reference']['wall_s']),CPU_increase_percent=100*(med['parallel8']['CPU_s']/med['reference']['CPU_s']-1))
j=dict(medians=med,metrics=metrics,paired8=pairs,complete_cells=18,modules_each=1330,entries_each=132484,excluded_each=2269,parallel_modules=858,serial_complex_modules=472,jobs=55255,waves=3616,module_local_fallbacks=0,all_identities_scopes_and_matrix_controller_retired=True,repaired_ordinary_controls=20,requalified_certificate_controls=3,max_RSS_KiB=max(x['RSS_KiB'] for x in rows),max_sampled_RSS_bytes=max(x['sampled_RSS_bytes'] for x in rows),max_charged_bytes=max(x['charged_peak_bytes'] for x in rows),scope='same-artifact paths in frozen runner, three fixed-order fresh-process repetitions per mode; no source-build/service/equivalence proof',additional_implementation_TCB=True,root_analysis_s=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native_runs=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
for name,data in [('native-packet.json',packet),('repaired-control-packet.json',controlpacket)]:(e/(name+'.gz')).write_bytes(gzip.compress(json.dumps(data).encode(),mtime=0))
with(e/'per-cell.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('STEP',s,'METRICS',json.dumps(metrics),'MEDIANS',json.dumps(med),'PAIR',pairs,'ROOT',j['root_analysis_s'],j['root_analysis_maxrss_kib'])
