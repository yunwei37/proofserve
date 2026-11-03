# perf script's native Python API. No browser, server, or raw ASCII expansion.
import os,json,csv,collections,gzip
from pathlib import Path
OUT=Path(os.environ['PERF_ANALYSIS_OUT']);OUT.mkdir(parents=True,exist_ok=True)
WORKERS=set(json.loads(Path(os.environ['PERF_NATIVE_TERMINAL']).read_text())['cell']['observed_worker_TIDs'])
totals=collections.Counter();categories=collections.Counter();symbols=collections.Counter()
addresses=collections.Counter();id_counts=collections.Counter();id_periods=collections.Counter();first=None;samples_without_period=collections.Counter();sample_counts=collections.Counter()
def family(stack):
 # Exclusive nearest operation in a leaf->root call chain, never sum inclusive
 # percentages. Missing inline debug information is an explicit limitation.
 for name in stack:
  low=name.lower()
  if any(x in low for x in ['lean_inc_ref','lean_dec_ref','lean_mark_mt','lean::object_ref::~','lean::object_ref::operator=']):
   return 'reference_counts_and_destruction'
  if low.startswith(('mi_','_mi_','cfree')) or any(x in low for x in ['mi_malloc','mi_free','_mi_','malloc','calloc','realloc','operator new','operator delete','lean_alloc','lean_free']):
   return 'allocation_and_free'
  if any(x in low for x in ['__hash_table','hashmap','dhashmap','lean_environment_find','environment::find(','::find(','::cache_','::hash(','sharecommon','share_common']):
   return 'hash_and_cache_lookup'
  if any(x in low for x in ['type_checker::whnf','type_checker::is_def_eq','type_checker::quick_is_def_eq',
    'type_checker::reduce_','type_checker::unfold_']):
   return 'whnf_and_defeq_including_unresolved_inlines'
  if 'type_checker::' in low:return 'other_kernel_type_inference'
  if any(x in low for x in ['memcpy','memmove','memset']):return 'memory_copy_and_clear'
 return 'other_or_unresolved'
def process_event(p):
 global first
 sample=p['sample'];event=p['ev_name'];tid=sample['tid'];weight=sample.get('period')
 sample_counts[event]+=1
 idkey=(sample['pid'],tid,event,sample['id']);id_counts[idkey]+=1;id_periods[idkey]+=weight or 0
 if weight is None or weight<=0:
  samples_without_period[event]+=1
  return
 if first is None:
  first={'keys':sorted(p),'sample':sample,'callchain':p.get('callchain',[])[:5],
   'symbol':p.get('symbol'),'ev_name':event,'dso':p.get('dso'),'symoff':p.get('symoff'),
   'dso_map_start':p.get('dso_map_start'),'dso_map_end':p.get('dso_map_end')}
  (OUT/'first-sample-shape.json').write_text(json.dumps(first,indent=2,default=str))
 chain=p.get('callchain',[]);stack=[(e.get('sym') or {}).get('name') or '[unknown]' for e in chain]
 leaf=p.get('symbol') or (stack[0] if stack else '[unknown]')
 if not stack:stack=[leaf]
 has_check=any('ParallelCore_0__checkOne' in x for x in stack)
 has_cpp=any('lean_add_decl' in x or 'lean::type_checker::' in x or 'lean::environment::add' in x for x in stack)
 if has_check and has_cpp:scope='ordinary_kernel_anchored'
 elif tid in WORKERS and has_cpp:scope='ordinary_worker_kernel_unanchored'
 elif has_cpp:scope='serial_or_other_kernel'
 elif tid in WORKERS:scope='ordinary_worker_other_or_truncated'
 else:scope='outside_or_unresolved'
 category=family(stack)
 totals[(event,scope)]+=weight
 categories[(event,scope,category,tid)]+=weight
 symbols[(event,scope,leaf)]+=weight
 addresses[(event,scope,tid,leaf,p.get('dso','[unknown]'),p.get('symoff'),sample.get('ip',0))]+=weight
def write(name,keys,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.writer(f,lineterminator=chr(10));w.writerow(keys);w.writerows(rows)
def trace_end():
 write('sample-ids.csv',['PID','TID','event','id','samples','period_sum'],
  [(*k,v,id_periods[k])for k,v in sorted(id_counts.items())])
 write('scope-periods.csv',['event','scope','sampled_period'],
  [(*k,v) for k,v in sorted(totals.items())])
 write('category-thread-periods.csv',['event','scope','category','TID','sampled_period'],
  [(*k,v) for k,v in sorted(categories.items())])
 write('symbol-periods.csv',['event','scope','leaf_symbol','sampled_period'],
  [(*k,v) for k,v in symbols.most_common(1000)])
 # Preserve all per-IP/thread weights compactly for later inline annotation.
 # Only small derived tables, never this complete address file, enter Git.
 with gzip.open(OUT/'address-periods.csv.gz','wt',newline='') as f:
  w=csv.writer(f,lineterminator=chr(10));w.writerow(['event','scope','TID','leaf_symbol','DSO','symbol_offset','sample_IP','sampled_period'])
  w.writerows((*k,v) for k,v in addresses.items())
 (OUT/'decode-terminal.json').write_text(json.dumps(dict(state='complete' if not samples_without_period else 'invalid_missing_period',
  events=len(totals),sample_counts=dict(sample_counts),samples_without_period=dict(samples_without_period),
  worker_TIDs=sorted(WORKERS),scope='weighted samples, not exact per-category hardware counts',
  inline_limitation='SDK C++ inline debug coverage incomplete; atomic instructions require annotation'),indent=2))
