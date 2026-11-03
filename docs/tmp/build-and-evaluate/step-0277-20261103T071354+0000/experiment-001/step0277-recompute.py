from pathlib import Path
import os,json,subprocess,gzip,csv,tarfile,time,resource,datetime,collections,math,statistics
from decimal import Decimal
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103');v2=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0277-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));s.mkdir();e=s/'experiment-001';e.mkdir();Path('/workspaces/.agent-state/gpu-smt-pmu-uncertainty-root-step.txt').write_text(str(s)+'\n')
for n in ['docs/paper/main.tex','docs/paper/main.pdf','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md','docs/cleanup-20261101.md']:
 (e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
start=time.monotonic();inputs=set();identities={};cells=[];graphs=None;workref=None;stats={};hwm=sampled=charged=0
def rd(p):inputs.add(p);return json.loads(p.read_text())
def retired(pid,birth):
 p=Path('/proc')/str(pid)/'stat'
 if p.exists():assert p.read_text().rsplit(')',1)[1].split()[19]!=str(birth),(pid,birth)
 identities[int(pid)]=str(birth)
term=rd(b/'foreground-terminal.json');keys=term['completed'];assert len(keys)==len(set(keys))==16 and term['error']is None
for key in keys:
 t=rd(b/(key+'-terminal.json'));v=t['cell'];q=b/'runs'/key;c=rd(q/'command.json');native=rd(q/'result.json')
 assert t['state']=='complete'and t['error']is None and all(native[k]==v[k]for k in native)and all(c[k]==v[k]for k in c)
 assert v['returncode']==0 and v['wait4_usage_complete']and v['native_retired']and v['cgroup_retired']and not v['stop_reasons']
 assert v['affinity']==list(range(8))and v['wall_limit_s']==1100 and v['cgroup_charged_memory_max_gib']==14 and not any(str(x).startswith('-M')for x in v['argv'])
 assert not Path(v['cgroup']).exists();ev=dict(x.split()for x in v['memory_events'].splitlines());assert int(ev['oom'])==int(ev['oom_kill'])==0
 retired(v['pid'],v['birth']);hwm=max(hwm,v['peak_rss_kib']);sampled=max(sampled,v['sampled_tree_peak_bytes']);charged=max(charged,v['charged_peak_bytes'])
 inputs.add(q/'memory.jsonl')
 for line in(q/'memory.jsonl').open():
  for p in json.loads(line)['processes']:retired(p['pid'],p['birth'])
 headers={};accepts={};prof={};completed=[];kernel=0;checks=hb=0
 inputs.update([q/'stdout',q/'stderr'])
 for line in(q/'stdout').open():
  if not line.strip():continue
  x=json.loads(line);kind=x.get('event')
  if kind=='module_header':
   assert x['module']not in headers;headers[x['module']]=(x['constants'],x['imports'])
  elif kind=='accept':
   assert x['module']not in accepts;accepts[x['module']]=(x['constants'],x['imports'])
  elif kind=='profile_module':
   m=x['metrics'];prof[x['module']]=(m['checks'],m['raw_HB']);checks+=m['checks'];hb+=m['raw_HB'];kernel+=m['kernel_cpu_ns']
  elif kind=='complete':completed.append(x)
 assert len(headers)==len(accepts)==len(prof)==4449 and headers==accepts and checks==237863 and hb==3283925639
 assert completed[-1]['constants']==425463 and completed[-1]['skipped_unsafe_partial']==3595 and completed[-1]['module_local_fallbacks']==0
 if graphs is None:graphs=headers;workref=prof
 else:assert headers==graphs and prof==workref
 root='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41';seen=set();todo=[root]
 while todo:
  m=todo.pop()
  if m in seen:continue
  seen.add(m);todo.extend(headers[m][1])
 assert seen==set(headers)
 cells.append(dict(key=key,workers=v['workers'],arm=v['arm'],repeat=v['repeat'],wall_s=v['wall_s'],cpu_s=v['user_s']+v['system_s'],observer_bracket_cpu_s=kernel/1e9,checks=checks,allocation_units=hb,modules=len(accepts)))
 if v['arm']=='stat':
  sf=b/(key+'-stat.json');inputs.add(sf);rs=[json.loads(x)for x in sf.read_text().splitlines()if x.strip()];assert len(rs)==7 and all(float(z['pcnt-running'])==100 for z in rs)
  stats[v['workers']]={z['event']:int(Decimal(z['counter-value']))for z in rs}
  assert len(stats[v['workers']])==7
 for p in [b/(key+'-application.time')]:
  inputs.add(p)
for n in ['foreground-launch.json','series-launch.json']:
 x=rd(b/n);retired(x['pid'],x['birth'])
assert set(stats)=={1,2,4,8}
# Equal graph against actual archived serial reference, with its actual accept schema.
ref=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/runs/barrier-full-reference1-r1/stdout')
refgraph={}
for line in ref.open():
 if line.startswith('{'):
  x=json.loads(line)
  if x.get('event')=='accept':refgraph[x['module']]=(x['constants'],x['imports'])
assert refgraph==graphs
pairs=[]
for p4 in [x for x in cells if x['workers']==4 and x['arm']=='plain']:
 for p8 in [x for x in cells if x['workers']==8 and x['arm']=='plain']:
  cpu=p8['cpu_s']-p4['cpu_s'];kc=p8['observer_bracket_cpu_s']-p4['observer_bracket_cpu_s']
  pairs.append(dict(P4=p4['key'],P8=p8['key'],extra_CPU_s=cpu,extra_bracket_CPU_s=kc,fraction=kc/cpu))
pmu=[]
for ev in stats[4]:pmu.append(dict(event=ev,P4=stats[4][ev],P8=stats[8][ev],change_percent=100*(stats[8][ev]/stats[4][ev]-1)))
def event(n,token):return next(v for k,v in stats[n].items()if token in k)
ipc4=event(4,'instructions')/event(4,'cpu-cycles');ipc8=event(8,'instructions')/event(8,'cpu-cycles')
for key in ['publication-original16','primary-source']:
 for p in (b/key).rglob('*'):
  if p.is_file():inputs.add(p)
for p in (r/'research/parallel-stream-check/perf').rglob('*'):
 if p.is_file()and p.suffix in ['.md','.csv','.json','.py','.txt']:inputs.add(p)
for n in ['native.py','perf_run.py','attribution.py','series.py','foreground.py','foreground-takeover.json','series-terminal.json','read-fields-transition.json']:
 inputs.add(b/n)
for p in (v2/'source').iterdir():
 if p.is_file():inputs.add(p)
# Source38 variance from the exact previously qualified fixed42 frame and original native ledgers.
prev=r/'docs/tmp/build-and-evaluate/step-0276-20261103T062502+0000/experiment-001'
frame=list(csv.DictReader((prev/'source38-frame.csv').open()));inputs.add(prev/'source38-frame.csv')
N={';'.join(x[k]for k in ['size_percentile_bin','import_depth_bin','has_decide_kernel']):int(x['population_modules'])for x in csv.DictReader((r/'workloads/openai-math/build-planning-4eaee875/strata.csv').open())};inputs.add(r/'workloads/openai-math/build-planning-4eaee875/strata.csv')
group=collections.defaultdict(list);cache={}
for row in frame:
 if row['status']!='completed_cost':continue
 p=Path(row['source_file']);inputs.add(p)
 if p not in cache:cache[p]=[json.loads(x)for x in p.read_text().splitlines()]
 x=cache[p][int(row['source_line'])-1];cpu=x['user_cpu_s']+x['system_cpu_s'];assert x['module']==row['module']and x['status']=='compile_ok'and abs(cpu-float(row['cpu_s']))<1e-9
 group[row['stratum']].append((row['module'],cpu))
assert sum(map(len,group.values()))==38 and len(group)==19 and all(len(v)==2 for v in group.values())
vr=[]
for h,ys in group.items():
 vals=[v[1]for v in ys];n=len(ys);var=statistics.variance(vals);vi=N[h]**2*(1-n/N[h])*var/n
 vr.append(dict(stratum=h,N=N[h],n=n,point_CPU_h=N[h]*statistics.mean(vals)/3600,variance_CPU_s2=vi,originals=';'.join(v[0]for v in ys)))
V=sum(x['variance_CPU_s2']for x in vr);df=V**2/sum(x['variance_CPU_s2']**2/(x['n']-1)for x in vr);point=sum(x['point_CPU_h']for x in vr)
# Direct numerical inversion of the standard Student t density, independent of owner interval code.
normalizer=math.exp(math.lgamma((df+1)/2)-math.lgamma(df/2))/math.sqrt(df*math.pi)
def cdf(x):
 n=5000;step=x/n;f=lambda y:normalizer*(1+y*y/df)**(-(df+1)/2)
 return .5+step/3*(f(0)+f(x)+4*sum(f(i*step)for i in range(1,n,2))+2*sum(f(i*step)for i in range(2,n,2)))
lo=0.;hi=20.
for _ in range(50):
 mid=(lo+hi)/2
 if cdf(mid)<.975:lo=mid
 else:hi=mid
crit=(lo+hi)/2;se=math.sqrt(V)/3600;ci=[max(0,point-crit*se),point+crit*se]
for x in vr:x['variance_share']=x['variance_CPU_s2']/V
w=r/'workloads/openai-math/final-seven-20261102/collection-remaining-six-20261103T0325/source38-TrackedTestBounds'
pub={x['stratum']:x for x in csv.DictReader((w/'sampling-uncertainty.csv').open())}
for x in vr:
 assert abs(float(pub[x['stratum']]['estimated_variance_share'])-x['variance_share'])<1e-10
assert abs(ci[0]-43.9877057)<1e-6 and abs(ci[1]-449.7383739)<1e-6
for p in [w/'sampling-uncertainty.csv',w/'sampling-uncertainty.md',w/'stratum-coverage.csv',r/'workloads/reports/step-W105-20261103-source38-sampling-uncertainty.md']:inputs.add(p)
inputs.add(ref)
with tarfile.open(e/'native16-and-source38-raw.tar.gz','w:gz')as tf:
 for p in sorted(inputs):
  if p.exists()and p.is_file():tf.add(p,arcname=str(p).lstrip('/'),recursive=False)
for name,rows in [('native16.csv',cells),('ordinary4-8-pairs.csv',pairs),('whole-command-P4-P8.csv',pmu),('source19-variance.csv',vr)]:
 with(e/name).open('w',newline='')as f:
  cw=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');cw.writeheader();cw.writerows(rows)
out=dict(native_points=16,accepted_per_point=4449,entries=425463,unsafe_partial_exclusions=3595,checks=237863,allocation_units=3283925639,identities_retired=len(identities),cgroups_absent=16,wait4_HWM_KiB=hwm,sampled_peak_bytes=sampled,charged_peak_bytes=charged,ordinary_extra_bracket_fraction_min=min(x['fraction']for x in pairs),ordinary_extra_bracket_fraction_max=max(x['fraction']for x in pairs),stat_IPC4=ipc4,stat_IPC8=ipc8,whole_stat_P4_P8=pmu,source19_point_CPU_h=point,source19_variance_CPU_s2=V,source19_df=df,source19_tcritical=crit,source19_nominal95_CPU_h=ci,source_variance_top=sorted(vr,key=lambda x:x['variance_share'],reverse=True)[:2],raw_tar_bytes=(e/'native16-and-source38-raw.tar.gz').stat().st_size,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,native_runs=0,agents=0)
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n');print('STEP',s);print(json.dumps(out))
