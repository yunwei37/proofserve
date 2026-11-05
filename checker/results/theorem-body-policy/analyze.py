#!/usr/bin/env python3
"""Reduce fixed replacement-policy qualification. No native task is launched."""
import argparse,json,csv,collections
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('raw',type=Path);args=a.parse_args()
D=args.raw;out=Path(__file__).resolve().parent
old=json.loads((out.parent/'pre-freeze-e1557c77/summary.json').read_text())
rows=[];reasons=[];comparison=[]
def load(p):return json.loads(p.read_text())
for dataset in ['nat','grid']:
    reference=next(r for r in old['rows'] if r['dataset']==dataset and r['source']=='3fe83c5a')
    strict=next(r for r in old['rows'] if r['dataset']==dataset and r['source']=='e1557c77')
    for label,r,policy in [('3fe-reference',reference,'historical reference'),('e155-strict-context',strict,'historical strict context strategy')]:
        rows.append(dict(dataset=dataset,source=label,policy=policy,modules=r['accepted'],axioms=r['declared_axioms'],
          module_local=r['whole_module_serial_replays'],segments=r['segments'],attempt_wall_s=r['attempt_wall_s'],
          actual_cpu_s=r['actual_attempt_cpu_s'],complete_segment_cpu_s=r['complete_segment_cpu_s'],
          peak_tree_gib=r['sampled_peak_rss_gib'],direct_duplicate_body_checks='not recorded',paper_eligible=False))
    receipt=load(D/(dataset+'-receipt.json'));run=load(D/'runs'/(dataset+'-default')/'result.json')
    assert receipt['status']=='complete' and receipt['theorem_body_policy']=='shared-checked'
    assert run['returncode']==0 and run['native_retired'] and run['cgroup_retired'] and not run['stop_reasons']
    state=D/(dataset+'-state');events=[]
    for p in state.glob('segment-*.json'):
        x=load(p);assert x['exit']==0;events.extend(x['events'])
    accept=[e for e in events if e.get('event')=='accept']
    local=[e for e in accept if e.get('context')=='module_local']
    assert len(local)==len({e['module'] for e in local})
    count=collections.Counter(e.get('fallback_reason','unknown').split(':',1)[0] for e in local)
    for reason,n in count.items():reasons.append(dict(dataset=dataset,reason=reason,modules=n))
    newrow=dict(dataset=dataset,source='replacement-shared-checked',policy=receipt['theorem_body_policy'],
      modules=len(receipt['accepted']),axioms=len(receipt['axioms']),module_local=len(local),
      segments=len(receipt['segments']),attempt_wall_s=json.dumps([run['wall_s']]),actual_cpu_s=run['cgroup_usage_s'],
      complete_segment_cpu_s=int(receipt['cumulative_segment_cpu_ns'])/1e9,peak_tree_gib=run['sampled_tree_peak_bytes']/1024**3,
      direct_duplicate_body_checks=sum(e.get('event')=='duplicate_theorem_body_checked' for e in events),paper_eligible=False)
    rows.append(newrow)
    prior=Path(old['raw'])
    prior_receipt=load(prior/(dataset+'-3fe-reference-receipt.json'))
    prior_strict=load(prior/(dataset+'-e155-receipt.json'))
    assert set(receipt['accepted'])==set(prior_receipt['accepted'])==set(prior_strict['accepted'])
    assert set(receipt['axioms'])==set(prior_receipt['axioms'])==set(prior_strict['axioms'])
    assert {e['module'] for e in accept}==set(receipt['accepted'])
    inputs=dict(load(state/'identity.json')['inputs'])
    old_inputs=dict(load(prior/(dataset+'-3fe-reference-state')/'identity.json')['inputs'])
    mismatches=[name for name,h in old_inputs.items() if inputs.get(name)!=h]
    assert not mismatches,mismatches
    assert newrow['module_local']<=reference['whole_module_serial_replays']*1.1
    comparison.append(dict(dataset=dataset,acceptance_equal=True,declared_axioms_equal=True,old_recorded_input_pairs=len(old_inputs),
      input_mismatches=mismatches,module_local_ratio=newrow['module_local']/reference['whole_module_serial_replays'],
      observed_cpu_ratio=newrow['actual_cpu_s']/reference['actual_attempt_cpu_s'],
      observed_wall_ratio=run['wall_s']/json.loads(reference['attempt_wall_s'])[0],
      caveat='one point per source under W background load; not final performance or isolated causal attribution'))
for name,data in [('closures.csv',rows),('fallback-reasons.csv',reasons)]:
    with (out/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
summary=dict(raw=str(D),comparison=comparison,rows=rows,baseline_raw=old['raw'],
  strict_remeasured=False,strict_note='Historical e155 context-isolation strategy only; new strict also explicitly validates skipped duplicate bodies, so old numbers are not exact timings of the new strict executable.',
  independent_execution_review=False,paper_eligible=False)
(out/'summary.json').write_text(json.dumps(summary,indent=2)+chr(10))
print(json.dumps(summary,indent=2))
