from pathlib import Path
import os,json,time,gzip,resource,subprocess,csv,statistics,math,re
os.sched_setaffinity(0,{22,23});begin=time.monotonic();r=Path('/workspaces/repository')
s=Path(Path('/workspaces/.agent-state/gpu-smt-wave-closures-paper-step.txt').read_text().strip());e=s/'experiment-001'
def freeze(p,name):
 b=Path(p).read_bytes();q=e/(name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(q.read_bytes())==b;return b
def live(pid,birth):
 p=Path(f'/proc/{pid}/stat')
 return p.exists() and p.read_text().rsplit(')',1)[1].split()[19]==str(birth)
m=r/'research/chunked-kernel-check';p=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/parallel-barrier-v1')
for f in ['terminal.json','launch.json','completed.json','qualification.json','input.json','ParallelReplay.lean','parallel_matrix.py','declaration_native.py']:
 freeze(p/f,'M-raw-'+f)
term=json.loads((p/'terminal.json').read_text());assert term['complete'] and term['completed']==15
launch=json.loads((p/'launch.json').read_text());assert not live(launch['pid'],launch['birth'])
cells=json.loads((p/'completed.json').read_text());assert len(cells)==15 and len({x['key'] for x in cells})==15
base=cells[0]['acceptance'];assert base['count']==3425 and base['typed_constants_identical']
assert len(base['names'])==len(set(base['names']))==3425
rr=[];packet=[];max_sample=max_charge=0
for cell in cells:
 assert cell['accepted'] and cell['all_native_retired'] and cell['acceptance']==base
 k=cell['k'];assert k in [0,1,2,4,8];rep=int(cell['key'].split('-')[0][1:])
 records=[];worker_modules=[];plan=None;totaljobs=[]
 for key in cell['stage_keys']:
  d=p/'runs'/key;q=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text())
  assert q['returncode']==0 and q['native_retired'] and q['cgroup_retired'] and not q['stop_reasons']
  assert not live(q['pid'],q['birth']) and not Path(q['cgroup']).exists()
  assert q['measured'] and q['affinity']==list(range(8)) and q['cgroup_charged_memory_max_gib']==14
  assert not any(a.startswith('-M') for a in q['argv']) and q['argv']==cmd['argv']
  events=[json.loads(x) for x in (d/'stdout').read_text().splitlines() if x.startswith('{')]
  arg=q['argv'];mode=arg[-3];target=arg[-2];config=json.loads(Path(arg[-1]).read_text())
  assert target==json.loads((p/'input.json').read_text())['olean'] and config.get('mutation','none')=='none'
  if mode=='plan':
   ev=next(x for x in events if x['event']=='plan');plan=ev['levels'];assert len(plan)==6 and sum(map(len,plan))==3425
  elif mode=='wave':
   ev=next(x for x in events if x['event']=='wave_complete')
   done=[i for worker in ev['workers'] for i in worker['indices']]
   assert len(done)==len(set(done)) and sorted(done)==sorted(config['jobs'])
   assert config['prior']==worker_modules
   worker_modules=[x['module'] for x in ev['workers']];totaljobs.extend(done)
  elif mode in ['stock','audit']:
   ev=next(x for x in events if x['event']=='accepted');assert ev==base
   if mode=='audit':assert config['prior']==worker_modules
  else:raise AssertionError(mode)
  records.append(q);packet.append({'cell':cell['key'],'key':key,'command':cmd,'result':q,'config':config})
  max_sample=max(max_sample,q['sampled_tree_peak_bytes']);max_charge=max(max_charge,q['charged_peak_bytes'])
 assert len(records)==(1 if k==0 else 8)
 if k:assert len(totaljobs)==len(set(totaljobs))==3425 and set(totaljobs)==set(range(3425))
 native_cpu=sum(x['user_s']+x['system_s'] for x in records);native_wall=sum(x['wall_s'] for x in records)
 assert math.isclose(native_cpu,cell['native_user_s']+cell['native_system_s'],abs_tol=1e-8)
 assert cell['whole_pipeline_wall_s']>=native_wall
 rr.append({'k':k,'rep':rep,'whole_wall_s':cell['whole_pipeline_wall_s'],'native_CPU_s':native_cpu,'interstage_wall_s':cell['whole_pipeline_wall_s']-native_wall})
assert len(packet)==99
(e/'M-all-native-stage-packet.json.gz').write_bytes(gzip.compress(json.dumps(packet,separators=(',',':')).encode(),mtime=0))
med={str(k):{'wall_s':statistics.median(x['whole_wall_s'] for x in rr if x['k']==k),'native_CPU_s':statistics.median(x['native_CPU_s'] for x in rr if x['k']==k),'minimum_wall_s':min(x['whole_wall_s'] for x in rr if x['k']==k),'maximum_wall_s':max(x['whole_wall_s'] for x in rr if x['k']==k)} for k in [0,1,2,4,8]}
paired=[next(x['whole_wall_s'] for x in rr if x['rep']==rep and x['k']==0)/next(x['whole_wall_s'] for x in rr if x['rep']==rep and x['k']==8) for rep in [0,1,2]]
assert (p/'ParallelReplay.lean').read_bytes()==(m/'ParallelReplay.lean').read_bytes()
for f in ['parallel-result.md','parallel-summary.csv','parallel-validation.json','parallel-qualification.json','step-009-report.md','step-010-report.md']:
 freeze(m/f,'M-'+f)
# Primary official module-task baseline source; this is not a new checker.
sdk=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux/src/lean/LeanChecker.lean')
freeze(sdk,'official-LeanChecker.lean')
assert 'Task' in sdk.read_text()
# Four completed matching O closures from one shared source DAG.
o=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
for f in ['measured.jsonl','cohort-plan.json','progress.json','all-complete.json','window.py','native.py']:
 freeze(o/f,'O-raw-'+f)
ledger=[json.loads(x) for x in gzip.decompress((e/'O-raw-measured.jsonl.gz').read_bytes()).decode().splitlines()]
plan=json.loads((o/'cohort-plan.json').read_text());sources=[x for x in ledger if x['operation']=='build']
assert len(sources)==len({x['module'] for x in sources})==5085
assert all(x['returncode']==0 and all(x['outputs'].values()) and not x['sorry_warning'] for x in sources)
oracles=[x for x in ledger if x['operation']=='matched_oracle']
verified=[]
for x in oracles:
 q=json.loads((o/(x['key']+'.result.json')).read_text());assert q['returncode']==0 and x['closure_complete']
 events=[json.loads(y) for y in (o/(x['key']+'.stdout')).read_text().splitlines()]
 got=[z['module'] for z in events if z['event']=='accept']
 assert len(got)==len(x['requested_modules']) and set(got)==set(x['requested_modules'])
 assert len([z for z in events if z['event']=='one_complete'])==len(got)
 verified.extend(got)
assert len(verified)==len(set(verified))==5085
opacket=[]
for x in sources+oracles+[x for x in ledger if x['operation']=='matched_stream']:
 q=json.loads((o/(x['key']+'.result.json')).read_text());assert q['returncode']==0
 assert q['affinity']==list(range(8)) and q['memory_max_bytes']==12750684160 and not any(a.startswith('-M') for a in q['args'])
 assert not Path(q['cgroup']).exists()
 opacket.append({'key':x['key'],'result':q})
(e/'O-all-completed-native-results.json.gz').write_bytes(gzip.compress(json.dumps(opacket,separators=(',',':')).encode(),mtime=0))
cohorts=[]
for name,spec in plan['cases'].items():
 wanted=set(spec['modules']);b=[x for x in sources if x['module'] in wanted];assert {x['module'] for x in b}==wanted
 st=next(x for x in ledger if x['operation']=='matched_stream' and x['cohort']==name)
 assert st['returncode']==0 and st['closure_complete'] and set(st['accepted_modules'])==wanted and wanted<=set(verified)
 events=[json.loads(y) for y in freeze(o/(st['key']+'.stdout'),'O-'+st['key']+'.stdout').decode().splitlines()]
 assert events[-1]['event']=='complete' and {x['module'] for x in events if x['event']=='accept'}==wanted
 tm=next(x for x in events if x['event']=='module_timing' and x['module']==spec['root']);br=next(x for x in b if x['module']==spec['root'])
 bw=sum(x['wall_s'] for x in b);component=(int(tm['read_ns'])+int(tm['map_ns'])+int(tm['replay_ns']))/1e9
 cohorts.append({'name':name,'root':spec['root'],'modules':len(wanted),'source_work_s':bw,'matched_stream_s':st['wall_s'],'closure_ratio':st['wall_s']/bw,'root_source_s':br['wall_s'],'root_read_map_replay_s':component,'root_kernel_s':int(tm['replay_ns'])/1e9,'root_component_ratio':component/br['wall_s'],'entries':events[-1]['constants'],'unsafe_partial':events[-1]['skipped_unsafe_partial'],'stream_wait4_RSS_KiB':st['peak_rss_kib'],'source_max_wait4_RSS_KiB':max(x['peak_rss_kib'] for x in b)})
assert json.loads((o/'all-complete.json').read_text())['status']=='complete'
original_O_identity={'pid':153406,'birth':'754528646'}
assert not live(**original_O_identity)
for f in ['results.md','cohort-costs.csv','root-components.csv','native-continuation.md','boundary-qualification.json']:
 freeze(r/'research/decoupled-check'/f,'O-'+f)
j={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'M':{'complete_cells':15,'native_stages':99,'typed_constants':3425,'all_final_audits_names_order_and_typed_values_equal':True,'all_stage_identities_and_cgroups_retired':True,'controller_retired':True,'medians':med,'wall_speedup_ratio_of_medians':med['0']['wall_s']/med['8']['wall_s'],'CPU_increase_fraction':med['8']['native_CPU_s']/med['0']['native_CPU_s']-1,'paired_8worker_speedups':paired,'max_sampled_tree_bytes':max_sample,'max_charged_peak_bytes':max_charge,'charged_cap_GiB':14,'boundary':'first stage-config write through final audit retirement; excludes initial output-directory/environment setup and lease wait; includes planning/import/export/driver gaps','scope':'one compiled Barrier module over trusted declared imports; direct stock API baseline, not stock CLI throughput'},'O':{'cohorts':cohorts,'unique_source_calls':5085,'unique_oracle_acceptances':5085,'complete_oracle_chunks':len(oracles),'original_four_cohort_plan_complete':True,'reported_original_controller_identity_retired':original_O_identity,'all_completed_native_scopes_removed':True,'source_max_RSS_KiB':max(x['peak_rss_kib'] for x in sources),'actual_native_cap_bytes':12750684160,'listed_O_share_bytes':4*1024**3,'share_deviation_retained':any(x['peak_rss_kib']*1024>4*1024**3 for x in sources)},'root_analysis_s':time.monotonic()-begin,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'new_native_runs':0}
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print('M',json.dumps(j['M']));print('O_COHORTS',json.dumps(cohorts));print('COUNTS',len(sources),len(verified),len(oracles),'ROOT',j['root_analysis_s'],j['root_analysis_maxrss_kib'])
