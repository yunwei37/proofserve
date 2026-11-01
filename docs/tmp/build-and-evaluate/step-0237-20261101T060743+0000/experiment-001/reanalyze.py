from pathlib import Path
import os,subprocess,json,gzip,time,resource,csv,re,datetime
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0237-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-context-boundary-paper-step.txt').write_text(str(s)+'\n')
def freeze(q,name):
 b=Path(q).read_bytes();dest=e/(name+'.gz');dest.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(dest.read_bytes())==b;return b
def live(pid,birth):
 f=Path('/proc')/str(pid)/'stat'
 return f.exists() and f.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/user-instruction.md','docs/questions-for-author.md']:
 if f!='docs/user-instruction.md':freeze(r/f,'entry-'+Path(f).name)
 text=(r/f).read_text()
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
p=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v10');m=r/'research/parallel-stream-check'
for f in ['README.md','math-results.md','math-completeness.json','controls.json','protocol.md','step002.md','step003.md','step004.md']:
 freeze(m/f,'published-'+f)
for f in ['ParallelStream.lean','ParallelCore.lean','RawControls.lean','checked_commit.c']:
 freeze(p/'source'/f,'frozen-v10-'+f)
for f in ['controls-qualified.json','controls-terminal.json','controls.json','run.py','native.py','tool-provenance.json','curve-clock-qualified.json']:
 freeze(p/f,'raw-v10-'+f)
controls=json.loads((p/'controls.json').read_text());assert len(controls)==20
assert {(x['key'].rsplit('-',1)[0],int(x['key'].rsplit('-',1)[1])) for x in controls}=={(case,k) for case in ['ordinary','duplicate-local-deps','hidden-cycle','corrupt','sibling','definitions','private','waves','duplicate-token','stale-token'] for k in [1,8]}
packet=[]
for key in [x['key'] for x in controls]+['hidden-cycle-v4-red','hidden-cycle-native-oracle']:
 d=p/'runs'/key;z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
 assert z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons']
 assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
 assert z['argv']==cmd['argv'] and not any(a.startswith('-M') for a in z['argv'])
 assert z['affinity']==list(range(8)) and z['cgroup_charged_memory_max_gib']==14 and not z['measured']
 assert all(int(line.split()[1])==0 for line in z['memory_events'].splitlines())
 stdout=freeze(d/'stdout',key+'-stdout').decode();freeze(d/'stderr',key+'-stderr')
 events=[json.loads(line) for line in stdout.splitlines() if line.startswith('{')]
 accepts=[x['module'] for x in events if x.get('event')=='accept'];rejects=[x for x in events if x.get('event')=='reject']
 if key=='hidden-cycle-v4-red':
  assert z['returncode']==0 and 'Cyclic' in accepts and not rejects
  assert '/parallel-stream-check-v4/' in ' '.join(z['argv'])
 elif key=='hidden-cycle-native-oracle':
  assert z['returncode']==1 and len(rejects)==1 and rejects[0]['module']=='Cyclic'
  assert "'Shared.helper'" in rejects[0]['error'] and "unknown constant 'Shared.t'" in rejects[0]['error']
  assert '/parallel-stream-check-v4/' in ' '.join(z['argv']) and z['argv'][-3:]==['one','none','Cyclic']
 else:
  record=next(x for x in controls if x['key']==key);assert record['qualified']
  assert z['returncode']==(0 if record['expected_accept'] else 1)
  assert bool(rejects)==(not record['expected_accept'])
  if key.startswith('hidden-cycle-'):
   assert rejects[0]['context']=='module_local' and 'Cyclic' not in accepts
 packet.append(dict(key=key,command=cmd,result=z,events=events))
rawcycle=(p/'source/RawControls.lean').read_text()
assert 'makeThm helper theoremName,makeThm theoremName helper' in rawcycle
assert 'Init.Prelude' in rawcycle and 'type:=mkConst '+chr(96)+'True' in rawcycle
for f in ['DupA.lean','Cyclic.olean']:freeze(p/'fixtures'/f,'control-input-'+f)
assert 'True.intro' in (p/'fixtures/DupA.lean').read_text()
guard=(p/'source/ParallelStream.lean').read_text();c=(p/'source/checked_commit.c').read_text()
assert '!reachesLocal map ci.name ci.getUsedConstantsAsSet.toList' in guard
assert 'validateDuplicate checked' in guard and 'lean_environment_add(dest, ci)' in c
old=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v4')
for f in ['matrix-complete.json','matrix-results.json','both-terminal.json']:
 freeze(old/f,'historical-v4-'+f)
matrix=json.loads((old/'matrix-results.json').read_text());assert len(matrix)==18
accepted=set(matrix[0]['accepted']);assert len(accepted)==1330
for z in matrix:
 assert z['returncode']==0 and set(z['accepted'])==accepted and z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons']
 assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
active=p/'runs/envelope-stream-r1'
active_observation={'point':str(p),'result_present':(active/'result.json').exists()}
if not active_observation['result_present']:
 samples=(active/'memory.jsonl').read_text().splitlines();last=json.loads(samples[-1]);active_observation['last_sample']=last
 active_observation['identities_live']=[dict(pid=x['pid'],birth=x['birth'],live=live(x['pid'],x['birth'])) for x in last['processes']]
 active_observation['locks']=Path('/proc/locks').read_text()
(e/'control-native-packet.json.gz').write_bytes(gzip.compress(json.dumps(packet).encode(),mtime=0))
j=dict(controls=20,raw_control_processes=22,all_control_identities_and_scopes_retired=True,v4_accepts_Cyclic=True,same_v4_binary_module_local_rejects_Cyclic=True,repaired_workers_1_and_8_reject_Cyclic=True,historical_v4_positive_cells=18,historical_v4_module_acceptances=1330,not_final_repaired_performance=True,active_point=active_observation,additional_trusted_code=['checked-token coordinator','pinned internal-ABI C environment insertion adapter'],claim='acceptance-contract mismatch on malformed True-proof module; not proof of a false theorem or original kernel defect',root_analysis_s=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native_runs=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
(e/'transport-initial-failure.txt').write_text('Initial tool script rejected before remote execution because a literal Lean backtick ended a JavaScript template. Retried with chr(96). No remote experiment ran or changed.\\n')
print('STEP',s,'VERIFIED',j['controls'],j['raw_control_processes'],'HISTORICAL',len(matrix),'ROOT',j['root_analysis_s'],j['root_analysis_maxrss_kib'],'ACTIVE',active_observation['result_present'])
