"""Reduce a retired corpus attempt; retain batch certification versus provisional events."""
from pathlib import Path
import csv,gzip,json,sys,datetime,collections
raw=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
launch=json.loads((raw/'controller.json').read_text())
p=Path('/proc',str(launch['pid']),'stat')
assert not p.exists()or p.read_text().rsplit(')',1)[1].split()[19]!=launch['birth']or p.read_text().rsplit(')',1)[1].split()[0]=='Z','collector still running'
state=raw/'whole-state';selected=set((raw/'whole-roots.txt').read_text().splitlines())
cfg=json.loads((raw/'workflow-config.json').read_text());deferred=set(Path(cfg['deferred_source_roots']).read_text().splitlines())
selection=json.loads((raw/'selection.json').read_text())
assert len(selected)==selection['requested_built_modules'] and len(deferred)==selection['deferred_source_modules'] and not(selected&deferred)
source=json.loads((raw/'frozen/source.json').read_text())
rows=[]
for f in sorted((raw/'runs').glob('*/result.json')):
 r=json.loads(f.read_text())
 assert r['native_retired']and r.get('cgroup_retired')and not Path(r['cgroup']).exists(),f
 rows.append(r)
assert rows and not [f for f in(raw/'runs').glob('*/command.json')if not(f.parent/'result.json').exists()]
result=next(r for r in rows if r['key'].startswith('whole-library-'))
assert result['affinity']==list(range(8))+list(range(10,24))
assert not any(str(v).startswith('-M')for v in result['argv'])
certified=set();provisional=set();seen=set();inflight=set();axioms=set();batch_rows=[];rejected=[]
segments=0
def validate(receipt):
 assert receipt['execution_path']=='proofserve-parallel'
 assert receipt['checker_binary_hash']==source['checker_binary_hash']
 assert receipt['lean_version'].startswith('Lean (version '+source['lean_version']+',')
 assert receipt['theorem_body_policy']=='shared-checked'
 assert len(receipt['accepted'])==len(set(receipt['accepted']))
for b in sorted(state.glob('batch-*')):
 cert=b/'certified.json';receipt=b/'receipt.json'
 cr=None;rr=None
 if cert.exists():
  j=json.loads(cert.read_text());cr=j['receipt'];validate(cr)
  assert cr['status']=='complete'
  assert set(j['input_identity']['roots'])<=set(cr['accepted'])
  certified.update(cr['accepted']);axioms.update(cr['axioms'])
 if receipt.exists():
  rr=json.loads(receipt.read_text());validate(rr);rejected.extend(rr.get('rejected',[]))
 for f in b.glob('segment-*.json'):
  j=json.loads(f.read_text())
  if j.get('exit')==0:segments+=1
  for e in j.get('events',[]):
   if 'module'in e:seen.add(e['module'])
   if e.get('event')=='accept':
    (provisional if j.get('exit')==0 else inflight).add(e['module'])
   if 'reject'in str(e.get('event','')).lower():rejected.append(dict(event=e,source=str(f)))
 for f in b.glob('segment-*.events'):
  if f.with_suffix('.json').exists():continue
  for line in f.read_text().splitlines():
   try:e=json.loads(line)
   except json.JSONDecodeError:continue
   if'module'in e:seen.add(e['module'])
   if e.get('event')=='accept':inflight.add(e['module'])
   if 'reject'in str(e.get('event','')).lower():rejected.append(dict(event=e,source=str(f)))
 if cr is not None or rr is not None:
  receipt_data=cr or rr
  batch_rows.append(dict(batch=b.name,outer_certified=cr is not None,status=receipt_data.get('status'),
    accepted_closure_modules=len(receipt_data['accepted']),accepted_requested_sources=len(set(receipt_data['accepted'])&selected),
    rejected_reports=len(receipt_data.get('rejected',[])),receipt=str(cert if cr is not None else receipt)))
top=state/'receipt.json'
top_complete=False
if result['returncode']==0 and top.exists():
 j=json.loads(top.read_text());validate(j)
 if j['status']=='complete':
  assert selected<=set(j['accepted'])
  certified.update(j['accepted']);axioms.update(j['axioms']);top_complete=True
# Confirm any rejection manually against native diagnostics before calling it a kernel failure.
if rejected:
 (out/'unclassified-rejection-diagnostics.json').write_text(json.dumps(rejected,indent=2)+'\n')
 raise RuntimeError('module rejection reports need explicit kernel/resource/tool classification')
accepted=certified&selected
provisional=(provisional&selected)-accepted
inflight=(inflight&selected)-accepted-provisional
attempted=(seen&selected)-accepted-provisional-inflight
unseen=selected-accepted-provisional-inflight-attempted
counts=dict(accepted_certified=len(accepted),complete_segment_accept_pending_batch=len(provisional),
 inflight_segment_accept_uncommitted=len(inflight),attempted_without_final_verdict=len(attempted),
 no_observed_module_verdict=len(unseen))
assert sum(counts.values())==len(selected)
def emit(name,rows):
 if not rows:return
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with(out/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
emit('batches.csv',batch_rows)
emit('accepted-requested-sources.csv',[dict(module=n,status='accepted_certified')for n in sorted(accepted)])
emit('source-status-counts.csv',[dict(status=k,modules=v)for k,v in counts.items()]+[
 dict(status='user_deferred_unbuilt',modules=len(deferred)),dict(status='configuration_excluded',modules=1)])
emit('native-cost.csv',[dict(native_commit=source['native_commit'],driver_commit=source['driver_commit'],workers=22,
 cpu_set='0-7,10-23',wall_s=result['wall_s'],cpu_s=result['cgroup_usage_s'],
 user_s=result['cgroup_user_s'],system_s=result['cgroup_system_s'],sampled_own_tree_rss_peak_bytes=result['sampled_tree_peak_bytes'],
 cgroup_charged_peak_bytes=result['charged_peak_bytes'],returncode=result['returncode'],stop_reasons=';'.join(result.get('stop_reasons',[])))])
status_sets=[('accepted_certified',accepted),('complete_segment_accept_pending_batch',provisional),
 ('inflight_segment_accept_uncommitted',inflight),('attempted_without_final_verdict',attempted),('no_observed_module_verdict',unseen),
 ('user_deferred_unbuilt',deferred),('configuration_excluded',{'lakefile'})]
with gzip.open(raw/'module-status-detailed.csv.gz','wt',newline='')as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['module','status'])
 for label,names in status_sets:
  for name in sorted(names):w.writerow([name,label])
summary=dict(native_commit=source['native_commit'],driver_commit=source['driver_commit'],native_binary_hash=source['checker_binary_hash'],
 request_built_modules=len(selected),source_frame_modules=163096,deferred_unbuilt_modules=len(deferred),configuration_units_excluded=1,
 accepted_certified_requested_sources=len(accepted),accepted_certified_closure_modules=len(certified),
 confirmed_kernel_rejected_modules=0,reported_rejection_diagnostics=0,
 not_certified_requested_sources=len(selected)-len(accepted),source_status_counts=counts,
 certified_batches=sum(r['outer_certified']for r in batch_rows),successful_native_segments=segments,
 complete_built_subset=top_complete,whole_source_corpus_complete=False,
 axioms=sorted(axioms),axiom_scope='declared inventory, not minimal used-axiom closure or sorry-free certificate',
 final_returncode=result['returncode'],stop_reasons=result.get('stop_reasons',[]),admission_events=result.get('admission_events',[]),
 termination_classification=('operational_deadline_timeout'if result['returncode']==124 and result.get('admission_events')else 'inspect_native_result'),
 native_process_and_cgroup_retired=True,
 raw=str(raw),per_module_status=str(raw/'module-status-detailed.csv.gz'),
 statement='Provisional segment events are not substituted for certified batch acceptance. No whole-corpus cost extrapolation.',
 reduced_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(out/'coverage.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'native-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(summary,indent=2))
