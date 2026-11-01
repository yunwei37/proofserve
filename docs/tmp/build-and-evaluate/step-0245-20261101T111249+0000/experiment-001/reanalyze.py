from pathlib import Path
import os,json,gzip,time,resource,csv,subprocess,datetime
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0245-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-envelope-timeout-paper-step.txt').write_text(str(s)+'\n')
def freeze(p,name):
 raw=Path(p).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(raw,mtime=0));return raw
def live(pid,birth):
 p=Path('/proc')/str(pid)/'stat'
 try:return p.read_text().rsplit(')',1)[1].split()[19]==str(birth)
 except FileNotFoundError:return False
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14');d=b/'runs/envelope-full-reference1-r1'
for f in ['result.json','command.json','stdout','stderr','memory.jsonl']:freeze(d/f,'native-'+f)
for f in ['envelope-full-reference-launch.json','envelope-reference-1-1-1680-terminal.json','envelope-full-reference1-r1-summary.json','envelope-full-reference-controller.log','full.py','native.py']:
 freeze(b/f,'raw-'+f)
z=json.loads((d/'result.json').read_text());cmd=json.loads((d/'command.json').read_text());launch=json.loads((b/'envelope-full-reference-launch.json').read_text())
assert z['argv']==cmd['argv'] and z['returncode']==124 and z['native_retired'] and z['cgroup_retired']
assert z['wall_limit_s']==1680 and 1680<=z['wall_s']<1685 and z['affinity']==list(range(8))
assert z['cgroup_charged_memory_max_gib']==14 and z['own_rss_sample_stop_gib']==14 and not any(x.startswith('-M')for x in z['argv'])
assert not live(z['pid'],z['birth']) and not live(launch['pid'],launch['birth']) and not Path(z['cgroup']).exists()
assert not z['stop_reasons'] and all(int(x.split()[1])==0 for x in z['memory_events'].splitlines())
assert z['charged_peak_bytes']<14*1024**3 and z['sampled_tree_peak_bytes']<14*1024**3
members=set();samples=[json.loads(x)for x in(d/'memory.jsonl').read_text().splitlines()]
for sample in samples:
 for proc in sample['processes']:
  members.add((proc['pid'],proc['birth']))
assert members and all(not live(*x)for x in members)
assert max(x['rss_bytes']for x in samples)==z['sampled_tree_peak_bytes']
events=[];fragments=[]
for i,line in enumerate((d/'stdout').read_text().splitlines(),1):
 try:events.append(json.loads(line))
 except json.JSONDecodeError:fragments.append((i,line))
assert len(fragments)==1 and fragments[0][0]==10745 and len(fragments[0][1])==222
assert not (d/'stdout').read_bytes().endswith(b'\n') and not (d/'stderr').read_bytes()
assert all(x.get('event')=='accept'for x in events)
ids=[x['module']for x in events];assert len(ids)==len(set(ids))==10744
old=json.loads((b/'envelope-stream-r1-summary.json').read_text());expected=set(old['accepted'])
assert len(expected)==10752 and set(ids)<expected
missing=sorted(expected-set(ids));assert len(missing)==8 and z['argv'][-1] in missing
summary=json.loads((b/'envelope-full-reference1-r1-summary.json').read_text())
assert summary['accepted']==ids and not summary['completed'] and summary['complete_event'] is None
assert not summary['accepted_set_equal_to_same_input_curve']
assert not summary['chunk_rewrite_enabled']
# The truncated acceptance record is evidence of partial output only, not a complete accepted module.
(e/'trailing-stdout-fragment.txt').write_text(fragments[0][1])
with(e/'unobserved-complete-acceptance-IDs.csv').open('w',newline='')as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['module','status'])
 w.writerows((n,'no_complete_acceptance_record_before_timeout')for n in missing)
with(e/'terminal-cost.csv').open('w',newline='')as f:
 cols=['returncode','wall_s','user_s','system_s','cgroup_usage_s','peak_rss_kib','sampled_tree_peak_bytes','charged_peak_bytes']
 w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerow({k:z[k]for k in cols})
j=dict(outcome='native_wall_timeout',returncode=124,native_limit_s=1680,wall_s=z['wall_s'],wait4_CPU_s=z['user_s']+z['system_s'],cgroup_CPU_s=z['cgroup_usage_s'],CPU_ledger_difference_s=abs(z['cgroup_usage_s']-z['user_s']-z['system_s']),complete_accept_records=10744,expected_modules=10752,missing_complete_accept_IDs=missing,trailing_partial_line_bytes=222,complete_event=False,explicit_native_rejection_observed=False,complete_parity='not established; incomplete output',speedup='unknown; no completed single-configuration pair',native_memory_budget_stop=False,kernel_OOM=False,sampled_RSS_bytes=z['sampled_tree_peak_bytes'],wait4_maxRSS_KiB=z['peak_rss_kib'],charged_peak_bytes=z['charged_peak_bytes'],sampled_members=sorted(members),all_sampled_members_controller_and_cgroup_retired=True,clock='Popen-to-wait4; post-wait sampler/cgroup cleanup outside clock',root_new_native_runs=0,root_analysis_s=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'step':str(s),**j},indent=2))
