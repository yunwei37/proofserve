"""Complete single-configuration costs; never substitute incremental-clock sums."""
import csv,json,re,statistics
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
 # Construction authority is O's complete source-build CSV; do not duplicate estimates.
 repo=Path('/workspaces/repository')
 costs=list(csv.DictReader((repo/'research/decoupled-check/cohort-costs.csv').open()))
 def source_cost(root):
  values=[x for x in costs if x['root']==root and x['construction_complete']=='True']
  return float(values[0]['source_compiler_work_s'])if len(values)==1 else 'unknown_no_complete_source_construction'
 stairs=[]
 mathfile=out/'v14-math-summary.csv'
 if mathfile.exists():
  math=list(csv.DictReader(mathfile.open()))
  ref=next(x for x in math if x['variant']=='reference')
  par=next(x for x in math if x['variant']=='parallel8')
  stairs.append(dict(cohort='Mathlib.Data.Nat.Basic',modules=int(ref['accepted_modules']),
   source_compiler_work_s=source_cost('Mathlib.Data.Nat.Basic'),
   serial_stream_s=float(ref['wall_s_median']),parallel_stream_s=float(par['wall_s_median']),
   configuration='uniform8',repetitions=int(ref['completed_repeats']),scope='complete closure',
   source_cost_scope='serial sum of compiler invocations; not parallel Lake wall'))
 for cohort,method in dict.fromkeys((x['cohort'],x['method'])for x in pairs):
  ps=[x for x in pairs if x['cohort']==cohort and x['method']==method]
  record=next(record for group in groups.values()for row,record in group if row['cohort']==cohort and row['complete'])
  root=record['result']['argv'][-1]
  stairs.append(dict(cohort=root,modules=ps[0]['accepted_modules'],
   source_compiler_work_s=source_cost(root),serial_stream_s=statistics.median(x['reference_wall_s']for x in ps),
   parallel_stream_s=statistics.median(x['method_wall_s']for x in ps),
   configuration='uniform'+method.removeprefix('parallel')if method.startswith('parallel')else method,
   repetitions=len(ps),scope='complete closure',
   source_cost_scope='serial sum of compiler invocations; not parallel Lake wall'))
 dump(out/'cost-staircase-current.csv',stairs)
 (out/'full-completeness.json').write_text(json.dumps(dict(raw=str(raw),cells=len(rows),
  complete=sum(x['complete']for x in rows),pairs=len(pairs),
  failed=[x['key']for x in rows if not x['complete']],paired_process_repeats='one unless more raw repetitions exist'),indent=2))
 print(json.dumps(dict(rows=rows,pairs=pairs),indent=2))
if __name__=='__main__':
 import sys;main(Path(sys.argv[1]),Path(sys.argv[2]))
