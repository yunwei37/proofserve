from pathlib import Path
import os,resource,time,json,csv,tarfile,gzip
os.sched_setaffinity(0,{22,23});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103');s=Path(Path('/workspaces/.agent-state/gpu-smt-stock-negative-root-step.txt').read_text().strip());e=s/'experiment-001'
root='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
def events(p):
 with p.open()as f:
  for l in f:
   if l.startswith('{'):yield json.loads(l)
positive=list(events(b/'runs/full-plain-m0-P8-r1/stdout'));ordered=[x['module']for x in positive if x.get('event')=='accept'];reference={x['module']:(x['constants'],x['imports'])for x in positive if x.get('event')=='module_header'};work={x['module']:(x['metrics']['checks'],x['metrics']['raw_HB'])for x in positive if x.get('event')=='profile_module'}
assert len(ordered)==len(reference)==len(work)==4449 and ordered[-1]==root
freeze={b/'runs/full-plain-m0-P8-r1/stdout',b/'auxiliary.py',b/'native.py',b/'attribution.py'}
source_equal=[]
prior=r/'docs/tmp/build-and-evaluate/step-0280-20261103T131855+0000/experiment-001/new-qualified-raw-source.tar.gz'
with tarfile.open(prior,'r:gz')as tar:
 for n in ['source/ParallelCore.lean','source/ParallelStream.lean','source/persistence.c','source/checked_commit.c','source/placement_profile.c','native.py','attribution.py']:
  p=b/n;assert p.read_bytes()==tar.extractfile(str(p).removeprefix('/workspaces/')).read();source_equal.append(n);freeze.add(p)
keys=['aux-stock-default-m0-P8','aux-stock-fresh-m0-P1','aux-stock-fresh-m0-P8','aux-bad-root-m0-P8','aux-bad-root-m1-P8']
identities=set();rows=[];neg=[]
for key in keys:
 p=b/'runs'/key;c=json.loads((p/'command.json').read_text());v=json.loads((p/'result.json').read_text());t=json.loads((b/(key+'-terminal.json')).read_text());launch=json.loads((b/(key+'-launch.json')).read_text())
 assert c['argv']==v['argv']==t['cell']['argv']
 assert c['affinity']==list(range(8))and c['wall_limit_s']==1100 and c['cgroup_charged_memory_max_gib']==14 and c['own_rss_sample_stop_gib']==14
 assert not any(str(a).startswith('-M')for a in c['argv'])
 assert v['wait4_usage_complete']and v['native_retired']and not v['stop_reasons']and not Path(v['cgroup']).exists()
 assert all(int(z.split()[1])==0 for z in v['memory_events'].splitlines()if z.split()[0]in ['oom','oom_kill','oom_group_kill'])
 assert launch['argv'][:2]==['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock']
 identities.update([(int(v['pid']),str(v['birth'])),(int(launch['pid']),str(launch['birth']))]);peak=0
 for l in(p/'memory.jsonl').read_text().splitlines():
  a=json.loads(l);peak=max(peak,a['rss_bytes']);identities.update((int(z['pid']),str(z['birth']))for z in a['processes'])
 assert peak==v['sampled_tree_peak_bytes']
 stdout=(p/'stdout').read_text();stderr=(p/'stderr').read_text()
 if 'stock'in key:
  assert v['returncode']==0 and t['state']=='stock_scope_completed_no_M_work_equivalence_claim'and not stderr.strip()
  expected='replaying '+root+(' with --fresh'if 'fresh'in key else'')
  assert stdout.strip()==expected and not list(events(p/'stdout'))
 else:
  assert v['returncode']==1 and t['state']=='expected_real_root_kernel_reject'
  heads={};accept=[];profiles={};reject=[];complete=[]
  for x in events(p/'stdout'):
   ev=x.get('event')
   if ev=='module_header':assert x['module']not in heads;heads[x['module']]=(x['constants'],x['imports'])
   if ev=='accept':accept.append(x['module']);assert(x['constants'],x['imports'])==reference[x['module']]
   if ev=='profile_module':assert x['module']not in profiles;profiles[x['module']]=(x['metrics']['checks'],x['metrics']['raw_HB'])
   if ev=='reject':reject.append(x)
   if ev=='complete':complete.append(x)
  assert heads==reference and accept==ordered[:-1]and profiles=={k:v for k,v in work.items()if k!=root}
  assert len(reject)==1 and reject[0]['module']==root and not complete
  err='kernel_reject:OAI.SepticProfile.ExteriorCertificates.C41.fourth226:(kernel) type checker does not support loose bound variables, replace them with free variables before invoking it'
  assert reject[0]['error']==err and stderr.strip()=='uncaught exception: '+err
  neg.append(dict(key=key,prefix_modules=len(accept),prefix_checks=sum(a[0]for a in profiles.values()),prefix_allocation_units=sum(a[1]for a in profiles.values()),root=root,error=err,root_accept=False,complete_event=False))
 rows.append(dict(key=key,returncode=v['returncode'],wall_s=v['wall_s'],user_s=v['user_s'],system_s=v['system_s'],CPU_s=v['user_s']+v['system_s'],CPU_over_wall=(v['user_s']+v['system_s'])/v['wall_s'],HWM_KiB=v['peak_rss_kib'],sampled_RSS_B=peak,charged_peak_B=v['charged_peak_bytes']))
 freeze.update(p/n for n in ['command.json','result.json','stdout','stderr','memory.jsonl']);freeze.update(b/(key+tail)for tail in ['-terminal.json','-launch.json','-application.time','-controller.log'])
for pid,birth in identities:
 try:
  f=Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split();assert f[19]!=birth,(pid,birth,f[0])
 except FileNotFoundError:pass
for name,a in [('five-native-resources.csv',rows),('negative-prefix-errors.csv',neg)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(a[0]),lineterminator='\n');w.writeheader();w.writerows(a)
sdk=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
for n in ['src/lean/LeanChecker.lean','src/lean/Lean/Replay.lean','src/lean/Lean/Environment.lean']:freeze.add(sdk/n)
checker=(sdk/'src/lean/LeanChecker.lean').read_text();replay=(sdk/'src/lean/Lean/Replay.lean').read_text()
assert 'finalizeImport s mod.imports {} 0 false false'in checker and 'mkEmptyEnvironment).toKernelEnv.replay env.constants.map₁'in checker
assert 'IO.asTask (replayFromImports m)'in checker and 'for n in names do replayConstant n'in replay
aux=(b/'auxiliary.py').read_text();assert "e['DECOUPLED_MUTATE_MODULE']=MODULE"in aux and "e.pop('DECOUPLED_MUTATE_CONSTANT',None)"in aux
for n in ['stock-results.md','bad-root-results.md','causal-results.md','source-and-scope.md','auxiliary-plan.md']:freeze.add(r/'research/parallel-stream-check/persistent'/n)
with tarfile.open(e/'qualified-auxiliary-raw-source.tar.gz','w:gz')as tar:
 for p in sorted(freeze):tar.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
out=dict(root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,source_equal_root0280=source_equal,stock_native_controls=3,real_root_negative_controls=2,retired_actual_PID_births=len(identities),negative_prefix_modules=4448,prefix_equal_ordered_reference=True,all_five_cgroups_absent=True,no_OOM_or_sample_stop=True,resources=rows,negatives=neg,archive_bytes=(e/'qualified-auxiliary-raw-source.tar.gz').stat().st_size,native_reruns=0)
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
