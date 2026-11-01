"""Summarize completed same-artifact cells; never promote partials to zeros."""
import argparse,csv,json,statistics
from pathlib import Path
def main(raw,out):
 results=json.loads((raw/'matrix-results.json').read_text())
 rows=[];oracle=None
 for r in results:
  e=[json.loads(s)for s in(raw/'runs'/r['key']/'stdout').read_text().splitlines()if s.startswith('{')]
  accept=[v['module']for v in e if v.get('event')=='accept']
  if oracle is None and r['returncode']==0:oracle=set(accept)
  work=[v for v in e if v.get('event')=='kernel_work']
  complete=next((v for v in reversed(e)if v.get('event')=='complete'),{})
  rows.append(dict(key=r['key'],variant=r['key'].rsplit('-',1)[0].removeprefix('math-'),
   repeat=int(r['key'].rsplit('-',1)[1]),returncode=r['returncode'],
   wall_s=r['wall_s'],cpu_s=r['user_s']+r['system_s'],user_s=r['user_s'],system_s=r['system_s'],
   peak_rss_kib=r['peak_rss_kib'],charged_peak_bytes=r['charged_peak_bytes'],
   sampled_tree_peak_bytes=r['sampled_tree_peak_bytes'],accepted_modules=len(accept),
   accepted_set_equal=oracle is not None and set(accept)==oracle,
   complete_modules=complete.get('modules','unknown'),input_entries=complete.get('constants','unknown'),
   upstream_skipped=complete.get('skipped_unsafe_partial','unknown'),
   kernel_work_s=sum(v['elapsed_ns']for v in work)/1e9 if work else 'unknown',
   parallel_modules=sum(v['path']=='parallel'for v in work),
   serial_complex_modules=sum(v['path']=='upstream_complex_or_cycle'for v in work),
   module_local_fallbacks=complete.get('module_local_fallbacks','unknown'),
   parallel_jobs=sum(v['jobs']for v in work),waves=sum(v['waves']for v in work)))
 out.mkdir(exist_ok=True)
 with (out/'math-cells.csv').open('w')as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
 summary=[]
 for variant in dict.fromkeys(r['variant']for r in rows):
  group=[r for r in rows if r['variant']==variant and r['returncode']==0]
  if not group:continue
  row=dict(variant=variant,completed_repeats=len(group),accepted_set_equal=all(r['accepted_set_equal']for r in group))
  for metric in ['wall_s','cpu_s','user_s','system_s','peak_rss_kib','kernel_work_s']:
   v=[r[metric]for r in group if isinstance(r[metric],(int,float))]
   row.update({metric+'_median':statistics.median(v)if v else 'unknown',
     metric+'_min':min(v)if v else 'unknown',metric+'_max':max(v)if v else 'unknown'})
  row.update({k:group[0][k]for k in ['accepted_modules','input_entries','upstream_skipped','parallel_modules',
     'serial_complex_modules','parallel_jobs','waves','module_local_fallbacks']})
  summary.append(row)
 with (out/'math-summary.csv').open('w')as f:
  w=csv.DictWriter(f,fieldnames=summary[0].keys(),lineterminator='\n');w.writeheader();w.writerows(summary)
 (out/'math-completeness.json').write_text(json.dumps(dict(raw=str(raw),actual_cells=len(rows),
  expected_cells=18,terminal=(raw/'matrix-complete.json').exists(),all_accepted_equal=all(r['accepted_set_equal']for r in rows),
  failed=[r['key']for r in rows if r['returncode']]),indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('raw',type=Path);p.add_argument('out',type=Path);a=p.parse_args();main(a.raw,a.out)
