from pathlib import Path
import os,time,json,datetime,subprocess,gzip,tarfile,csv,collections,math,resource
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-replay-root-step.txt').read_text().strip());e=s/'experiment-001';e.mkdir(parents=True,exist_ok=True)
(e/'initial-root-analysis-failure.txt').write_text('First offline analysis failed at tuple-key typo many[0,1,2] instead of many[0,1]. No native process or data change; corrected and rerun same stored evidence.\n')
b=Path('/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v11');t=json.loads((b/'module-terminal.json').read_text());mods=json.loads((b/'modules.json').read_text());launch=json.loads((b/'module-launch.json').read_text());runtime=json.loads((b/'runtime.json').read_text());assert t['state']=='complete' and not t['errors'] and len(t['cells'])==86
ids=set();freeze=set();phases=[];data={};stock=0
def retire(pid,birth):
 try:live=Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[19]==str(birth)
 except OSError:live=False
 assert not live,(pid,birth);ids.add((int(pid),str(birth)))
retire(launch['pid'],launch['birth'])
for q in t['cells']:
 p=b/'runs'/q['key'];assert q==json.loads((p/'result.json').read_text()) and q['returncode']==0 and q['wait4_usage_complete'] and not q['stop_reasons']
 assert q['affinity']==list(range(8)) and q['cgroup_charged_memory_max_gib']==14 and not any(str(x).startswith('-M')for x in q['argv'])
 assert not Path(q['cgroup']).exists();retire(q['pid'],q['birth'])
 assert all(int(l.split()[1])==0 for l in q['memory_events'].splitlines()if l.split()[0].startswith('oom'))
 for l in (p/'memory.jsonl').open():
  for x in json.loads(l).get('processes',[]):retire(x['pid'],x['birth'])
 if q['key'].startswith('stock-'):stock+=1
 else:
  mode='front'if q['key'].startswith('front-')else'kernel';prefix='FRONT 'if mode=='front'else'KERNEL '
  rows=[json.loads(l[len(prefix):])for l in (p/'stdout').open()if l.startswith(prefix)]
  expected=8 if mode=='front'else rows[0]['selected'];assert len(rows)==expected
  vals={}
  for x in rows:
   if mode=='front':
    assert x['verdict']=='accepted' and not x['errors'] and not x['new_axioms'] and not x['sorry']
    uid=str(x['index']);hb=[v['rawHB']for v in x['commands']];cpu=sum(int(v['cpuNS'])for v in x['commands'])/1e9;tid=x['tid'];verdict=x['verdict'];diag=x['errors']
   else:
    z=x['result'];assert z['verdict']=='accepted' and not z['error'] and x['kernel_poll_count'] is None
    uid=z['target'];hb=[z['rawHB']];cpu=int(z['cpuNS'])/1e9;tid=z['tid'];verdict=z['verdict'];diag=z['error'];assert int(z['cpuNS'])<=int(z['wallNS'])*1.1+1000000
   assert uid not in vals;vals[uid]={'hb':hb,'cpu_s':cpu,'tid':tid,'verdict':verdict,'diagnostics':diag}
  data[q['key']]=vals
 phases.append({k:q[k]for k in ['key','returncode','wall_s','user_s','system_s','peak_rss_kib','sampled_tree_peak_bytes','charged_peak_bytes']})
 freeze.update(x for x in p.iterdir()if x.is_file())
assert stock==2 and len(data)==84
summary=[];pairs=[];ranges=[];unitcounts={}
for m in mods:
 short=m['module'].split('.')[-1]
 # Resolve exact target from frozen runtime path; compare actual file bytes to retained original source-produced artifact.
 rel=Path(*m['module'].split('.')).with_suffix('.olean');path=next((Path(z)/rel for z in runtime['LEAN_PATH'].split(':') if(Path(z)/rel).exists()),None)
 assert path is not None and path.read_bytes()==Path(m['path']).read_bytes(),m['module']
 for mode in (['front','kernel']if m['regime']=='mathematical'else['kernel']):
  many={}
  for rep in [0,1,2]:
   for workers in [1,2,4,8]:many[rep,workers]=data[f'{mode}-{short}-r{rep}-j{workers}']
  n=len(many[0,1]);assert all(len(v)==n for v in many.values());unitcounts[short,mode]=n
  cc=[]
  for rep in [0,1,2]:
   base=many[rep,1]
   for workers in [2,4,8]:
    cur=many[rep,workers];assert base.keys()==cur.keys()
    for uid,a in base.items():
     z=cur[uid];cc.append({'module':short,'stage':mode,'repeat':rep,'workers':workers,'unit':uid,'verdict_equal':a['verdict']==z['verdict'],'diagnostic_equal':a['diagnostics']==z['diagnostics'],'unit_vector_equal':a['hb']==z['hb']})
  maxrange=0.;cpu_lo=float('inf');cpu_hi=0.
  for uid in many[0,1]:
   values=[v[uid]for v in many.values()];h=[sum(x['hb'])for x in values];c=[x['cpu_s']for x in values]
   rr=(max(h)-min(h))/min(h);maxrange=max(maxrange,rr);cpu_lo=min(cpu_lo,min(c));cpu_hi=max(cpu_hi,max(c))
   ranges.append({'module':short,'stage':mode,'unit':uid,'observations':12,'min_raw_HB':min(h),'max_raw_HB':max(h),'relative_range':rr,'min_thread_CPU_s':min(c),'max_thread_CPU_s':max(c)})
  summary.append({'module':short,'regime':m['regime'],'stage':mode,'unique_units':n,'rows':12*n,'pairs':len(cc),'HB_vector_differences':sum(not x['unit_vector_equal']for x in cc),'verdict_differences':sum(not x['verdict_equal']for x in cc),'diagnostic_differences':sum(not x['diagnostic_equal']for x in cc),'maximum_relative_raw_count_range':maxrange,'unit_CPU_min_s':cpu_lo,'unit_CPU_max_s':cpu_hi,'active_TID_counts_by_requested_workers':{str(k):sorted({len({x['tid']for x in many[rep,k].values()}) for rep in [0,1,2]})for k in [1,2,4,8]}})
  pairs+=cc
assert sum(z['rows']for z in summary)==504 and sum(z['pairs']for z in summary)==378
assert sum(z['HB_vector_differences']for z in summary if z['stage']=='kernel')==0
assert sum(z['HB_vector_differences']for z in summary if z['stage']=='front')==78
assert not any(z['verdict_differences']or z['diagnostic_differences']for z in summary)

# Reconstruct observed logical-source envelopes across all clones and configurations.
pooled=[]
for short in ['InteriorH1Derivative','ReindexSingle']:
 vals=[sum(z['hb']) for k,v in data.items() if k.startswith('front-'+short+'-') for z in v.values()]
 assert len(vals)==96
 pooled.append({'module':short,'observations':len(vals),'min_raw_HB':min(vals),'max_raw_HB':max(vals),'relative_range':max(vals)/min(vals)-1})
for p in b.iterdir():
 if p.is_file() and p.suffix in ['.json','.py','.lean','.c','.log']:freeze.add(p)
# W fresh target-only replay: reconstruct from original source ledgers and native logs.
wbase=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-noM-original31-kernel-replay-namespace-v2-20261101')
wt=json.loads((wbase/'terminal.json').read_text());wl=json.loads((wbase/'launch.json').read_text());assert wt['complete']and wt['rows']==wt['native_rows']==31 and wt['stop']is None
retire(wl['pid'],wl['birth_ticks']);wid=[(wl['pid'],wl['birth_ticks'])]
source={};csvrows=list(csv.DictReader((r/'workloads/openai-math/noM-original-c-suffix48/sample-costs.csv').open()));assert len(csvrows)==42
for x in csvrows:
 if x['status']!='completed_cost':continue
 p=Path(x['source_file']);z=json.loads(p.read_text().splitlines()[int(x['source_line'])-1])
 assert z['status']=='compile_ok'and z['source_exact']and z['lean_memory_option_MiB']==0 and z['pcore_lock']and z['threads']==8 and not z['profiled']and z['compilation_outputs']=='olean_ilean_c'and z['heartbeat_budget']=='authored_or_native_default'
 source[z['module']]=z
 freeze.add(p)
assert len(source)==31
paired_owner={x['module']:x for x in csv.DictReader((r/'workloads/openai-math/native-replay31/paired-modules.csv').open())}
wrows=[];srcfreeze=[]
for p in sorted((wbase/'runs').glob('*/result.json')):
 z=json.loads(p.read_text());q=json.loads((p.parent/'command.json').read_text());m=z['module'];a=source[m]
 assert z['returncode']==0 and z['status']=='accepted'and z['source_exact']and z['pcore_lock']and z['native_retired']and z['cgroup_retired']and z['threads']==8 and not z['profiled']
 assert not any(str(v).startswith('-M')for v in q['args']) and q['affinity']==list(range(8))and q['cgroup_settings']['memory.max']==str(15*1024**3)and not Path(q['native_cgroup']).exists()
 assert all(int(l.split()[1])==0 for l in z['cgroup_memory_events'].splitlines()if l.split()[0].startswith('oom'))
 retire(z['pid'],z['birth_ticks']);wid.append((z['pid'],z['birth_ticks']))
 ev=[json.loads(l)for l in(p.parent/'native.log').read_text().splitlines()]
 assert ev==z['verification_events']and len(ev)==2 and ev[0]['event']=='accept'and ev[0]['module']==m and ev[0]['skipped_unsafe_partial']==0 and ev[1]['event']=='one_complete'
 for part in z['matched_artifact_parts']:
  assert Path(part['producer_copy']).parent==Path(a['raw'])/'artifacts'
  assert Path(part['input']).read_bytes()==Path(part['producer_copy']).read_bytes()
 cpu=a['user_cpu_s']+a['system_cpu_s'];qc=z['user_cpu_s']+z['system_cpu_s']
 item={'module':m,'stratum':z['stratum'],'source_CPU_s':cpu,'replay_CPU_s':qc,'source_wall_s':a['wall_s'],'replay_wall_s':z['wall_s'],'CPU_ratio':qc/cpu,'wall_ratio':z['wall_s']/a['wall_s'],'population_weight':float(paired_owner[m]['population_weight'])}
 for key in ['source_CPU_s','replay_CPU_s','source_wall_s','replay_wall_s']:assert abs(item[key]-float(paired_owner[m][key]))<1e-8
 assert item['CPU_ratio']<1 and item['wall_ratio']<1
 wrows.append(item);freeze.update(x for x in p.parent.iterdir()if x.is_file())
 assert all(json.loads(l)['birth_ticks']==z['birth_ticks']for l in(p.parent/'memory.jsonl').open())
for p in wbase.iterdir():
 if p.is_file()and(p.suffix in ['.json','.jsonl','.py','.csv','.lean','.log']):freeze.add(p)
assert len(wrows)==31
import statistics
observed={'pairs':31,'source_CPU_s':sum(x['source_CPU_s']for x in wrows),'replay_CPU_s':sum(x['replay_CPU_s']for x in wrows),'source_wall_s':sum(x['source_wall_s']for x in wrows),'replay_wall_s':sum(x['replay_wall_s']for x in wrows),'median_module_CPU_ratio':statistics.median(x['CPU_ratio']for x in wrows),'median_module_wall_ratio':statistics.median(x['wall_ratio']for x in wrows),'queue_inclusive_controller_s':wt['elapsed_including_queue_s']}
observed['ratio_CPU_sums']=observed['replay_CPU_s']/observed['source_CPU_s'];observed['ratio_wall_sums']=observed['replay_wall_s']/observed['source_wall_s']
assert abs(observed['replay_wall_s']-wt['native_wall_sum_s'])<1e-8
groups=collections.defaultdict(list)
for x in wrows:groups[x['stratum']].append(x)
complete=[x for x in groups.values()if len(x)==2];assert len(complete)==14
cond={}
for label,sel in [('all',complete),('ordinary',[x for x in complete if x[0]['stratum'].endswith(';0')]),('marked',[x for x in complete if x[0]['stratum'].endswith(';1')])]:
 B=sum(z['population_weight']*z['source_CPU_s']for x in sel for z in x);Q=sum(z['population_weight']*z['replay_CPU_s']for x in sel for z in x)
 cond[label]={'cells':len(sel),'source_CPU_h':B/3600,'target_replay_CPU_h':Q/3600,'ratio':Q/B}
# Reconstruct fragile nominal delta/t interval independently from paired residuals.
import sys
sys.path.insert(0,'/workspaces/.agent-state/gpu-smt-captures/workloads/statistics-python-deps')
from scipy.stats import t as tdist
for label,vals in cond.items():
 sel=complete if label=='all'else[x for x in complete if x[0]['stratum'].endswith(';0'if label=='ordinary'else';1')]
 B=vals['source_CPU_h']*3600;rr=vals['ratio'];varparts=[]
 for x in sel:
  N=2*x[0]['population_weight'];res=[z['replay_CPU_s']-rr*z['source_CPU_s']for z in x]
  varparts.append(N*N*(1-2/N)*statistics.variance(res)/2/B**2)
 var=sum(varparts);df=var**2/sum(v*v for v in varparts);margin=float(tdist.ppf(.975,df))*math.sqrt(var)
 vals.update(nominal_ratio95_low=max(0,rr-margin),nominal_ratio95_high=rr+margin,nominal_df=df)
assert abs(cond['all']['target_replay_CPU_h']-54.905548)<1e-6
# O first full-stream failure: retain partial records without completing the acceptance set.
ob=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
oq=json.loads((ob/'primary.result.json').read_text());assert oq['returncode']==124 and oq['limit_s']==1500 and not Path(oq['cgroup']).exists() and oq['affinity']==list(range(8))and not any(str(v).startswith('-M')for v in oq['args'])
assert all(int(l.split()[1])==0 for l in oq['memory_events'].splitlines()if l.split()[0].startswith('oom'))
events=[];bad=[]
for i,l in enumerate((ob/'primary.stdout').read_text().splitlines(keepends=True)):
 try:events.append(json.loads(l))
 except json.JSONDecodeError:bad.append({'line':i+1,'bytes':len(l.encode()),'trailing_newline':l.endswith('\n'),'fragment':l})
accepts=[v for v in events if v.get('event')=='accept'];headers=[v for v in events if v.get('event')=='module_header']
assert len(accepts)==len({v['module']for v in accepts})==8942 and len(headers)==8943 and len(bad)==1 and not bad[0]['trailing_newline']
assert not any(v.get('event')in['complete','audit_complete']for v in events)
oj={'native':oq,'complete_accepts':len(accepts),'complete_headers':len(headers),'fragment':bad,'coordinator_terminal':json.loads((ob/'coordinator-terminal.json').read_text()),'reported_source_summary':json.loads((ob/'reduced-summary.json').read_text()),'PID_birth_emitted_by_native_receipt':False,'cgroup_absent':True,'ratio_computed':False}
for n in ['primary.command.json','primary.result.json','primary.stdout','primary.stderr','coordinator-terminal.json','progress.json','reduced-summary.json','falconer-window.py']:
 freeze.add(ob/n)
for n in ['research/decoupled-check/falconer-interruption-20261102.md','research/decoupled-check/falconer-source-costs.csv','workloads/openai-math/native-replay31/README.md','workloads/openai-math/estimate_paired_replay_costs.py','workloads/reports/W075-step.md','research/reproducible-verdict/module-results-v11/results.md']:freeze.add(r/n)
with tarfile.open(e/'new-complete-and-failed-capture-records.tar.gz','w:gz')as tf:
 for p in sorted(freeze):
  if p.exists():tf.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
for name,rows in [('stage-summary',summary),('pairs',pairs),('unit-ranges',ranges),('source-pooled-count-ranges',pooled),('W-native-pairs',wrows)]:
 with(e/(name+'.csv')).open('w',newline='')as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');wr.writeheader();wr.writerows(rows)
(e/'O-first-stream-timeout.json').write_text(json.dumps(oj,indent=2)+'\n')
j={'M_native_phases':86,'M_stock_controls':2,'M_stage_cells':84,'M_stage_rows':504,'M_stage_pairs':378,'M_summary':summary,'M_logical_source_ranges':pooled,'retired_identity_count_M_W':len(ids),'retired_identities':sorted(ids),'M_controller':launch,'M_whole_controller_wall_s':t['wall_s'],'M_max_wait4_RSS_KiB':max(x['peak_rss_kib']for x in phases),'M_max_sampled_RSS_B':max(x['sampled_tree_peak_bytes']for x in phases),'M_max_charged_memory_B':max(x['charged_peak_bytes']for x in phases),'W_observed':observed,'W_conditional':cond,'W_controller':wl,'W_identities':wid,'O_timeout':{k:v for k,v in oj.items()if k not in ['native','reported_source_summary','fragment']},'new_root_native':0,'root_analysis_seconds':time.monotonic()-start,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
for n in ['docs/paper/main.tex','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md']:(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
print('STEP',s);print(json.dumps({k:v for k,v in j.items()if k not in ['retired_identities','M_summary','M_controller','W_controller','W_identities']}))
