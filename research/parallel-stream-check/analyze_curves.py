"""Summarize complete one-process computational-leaf curves only."""
import csv,json,statistics
from pathlib import Path
def dump(path,rows):
 if not rows:return
 with path.open('w')as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
def main(raw,out):
 raws=[raw]if isinstance(raw,Path)else list(raw)
 rows=[];runs=[];failures=[]
 files=[(root,file)for root in raws for file in sorted(root.glob('*-stream-r*-summary.json'))]
 for raw,file in files:
  record=json.loads(file.read_text());r=record['result'];complete=record['completed']
  events=[]
  for line in(raw/'runs'/r['key']/'stdout').read_text().splitlines():
   if line.startswith('{'):
    try:events.append(json.loads(line))
    except json.JSONDecodeError:pass
  runs.append(dict(capture=raw.name,key=r['key'],complete=complete,returncode=r['returncode'],whole_wall_s=r['wall_s'],
   whole_cpu_s=r.get('cgroup_usage_s', 'unknown_guard_killed_parent' if r['stop_reasons'] or r['returncode']<0 else r['user_s']+r['system_s']),
   whole_peak_rss_mib='unknown_guard_killed_parent'if r['stop_reasons']or r['returncode']<0 else r['peak_rss_kib']/1024,
   sampled_tree_peak_mib=r['sampled_tree_peak_bytes']/1024**2,
   accepted_modules=len(record['accepted']),fallback_events=sum('fallback_reason'in e for e in events),
   native_retired=r['native_retired'],cgroup_retired=r.get('cgroup_retired',False)))
  if not complete:failures.append(dict(capture=raw.name,key=r['key'],returncode=r['returncode'],completed_cells=len(record['curves'])));continue
  baseline=next(e for e in record['curves']if e['kind']=='serial')
  baseWall=int(baseline['elapsed_ns'])/1e9;baseCPU=int(baseline['cpu_ns'])/1e9
  for cell in record['curves']:
   wall=int(cell['elapsed_ns'])/1e9;cpu=int(cell['cpu_ns'])/1e9
   rows.append(dict(capture=raw.name,module=cell['module'],key=r['key'],variant=cell['kind'],workers=cell['workers'],
    wall_s=wall,cpu_s=cpu,speedup_to_same_process_serial=baseWall/wall,
    cpu_ratio_to_serial=cpu/baseCPU,mean_cores=cpu/wall,
    chunk_parents=cell['actual_chunk_parents'],chunk_subjobs=cell['actual_chunk_subjobs'],
    waves=cell['waves'],jobs=cell['jobs'],route=cell['route'],
    all_source_constants_match=True,scope='incremental_root_same_verified_prefix',
    chunk_payload_read_included=cell['kind'].startswith('chunk')))
 dump(out/'compute-cells.csv',rows);dump(out/'compute-runs.csv',runs)
 summary=[]
 for capture,module,variant in dict.fromkeys((r['capture'],r['module'],r['variant'])for r in rows):
  group=[r for r in rows if r['capture']==capture and r['module']==module and r['variant']==variant]
  x=dict(capture=capture,module=module,variant=variant,completed_repeats=len(group),scope='incremental_root_same_verified_prefix')
  for metric in ['wall_s','cpu_s','speedup_to_same_process_serial']:
   values=[r[metric]for r in group];x.update({metric+'_median':statistics.median(values),
    metric+'_min':min(values),metric+'_max':max(values)})
  x.update(chunk_parents=group[0]['chunk_parents'],chunk_subjobs=group[0]['chunk_subjobs'])
  summary.append(x)
 dump(out/'compute-summary.csv',summary)
 (out/'compute-completeness.json').write_text(json.dumps(dict(raw=[str(x)for x in raws],complete_native_runs=sum(r['complete']for r in runs),
  actual_cells=len(rows),failed_runs=failures,
  caveat='Whole process runs all variants and prefix; incremental cells are not cold module invocation speedups',
  no_per_variant_peak_rss='only whole-process peak RSS is measured'),indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':
 import sys;main([Path(x)for x in sys.argv[1:-1]],Path(sys.argv[-1]))
