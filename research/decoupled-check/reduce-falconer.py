#!/usr/bin/env python3
"""Reduce only observed exact-artifact source work and finalized native cells."""
import json,csv,re
from pathlib import Path
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
ROOT=BASE/'scale-study/falconer-project-20261101'
REPO=Path('/workspaces/repository/research/decoupled-check')
def read_rows(file):
 return [json.loads(x)for x in file.read_text().splitlines()]if file.exists()else[]
def main():
 if not(ROOT/'progress.json').exists():return
 state=json.loads((ROOT/'progress.json').read_text());frame=json.loads((ROOT/'build-frame.json').read_text())
 old=read_rows(BASE/'measured.jsonl');new=read_rows(ROOT/'measured.jsonl')
 old_build={r['module']:r for r in old if r.get('operation')=='build'and not r['returncode']and not r.get('sorry_warning')}
 new_build={r['module']:r for r in new if r.get('operation')=='build'and not r['returncode']and not r.get('sorry_warning')}
 rows=[]
 for module in [r['module']for r in frame]:
  reused=module in state['reused'];cell=old_build.get(module)if reused else new_build.get(module)
  if cell:rows.append(dict(module=module,source_cell=cell['key'],source_cell_root=str(BASE if reused else ROOT),
   reused_exact_artifact=reused,source_compiler_wall_s=cell['wall_s'],source_user_s=cell['user_s'],source_system_s=cell['system_s'],source_peak_rss_kib=cell['peak_rss_kib']))
 def csvwrite(name,rows):
  if not rows:return
  dest=REPO/name;pending=dest.with_suffix('.pending')
  with pending.open('w',newline='')as f:
   w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
  pending.replace(dest)
 csvwrite('falconer-source-costs.csv',rows)
 construction_complete=len(rows)==len(frame)
 total=sum(r['source_compiler_wall_s']for r in rows)
 primary=next((r for r in new if r.get('operation')=='primary'and r.get('closure_complete')),None)
 parity=bool(state.get('complete'))
 ratio=primary['wall_s']/total if primary and construction_complete and parity else None
 summary=dict(closure_modules=len(frame),successful_source_nodes=len(rows),construction_complete=construction_complete,
  reused_same_capture_nodes=sum(r['reused_exact_artifact']for r in rows),source_compiler_wall_s=total,
  matched_stream_wall_s=primary['wall_s']if primary else None,acceptance_parity_complete=parity,
  finalized_check_over_source_ratio=ratio,module_local_fallbacks=None,
  status='complete'if parity else'partial',failure=state.get('failure'))
 if primary:
  es=read_rows(ROOT/(primary['key']+'.stdout'))
  summary['module_local_fallbacks']=next((e['module_local_fallbacks']for e in reversed(es)if e.get('event')=='complete'),None)
 if state.get('memory_profile'):
  memory=[]
  for e in read_rows(ROOT/(state['memory_profile']+'.stdout')):
   if e.get('event')!='memory_checkpoint':continue
   row=dict(modules=e['modules'],input_entries=e['input_entries'],
    checked_shared_declarations=e['shared_kernel_declarations'],eligible_input_entries=e['processed_eligible_entries'],
    module_local_checks=e['module_local_checks'])
   found=re.search(r'^VmHWM:\s+(\d+) kB$',e['process_status'],re.M)
   row['peak_rss_kib']=int(found.group(1))if found else None
   for k in ['Rss','Pss','Shared_Clean','Shared_Dirty','Private_Clean','Private_Dirty']:
    found=re.search('^'+k+':\\s+(\\d+) kB$',e['smaps_rollup'],re.M)
    row[k.lower()+'_kib']=int(found.group(1))if found else None
   memory.append(row)
  csvwrite('falconer-memory-curve.csv',memory)
  # Measured one-process peak-RSS trend; extrapolations are explicitly conditional.
  xs=[float(r['checked_shared_declarations'])for r in memory if r['peak_rss_kib']is not None]
  ys=[float(r['peak_rss_kib'])for r in memory if r['peak_rss_kib']is not None]
  if len(xs)>2 and max(xs)>min(xs):
   xbar=sum(xs)/len(xs);ybar=sum(ys)/len(ys)
   b=sum((x-xbar)*(y-ybar)for x,y in zip(xs,ys))/sum((x-xbar)**2 for x in xs);a=ybar-b*xbar
   residuals=[y-(a+b*x)for x,y in zip(xs,ys)]
   ss=sum((y-ybar)**2 for y in ys)
   fit=dict(points=len(xs),n_min=min(xs),n_max=max(xs),intercept_kib=a,kib_per_shared_declaration=b,
    r_squared=1-sum(r*r for r in residuals)/ss if ss else None,max_abs_residual_kib=max(map(abs,residuals)),
    scope='within-run VmHWM trend with mapped modules and audit state; not a causal per-declaration law or population bound')
   (ROOT/'memory-fit.json').write_text(json.dumps(fit,indent=2));csvwrite('falconer-memory-fit.csv',[fit])
   lexical=json.loads((ROOT.parent/'falconer-plan.json').read_text())
   remaining=lexical['whole_source_metrics']['lemma_theorem_declarations']-lexical['source_metrics']['lemma_theorem_declarations']
   final_n=xs[-1];scenarios=[]
   for factor in [1,2,4,8]:
    n=final_n+factor*remaining
    scenarios.append(dict(assumed_new_unique_declarations_per_remaining_source_theorem=factor,
     measured_falconer_closure_shared_declarations=int(final_n),remaining_lexical_theorems=remaining,
     assumed_whole_library_declarations=int(n),fitted_peak_rss_gib=(a+b*n)/1024**2,
     within_measured_range=n<=max(xs),scope='conditional extrapolation; source sites are not typed declaration counts; compute-heavy cases not calibrated'))
   csvwrite('falconer-whole-library-memory-scenarios.csv',scenarios)

 (ROOT/'reduced-summary.json').write_text(json.dumps(summary,indent=2))
 text='# Complete Falconer project extension: observed status\n\nSelf-review.\n\n'
 text+='\n'.join('- '+k+': '+str(v)for k,v in summary.items())+'\n\n'
 text+='Only complete exit0 cells and the full per-module acceptance comparison finalize a ratio. '
 text+='The numerator consumes exact newly constructed artifacts. Common dependency nodes reuse actual '
 text+='successful compiler cells and immutable artifacts from this same pinned experiment; their work is '
 text+='charged once per complete dependency closure. This is summed native compiler work, not parallel '
 text+='Lake wall time, a whole AI source-verification speedup, or a fresh reconstruction of shared nodes. '
 text+='Source failure, missing typed inputs, resource/timeout and graph mismatch stay explicit. '
 text+='A nonzero module-local fallback count means context segmentation, not one global environment. '
 text+='Memory checkpoints belong to a separate profiling pass; primary timing has them disabled.\n'
 pending=REPO/'falconer-result.pending';pending.write_text(text);pending.replace(REPO/'falconer-result.md')
 print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
