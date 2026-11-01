"""Complete single-configuration costs; never substitute incremental-clock sums."""
import csv,json,re
from pathlib import Path
from analyze_curves import dump
def main(raw,out):
 rows=[];groups={}
 for file in sorted(raw.glob('*-full-*-r*-summary.json')):
  record=json.loads(file.read_text());r=record['result'];complete=record['completed']
  parsed=re.fullmatch(r'(.+)-full-(reference|audit|parallel|chunk)([1248])-r(\d+)',r['key'])
  if not parsed:continue
  cohort,variant,workers,repeat=parsed.groups()
  native_complete=complete and r['native_retired']and r.get('cgroup_retired',False)
  ending=record['complete_event']or{}
  row=dict(capture=raw.name,key=r['key'],cohort=cohort,variant=variant,workers=int(workers),repeat=int(repeat),
   complete=native_complete,returncode=r['returncode'],scope=record['scope'],
   cache_scope='empty checked environment; OS page cache retained',
   whole_wall_s=r['wall_s'],whole_cpu_s=r.get('cgroup_usage_s','unknown'if r['stop_reasons']or r['returncode']<0 else r['user_s']+r['system_s']),
   wait4_peak_rss_mib='unknown'if r['stop_reasons']or r['returncode']<0 else r['peak_rss_kib']/1024,
   sampled_tree_peak_mib=r['sampled_tree_peak_bytes']/2**20,
   native_limit_s=r['wall_limit_s'],accepted_modules=len(record['accepted']),
   accepted_set_equal_to_full_curve=record['accepted_set_equal_to_same_input_curve'],
   input_entries=ending.get('constants','unknown'),upstream_exclusions=ending.get('skipped_unsafe_partial','unknown'),
   chunk_rewrite=record['chunk_rewrite_enabled'],certificate_generation_excluded=record['certificate_generation_excluded'])
  rows.append(row);groups.setdefault((cohort,int(repeat)),[]).append((row,record))
 out.mkdir(exist_ok=True)
 dump(out/'full-cells.csv',rows)
 pairs=[]
 for(cohort,repeat),group in groups.items():
  refs=[x for x in group if x[0]['variant']=='reference'and x[0]['complete']]
  if len(refs)!=1:continue
  ref,refRecord=refs[0]
  for row,record in group:
   if row['variant']=='reference'or not row['complete']:continue
   equality=set(record['accepted'])==set(refRecord['accepted'])
   pairs.append(dict(cohort=cohort,repeat=repeat,method=row['variant']+str(row['workers']),
    reference_wall_s=ref['whole_wall_s'],method_wall_s=row['whole_wall_s'],
    speedup=ref['whole_wall_s']/row['whole_wall_s'],
    cpu_ratio=row['whole_cpu_s']/ref['whole_cpu_s'],
    accepted_modules=row['accepted_modules'],accepted_sets_equal=equality,
    scope='both actual complete cold native processes; one selected configuration each'))
 dump(out/'full-pairs.csv',pairs)
 (out/'full-completeness.json').write_text(json.dumps(dict(raw=str(raw),cells=len(rows),
  complete=sum(x['complete']for x in rows),pairs=len(pairs),
  failed=[x['key']for x in rows if not x['complete']],paired_process_repeats='one unless more raw repetitions exist'),indent=2))
 print(json.dumps(dict(rows=rows,pairs=pairs),indent=2))
if __name__=='__main__':
 import sys;main(Path(sys.argv[1]),Path(sys.argv[2]))
