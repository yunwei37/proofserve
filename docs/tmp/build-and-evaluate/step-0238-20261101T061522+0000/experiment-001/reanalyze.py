from pathlib import Path
import os,subprocess,json,gzip,time,resource,csv,statistics,datetime,math
os.sched_setaffinity(0,{22,23});begin=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0238-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-W48-paper-step.txt').write_text(str(s)+'\n')
def freeze(p,name):
 b=Path(p).read_bytes();q=e/(name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(q.read_bytes())==b;return b
def live(pid,birth):
 p=Path('/proc')/str(pid)/'stat'
 return p.exists() and p.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
w=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-noM-original-c-suffix48-prepared-20261101')
for f in ['terminal.json','launch.json','results.jsonl','controller.py','controller.log']:freeze(w/f,'W48-'+f)
term=json.loads((w/'terminal.json').read_text());launch=json.loads((w/'launch.json').read_text())
assert term['complete'] and term['rows']==term['planned_jobs']==term['native_rows']==48 and term['stop'] is None
assert not live(launch['pid'],launch['birth_ticks'])
rows=[json.loads(x) for x in (w/'results.jsonl').read_text().splitlines()];assert len(rows)==48 and len({x['module'] for x in rows})==48
packet=[]
for x in rows:
 d=Path(x['raw']);z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text());identity=json.loads((d/'native-identity.json').read_text());clean=json.loads((d/'cleanup.json').read_text())
 assert x['status']=='compile_ok' and x['returncode']==0 and x['native_retired'] and x['cgroup_retired']
 assert z['pid']==x['pid']==identity['pid'] and z['birth_ticks']==x['birth_ticks']==identity['birth_ticks']
 assert not live(x['pid'],x['birth_ticks']) and not Path(cmd['native_cgroup']).exists()
 assert cmd['affinity']==list(range(8)) and cmd['pcore_lock'] and cmd['source_exact']
 assert cmd['cgroup_settings']['memory.max']==str(15*1024**3) and clean==dict(cgroup_removed=True,stop_reason=None)
 assert cmd['args']==x['args'] and not any(a.startswith('-M') for a in x['args'])
 assert x['threads']==8 and not x['profiled'] and x['heartbeat_budget']=='authored_or_native_default' and x['compilation_outputs']=='olean_ilean_c'
 assert all(int(l.split()[1])==0 for l in x['cgroup_memory_events'].splitlines())
 log=(d/'native.log').read_text();assert 'declaration uses' not in log and 'error:' not in log
 assert len(x['artifact_bytes'])==3
 for f,size in x['artifact_bytes'].items():assert (d/'artifacts'/f).stat().st_size==size
 packet.append(dict(row=x,command=cmd,identity=identity,cleanup=clean))
 if x['probability_sample_target']:
  for f in ['native.log','memory.jsonl']:freeze(d/f,'newtarget-'+str(x['index'])+'-'+f)
assert math.isclose(sum(x['wall_s'] for x in rows),term['native_wall_sum_s'],abs_tol=1e-8)
planning=r/'workloads/openai-math/build-planning-4eaee875';cost=r/'workloads/openai-math/cost-regimes-noM'
for q in [planning/'phaseA-targets.csv',planning/'strata.csv',cost/'sample-classification.csv',cost/'stratum-domain-estimates.csv',cost/'receipt.json']:
 freeze(q,'input-'+q.name)
frame=list(csv.DictReader((planning/'phaseA-targets.csv').open()));draws={x['module']:x for x in frame if x['role']=='probability_sample'};assert len(draws)==42
pop=list(csv.DictReader((planning/'strata.csv').open()))
N={';'.join([x['size_percentile_bin'],x['import_depth_bin'],x['has_decide_kernel']]):int(x['population_modules']) for x in pop};assert len(N)==21 and sum(N.values())==163097
old=list(csv.DictReader((cost/'sample-classification.csv').open()))
known={}
for x in old:
 if x['original_random_draw']=='True' and x['completed_cost']=='True':
  q=json.loads(Path(x['source_file']).read_text().splitlines()[int(x['source_line'])-1]);assert q['module']==x['module']
  assert x['module'] in draws and x['stratum']==draws[x['module']]['stratum']
  assert math.isclose(float(x['CPU_s']),q['user_cpu_s']+q['system_cpu_s'],abs_tol=1e-8)
  known[x['module']]=dict(module=x['module'],stratum=x['stratum'],CPU_s=q['user_cpu_s']+q['system_cpu_s'],wall_s=q['wall_s'],source=x['source_file'])
assert len(known)==29
new=[x for x in rows if x['probability_sample_target']]
assert len(new)==2 and not(set(known)&{x['module'] for x in new})
for x in new:
 assert x['module'] in draws and draws[x['module']]['stratum']==x['stratum']
 assert (int(x['stratum'].split(';')[-1])>0)==(int(draws[x['module']]['decide_kernel_occurrences'])>0)
 known[x['module']]=dict(module=x['module'],stratum=x['stratum'],CPU_s=x['user_cpu_s']+x['system_cpu_s'],wall_s=x['wall_s'],source=str(w/'results.jsonl'))
assert len(known)==31
popclass=list(csv.DictReader((cost/'stratum-domain-estimates.csv').open()));primary={x['stratum']:x for x in popclass if x['rule']=='explicit_any'}
strata=[];covered=positive=0;tc=to=0.0
for key,n in N.items():
 xs=[x for x in known.values() if x['stratum']==key]
 assert len([x for x in draws.values() if x['stratum']==key])==2 and len(xs)<=2
 pos=int(primary[key]['population_certificate_proxy']);assert pos==(n if key.endswith(';1') else 0)
 row=dict(stratum=key,N=n,completed_draws=len(xs),complete=len(xs)==2,positive_modules=pos,estimated_marked_CPU_h='',estimated_other_CPU_h='')
 if len(xs)==2:
  value=n*statistics.mean(x['CPU_s'] for x in xs)/3600
  row['estimated_marked_CPU_h']=value if pos else 0;row['estimated_other_CPU_h']=0 if pos else value
  tc+=row['estimated_marked_CPU_h'];to+=row['estimated_other_CPU_h'];covered+=n;positive+=pos
 strata.append(row)
missing=sorted(set(draws)-set(known))
j=dict(completed_queue_jobs=48,queue_dependency_jobs=46,new_original_draws=2,original_draws_completed=31,original_draws_total=42,missing_original_draws=missing,complete_strata=sum(x['complete'] for x in strata),total_strata=21,covered_population_modules=covered,covered_marked_modules=positive,missing_population_modules=163097-covered,missing_marked_modules=5848-positive,conditional_marked_CPU_h=tc,conditional_other_CPU_h=to,conditional_marked_share=tc/(tc+to),global_weight_established=False,global_share_bound='0–100%; no finite global cost estimate under incomplete nonresponse',random_CPU_s=sum(x['CPU_s'] for x in known.values()),random_native_wall_s=sum(x['wall_s'] for x in known.values()),queue_native_wall_s=sum(x['wall_s'] for x in rows),queue_inclusive_elapsed_s=term['elapsed_including_queue_s'],queue_wall_is_not_native_cost=True,controller_and_all_native_identities_cgroups_retired=True,max_RSS_KiB=max(x['peak_rss_kib'] for x in rows),max_sampled_RSS_bytes=max(x['sampled_native_rss_peak_bytes'] for x in rows),max_charged_bytes=max(x['cgroup_memory_peak_bytes'] for x in rows),root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native_runs=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
(e/'W48-native-packet.json.gz').write_bytes(gzip.compress(json.dumps(packet).encode(),mtime=0))
for name,rs in [('original-draw-costs.csv',sorted(known.values(),key=lambda x:x['module'])),('stratum-coverage-and-primary-costs.csv',strata)]:
 with (e/name).open('w') as f:
  z=csv.DictWriter(f,fieldnames=list(rs[0]),lineterminator='\n');z.writeheader();z.writerows(rs)
print('STEP',s,'SUMMARY',json.dumps({k:v for k,v in j.items() if k!='missing_original_draws'}))
