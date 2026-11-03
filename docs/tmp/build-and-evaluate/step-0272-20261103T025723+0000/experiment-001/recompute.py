from pathlib import Path
import os,json,csv,gzip,tarfile,time,resource,subprocess,collections,datetime,math
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0272-'+stamp);s.mkdir();e=s/'experiment-001';e.mkdir()
Path('/workspaces/.agent-state/gpu-smt-source36-root-step.txt').write_text(str(s)+'\n')
for n in ['docs/paper/main.tex','docs/paper/main.pdf','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md','docs/cleanup-20261101.md']:
 (e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
start=time.monotonic();d=r/'workloads/openai-math/final-seven-20261102/source36-NativeCodeAssembly'
base=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-noM-final-NativeCodeAssembly-targetP-20261103')
rows=[json.loads(x)for x in(base/'results.jsonl').read_text().splitlines()];assert len(rows)==1
plan=json.loads((base/'plan.json').read_text());term=json.loads((base/'terminal.json').read_text());launch=json.loads((base/'launch.json').read_text())
assert term['complete']and term['stop']is None and term['statuses']=={'compile_ok':1}
inputs={base/'plan.json',base/'terminal.json',base/'launch.json',base/'results.jsonl',base/'controller.py'}
ids={};cg=[];sourcebytes=0;native=[];cpu=0;wall=0;hwm=0;sampled=0;charged=0
def retired(pid,birth):
 p=Path(f'/proc/{pid}/stat')
 if p.exists():assert p.read_text().rsplit(')',1)[1].split()[19]!=str(birth),(pid,birth)
 ids[int(pid)]=str(birth)
retired(launch['pid'],launch['birth_ticks'])
ledger=[json.loads(v)for v in (base/'results.jsonl').read_text().splitlines()];assert len(ledger)==1
for i,(row,case,le)in enumerate(zip(rows,plan['cases'],ledger)):
 q=Path(row['raw']);v=json.loads((q/'result.json').read_text());cmd=json.loads((q/'command.json').read_text());ident=json.loads((q/'native-identity.json').read_text());clean=json.loads((q/'cleanup.json').read_text())
 assert v['module']==row['module']==case['module']==le['module']
 assert v['args']==cmd['args']==case['args'] and v['status']=='compile_ok' and v['returncode']==0
 assert v['native_retired']and v['cgroup_retired']and clean['cgroup_removed']and clean['stop_reason']is None
 assert v['source_exact']and not v['profiled']and v['pcore_lock']and v['heartbeat_budget']=='authored_or_native_default'and v['compilation_outputs']=='olean_ilean_c'
 assert cmd['affinity']==list(range(8))and cmd['cgroup_settings']['memory.max']==str(15*1024**3)
 assert '-j8'in v['args']and not any(x.startswith('-M')for x in v['args'])
 source=Path(cmd['source']);pinned=Path(case['pinned_source']);assert source.read_bytes()==pinned.read_bytes();sourcebytes+=source.stat().st_size
 assert not Path(cmd['native_cgroup']).exists();cg.append(cmd['native_cgroup'])
 events=dict(x.split()for x in v['cgroup_memory_events'].splitlines());assert int(events['oom'])==int(events['oom_kill'])==0
 retired(v['pid'],v['birth_ticks']);assert ident['pid']==v['pid']and ident['birth_ticks']==v['birth_ticks']
 mem=[json.loads(x)for x in(q/'memory.jsonl').read_text().splitlines()];assert all(x['birth_ticks']==v['birth_ticks']for x in mem)
 assert max(x['native_rss_bytes']for x in mem)<=v['sampled_native_rss_peak_bytes']
 for name,n in v['artifact_bytes'].items():assert(q/'artifacts'/name).stat().st_size==n
 assert abs(float(row['wall_s'])-v['wall_s'])<1e-10
 c=v['user_cpu_s']+v['system_cpu_s'];cpu+=c;wall+=v['wall_s'];hwm=max(hwm,v['peak_rss_kib']);sampled=max(sampled,v['sampled_native_rss_peak_bytes']);charged=max(charged,v['cgroup_memory_peak_bytes'])
 native.append(dict(module=v['module'],role=case['role'],wall_s=v['wall_s'],cpu_s=c,pid=v['pid'],birth=v['birth_ticks'],raw=str(q)))
 for name in ['result.json','command.json','native-identity.json','memory.jsonl','cleanup.json','native.log']:inputs.add(q/name)
 inputs.add(source);inputs.add(pinned)
assert sum(v['role']!='dependency'for v in native)==1
assert abs(wall-term['native_wall_sum_s'])<1e-8
old=list(csv.DictReader((r/'docs/tmp/build-and-evaluate/step-0270-20261102T233639+0000/experiment-001/source35-frame.csv').open()))
frame=[dict(x)for x in old]
originals=[x for x in ledger if x.get('probability_sample_target')]
assert len(originals)==1
for x in originals:
 row=next(v for v in frame if v['module']==x['module']);assert row['status']!='completed_cost'and row['stratum']==x['stratum']
 row.update(status='completed_cost',cpu_s=x['user_cpu_s']+x['system_cpu_s'],source_file=str(base/'results.jsonl'),source_line=x['index']+1,sorry_warning='unknown',pcore_lock=True)
assert len(frame)==42 and [(x['module'],x['stratum'])for x in frame]==[(x['module'],x['stratum'])for x in old]
published34=list(csv.DictReader((d/'sample-costs.csv').open()))
for x in published34:
 if x['status']=='completed_cost':
  z=next(v for v in frame if v['module']==x['module']);assert abs(float(z['cpu_s'])-float(x['cpu_s']))<1e-10
with (e/'source36-frame.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,list(frame[0]),lineterminator='\n');w.writeheader();w.writerows(frame)
new=[x for x,y in zip(frame,old)if x['status']!=y['status']];assert len(new)==1
N={';'.join(x[k]for k in ['size_percentile_bin','import_depth_bin','has_decide_kernel']):int(x['population_modules'])for x in csv.DictReader((r/'workloads/openai-math/build-planning-4eaee875/strata.csv').open())}
groups=collections.defaultdict(list);actual=[];cache={}
for row in frame:
 if row['status']!='completed_cost':continue
 p=Path(row['source_file'])
 if p not in cache:cache[p]=[json.loads(v)for v in p.read_text().splitlines()];inputs.add(p)
 v=cache[p][int(row['source_line'])-1];c=v['user_cpu_s']+v['system_cpu_s']
 assert v['status']=='compile_ok'and v['module']==row['module']and abs(c-float(row['cpu_s']))<1e-10
 assert v['source_exact']and v['pcore_lock']and v['lean_memory_option_MiB']==0
 groups[row['stratum']].append(dict(cpu=c,wall=v['wall_s']));actual.append(dict(module=row['module'],stratum=row['stratum'],cpu_s=c,wall_s=v['wall_s']))
assert len(actual)==36
complete={h:ys for h,ys in groups.items()if len(ys)==2};assert len(complete)==18
conditional_cpu=sum(N[h]*sum(v['cpu']for v in ys)/2/3600 for h,ys in complete.items())
conditional_wall=sum(N[h]*sum(v['wall']for v in ys)/2/3600 for h,ys in complete.items())
marked_cpu=sum(N[h]*sum(v['cpu']for v in ys)/2/3600 for h,ys in complete.items()if h.endswith(';1'))
marked_wall=sum(N[h]*sum(v['wall']for v in ys)/2/3600 for h,ys in complete.items()if h.endswith(';1'))
covered=sum(N[h]for h in complete)
known=sum(N[v['stratum']]/2*v['cpu_s']/3600 for v in actual);missing=[v for v in frame if v['status']!='completed_cost'];assert len(missing)==6 and all(v['stratum'].endswith(';0')for v in missing)
ordinary=[v['cpu_s']for v in actual if v['stratum'].endswith(';0')];lo=min(ordinary);hi=max(ordinary)
coef=sum(N[v['stratum']]/2/3600 for v in missing)
scenarios=[]
root268=json.loads((r/'docs/tmp/build-and-evaluate/step-0268-20261102T190628+0000/experiment-001/reanalysis.json').read_text())
f=[x['cpu_ratio']for x in root268['results']]
# Historical computation transfer factors retained from W calibration, independently reconstruct literal totals.
cal=list(csv.DictReader((r/'workloads/openai-math/cost_staircase/calibration.csv').open()))
cf=[float(x['CPU_factor'])for x in cal if x['calibration']in ['compute-grid','compute-amplitudes']]
assert len(cf)==2
for name,cost in [('observed_class_min',lo),('observed_class_max',hi)]:
 total=known+coef*cost;ordinary_h=total-marked_cpu
 scenarios.append(dict(scenario=name,source_CPU_h=total,modeled_check_low_h=ordinary_h*min(f)+marked_cpu*min(cf),modeled_check_high_h=ordinary_h*max(f)+marked_cpu*max(cf)))
# Freeze raw and source, no olean/ilean/C/build-tree copies.
with tarfile.open(e/'source36-raw-source.tar.gz','w:gz')as tf:
 for p in sorted(inputs):
  if p.exists():tf.add(p,arcname=str(p).removeprefix('/workspaces/'))
 for p in sorted(d.rglob('*')):
  if p.is_file():tf.add(p,arcname=str(p.relative_to(r)))
for n,rs in [('native1.csv',native),('source36-costs.csv',actual),('scenarios.csv',scenarios)]:
 with (e/n).open('w',newline='')as file:
  w=csv.DictWriter(file,list(rs[0]),lineterminator='\n');w.writeheader();w.writerows(rs)
a=dict(native_count=1,native_wall_s=wall,native_CPU_s=cpu,controller_wall_s=term['elapsed_including_queue_s'],identities_retired=len(ids),cgroups_absent=len(set(cg)),source_bytes_compared=sourcebytes,wait4_maxRSS_KiB=hwm,sampled_peak_bytes=sampled,charged_peak_bytes=charged,new_originals=[v for v in native if v["role"]!="dependency"],originals=36,missing_originals=6,complete_strata=18,covered_modules=covered,missing_module_domain=163097-covered,source_sum_CPU_s=sum(x['cpu_s']for x in actual),source_sum_wall_s=sum(x['wall_s']for x in actual),conditional_CPU_h=conditional_cpu,conditional_native_elapsed_h=conditional_wall,marked_CPU_h=marked_cpu,marked_elapsed_h=marked_wall,marked_CPU_share=marked_cpu/conditional_cpu,marked_elapsed_share=marked_wall/conditional_wall,known_HT_CPU_h=known,missing_plus_one_CPU_s_h=coef,observed_ordinary_min_CPU_s=lo,observed_ordinary_max_CPU_s=hi,scenarios=scenarios,scenario_ten_times_max_CPU_h=known+coef*hi*10,scenario_missing_check_equals_source_CPU_h=(known-marked_cpu)*min(f)+marked_cpu*min(cf)+coef*hi,scenario_missing_check_twice_source_CPU_h=(known-marked_cpu)*min(f)+marked_cpu*min(cf)+2*coef*hi,ordinary_transfer_CPU_factors=f,computation_transfer_CPU_factors=cf,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n');print('STEP',s);print(json.dumps(a,indent=2))
