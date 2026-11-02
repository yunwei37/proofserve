from pathlib import Path
import os,json,csv,collections,statistics,math,time,datetime,subprocess,gzip,tarfile,resource
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-source32-root-step.txt').read_text().strip());e=s/'experiment-001'
(e/'initial-ledger-equality-assertion.txt').write_text('Initial offline full-row equality failed because controller adds probability_sample_target/queue_plus_setup_cleanup_s/queue_scope to native result. All shared fields match; corrected comparison to exact native-result subset. No native rerun or data mutation.\n')
b=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-noM-hard-two-suffix19-prepared-20261101');plan=json.loads((b/'plan.json').read_text());terminal=json.loads((b/'terminal.json').read_text());launch=json.loads((b/'launch.json').read_text());rows=[json.loads(l)for l in(b/'results.jsonl').open()];assert terminal['complete']and len(rows)==19 and terminal['native_rows']==13
ids=set();freeze=set();natives=[];new=[]
def retired(pid,birth):
 p=Path('/proc')/str(pid);assert not p.exists()or p.joinpath('stat').read_text().rsplit(')',1)[1].split()[19]!=str(birth);ids.add((int(pid),str(birth)))
retired(launch['pid'],launch['birth_ticks'])
cases={x['module']:x for x in plan['cases']}
for z in rows:
 if not z['native_invoked']:
  assert z['status']=='dependency_not_compiled';continue
 p=Path(z['raw']);q=json.loads((p/'command.json').read_text());native_result=json.loads((p/'result.json').read_text());assert all(k in z and z[k]==v for k,v in native_result.items())
 assert z['source_exact']and z['lean_memory_option_MiB']==0 and z['pcore_lock']and z['threads']==8 and not z['profiled']and z['heartbeat_budget']=='authored_or_native_default'and z['compilation_outputs']=='olean_ilean_c'
 assert q['affinity']==list(range(8))and q['cgroup_settings']['memory.max']==str(15*1024**3)and not Path(q['native_cgroup']).exists()and not any(str(v).startswith('-M')for v in q['args'])
 assert all(int(l.split()[1])==0 for l in z['cgroup_memory_events'].splitlines()if l.split()[0].startswith('oom'))
 retired(z['pid'],z['birth_ticks']);assert json.loads((p/'cleanup.json').read_text())['cgroup_removed']
 assert all(str(json.loads(l)['birth_ticks'])==str(z['birth_ticks'])for l in(p/'memory.jsonl').open())
 src=Path(q['source']);original=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875')/z['path'];assert src.read_bytes()==original.read_bytes()
 if z['status']=='compile_ok':
  assert z['returncode']==0
  for n,size in z['artifact_bytes'].items():assert(p/'artifacts'/n).stat().st_size==size
  assert all(any(n.endswith(ext)for n in z['artifact_bytes'])for ext in ['.olean','.ilean','.c'])
  if cases[z['module']]['role']=='original_probability_sample':new.append(z)
 else:assert z['status']=='wall_budget_exceeded'and z['returncode']==-14 and not z['artifact_bytes']
 natives.append(z);freeze.update(x for x in p.iterdir()if x.is_file())
assert len(new)==1 and new[0]['module'].endswith('LowBlock15_1')
root=r/'workloads/openai-math';frame=list(csv.DictReader((root/'noM-original-c-suffix48/sample-costs.csv').open()));assert len(frame)==42
strata={';'.join(x[k]for k in ['size_percentile_bin','import_depth_bin','has_decide_kernel']):int(x['population_modules'])for x in csv.DictReader((root/'build-planning-4eaee875/strata.csv').open())}
known={}
for x in frame:
 if x['status']!='completed_cost':continue
 p=Path(x['source_file']);z=json.loads(p.read_text().splitlines()[int(x['source_line'])-1]);assert z['status']=='compile_ok'and z['source_exact']and z['lean_memory_option_MiB']==0
 known[x['module']]=z;freeze.add(p)
assert len(known)==31 and new[0]['module']in{x['module']for x in frame}and new[0]['module']not in known
known[new[0]['module']]=new[0]
by=collections.defaultdict(list);members=collections.defaultdict(list)
for x in frame:
 members[x['stratum']].append(x['module'])
 if x['module']in known:by[x['stratum']].append(known[x['module']])
complete=[h for h in strata if len(by[h])==2];assert len(complete)==15
cpu=lambda z:z['user_cpu_s']+z['system_cpu_s']
domains={}
for d in ['all','marked','ordinary']:
 hs=[h for h in complete if d=='all'or h.endswith(';1'if d=='marked'else';0')]
 domains[d]={'complete_strata':len(hs),'population_modules':sum(strata[h]for h in hs),'CPU_h':sum(strata[h]/2*cpu(z)for h in hs for z in by[h])/3600,'native_elapsed_h':sum(strata[h]/2*z['wall_s']for h in hs for z in by[h])/3600}
share=domains['marked']['CPU_h']/domains['all']['CPU_h'];wallshare=domains['marked']['native_elapsed_h']/domains['all']['native_elapsed_h']
missing=[x for x in frame if x['module']not in known];assert len(missing)==10 and all(x['stratum'].endswith(';0')for x in missing)
cal={x['calibration']:float(x['CPU_factor'])for x in csv.DictReader((root/'cost_staircase/calibration.csv').open())};ratios={'ordinary':(cal['ordinary-oai'],cal['math']),'marked':(cal['compute-amplitudes'],cal['compute-grid'])}
D=lambda h:'marked'if h.endswith(';1')else'ordinary';classcost=collections.defaultdict(list);K=0
for x in frame:
 if x['module']in known:classcost[D(x['stratum'])].append(cpu(known[x['module']]));K+=strata[x['stratum']]/2*cpu(known[x['module']])
scenarios=[]
for rule,assumption in [('observed_class_min',min),('observed_class_max',max)]:
 M=sum(strata[x['stratum']]/2*assumption(classcost[D(x['stratum'])])for x in missing);source=K+M
 stream=[sum(strata[x['stratum']]/2*cpu(known[x['module']])*ratios[D(x['stratum'])][k]for x in frame if x['module']in known)+sum(strata[x['stratum']]/2*assumption(classcost[D(x['stratum'])])*ratios[D(x['stratum'])][k]for x in missing)for k in [0,1]]
 knownhigh=sum(strata[x['stratum']]/2*cpu(known[x['module']])*ratios[D(x['stratum'])][1]for x in frame if x['module']in known)
 scenarios.append({'scenario':rule,'source_CPU_h':source/3600,'modeled_stream_low_h':stream[0]/3600,'modeled_stream_high_h':stream[1]/3600,'missing_no_saving_h':(knownhigh+M)/3600,'missing_twice_source_h':(knownhigh+2*M)/3600,'missing_checker_source_break_even':(source-knownhigh)/M})
derived=[]
for x in frame:
 z=known.get(x['module']);derived.append({'module':x['module'],'stratum':x['stratum'],'status':'completed_cost'if z else'missing','CPU_s':cpu(z)if z else'','native_elapsed_s':z['wall_s']if z else'','raw':z['raw']if z else''})
for name,zs in [('source32-frame',derived),('scenario32',scenarios)]:
 with(e/(name+'.csv')).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(zs[0]),lineterminator='\n');w.writeheader();w.writerows(zs)
for p in b.iterdir():
 if p.is_file()and p.suffix in ['.json','.jsonl','.py','.log']:freeze.add(p)
freeze.update([root/'noM-original-c-suffix48/sample-costs.csv',root/'build-planning-4eaee875/strata.csv',root/'cost_staircase/calibration.csv'])
with tarfile.open(e/'source19-terminal-and-source32-reduction-inputs.tar.gz','w:gz')as tf:
 for p in sorted(freeze):tf.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
j={'native_rows':13,'statuses':dict(collections.Counter(z['status']for z in rows)),'new_original_source_draws':1,'new_target':new[0],'source_completed':32,'source_missing':10,'complete_source_strata':15,'domains':domains,'conditional_marked_CPU_share':share,'conditional_marked_native_elapsed_share':wallshare,'observed32_CPU_s':sum(cpu(z)for z in known.values()),'observed32_native_elapsed_s':sum(z['wall_s']for z in known.values()),'known_HT_subtotal_CPU_h':K/3600,'remaining_missing_weight_sensitivity_CPU_h_per_uniform_second':sum(strata[x['stratum']]/2 for x in missing)/3600,'scenarios':scenarios,'missing_population_modules':sum(strata[h]for h in strata if h not in complete),'retired_identities':sorted(ids),'recorded_identity_count':len(ids),'terminal':terminal,'controller':launch,'native_wall_sum_s':sum(z['wall_s']for z in natives),'native_CPU_sum_s':sum(cpu(z)for z in natives),'max_wait4_RSS_KiB':max(z['peak_rss_kib']for z in natives),'max_sampled_RSS_B':max(z['sampled_native_rss_peak_bytes']for z in natives),'max_charged_B':max(z['cgroup_memory_peak_bytes']for z in natives),'new_root_native':0,'root_analysis_seconds':time.monotonic()-start,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
for n in ['docs/paper/main.tex','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md']:(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
print('STEP',s);print(json.dumps({k:v for k,v in j.items()if k not in ['new_target','retired_identities','controller','terminal']}))
