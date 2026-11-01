"""Cost-weighted exposure/proxy, never a claim of measured removable tactic time."""
import os,pathlib,json,re,csv,gzip
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
KNOWN_RECORDS={'OAI.SharpPlanar.IntegerIntervals.RBox','OAI.SharpPlanar.IntegerIntervals.CBox',
'OAI.SharpPlanar.IntegerIntervals.PointBox','OAI.SepticProfile.FixedInterval.Box'}
def eligible(shape):
 return shape=='conjunction:And' or shape=='forall:Fin' or shape.removeprefix('record_equality:') in KNOWN_RECORDS
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 costs=json.loads((RAW/'native-panel/all31-costs.json').read_text())
 counts={};known=set()
 for index in [0,4,8,12,16,20]:
  p=RAW/'native-panel'/f'batch-{index}'
  text=p.with_suffix('.log').read_text()
  assert 'CK_NATIVE_COUNT' in text
  imports=re.findall(r'^import (OAI\S+)$',p.with_suffix('.lean').read_text(),re.M);known.update(imports)
  for module,shape,n in re.findall(r'^CK_NATIVE_COUNT (\S+) (\S+) (\d+)$',text,re.M):
   counts.setdefault(module,{})[shape]=int(n)
 # Reuse the separately completed native 3-module census, no native rerun.
 for module,shape,n in re.findall(r'^CK_NATIVE_COUNT (\S+) (\S+) (\d+)$',(RAW/'native-census-v2.log').read_text(),re.M):
  old=counts.setdefault(module,{}).get(shape)
  assert old is None or old==int(n),(module,shape,old,n)
  counts[module][shape]=int(n);known.add(module)
 metrics=HERE.parents[1]/'workloads/openai-math/static-4eaee875/content/file-metrics.csv.gz'
 with gzip.open(metrics,'rt') as f:
  source={r['path']:int(r['decide_plus_kernel']) for r in csv.DictReader(f)}
 rows=[]
 for r in costs:
  module=r['module'];shapes=counts.get(module,{})
  n=sum(shapes.values());yes=sum(v for k,v in shapes.items() if eligible(k))
  src=source[r['path']];is_known=module in known or src==0
  fraction=yes/n if n else 0. if is_known and src==0 else None
  rows.append(dict(module=module,wall_s=r['wall_s'],cpu_s=r['user_cpu_s']+r['system_cpu_s'],
     source_sites=src,native_decide_auxiliaries=n,known_structural_split_auxiliaries=yes,
     native_type_census_completed=is_known,helper_fraction=fraction,
     has_known_splittable_shape=yes>0,native_count_vs_source_count_delta=n-src if module in known else None))
 with (HERE/'cost-weighted-panel.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 result=dict(modules=31,completed_native_or_zero_site_metadata=sum(x['native_type_census_completed'] for x in rows),
  usable_helper_mix_modules=sum(r['helper_fraction'] is not None for r in rows),
  unknown_modules=[r['module'] for r in rows if r['helper_fraction'] is None],
  counting_units='source sites and checked helper declarations are separate; no measured per-site CPU',
  proxy_assumption='Within a module, allocate its complete wall/CPU uniformly over native decide-helper declarations; not an empirical tactic-time fraction',
  context='W fixed31 no-M standard-artifact point, not entire library or service')
 for metric in ['wall_s','cpu_s']:
  total=sum(r[metric] for r in rows);known_total=sum(r[metric] for r in rows if r['helper_fraction'] is not None)
  proxy=sum(r[metric]*r['helper_fraction'] for r in rows if r['helper_fraction'] is not None)
  unknown=total-known_total
  result[metric]=dict(total=total,known_cost=known_total,unknown_cost=unknown,
    modeled_split_share_lower=proxy/total,modeled_split_share_upper=(proxy+unknown)/total,
    module_exposure_fraction=sum(r[metric] for r in rows if r['has_known_splittable_shape'])/total,
    caveat='Proxy bounds assign unknown helper mixes 0..1, not bounds on actually saved runtime')
 (HERE/'cost-weighted-summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
