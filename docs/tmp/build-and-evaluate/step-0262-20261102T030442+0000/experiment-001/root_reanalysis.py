from pathlib import Path
import os,json,collections,statistics,time,datetime,subprocess,gzip,tarfile,csv,resource,math
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0262-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));e=s/'experiment-001';e.mkdir(parents=True);Path('/workspaces/.agent-state/gpu-smt-census-root-step.txt').write_text(str(s))
b=Path('/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v12');t=json.loads((b/'census-terminal.json').read_text());launch=json.loads((b/'census-launch.json').read_text());assert t['state']=='complete'and not t['errors']and len(t['cells'])==36 and t['repeats']==[0,1,2]
ids=set();freeze=set();data={};units=collections.defaultdict(list);cells=[]
def retire(pid,birth):
 p=Path('/proc')/str(pid);assert not p.exists()or p.joinpath('stat').read_text().rsplit(')',1)[1].split()[19]!=str(birth);ids.add((int(pid),str(birth)))
retire(launch['pid'],launch['birth'])
for q in t['cells']:
 p=b/'runs'/q['key'];assert q==json.loads((p/'result.json').read_text())and q['returncode']==0 and q['wait4_usage_complete']and not q['stop_reasons']and q['affinity']==list(range(8))and q['cgroup_charged_memory_max_gib']==14
 assert not any(str(x).startswith('-M')for x in q['argv'])and not Path(q['cgroup']).exists()
 assert all(int(l.split()[1])==0 for l in q['memory_events'].splitlines()if l.split()[0].startswith('oom'))
 retire(q['pid'],q['birth'])
 for l in(p/'memory.jsonl').open():
  for z in json.loads(l).get('processes',[]):retire(z['pid'],z['birth'])
 rows=[json.loads(l[7:])for l in(p/'stdout').open()if l.startswith('KERNEL ')];short=rows[0]['module'].split('.')[-1];n=t['expected'][short];assert len(rows)==n and len({x['result']['target']for x in rows})==n
 vals={}
 for x in rows:
  z=x['result'];assert x['selected']==x['eligible']==n and x['kernel_poll_count']is None and z['verdict']=='accepted'and z['error']==''
  assert int(z['cpuNS'])<=int(z['wallNS'])*1.1+1000000
  vals[z['target']]=z;units[short,z['target']].append((x['workers'],z['rawHB'],int(z['cpuNS']),z['tid']))
 data[q['key']]=vals
 cells.append({'module':short,'key':q['key'],'workers':rows[0]['workers'],'rows':n,'active_TIDs':len({z['tid']for z in vals.values()}),'summed_unit_thread_CPU_s':sum(int(z['cpuNS'])for z in vals.values())/1e9,'native_wall_s':q['wall_s'],'native_wait4_CPU_s':q['user_s']+q['system_s'],'cgroup_CPU_s':q['cgroup_usage_s'],'wait4_peak_RSS_KiB':q['peak_rss_kib'],'sampled_RSS_B':q['sampled_tree_peak_bytes'],'charged_peak_B':q['charged_peak_bytes']})
 freeze.update(x for x in p.iterdir()if x.is_file())
assert len(units)==2524 and sum(len(x)for x in units.values())==30288 and all(len(x)==12 for x in units.values())
pairs=0;changed=0;verdict=0;diagnostic=0;ranges=[];summary=[]
for short,n in t['expected'].items():
 keys=set(data[f'kernel-{short}-r0-j1']);assert len(keys)==n
 for rep in [0,1,2]:
  base=data[f'kernel-{short}-r{rep}-j1']
  for workers in [1,2,4,8]:
   cur=data[f'kernel-{short}-r{rep}-j{workers}'];assert set(cur)==keys
   if workers==1:continue
   for name,a in base.items():
    z=cur[name];pairs+=1;changed+=a['rawHB']!=z['rawHB'];verdict+=a['verdict']!=z['verdict'];diagnostic+=a['error']!=z['error']
 for name in sorted(keys):
  v=units[short,name];counts=[x[1]for x in v]
  ranges.append({'module':short,'target':name,'observations':12,'min_raw_HB':min(counts),'max_raw_HB':max(counts),'range_percent':100*(max(counts)/min(counts)-1),'unit_thread_CPU_min_s':min(x[2]for x in v)/1e9,'unit_thread_CPU_max_s':max(x[2]for x in v)/1e9})
 c=[x for x in cells if x['module']==short]
 summary.append({'module':short,'eligible_local_helpers':n,'observations':12*n,'j1_vs_higher_pairs':9*n,'changed_allocation_targets':sum(x['min_raw_HB']!=x['max_raw_HB']for x in ranges if x['module']==short),'max_observed_allocation_range_percent':max(x['range_percent']for x in ranges if x['module']==short),'active_TID_counts':{str(k):sorted({x['active_TIDs']for x in c if x['workers']==k})for k in [1,2,4,8]},'unit_CPU_medians':{str(k):statistics.median(x['summed_unit_thread_CPU_s']for x in c if x['workers']==k)for k in [1,2,4,8]}})
assert pairs==22716 and changed==verdict==diagnostic==0 and all(x['range_percent']==0 for x in ranges)
# Exact three input artifacts, with existing frozen import path and original producer references.
runtime=json.loads((b/'runtime.json').read_text());mods=json.loads((b/'modules.json').read_text());inputs=[]
for m in mods:
 if m['regime']!='computation':continue
 rel=Path(*m['module'].split('.')).with_suffix('.olean');actual=next(Path(p)/rel for p in runtime['LEAN_PATH'].split(':')if(Path(p)/rel).exists());orig=Path(m['path'])
 assert actual.read_bytes()==orig.read_bytes()
 inputs.append({'module':m['module'],'resolved':str(actual),'original':str(orig),'bytes':orig.stat().st_size,'byte_equal':True})
assert len(inputs)==3
source=(b/'AllHelpers.lean').read_text();prior=Path('/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v11/ModuleProbe.lean').read_text()
for marker,end in [('structure UnitRow','partial def commands'),('partial def commands','unsafe def main')]:
 assert source[source.index(marker):source.index(end)]==prior[prior.index(marker):prior.index(end)]
assert 'let count := candidates.size'in source and 'env.getModuleIdxFor? n == some modIdx'in source and 'cleanupAnnotations.getAppFn.isConstOf 'in source
assert 'base.addDeclCore 2000000000 20000 decl none'in source and '@[noinline] def checked'in source
assert json.loads((b/'build-terminal.json').read_text())['complete']
for p in b.iterdir():
 if p.is_file()and p.suffix in ['.json','.py','.lean','.c','.log']:freeze.add(p)
freeze.add(r/'research/reproducible-verdict/all-helper-census-plan.md');freeze.add(r/'research/reproducible-verdict/step-014-report.md')
with tarfile.open(e/'census-native-source-and-terminal-records.tar.gz','w:gz')as tf:
 for p in sorted(freeze):tf.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
for name,rows in [('module-summary',summary),('unit-count-ranges',ranges),('native-cells',cells)]:
 with(e/(name+'.csv')).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
j={'native_phases':36,'modules':3,'eligible_helpers':2524,'observations':30288,'j1_vs_higher_pairs':pairs,'changed_allocation_pairs':changed,'changed_allocation_targets':0,'verdict_differences':verdict,'diagnostic_differences':diagnostic,'summary':summary,'inputs':inputs,'controller':launch,'retired_identity_count':len(ids),'retired_identities':sorted(ids),'whole_controller_wall_s':t['wall_s'],'native_wall_sum_s':sum(q['wall_s']for q in t['cells']),'max_wait4_RSS_KiB':max(q['peak_rss_kib']for q in t['cells']),'max_sampled_RSS_B':max(q['sampled_tree_peak_bytes']for q in t['cells']),'max_charged_memory_B':max(q['charged_peak_bytes']for q in t['cells']),'kernel_poll_counter':'null/unmeasured','context':'full original target imported and trusted, fresh renamed closed stored proof','new_root_native':0,'root_analysis_seconds':time.monotonic()-start,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
for n in ['docs/paper/main.tex','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md']:(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
print('STEP',s);print(json.dumps({k:v for k,v in j.items()if k not in ['retired_identities','inputs','controller']}))
