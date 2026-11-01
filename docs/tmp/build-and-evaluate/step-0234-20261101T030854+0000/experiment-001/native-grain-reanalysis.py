from pathlib import Path
import os,time,json,csv,gzip,math,statistics,re,resource
os.sched_setaffinity(0,{22,23});begin=time.monotonic();csv.field_size_limit(32*1024**2)
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-native-grain-paper-step.txt').read_text().strip());e=s/'experiment-001'
m=r/'research/chunked-kernel-check';raw=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/declaration-distribution-v1')
def freeze(p,name):
 b=Path(p).read_bytes();q=e/(name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(q.read_bytes())==b;return b
def live(pid,birth):
 p=Path(f'/proc/{pid}/stat')
 return p.exists() and p.read_text().rsplit(')',1)[1].split()[19]==str(birth)
for f in ['terminal.json','inputs.json','launch.json','controls.json','TimedReplay.lean','declaration_native.py','controller.py']:
 freeze(raw/f,'raw-'+f)
term=json.loads((raw/'terminal.json').read_text());assert term['complete'] and term['completed']==term['planned']==34
launch=json.loads((raw/'launch.json').read_text());assert not live(launch['pid'],launch['birth'])
inputs=json.loads((raw/'inputs.json').read_text());lookup={x['module']:x for x in inputs};assert len(inputs)==len(lookup)==31
assert sum(bool(x['inclusion_probability']) for x in inputs)==29 and all(not x['source_has_M_flag'] for x in inputs)
trials=sorted((raw/'runs').glob('[0-9][0-9]-*/result.json'));assert len(trials)==34
summary=[];completes={};receipts=[];calls=[];rawmeta=[];maxrss=maxcharged=maxsample=0
for file in trials:
 p=file.parent;q=json.loads(file.read_text());c=json.loads((p/'command.json').read_text())
 assert q['returncode']==0 and q['native_retired'] and q['cgroup_retired'] and not q['stop_reasons']
 assert not live(q['pid'],q['birth']) and not Path(q['cgroup']).exists()
 assert q['affinity']==list(range(8)) and q['cgroup_charged_memory_max_gib']==14
 assert not any(a.startswith('-M') for a in q['argv'])
 assert c['argv']==q['argv'] and q['argv'][q['argv'].index('--run')+2] in ['timed','stock']
 argv=q['argv'];mode=argv[argv.index('--run')+2];module=argv[argv.index('--run')+3]
 assert argv[argv.index('--run')+4]==lookup[module]['path']
 ev=[];done=[];inputevents=[]
 for line in (p/'stdout').open():
  if not line.startswith('{'):continue
  x=json.loads(line)
  if x['event']=='complete':done.append(x)
  elif x['event']=='input':inputevents.append(x)
  elif x['event']=='kernel_declaration':
   assert x['accepted'] and int(x['thread_cpu_ns'])<=int(x['wall_ns'])*1.05+1000000
   ev.append({k:x[k] for k in ['names','decide_helper','wall_ns','thread_cpu_ns']})
 assert len(done)==len(inputevents)==1 and done[0]['all_eligible_present']
 assert done[0]['module']==module and done[0]['mode']==mode
 assert set(done[0]['eligible_names']) and len(done[0]['eligible_names'])==len(set(done[0]['eligible_names']))
 completes[(module,mode)]=done[0]
 if mode=='timed':
  helpers=[x for x in ev if x['decide_helper']];large=[x for x in helpers if int(x['thread_cpu_ns'])>=10**9]
  total=sum(int(x['thread_cpu_ns']) for x in ev)/1e9;dcpu=sum(int(x['thread_cpu_ns']) for x in helpers)/1e9;lcpu=sum(int(x['thread_cpu_ns']) for x in large)/1e9
  summary.append({'module':module,'traced_calls':len(ev),'decision_calls':len(helpers),'native_call_CPU_s':total,'decision_CPU_s':dcpu,'large_decision_calls':len(large),'large_decision_CPU_s':lcpu,'median_decision_CPU_s':statistics.median(int(x['thread_cpu_ns'])/1e9 for x in helpers) if helpers else None,'max_decision_CPU_s':max((int(x['thread_cpu_ns'])/1e9 for x in helpers),default=0),'all_large_call_CPU_s':sum(int(x['thread_cpu_ns']) for x in ev if int(x['thread_cpu_ns'])>=10**9)/1e9})
  calls.extend({'module':module,**x} for x in ev)
 receipts.append({'key':p.name,'command':c,'result':q})
 rawmeta.append({'stdout':str(p/'stdout'),'bytes':(p/'stdout').stat().st_size,'mtime_ns':(p/'stdout').stat().st_mtime_ns})
 maxrss=max(maxrss,q['peak_rss_kib']);maxcharged=max(maxcharged,q['charged_peak_bytes']);maxsample=max(maxsample,q['sampled_tree_peak_bytes'])
assert len(summary)==31
published={x['module']:x for x in csv.DictReader((m/'declaration-distribution.csv').open())};assert set(published)=={x['module'] for x in summary}
for x in summary:
 p=published[x['module']]
 for a,b in [('native_call_CPU_s','all_kernel_call_cpu_s'),('decision_CPU_s','decision_call_cpu_s'),('large_decision_CPU_s','large_decision_cpu_s')]:
  assert math.isclose(x[a],float(p[b]),abs_tol=1e-8)
 assert x['decision_calls']==int(p['traced_decide_helpers'])
hot=[]
for (module,mode),done in completes.items():
 if mode!='stock':continue
 timed=completes[(module,'timed')]
 assert set(done['eligible_names'])==set(timed['eligible_names'])
 hot.append({'module':module,'accepted_sets_equal':True,'stock_process_replay_CPU_s':int(done['replay_process_cpu_ns'])/1e9,'timed_process_replay_CPU_s':int(timed['replay_process_cpu_ns'])/1e9,'timed_over_stock_CPU':int(timed['replay_process_cpu_ns'])/int(done['replay_process_cpu_ns'])})
assert len(hot)==3
controls={}
for mode in ['stock','timed']:
 for kind in ['control','invalid']:
  p=raw/'runs'/(kind+'-'+mode);q=json.loads((p/'result.json').read_text());assert q['returncode']==(0 if kind=='control' else 1) and q['native_retired'] and not q['stop_reasons'] and q['cgroup_retired']
  if kind=='invalid':
   assert '(kernel)' in (p/'stderr').read_text()
   if mode=='timed':assert any(x.get('event')=='kernel_declaration' and not x['accepted'] for x in map(json.loads,(p/'stdout').read_text().splitlines()) if isinstance(x,dict))
  else:
   done=[json.loads(x) for x in (p/'stdout').read_text().splitlines() if json.loads(x).get('event')=='complete'];assert len(done)==1;controls[mode]=done[0]
  for f in ['result.json','stdout','stderr']:freeze(p/f,'control-'+p.name+'-'+f)
assert set(controls['stock']['eligible_names'])==set(controls['timed']['eligible_names'])
total=sum(x['native_call_CPU_s'] for x in summary);decision=sum(x['decision_CPU_s'] for x in summary);big=sum(x['large_decision_CPU_s'] for x in summary)
sampled=[x for x in summary if lookup[x['module']]['inclusion_probability']]
w=lambda x:1/float(lookup[x['module']]['inclusion_probability'])
weighted_big=sum(w(x)*x['large_decision_CPU_s'] for x in sampled)
weighted_all=sum(w(x)*x['native_call_CPU_s'] for x in sampled);weighted_dec=sum(w(x)*x['decision_CPU_s'] for x in sampled)
estimate=json.loads((m/'declaration-estimate.json').read_text())
assert math.isclose(weighted_big/weighted_all,estimate['available_case_weighted_large_decision_share_of_all_kernel_cpu'],abs_tol=1e-12)
assert math.isclose(weighted_big/weighted_dec,estimate['available_case_weighted_large_decision_share_of_decision_kernel_cpu'],abs_tol=1e-12)
for name,content in [('native-clock-calls.json.gz',calls),('native-command-result-packet.json.gz',receipts),('native-module-summary.json.gz',summary)]:
 (e/name).write_bytes(gzip.compress(json.dumps(content,separators=(',',':')).encode(),mtime=0))
for f in ['step-005-report.md','step-005-audit.md','step-006-report.md','step-006-audit.md','declaration-distribution.csv','declaration-observer-controls.csv','declaration-estimate.json','components-semantic-comparison.json','components-summary.csv','components-validation.json']:
 freeze(m/f,'M-'+f)
# A distinct component-preserving, already completed diagnostic point.
cp=raw.parent/'frozen-grid-components-v1'
ct=json.loads(freeze(cp/'terminal.json','components-terminal.json'));assert ct['complete'] and ct['completed']==15 and ct['qualified']
assert json.loads(freeze(cp/'client-exit.json','components-client-exit.json'))['returncode']==0
manifest=json.loads(freeze(cp/'manifest.json','components-manifest.json'));locations={(x['k'],x['rep']):Path(x['raw']) for x in manifest}
assert len(locations)==15
cm=[];different=set()
for x in manifest:
 p=Path(x['raw']);q=json.loads(freeze(p/'result.json',p.name+'-result.json'));c=json.loads(freeze(p/'command.json',p.name+'-command.json'));ident=json.loads(freeze(p/'identity.json',p.name+'-identity.json'));text=freeze(p/'native.log',p.name+'-native.log').decode()
 assert q['returncode']==0 and q['retired'] and not q['stop_reasons'] and not live(ident['pid'],ident['birth'])
 assert c['pcore']=='0-7' and not any(a.startswith('-M') for a in c['argv'])
 k=x['k'];ph=[tuple(map(int,z)) for z in re.findall(r'^CK_KERNEL (\d+) (\d+) (\d+) (\d+)$',text,re.M)];assert len(ph)==max(k,1)
 if k:assert f'CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={k}' in text
 else:assert 'CK_ORIGINAL_AXIOMS [propext]' in text
 span=(max(z[2] for z in ph)-min(z[1] for z in ph))/1e9
 cm.append({'k':k,'rep':x['rep'],'span_s':span,'wall_s':q['wall_s']})
 artifacts=[p/'ChunkOriginal.olean'] if k==0 else [p/f'ChunkK{k}Part{i}.olean' for i in range(k)]+[p/'ChunkCombined.olean']
 for a in artifacts:
  ref=locations[(k,1)]/a.name
  if a.read_bytes()!=ref.read_bytes():different.add((str(ref),str(a)))
sem=raw/'runs/old-artifact-semantic-v2'
sr=json.loads(freeze(sem/'result.json','semantic-result.json'));assert sr['returncode']==0 and sr['native_retired'] and sr['cgroup_retired']
sv=[json.loads(x) for x in freeze(sem/'stdout','semantic-stdout').decode().splitlines()]
assert len(different)==len(sv)==27 and all(x['same_constants'] for x in sv)
assert {(x['a'],x['b']) for x in sv}==different
cms={str(k):{'kernel_span_s':statistics.median(x['span_s'] for x in cm if x['k']==k),'whole_native_s':statistics.median(x['wall_s'] for x in cm if x['k']==k)} for k in [0,1,2,4,8]}
j={'input_raw':str(raw),'completed_target_units':34,'timed_modules':31,'retained_probability_modules':29,'original_missing_draws':13,'source_scope':'module-local independent replay; declared imports trusted; not source compilation or full closure','decision_shape':'theorem value head after cleanupAnnotations is of_decide_eq_true; not every computational proof','all_native_call_CPU_s':total,'decision_call_CPU_s':decision,'large_decision_CPU_s':big,'large_decision_count':sum(x['large_decision_calls'] for x in summary),'unweighted_large_decision_share_all_calls':big/total,'unweighted_large_decision_share_decisions':big/decision,'weighted_available_case_share_all_calls':weighted_big/weighted_all,'weighted_available_case_share_decisions':weighted_big/weighted_dec,'all_large_native_call_CPU_s':sum(x['all_large_call_CPU_s'] for x in summary),'hot_observer_controls':hot,'max_wait4_RSS_KiB':maxrss,'max_charged_peak_bytes':maxcharged,'max_sampled_native_tree_bytes':maxsample,'charged_cap_GiB':14,'all_target_PIDbirths_and_cgroups_retired':True,'declaration_capture_controller_retired':True,'component_medians':cms,'component_unequal_byte_pairs':27,'component_typed_constant_pairs_equal':27,'root_analysis_s':time.monotonic()-begin,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'new_native_runs':0,'raw_stdout_metadata':rawmeta}
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print('COMPACT',json.dumps({k:v for k,v in j.items() if k not in ['raw_stdout_metadata','hot_observer_controls','component_medians']}))
print('MODULES',json.dumps([x for x in summary if any(z in x['module'] for z in ['Grid','UMoments9','BarrierData41','EnvelopePsiB','ResiduesModThree'])]))
print('COMPONENT_MEDIANS',cms)
