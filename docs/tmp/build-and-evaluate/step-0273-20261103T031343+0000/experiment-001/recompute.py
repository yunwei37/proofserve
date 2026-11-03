from pathlib import Path
import os,json,csv,gzip,tarfile,time,resource,subprocess,collections,statistics,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-attribution-root-step.txt').read_text().strip());e=s/'experiment-001'
start=time.monotonic();b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2');root='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
refp=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/barrier-full-reference1-r1-summary.json');ref=set(json.loads(refp.read_text())['accepted']);assert len(ref)==4449
inputs={refp};identities=set();cgroups=set();allgraphs=[];full=[];phases=[];work={};units=collections.defaultdict(list);leaf=[];snapshots=[];peakrss=sample=charged=0
def retired(pid,birth):
 p=Path(f'/proc/{pid}/stat')
 if p.exists():assert p.read_text().rsplit(')',1)[1].split()[19]!=str(birth),(pid,birth)
 identities.add((int(pid),str(birth)))
for p in b.glob('*launch.json'):
 j=json.loads(p.read_text())
 for pk,bk in [('pid','birth'),('pid','birth_ticks'),('controller_pid','controller_birth')]:
  if pk in j and bk in j:retired(j[pk],j[bk])
 inputs.add(p)
series=json.loads((b/'series-terminal.json').read_text());assert series['state']=='complete'and series['error']is None and all(v['state']=='complete'and v['returncode']==0 for v in series['phases']);inputs.add(b/'series-terminal.json')
terms={}
for f in ['p12','p48','types','observer','placement','placement-profile','det24']:
 p=b/(f+'-terminal.json');inputs.add(p);j=json.loads(p.read_text());assert j['state']=='complete'and j['error']is None
 for v in j['cells']:terms[v['key']]=v
assert len(terms)==13
for key,term in terms.items():
 q=b/'runs'/key;v=json.loads((q/'result.json').read_text());cmd=json.loads((q/'command.json').read_text())
 assert v['returncode']==0 and v['wait4_usage_complete']and v['native_retired']and v['cgroup_retired']and not v['stop_reasons']
 assert v['argv']==cmd['argv']==term['argv']and v['measured']and v['cgroup_charged_memory_max_gib']==v['own_rss_sample_stop_gib']==14
 assert not any(x.startswith('-M')for x in v['argv']);assert not Path(v['cgroup']).exists();cgroups.add(v['cgroup'])
 events=dict(x.split()for x in v['memory_events'].splitlines());assert int(events['oom'])==int(events['oom_kill'])==0
 retired(v['pid'],v['birth'])
 for line in(q/'memory.jsonl').open():
  m=json.loads(line)
  for x in m['processes']:retired(x['pid'],x['birth'])
 assert (q/'stderr').read_bytes()==b''
 graph={};accept={};profiles={};deps={};duplicates=[];complete=[];cur=None;evcount=collections.Counter()
 for line in(q/'stdout').open():
  j=json.loads(line);typ=j['event'];evcount[typ]+=1
  if typ=='module_header':assert j['module']not in graph;graph[j['module']]=(j['constants'],tuple(j['imports']))
  elif typ=='accept':assert j['module']not in accept;accept[j['module']]=(j.get('constants'),tuple(j.get('imports',[])))
  elif typ=='dependency_phase':assert j['module']not in deps;deps[j['module']]=j
  elif typ=='profile_module'and cur is None:assert j['module']not in profiles;profiles[j['module']]=j
  elif typ=='serial_duplicate_phase':duplicates.append(j)
  elif typ=='complete':complete.append(j)
  elif typ=='curve_begin':cur=(j['kind'],j['repeat'])
  elif typ=='unit_check':assert cur is not None;units[cur].append(j)
  elif typ=='curve_cell':assert cur==(j['kind'],j['repeat']);leaf.append(j)
  elif typ=='snapshot':snapshots.append(j)
 assert len(complete)==1 and complete[0]['modules']==4449 and complete[0]['constants']==425463 and complete[0]['skipped_unsafe_partial']==3595 and complete[0]['module_local_fallbacks']==0
 assert set(graph)==set(accept)==ref and graph==accept
 reached=set();todo=[root]
 while todo:
  x=todo.pop()
  if x in reached:continue
  reached.add(x);todo.extend(graph[x][1])
 assert reached==ref
 if allgraphs:assert graph==allgraphs[0]
 else:allgraphs.append(graph)
 assert len(deps)==(4449 if term.get('profile_enabled',key=='hardware-leaf') else 0)
 cpu=v['user_s']+v['system_s'];peakrss=max(peakrss,v['peak_rss_kib']);sample=max(sample,v['sampled_tree_peak_bytes']);charged=max(charged,v['charged_peak_bytes'])
 if key!='hardware-leaf':
  full.append(dict(key=key,wall_s=v['wall_s'],CPU_s=cpu,profile=term['profile_enabled'],pins=str(term['worker_pins']),allowed=str(cmd['affinity']),wait4_maxRSS_KiB=v['peak_rss_kib'],sampled_peak_bytes=v['sampled_tree_peak_bytes'],charged_peak_bytes=v['charged_peak_bytes']))
 if profiles and key!='hardware-leaf':
  assert len(profiles)==4449
  sig={name:(p['metrics']['checks'],p['metrics']['raw_HB'])for name,p in profiles.items()};work[key]=sig
  totals=collections.Counter();migrations={};corechecks=collections.Counter()
  for name,p in profiles.items():
   m=p['metrics'];assert m['kernel_union_ns']<=m['batch_wall_ns']and m['kernel_cpu_ns']<=m['batch_cpu_ns']
   assert sum(w['checks']for w in m['workers'])==m['checks']and sum(w['raw_HB']for w in m['workers'])==m['raw_HB']
   for w in m['workers']:
    assert w['cpu']in cmd['affinity'];corechecks[w['cpu']]+=w['checks'];migrations[(name,w['tid'])]=w['within_check_migrations']
    if term['worker_pins']:assert w['cpu']in term['worker_pins']and w['within_check_migrations']==0
   for fld in ['kernel_union_ns','batch_wall_ns','batch_cpu_ns','kernel_cpu_ns','checks','raw_HB']:totals[fld]+=m[fld]
   totals['plan_ns']+=p['plan_ns'];totals['fallback_ns']+=p['fallback_ns']
  serial=sum(x['read_ns']+x['context_ns']for x in deps.values())+totals['plan_ns']+totals['fallback_ns']+sum(x['wall_ns']for x in duplicates)
  row=dict(key=key,checks=totals['checks'],raw_HB=totals['raw_HB'],serial_s=serial/1e9,kernel_occupied_s=totals['kernel_union_ns']/1e9,batch_other_s=(totals['batch_wall_ns']-totals['kernel_union_ns'])/1e9,kernel_CPU_s=totals['kernel_cpu_ns']/1e9,batch_CPU_s=totals['batch_cpu_ns']/1e9,endpoint_changes=sum(migrations.values()))
  row['other_s']=v['wall_s']-row['serial_s']-row['kernel_occupied_s']-row['batch_other_s'];phases.append(row)
  assert row['checks']==237863 and row['raw_HB']==3283925639
  if key=='full-P2':assert set(corechecks)=={0,1}
 for p in q.iterdir():
  if p.is_file():inputs.add(p)
assert len(full)==12 and len(phases)==8 and all(x==next(iter(work.values()))for x in work.values())
assert len(units)==9 and len(leaf)==9 and len(snapshots)==9
targets=None
for (kind,rep),rs in units.items():
 assert len(rs)==50 and len({x['target']for x in rs})==50 and all(x['accept']for x in rs)
 ids={x['target']for x in rs}
 if targets is None:targets=ids
 assert ids==targets
 allowed={0}if kind=='p1'else{8}if kind=='e1'else set(range(24));assert all(x['cpu']in allowed for x in rs)
counts=collections.defaultdict(list)
for rs in units.values():
 for x in rs:counts[x['target']].append(x['raw_HB'])
assert all(len(v)==9 and min(v)==max(v)for v in counts.values())
original=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets/overlay-complete-v2')/Path(root.replace('.','/')+'.olean');raw=original.read_bytes();assert len(raw)==9160440
for x in snapshots:
 assert x['checked_substitutions']==3425 and x['parts']==1 and not x['extension_entries_revalidated'];assert Path(x['file']).read_bytes()==raw
solos={}
for kind in ['p1','e1']:
 solos[kind]={t:statistics.median(int(x['cpu_ns'])for (k,rep),rs in units.items()if k==kind for x in rs if x['target']==t)for t in targets}
ratios={'P':[],'E':[]}
for (kind,rep),rs in units.items():
 if kind=='mixed24':
  for x in rs:
   typ='P'if x['cpu']<8 else'E';ratios[typ].append(int(x['cpu_ns'])/solos['p1'if typ=='P'else'e1'][x['target']])
# The actual raw mode spelling is checked explicitly below; no missing normalization as zero.
assert sum(map(len,ratios.values()))==150
rates=sum(solos['p1'].values())/sum(solos['e1'].values())
# Finite controls retained separately, including deliberate bad proof.
for key in ['attribution-control','attribution-two-core-control','attribution-bad-control']:
 q=b/'runs'/key;v=json.loads((q/'result.json').read_text());assert v['returncode']==(1 if key.endswith('bad-control')else 0)and not v['stop_reasons']and not Path(v['cgroup']).exists()
 retired(v['pid'],v['birth']);cgroups.add(v['cgroup'])
 for line in(q/'memory.jsonl').open():
  for x in json.loads(line)['processes']:retired(x['pid'],x['birth'])
 for p in q.iterdir():
  if p.is_file():inputs.add(p)
assert 'loose bound variables'in(b/'runs/attribution-bad-control/stderr').read_text()
for p in b.iterdir():
 if p.is_file()and p.suffix in ['.json','.py','.log']:inputs.add(p)
inputs.update((b/'source').iterdir())
with tarfile.open(e/'attribution-raw-source-terminals.tar.gz','w:gz')as tf:
 for p in sorted(inputs):
  if p.is_file():tf.add(p,arcname=str(p).removeprefix('/workspaces/'))
 for sub in ['attribution-results','perf']:
  for p in(r/'research/parallel-stream-check'/sub).rglob('*'):
   if p.is_file()and p.stat().st_size<10000000:tf.add(p,arcname=str(p.relative_to(r)))
for name,rs in [('full-cells.csv',full),('phase-ledger.csv',phases),('leaf-cells.csv',leaf)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,list(rs[0]),lineterminator='\n');w.writeheader();w.writerows(rs)
D={x['key']:x for x in full};P={x['key']:x for x in phases};p4=P['full-P4'];p8=P['full-P8']
deltaCPU=D['full-P8']['CPU_s']-D['full-P4']['CPU_s'];kernelDelta=p8['kernel_CPU_s']-p4['kernel_CPU_s']
natural={x:P['full-M24-unpinnedProfile'][x]-P['full-P8-unpinnedProfile'][x]for x in ['serial_s','kernel_occupied_s','batch_other_s','other_s','kernel_CPU_s']}
a=dict(full_cells=12,compound_cells=1,control_cells=3,accepted_modules=4449,entries=425463,unsafe_partial_exclusions=3595,all_graphs_equal=True,observed_profile_cohorts=8,checks_per_cohort=237863,allocation_units_per_cohort=3283925639,identities_retired=len(identities),cgroups_absent=len(cgroups),wait4_maxRSS_KiB=peakrss,sampled_peak_bytes=sample,charged_peak_bytes=charged,native_full_wall_sum=sum(x['wall_s']for x in full),native_full_CPU_sum=sum(x['CPU_s']for x in full),compound_wall_s=terms['hardware-leaf']['wall_s'],compound_CPU_s=terms['hardware-leaf']['user_s']+terms['hardware-leaf']['system_s'],P4_P8_CPU_delta_s=deltaCPU,P4_P8_kernel_CPU_delta_s=kernelDelta,P4_P8_kernel_fraction=kernelDelta/deltaCPU,natural_deltas=natural,natural_wall_delta_s=D['full-M24-unpinnedProfile']['wall_s']-D['full-P8-unpinnedProfile']['wall_s'],natural_CPU_delta_s=D['full-M24-unpinnedProfile']['CPU_s']-D['full-P8-unpinnedProfile']['CPU_s'],targets=50,observations=450,all_target_count_ranges_zero=True,artifacts_equal_original=9,artifact_bytes=len(raw),solo_E_P_work_rate=rates,mixed_same_type_median={k:statistics.median(v)for k,v in ratios.items()},root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n');print('STEP',s);print(json.dumps(a,indent=2))
