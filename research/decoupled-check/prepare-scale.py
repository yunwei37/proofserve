#!/usr/bin/env python3
"""Untimed, bounded-memory preparation from pinned source census and retained captures."""
import os,csv,gzip,json,sqlite3,collections
from pathlib import Path
os.sched_setaffinity(0,{8})
REPO=Path('/workspaces/repository')
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
OUT=BASE/'scale-study';OUT.mkdir(exist_ok=True)
INV=REPO/'workloads/openai-math/static-4eaee875'
prefix='lean/OAI/MeasureTheory/Falconer/'
targets={}
with gzip.open(INV/'files.csv.gz','rt')as f:
 for r in csv.DictReader(f):
  if r['path'].startswith(prefix)or r['path']==prefix.rstrip('/')+'.lean':
   targets[r['path'][5:-5].replace('/','.')]=r['path']
db=sqlite3.connect(OUT/'source-imports.sqlite')
db.execute('create table if not exists imports(module text, dependency text, internal integer)')
if db.execute('select count(*)from imports').fetchone()[0]==0:
 batch=[]
 with gzip.open(INV/'content/imports.csv.gz','rt')as f:
  for r in csv.DictReader(f):
   batch.append((r['module'],r['imports'],int(r['internal']=='True')))
   if len(batch)==1000:db.executemany('insert into imports values(?,?,?)',batch);batch=[]
 if batch:db.executemany('insert into imports values(?,?,?)',batch)
 db.execute('create index if not exists by_module on imports(module)');db.commit()
seen=set();todo=list(targets);external=set();edges={}
while todo:
 m=todo.pop()
 if m in seen:continue
 seen.add(m);values=list(db.execute('select dependency,internal from imports where module=?',(m,)))
 edges[m]=[d for d,internal in values]
 for d,internal in values:
  if internal and d not in seen:todo.append(d)
  if not internal:external.add(d)
paths={};sizes={}
with gzip.open(INV/'files.csv.gz','rt')as f:
 for r in csv.DictReader(f):
  name=r['path'][5:-5].replace('/','.')
  if name in seen:paths[name]=r['path'];sizes[name]=int(r['size'])
total=collections.Counter();project=collections.Counter();kinds=collections.Counter()
with gzip.open(INV/'content/file-metrics.csv.gz','rt')as f:
 for r in csv.DictReader(f):
  total['modules']+=1
  for k in ['bytes','lemma_theorem_declarations','decide_plus_kernel','native_decide','bv_decide','ofReduceBool']:
   total[k]+=int(r[k])
  if r['path'].startswith(prefix):
   project['modules']+=1
   for k in ['bytes','lemma_theorem_declarations','decide_plus_kernel','native_decide','bv_decide']:
    project[k]+=int(r[k])
  kinds['explicit_kernel_compute_modules'if int(r['decide_plus_kernel'])else'no_explicit_kernel_compute_modules']+=1
payload=dict(source_revision='4eaee87548250b2682affda7d05d947c05554bae',
 target_project='OAI.MeasureTheory.Falconer',target_modules=sorted(targets),internal_closure=sorted(seen),
 source_paths=paths,source_sizes=sizes,source_imports=edges,external_frontier=sorted(external),
 source_metrics=dict(project),whole_source_metrics=dict(total),whole_source_lexical_classes=dict(kinds),
 scope='source-name graph, external dependencies not yet expanded; lexical sites are not compiled declaration counts')
(OUT/'falconer-plan.json').write_text(json.dumps(payload,indent=2))
# Both observations are complete, but different workload compositions: scenarios, not bounds.
samples=[]
for name in ['timed-constructed-stream-math','timed-stream-compute-grid']:
 r=json.loads((BASE/(name+'.result.json')).read_text())
 last=None;timings=[]
 for line in(BASE/(name+'.stdout')).open():
  e=json.loads(line)
  if e['event']=='complete':last=e
  if e['event']=='module_timing':timings.append(e)
 samples.append(dict(capture=name,modules=last['modules'],input_declaration_entries=last['constants'],
  upstream_skipped_entries=last['skipped_unsafe_partial'],wall_s=r['wall_s'],peak_rss_kib=r['peak_rss_kib'],
  rss_kib_per_input_entry=r['peak_rss_kib']/last['constants'],seconds_per_input_entry=r['wall_s']/last['constants'],
  kernel_component_s=sum(e['replay_ns']for e in timings)/1e9))
(OUT/'scaling-observations.json').write_text(json.dumps(samples,indent=2))
scenarios=[]
sites=total['lemma_theorem_declarations'];base_entries=max(s['input_declaration_entries']for s in samples)
for multiplier in [1,2,4,8]:
 n=base_entries+multiplier*sites
 scenarios.append(dict(compiled_entries_per_lexical_theorem_site=multiplier,assumed_base_entries=base_entries,
 lexical_sites=sites,assumed_total_entries=n,
 rss_gib_at_low_observed_rate=min(s['rss_kib_per_input_entry']for s in samples)*n/1024**2,
 rss_gib_at_high_observed_rate=max(s['rss_kib_per_input_entry']for s in samples)*n/1024**2,
 hours_at_low_observed_rate=min(s['seconds_per_input_entry']for s in samples)*n/3600,
 hours_at_high_observed_rate=max(s['seconds_per_input_entry']for s in samples)*n/3600,
 classification='conditional scenario; not a runtime/memory bound or calibrated population estimate'))
with(OUT/'full-library-scenarios.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=scenarios[0]);w.writeheader();w.writerows(scenarios)
(OUT/'preparation-terminal.json').write_text(json.dumps(dict(status='complete',project_source_modules=len(targets),internal_closure_modules=len(seen),external_frontier_names=len(external),project_source_metrics=dict(project),whole_source_metrics=dict(total),samples=samples),indent=2))
print((OUT/'preparation-terminal.json').read_text(),flush=True)
