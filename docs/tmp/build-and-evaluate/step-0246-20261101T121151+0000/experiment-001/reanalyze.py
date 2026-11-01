from pathlib import Path
import os,json,gzip,time,resource,csv,subprocess,datetime,collections,math
os.sched_setaffinity(0,{22,23});begin=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0246-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-namespace-paper-step.txt').write_text(str(s)+'\n')
def freeze(p,name):
 raw=Path(p).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(raw,mtime=0));return raw
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
b=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031');m=r/'research/decoupled-check'
frame=json.loads(freeze(b/'source-frame.json','raw-source-frame.json'));byname={x['module']:x for x in frame};assert len(frame)==len(byname)==5085
costrows=list(csv.DictReader((m/'source-module-costs.csv').open()));freeze(m/'source-module-costs.csv','published-source-module-costs.csv')
freeze(m/'cohort-costs.csv','published-cohort-costs.csv');freeze(m/'StreamCheck.lean','frozen-StreamCheck.lean')
cohorts=list(csv.DictReader((m/'cohort-costs.csv').open()));assert len(cohorts)==4
assert set(x['module']for x in costrows)==set(byname)
source={};resultlines=[]
for row in costrows:
 raw=(b/(row['raw_key']+'.result.json')).read_bytes();z=json.loads(raw);name=row['module'];args=z['args']
 assert z['returncode']==0 and z['affinity']==list(range(8)) and not any(x.startswith('-M')for x in args)
 assert args[-1]==byname[name]['source'] and Path(z['cgroup']).exists()==False
 assert z['memory_max_bytes']==12750684160
 assert abs(float(row['wall_s'])-z['wall_s'])<=0.000000501
 assert all(int(x.split()[1])==0 for x in z['memory_events'].splitlines())
 is_oai=name.startswith('OAI.')
 assert is_oai==('/openai-math-4eaee875/lean/OAI/' in byname[name]['source'])
 source[name]=z['wall_s'];resultlines.append(json.dumps({'module':name,'result':z},separators=(',',':')))
(e/'raw-source-results.jsonl.gz').write_bytes(gzip.compress(('\n'.join(resultlines)+'\n').encode(),mtime=0))
totals=[];groups=[];module_rows=[]
for spec in cohorts:
 label=spec['cohort'];key='timed-constructed-stream-'+label
 for f in ['stdout','stderr','command.json','result.json']:freeze(b/(key+'.'+f),key+'-'+f)
 z=json.loads((b/(key+'.result.json')).read_text());cmd=json.loads((b/(key+'.command.json')).read_text())
 assert z['returncode']==0 and z['args']==cmd['args'] and z['affinity']==list(range(8))
 assert not any(x.startswith('-M')for x in z['args']) and z['memory_max_bytes']==12750684160 and not Path(z['cgroup']).exists()
 ev=[json.loads(line)for line in(b/(key+'.stdout')).read_text().splitlines()]
 ac=[x for x in ev if x.get('event')=='accept'];timed=[x for x in ev if x.get('event')=='module_timing'];done=[x for x in ev if x.get('event')=='complete']
 names=[x['module']for x in ac];times={x['module']:x for x in timed};wanted={x['module']for x in frame if spec['root'] in x['cohorts']}
 assert len(names)==len(set(names))==len(times)==len(wanted)==int(spec['closure_modules'])
 assert set(names)==set(times)==wanted and len(timed)==len(times) and len(done)==1 and done[0]['mutated']==0
 assert done[0]['modules']==len(wanted)
 group=collections.defaultdict(lambda:dict(modules=0,source_compiler_work_s=0.0,replay_ns=0,readmap_ns=0))
 for name,x in times.items():
  ns='OAI'if name.startswith('OAI.')else'other';g=group[ns]
  assert all(int(x[k])>=0 for k in ['replay_ns','read_ns','map_ns'])
  g['modules']+=1;g['source_compiler_work_s']+=source[name];g['replay_ns']+=int(x['replay_ns']);g['readmap_ns']+=int(x['read_ns'])+int(x['map_ns'])
  if ns=='OAI':module_rows.append(dict(cohort=label,module=name,source_compiler_work_s=source[name],replay_s=int(x['replay_ns'])/1e9,readmap_s=(int(x['read_ns'])+int(x['map_ns']))/1e9))
 total_source=sum(g['source_compiler_work_s']for g in group.values());total_replay=sum(g['replay_ns']for g in group.values())
 assert math.isclose(total_source,float(spec['source_compiler_work_s']),abs_tol=1e-8)
 assert math.isclose(z['wall_s'],float(spec['matched_artifact_stream_s']),abs_tol=1e-8)
 assert total_replay/1e9<=z['wall_s']
 oai=group.get('OAI',dict(modules=0,source_compiler_work_s=0,replay_ns=0,readmap_ns=0))
 row=dict(cohort=label,closure_modules=len(wanted),OAI_modules=oai['modules'],source_compiler_work_s=total_source,timed_replay_sum_s=total_replay/1e9,OAI_source_compiler_work_s=oai['source_compiler_work_s'],OAI_timed_replay_s=oai['replay_ns']/1e9,OAI_share_source_percent=100*oai['source_compiler_work_s']/total_source,OAI_share_timed_replay_percent=100*oai['replay_ns']/total_replay,OAI_replay_to_source_percent=(100*oai['replay_ns']/1e9/oai['source_compiler_work_s'])if oai['modules']else None)
 totals.append(row)
 for ns,g in group.items():groups.append(dict(cohort=label,source_namespace=ns,modules=g['modules'],source_compiler_work_s=g['source_compiler_work_s'],timed_replay_s=g['replay_ns']/1e9,readmap_s=g['readmap_ns']/1e9))
for name,rs in [('cohort-namespace-shares.csv',totals),('namespace-components.csv',groups),('OAI-module-components.csv',module_rows)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]),lineterminator='\n');w.writeheader();w.writerows(rs)
scope=dict(population='same four purposefully selected complete O closures; overlapping immutable dependencies',source_boundary='sum of serial native per-module compiler wall, includes imports/elaboration/tactics/check/output',replay_boundary='sum of nonoverlapping monoNanos per-module Environment.replay call intervals after checked dependencies; excludes read/map/log/setup/cleanup',classification='OAI namespace and matching fixed openai source path, not semantic regime classifier',resource_deviation='original O11.875GiB native cap/sourcepeak7.57GiB exceeded listed O4share; retained, not retroactively approved',new_native_runs=0)
j=dict(cohorts=totals,scope=scope,source_modules=5085,root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'step':str(s),**j},indent=2))
