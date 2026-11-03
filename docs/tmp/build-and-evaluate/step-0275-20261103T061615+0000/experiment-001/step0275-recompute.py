from pathlib import Path
import os,subprocess,json,csv,gzip,tarfile,datetime,time,resource,random,statistics,re
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');d=r/'research/decoupled-check';a=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102');ss=a/'size-sample'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0275-'+stamp);s.mkdir();e=s/'experiment-001';e.mkdir();Path('/workspaces/.agent-state/gpu-smt-ramsey-sample-root-step.txt').write_text(str(s)+'\n')
for n in ['docs/paper/main.tex','docs/paper/main.pdf','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md','docs/cleanup-20261101.md']:
 (e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
start=time.monotonic();inputs=set()
def read(p):
 inputs.add(p);return json.loads(p.read_text())
frame={v['module']:v for v in read(a/'frame.json')};plan=read(ss.parent/'size-sample-plan.json');assert plan==read(d/'ramsey-sample-plan.json')
ledger=[json.loads(x)for x in(a/'ledger.jsonl').read_text().splitlines()];inputs.add(a/'ledger.jsonl')
builds=[v for v in ledger if v['operation']=='build'];assert len(builds)==190 and all(v['valid']and not v['sorry_warning']for v in builds)
byname={v['module']:v for v in builds};assert len(byname)==190
state=read(a/'state.json');assert not state['stream_ids']and state['segments']==0 and len(state['built'])==10934
sourcepub={v['module']:v for v in csv.DictReader((d/'ramsey-source-costs.csv').open())if v['target']=='True'};assert set(sourcepub)==set(byname)
selected={v['module']for v in plan['selected']};k10=plan['supplemental_k10'];assert k10 not in selected
rawsample=[json.loads(x)for x in(ss/'results.jsonl').read_text().splitlines()];inputs.add(ss/'results.jsonl')
assert [v['module']for v in rawsample]==[v['module']for v in plan['selected']] and len(rawsample)==20
term=read(ss/'terminal.json');assert term['complete']and term['accepted']==20 and term['failed']==0
cgroups=[];hwm_source=hwm_check=charged_source=charged_check=0
sources=[];checks=[]
def cell(base,key,scope):
 global hwm_source,hwm_check,charged_source,charged_check
 v=read(base/(key+'.result.json'));c=read(base/(key+'.command.json'))
 assert all(c[k]==v[k]for k in c) and v['returncode']==0 and v['affinity']==list(range(8)) and v['measured'] and v['limit_s']==1400
 assert v['memory_max_bytes']==12616466432 and not any(x.startswith('-M')for x in v['args'])
 assert not Path(v['cgroup']).exists();cgroups.append(v['cgroup'])
 ev=dict(x.split()for x in v['memory_events'].splitlines());assert int(ev['oom'])==int(ev['oom_kill'])==0
 for suffix in ['.stdout','.stderr']:inputs.add(base/(key+suffix))
 assert 'cleanup_pending' not in v
 if scope=='source':hwm_source=max(hwm_source,v['peak_rss_kib']);charged_source=max(charged_source,v['cgroup_peak_bytes'])
 else:hwm_check=max(hwm_check,v['peak_rss_kib']);charged_check=max(charged_check,v['cgroup_peak_bytes'])
 return v
for m,v in byname.items():
 c=cell(a,v['cell']['key'],'source');assert c==v['cell'] and c['args'][-1]==frame[m]['source']
 args=c['args'];assert '-j8'in args and '-DautoImplicit=false'in args and all(z in args for z in ['-o','-i','-c'])
 for flag in ['-o','-i','-c']:assert Path(args[args.index(flag)+1]).stat().st_size>0
 cpu=c['user_s']+c['system_s'];pub=sourcepub[m]
 assert abs(cpu-float(pub['source_cpu_s']))<1e-9 and abs(c['wall_s']-float(pub['source_wall_s']))<1e-9
 p=Path(frame[m]['source']);sources.append(dict(module=m,bytes=p.stat().st_size,source_cpu_s=cpu,source_wall_s=c['wall_s'],key=c['key']))
 assert "declaration uses 'sorry'"not in ((a/(c['key']+'.stdout')).read_text()+(a/(c['key']+'.stderr')).read_text())
src={v['module']:v for v in sources};ordered=sorted(sources,key=lambda x:(x['bytes'],x['module']));rng=random.Random(20261103)
for k in range(5):
 chosen=rng.sample(ordered[k*38:(k+1)*38],4)
 assert {v['module']for v in chosen}=={v['module']for v in plan['selected']if v['stratum']==k+1}
for i,row in enumerate(rawsample):
 c=cell(ss,'sample-'+str(i).zfill(2),'check');assert c==row['cell']and row['valid']and row['accepted']==[row['module']]
 assert c['args'][-4:]==['/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/measurement-v1/audited-stream','one','none',row['module']]
 es=[json.loads(x)for x in(ss/(c['key']+'.stdout')).read_text().splitlines()if x.startswith('{')]
 assert [v['module']for v in es if v.get('event')=='accept']==[row['module']]and not any(v.get('event')=='reject'for v in es)
 v=src[row['module']];cpu=c['user_s']+c['system_s'];assert row['bytes']==v['bytes']and abs(row['source_cpu_s']-v['source_cpu_s'])<1e-9
 checks.append(dict(module=row['module'],stratum=row['stratum'],bytes=v['bytes'],source_cpu_s=v['source_cpu_s'],check_cpu_s=cpu,source_wall_s=v['source_wall_s'],check_wall_s=c['wall_s'],cpu_ratio=cpu/v['source_cpu_s'],wall_ratio=c['wall_s']/v['source_wall_s'],key=c['key']))
pub={v['module']:v for v in csv.DictReader((d/'ramsey-sample-costs.csv').open())}
for v in checks:
 assert abs(v['check_cpu_s']-float(pub[v['module']]['check_cpu_s']))<1e-9
ref=cell(a,'oracle-early-k10','check');sc=byname[k10]['cell'];es=[json.loads(x)for x in(a/'oracle-early-k10.stdout').read_text().splitlines()if x.startswith('{')];assert [v['module']for v in es if v.get('event')=='accept']==[k10]
# Compare selected original sources with exact members in the retained fixed archive.
archive=Path('/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz')
wanted={'lean/'+m.replace('.','/')+'.lean':m for m in byname};found=set();sourcebytes=0;frozen_selected_bytes=0
with tarfile.open(archive,'r|gz')as tf:
 for member in tf:
  parts=member.name.split('/',1)
  rel=parts[1]if len(parts)>1 else ''
  if rel in wanted:
   m=wanted[rel];data=tf.extractfile(member).read();assert data==Path(frame[m]['source']).read_bytes();found.add(m);sourcebytes+=len(data)
   if m in selected or m==k10:inputs.add(Path(frame[m]['source']));frozen_selected_bytes+=len(data)
assert found==set(byname)
def quant(v,q):
 v=sorted(v);p=(len(v)-1)*q;i=int(p);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(p-i)
source_sum=sum(v['source_cpu_s']for v in sources);check_sum=sum(v['check_cpu_s']for v in checks);sample_source=sum(v['source_cpu_s']for v in checks)
strata=[dict(stratum=k,N=38,n=4,source_cpu_s=sum(v['source_cpu_s']for v in checks if v['stratum']==k),check_cpu_s=sum(v['check_cpu_s']for v in checks if v['stratum']==k))for k in range(1,6)]
estimate=sum(38*v['check_cpu_s']/4 for v in strata);rng=random.Random(20261103);groups=[[v['check_cpu_s']for v in checks if v['stratum']==k]for k in range(1,6)]
boot=[sum(38*statistics.mean(rng.choices(v,k=4))for v in groups)/source_sum for _ in range(10000)]
est=read(d/'ramsey-sample-estimate.json');assert abs(est['estimated_retained190_independent_module_local_cpu_s']-estimate)<1e-7
assert abs(est['bootstrap95_low']-quant(boot,.025))<1e-10 and abs(est['bootstrap95_high']-quant(boot,.975))<1e-10
census=list(csv.DictReader((d/'ramsey-target-census.csv').open()));assert len(census)==444
built=[v for v in census if v['module']in byname];unbuilt=[v for v in census if v['module']not in byname];assert len(built)==190
for v in census:assert int(v['bytes'])==Path(frame[v['module']]['source']).stat().st_size
assert all('.Construction.'in v['module']for v in built)
ids=[]
def retire(pid,birth):
 q=Path('/proc')/str(pid)/'stat'
 if q.exists():assert q.read_text().rsplit(')',1)[1].split()[19]!=str(birth)
 ids.append(dict(pid=pid,birth=birth))
sub=read(ss/'submission.json');retire(sub['pid'],sub['birth'])
stop=read(a/'user-stop-after-window.json');retire(stop['controller_pid'],stop['controller_birth']);retire(stop['cancelled_waiter_pid'],stop['cancelled_waiter_birth'])
assert not stop['native_signalled']
pidonly=[]
for q in ss.glob('task-*.submission.json'):
 v=read(q);assert not (Path('/proc')/str(v['pid'])).exists();pidonly.append(v['pid'])
for base in [a,ss]:
 for q in base.glob('task-*.submission.json'):
  inputs.add(q)
for q in ss.glob('*.log'):inputs.add(q)
for q in [a/'ramsey-run-v3.py',a/'frame-receipt.json',a/'queue-terminal.json',a/'continuation-v3-submission.json',a/'continuation-v3-terminal.json',ss/'runner.py',ss/'terminal.json']:
 inputs.add(q)
for q in d.glob('ramsey*'):
 if q.suffix in ['.md','.py','.json','.csv']:inputs.add(q)
inputs.add(d/'analyze-ramsey-sample.py')
collector=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101/native_project.py');inputs.add(collector)
ad=collector.parent.parent/'measurement-v1'/'AuditedStream.lean';inputs.add(ad)
# Preserve the real source and complete raw records; no SDK/native objects.
with tarfile.open(e/'ramsey-selected-raw-and-source.tar.gz','w:gz')as tf:
 for q in sorted(inputs):
  if q.exists()and q.is_file():tf.add(q,arcname=str(q).lstrip('/'),recursive=False)
for name,rows in [('source190.csv',sources),('sample20.csv',checks),('strata.csv',strata)]:
 with(e/name).open('w',newline='')as fo:
  w=csv.DictWriter(fo,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
out=dict(source_targets=190,full_targets=444,stream_targets=0,stream_cpu_s=0,source_cpu_s=source_sum,source_wall_s=sum(v['source_wall_s']for v in sources),selected=20,accepted=20,sample_check_cpu_s=check_sum,sample_source_cpu_s=sample_source,sample_pooled_ratio=check_sum/sample_source,individual_p10=quant([v['cpu_ratio']for v in checks],.1),individual_median=statistics.median(v['cpu_ratio']for v in checks),individual_p90=quant([v['cpu_ratio']for v in checks],.9),estimated_prefix_check_cpu_s=estimate,estimated_prefix_ratio=estimate/source_sum,bootstrap_low=quant(boot,.025),bootstrap_high=quant(boot,.975),source_HWM_KiB=hwm_source,check_HWM_KiB=hwm_check,source_charged_peak_B=charged_source,check_charged_peak_B=charged_check,cgroups_absent=len(cgroups),recorded_births_retired=ids,pid_only_retired=pidonly,native_child_births_emitted=False,independent_RSS_sample_emitted=False,source_archive_bytes_compared=sourcebytes,selected_source_frozen_bytes=frozen_selected_bytes,archive_size=archive.stat().st_size,raw_frozen_bytes=(e/'ramsey-selected-raw-and-source.tar.gz').stat().st_size,built_median_bytes=statistics.median(int(v['bytes'])for v in built),unbuilt_median_bytes=statistics.median(int(v['bytes'])for v in unbuilt),built_marked=sum(int(v['kernel_marker_occurrences'])>0 for v in built),all_marked=sum(int(v['kernel_marker_occurrences'])>0 for v in census),K10_source_cpu_s=sc['user_s']+sc['system_s'],K10_reference_cpu_s=ref['user_s']+ref['system_s'],K10_wall_ratio=ref['wall_s']/sc['wall_s'],root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,native_runs=0,agents=0)
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n')
print('ROOT275',s);print(json.dumps(out))
