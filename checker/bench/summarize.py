"""Reduce a completed frozen matrix; failures remain visible,never imputed."""
import json,csv,re,statistics,sys
from pathlib import Path
def emit(path,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)

def preview(raw,out,cfg,rows):
 """Preview results are functional evidence,never final performance evidence."""
 identities={};accepted={};axioms={};hashes={};native=0
 for r in rows:
  r['evaluation_status']='nonfinal_preview_not_paper'
  r['paper_eligible']='false'
  if r['arm']=='native' and not r['manual_interruption'] and r['key']!='math-resume':
   assert r['returncode']==0
   j=json.loads((raw/(r['key']+'-receipt.json')).read_text())
   ident=json.loads((raw/r['key']/'identity.json').read_text())
   sig={k:ident[k]for k in ['inputs','manifest','roots']}
   d=r['dataset'];native+=1
   if d in accepted:
    assert accepted[d]==j['accepted']and axioms[d]==j['axioms']and hashes[d]==j['module_set_hash']
    assert identities[d]==sig
   else:
    accepted[d]=j['accepted'];axioms[d]=j['axioms'];hashes[d]=j['module_set_hash'];identities[d]=sig
  if r['arm']=='official':
   stderr=(raw/'runs'/r['key']/'stderr').read_text()
   r['outcome_class']='complete_root_control'if r['returncode']==0 else(
    'path_lookup_failure_before_kernel'if 'Could not find any oleans for:'in stderr else'official_failure_unclassified')
 bad=[r for r in rows if r['arm']=='bad-control']
 assert len(bad)==3
 for r in bad:
  text=(raw/'runs'/r['key']/'stdout').read_text()+(raw/'runs'/r['key']/'stderr').read_text()
  assert r['returncode']!=0 and ('kernel_reject:'in text or('while replaying declaration'in text and'(kernel)'in text))
  r['outcome_class']='original_kernel_rejection'
 kill=next(r for r in rows if r['key']=='math-interrupt')
 resumed=next(r for r in rows if r['key']=='math-resume')
 assert kill['manual_interruption']and kill['returncode']!=0 and resumed['returncode']==0
 j=json.loads((raw/'math-resume-receipt.json').read_text())
 assert j['accepted']==accepted['math']and j['axioms']==axioms['math']and j['module_set_hash']==hashes['math']
 assert any(part['reused']for part in j['segments'])
 full=next(r for r in rows if r['arm']=='full-math')
 assert full['returncode']==0
 f=json.loads((raw/(full['key']+'-receipt.json')).read_text())
 assert set(cfg['full_math_modules'])<=set(f['accepted'])
 full['resolved_workers']=f['workers']
 full['requested_source_modules']=len(cfg['full_math_modules'])
 full['directory_source_modules']=cfg['mathlib_directory_modules']
 full['includes_umbrella_module']=cfg['includes_umbrella_module']
 emit(out/'loaded-preview-cells.csv',rows)
 (out/'loaded-preview-qualification.json').write_text(json.dumps(dict(
  evaluation_status='nonfinal_preview_not_paper',executable_commit=cfg['commit'],
  completed_cells=len(rows),complete_native_preview_cells=native,
  within_dataset_artifacts_acceptance_axioms_and_hashes_equal=True,
  scope_counts={d:len(v)for d,v in accepted.items()},
  original_kernel_bad_proofs_rejected=len(bad),
  actual_interrupt_resume=dict(acceptance_equal=True,axioms_equal=True,module_hash_equal=True,
   reused_segments=sum(part['reused']for part in j['segments']),
   combined_wall_s=kill['wall_s']+resumed['wall_s'],combined_cpu_s=kill['cpu_s']+resumed['cpu_s'],
   paper_eligible=False),
  official_successful_root_controls=sum(r['arm']=='official'and r['returncode']==0 for r in rows),
  official_precheck_path_failures=sum(r.get('outcome_class')=='path_lookup_failure_before_kernel'for r in rows),
  full_mathlib=dict(requested_source_modules=len(cfg['full_math_modules']),
   directory_source_modules=cfg['mathlib_directory_modules'],umbrella_module=True,
   accepted_closure_modules=len(f['accepted']),segments=len(f['segments']),workers=f['workers'],
   wall_s=full['wall_s'],cpu_s=full['cpu_s'],
   sampled_tree_rss_peak_bytes=full['rss_sample_bytes'],
   cgroup_charged_peak_bytes=full['cgroup_charged_peak_bytes'],paper_eligible=False),
  final_matrix='not run; wait for census completion and quiet host'
 ),indent=2)+'\n')
 print('Preview reduced without creating any final-performance tables.')

def main():
 raw=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 is_preview='--preview'in sys.argv[3:]
 terminal=json.loads((raw/('preview-terminal.json'if is_preview else'terminal.json')).read_text());assert terminal['complete']
 cfg=json.loads(Path(terminal.get('configuration',str(raw/'config.json'))).read_text());rows=json.loads((raw/'completed.json').read_text())
 for r in rows:
  assert r['commit']==cfg['commit']
  n=json.loads((raw/'runs'/r['key']/'result.json').read_text())
  assert n['native_retired']and n['cgroup_retired']
  r['wait4_cpu_s']=r['cpu_s']
  # Abruptly killed parents cannot reap descendant CPU. The closed native cgroup
  # provides the same whole-tree CPU metric for successful and interrupted arms.
  assert 'cgroup_usage_s'in n
  r['cpu_s']=n['cgroup_usage_s'];r['cpu_source']='closed native cgroup'
  r['cpu_user_s']=n.get('cgroup_user_s');r['cpu_system_s']=n.get('cgroup_system_s')
  r['cgroup_charged_peak_bytes']=n['charged_peak_bytes']
 if is_preview:
  preview(raw,out,cfg,rows)
  return
 primary=[r for r in rows if re.fullmatch(r'(math|grid|barrier)-P[1248]-r[123]',r['key'])]
 assert len(primary)==36
 emit(out/'fixed-cells.csv',rows)
 identities={};accepts={};axioms={};module_hashes={}
 for r in primary+[r for r in rows if '-no-persistence-'in r['key']or'-no-split-fallback-'in r['key']]:
  assert r['returncode']==0
  receipt=json.loads((raw/(r['key']+'-receipt.json')).read_text())
  identity=json.loads((raw/r['key']/'identity.json').read_text())
  sig=dict(inputs=identity['inputs'],manifest=identity['manifest'],roots=identity['roots'])
  if r['dataset']in identities:
   assert identities[r['dataset']]==sig,'input artifact identity changed'
   assert accepts[r['dataset']]==receipt['accepted']
   assert axioms[r['dataset']]==receipt['axioms']
   assert module_hashes[r['dataset']]==receipt['module_set_hash']
  else:
   identities[r['dataset']]=sig;accepts[r['dataset']]=receipt['accepted']
   axioms[r['dataset']]=receipt['axioms'];module_hashes[r['dataset']]=receipt['module_set_hash']
 summary=[]
 for dataset in ['math','grid','barrier']:
  for arm in ['native','no-persistence','no-split-fallback']:
   if arm!='native'and dataset=='barrier':continue
   ns=[1,2,4,8]if arm=='native'else[8]
   for n in ns:
    prefix=dataset+'-P'+str(n)+('-'+arm if arm!='native'else'')+'-r'
    g=[r for r in rows if r['key'].startswith(prefix)]
    assert len(g)==3 and all(r['returncode']==0 for r in g)
    s=dict(dataset=dataset,arm=arm,workers=n,repeats=3,modules=g[0]['modules'],commit=cfg['commit'])
    for metric in ['wall_s','cpu_s','peak_rss_kib','rss_sample_bytes','cgroup_charged_peak_bytes']:
     z=[r[metric]for r in g];s.update({metric+'_median':statistics.median(z),metric+'_min':min(z),metric+'_max':max(z)})
    summary.append(s)
 for s in summary:
  baseline=next(x for x in summary if x['dataset']==s['dataset']and x['arm']=='native'and x['workers']==1)
  s['native_1worker_wall_ratio']=baseline['wall_s_median']/s['wall_s_median']
 emit(out/'fixed-native-summary.csv',summary)
 official=[]
 for dataset in ['math','grid','barrier']:
  for mode in ['default','fresh']:
   g=[r for r in rows if r['key'].startswith(dataset+'-official-'+mode+'-')]
   assert len(g)==3
   s=dict(dataset=dataset,mode=mode,complete_runs=sum(r['returncode']==0 for r in g),planned_runs=3,
     scope='leaf with trusted imports'if mode=='default'else'final imported map,not per-input proof ledger',
     native_speedup='not computed: different proof ledger')
   if len(g)==s['complete_runs']:
    for metric in ['wall_s','cpu_s','rss_sample_bytes','cgroup_charged_peak_bytes']:
     z=[r[metric]for r in g];s.update({metric+'_median':statistics.median(z),metric+'_min':min(z),metric+'_max':max(z)})
   official.append(s)
 emit(out/'fixed-official-summary.csv',official)
 bad=[r for r in rows if r['arm']=='bad-control'];assert len(bad)==3 and all(r['returncode']!=0 for r in bad)
 kill=next(r for r in rows if r['key']=='math-interrupt');resume=next(r for r in rows if r['key']=='math-resume')
 assert kill['manual_interruption']and resume['returncode']==0
 j=json.loads((raw/'math-resume-receipt.json').read_text());assert j['accepted']==accepts['math']
 assert j['axioms']==axioms['math']and j['module_set_hash']==module_hashes['math']
 assert any(s['reused']for s in j['segments']),'interruption must reuse a certified segment'
 base=next(s for s in summary if s['dataset']=='math'and s['workers']==4 and s['arm']=='native')
 interruption=dict(accepted_equal=True,axioms_equal=True,module_set_hash_equal=True,
  reused_segments=sum(s['reused']for s in j['segments']),wall_s=kill['wall_s']+resume['wall_s'],cpu_s=kill['cpu_s']+resume['cpu_s'],
  uninterrupted_wall_median_s=base['wall_s_median'],uninterrupted_cpu_median_s=base['cpu_s_median'])
 interruption['wall_overhead_fraction']=interruption['wall_s']/base['wall_s_median']-1
 (out/'fixed-resume.json').write_text(json.dumps(interruption,indent=2))
 full=[dict(r)for r in rows if r['arm']=='full-math']
 for r in full:
  r['requested_source_modules']=len(cfg['full_math_modules'])
  r['directory_source_modules']=cfg.get('mathlib_directory_modules',len(cfg['full_math_modules']))
  r['includes_umbrella_module']=cfg.get('includes_umbrella_module',False)
  states=raw/('full-math-quota'+('100'if '100'in r['key']else'500'))
  records=[json.loads(f.read_text())for f in states.glob('segment-*.json')]
  r['completed_segments']=sum(j.get('exit')==0 for j in records)
  r['completed_prefix_modules']=sum(sum(e.get('event')=='accept'for e in j.get('events',[]))for j in records if j.get('exit')==0)
  if r['returncode']==0:
   j=json.loads((raw/(r['key']+'-receipt.json')).read_text())
   assert set(cfg['full_math_modules'])<=set(j['accepted'])
   r['resolved_workers']=j['workers']
  else:r['resolved_workers']=None
 emit(out/'fixed-full-mathlib.csv',full)
 (out/'fixed-acceptance.json').write_text(json.dumps(dict(complete_native_points=48,
  within_dataset_module_sets_equal=True,within_dataset_axiom_sets_equal=True,
  within_dataset_module_set_hashes_equal=True,within_dataset_artifact_identities_equal=True,
  bad_original_kernel_rejections=3,actual_interruption_resume_equal=True,
  official_whole_ledger_equivalence='not established',scope_counts={d:len(v)for d,v in accepts.items()}),indent=2))
 print(json.dumps(dict(native=summary,official=official,resume=interruption,full=full),indent=2))
if __name__=='__main__':main()
