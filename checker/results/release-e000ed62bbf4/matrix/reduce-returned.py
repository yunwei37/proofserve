"""Reduce all returned final cells, preserving incomplete planned points explicitly."""
from pathlib import Path
import csv,json,re,statistics,sys,importlib.util
raw=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
end=json.loads((raw/'matrix-collection-handoff.json').read_text())
assert end['handoff_ready'],end
pid=json.loads((raw/'continuation-2-controller.json').read_text())['pid']
assert not Path('/proc',str(pid)).exists(),'wait for collector retirement'
spec=importlib.util.spec_from_file_location('frozen_summary',raw/'frozen/bench/summarize.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=json.loads((raw/'completed.json').read_text())
plan=json.loads((raw/'planned-cells.json').read_text())
def emit(name,rs):
 keys=list(dict.fromkeys(k for r in rs for k in r))
 with(out/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rs)
for r in rows:
 n=json.loads((raw/'runs'/r.get('run_key',r['key'])/'result.json').read_text())
 assert n['native_retired']and n['cgroup_retired']
 assert not Path(n['cgroup']).exists()
 assert n['affinity']==list(range(8))and n['measured']
 assert not any(str(v).startswith('-M')for v in n['argv'])
 r['wait4_cpu_s']=r['cpu_s'];r['cpu_s']=n['cgroup_usage_s']
 r['cpu_user_s']=n['cgroup_user_s'];r['cpu_system_s']=n['cgroup_system_s']
 r['cpu_source']='closed native cgroup'
 r['cgroup_charged_peak_bytes']=n['charged_peak_bytes']
 if r['manual_interruption']:r['outcome']='intentional_interruption'
 elif r['arm']=='bad-control':
  text=(raw/'runs'/r['run_key']/'stdout').read_text()+(raw/'runs'/r['run_key']/'stderr').read_text()
  assert r['returncode']!=0 and('kernel_reject:'in text or('while replaying declaration'in text and'(kernel)'in text))
  assert 'Mathlib.Data.Nat.Basic'in text
  r['outcome']='original_kernel_rejection'
 elif r['returncode']==124:r['outcome']=('six_hour_budget_stop_not_kernel_rejection'if n['wall_limit_s']<1800 else'per_cell_wall_timeout_not_kernel_rejection')
 elif r['returncode']==0:r['outcome']='complete'
 else:r['outcome']='failure_requires_classification'
emit('fixed-cells.csv',rows)
emit('fixed-failed-attempts.csv',[r for r in rows if r['returncode']!=0 and not r['manual_interruption']and r['arm']!='bad-control'])
by={r['key']:r for r in rows}
statuses=[]
for c in plan:
 row=dict(c);row['flags']=' '.join(c.get('flags',[]))
 if c['key']in by:
  r=by[c['key']];row.update(status=r['outcome'],returncode=r['returncode'],wall_s=r['wall_s'],cpu_s=r['cpu_s'])
 else:row.update(status='not_run',reason=next(x['reason']for x in end['unattempted']if x['key']==c['key']))
 statuses.append(row)
emit('planned-status.csv',statuses)
refs={};native=[]
for r in rows:
 if r['arm']!='native'or r['returncode']!=0:continue
 j=json.loads((raw/(r['key']+'-receipt.json')).read_text())
 assert j['status']=='complete'and j['execution_path']=='proofserve-parallel'
 assert j['checker_binary_hash']=='14707787067517532260'
 sig=mod.artifact_identity(Path(r['state_directory']))
 d=r['dataset'];value=(j['accepted'],j['axioms'],j['module_set_hash'],sig)
 if d in refs:assert refs[d]==value,(d,r['key'])
 else:refs[d]=value
 native.append(r)
summary=[]
for d in ['math','grid','barrier']:
 for arm in ['native','no-persistence','no-split-fallback','strict-theorem-bodies']:
  if d=='barrier'and arm!='native':continue
  ns=([1,8]if d=='barrier'else[1,2,4,8])if arm=='native'else[8]
  for n in ns:
   prefix=d+'-P'+str(n)+(''if arm=='native'else'-'+arm)+'-r'
   planned=[c for c in plan if c['key'].startswith(prefix)]
   returned=[r for r in rows if r['key'].startswith(prefix)]
   good=[r for r in returned if r['returncode']==0]
   s=dict(dataset=d,arm=arm,workers=n,planned_repeats=len(planned),complete_repeats=len(good),
    status='complete'if len(good)==len(planned)else'incomplete',
    repeats=len(good),modules=len(refs[d][0]),commit='e000ed62bbf4b9c420bd99d0273a5d21829b4edc',native_commit='e000ed62bbf4b9c420bd99d0273a5d21829b4edc')
   if len(good)==len(planned):
    for metric in ['wall_s','cpu_s','peak_rss_kib','rss_sample_bytes','cgroup_charged_peak_bytes']:
     z=[r[metric]for r in good]
     s.update({metric+'_median':statistics.median(z),metric+'_min':min(z),metric+'_max':max(z)})
   else:
    s['timeout_attempts']=sum(r['returncode']==124 for r in returned)
    s['unattempted']=len(planned)-len(returned)
    s['wall_timeout_s']=next((r['wall_s']for r in returned if r['returncode']==124),None)
    s['median']='not estimable: no completed strict Grid repeat'
   summary.append(s)
for s in summary:
 if s['status']!='complete':continue
 base=next(x for x in summary if x['dataset']==s['dataset']and x['arm']=='native'and x['workers']==1)
 p8=next(x for x in summary if x['dataset']==s['dataset']and x['arm']=='native'and x['workers']==8)
 s['native_1worker_wall_ratio']=base['wall_s_median']/s['wall_s_median']
 s['relative_to_default_8_wall']=s['wall_s_median']/p8['wall_s_median']
 s['relative_to_default_8_cpu']=s['cpu_s_median']/p8['cpu_s_median']
emit('fixed-native-summary.csv',[s for s in summary if s['status']=='complete'])
emit('fixed-incomplete-native-points.csv',[s for s in summary if s['status']!='complete'])
official=[]
for d in ['math','grid','barrier']:
 for mode in ['default','fresh']:
  group=[r for r in rows if r['key'].startswith(d+'-official-'+mode+'-')]
  g=[r for r in group if r['returncode']==0]
  s=dict(dataset=d,mode=mode,planned_repeats=3,returned_repeats=len(group),complete_repeats=len(g),planned_runs=3,complete_runs=len(g),status='complete'if len(g)==3 else'incomplete',
   scope='root with trusted imports'if mode=='default'else'final imported constant map; not a per-input proof-body ledger',
   native_speedup='not computed: different proof ledger and full-search-path discovery included',native_whole_ledger_speedup='not comparable')
  if len(g)==3:
   for metric in ['wall_s','cpu_s','peak_rss_kib','rss_sample_bytes','cgroup_charged_peak_bytes']:
    z=[r[metric]for r in g];s.update({metric+'_median':statistics.median(z),metric+'_min':min(z),metric+'_max':max(z)})
  official.append(s)
emit('fixed-official-summary.csv',official)
kill=by['math-interrupt'];resume=by['math-resume']
assert kill['manual_interruption']and kill['returncode']!=0 and resume['returncode']==0
j=json.loads((raw/'math-resume-receipt.json').read_text())
assert any(s['reused']for s in j['segments'])
base=next(s for s in summary if s['dataset']=='math'and s['arm']=='native'and s['workers']==4)
rr=dict(accepted_equal=True,axioms_equal=True,module_set_hash_equal=True,artifact_identity_equal=True,
 reused_segments=sum(s['reused']for s in j['segments']),
 interrupted_returncode=kill['returncode'],resumed_returncode=resume['returncode'],
 wall_s=kill['wall_s']+resume['wall_s'],cpu_s=kill['cpu_s']+resume['cpu_s'],
 uninterrupted_wall_median_s=base['wall_s_median'],uninterrupted_cpu_median_s=base['cpu_s_median'])
rr['wall_overhead_fraction']=rr['wall_s']/base['wall_s_median']-1
rr['cpu_overhead_fraction']=rr['cpu_s']/base['cpu_s_median']-1
(out/'fixed-resume.json').write_text(json.dumps(rr,indent=2)+'\n')
accept=dict(native_commit='e000ed62bbf4b9c420bd99d0273a5d21829b4edc',
 driver_commit=json.loads((raw/'controller.json').read_text())['driver_commit'],
 checker_binary_hash='14707787067517532260',original_planned_cells=len(plan),returned_cells=len(rows),
 all_original_cells_complete=False,complete_native_fixed_points=len(native)-1,
 within_dataset_artifact_identities_acceptance_axioms_and_module_hashes_equal=True,
 within_dataset_module_sets_equal=True,within_dataset_axiom_sets_equal=True,within_dataset_module_set_hashes_equal=True,within_dataset_artifact_identities_equal=True,
 actual_interruption_resume_equal=True,complete_native_points=len(native)-1,
 axiom_inventory_scope='Declared axioms observed in the checked closures, including sorryAx and compiler axioms; not a minimal used-axiom closure or sorry-free certification',
 scope_counts={d:len(v[0])for d,v in refs.items()},axioms={d:v[1]for d,v in refs.items()},
 bad_original_kernel_rejections=sum(r['outcome']=='original_kernel_rejection'for r in rows),
 official_whole_ledger_equivalence='not established',strict_grid='one 1800s timeout, two unattempted; no strict Grid median',
 raw=str(raw),background='Protected zettai-dev retained; approximately one P-core of host background observed before launch; no study Workspace compilation.',
 measurement_affinity=list(range(8)),lean_M_used=False)
assert accept['bad_original_kernel_rejections']==3
(out/'fixed-acceptance.json').write_text(json.dumps(accept,indent=2)+'\n')
for f in end['failures']:
 f.update({k:by[f['key']][k]for k in ['cpu_s','wait4_cpu_s','cpu_source','outcome']})
(out/'collection-terminal.json').write_text(json.dumps(end,indent=2)+'\n')
print(json.dumps(dict(summary=summary,official=official,resume=rr,acceptance=accept),indent=2))
