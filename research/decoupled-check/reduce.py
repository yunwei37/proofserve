#!/usr/bin/env python3
"""Reduce actual same-capture observations; never fill incomplete denominators."""
import os,json,csv,statistics,time
from pathlib import Path
os.sched_setaffinity(0,set(range(8,16)))
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
OUT=Path('/workspaces/repository/research/decoupled-check')
plan=json.loads((ROOT/'cohort-plan.json').read_text())
state=json.loads((ROOT/'progress.json').read_text())if(ROOT/'progress.json').exists()else{}
rows=[json.loads(x)for x in(ROOT/'measured.jsonl').read_text().splitlines()]
build=[x for x in rows if x['operation']=='build']
success={x['module']:x for x in build if x['returncode']==0 and all(x['outputs'].values())and not x['sorry_warning']}
global_oracle=set(state.get('oracle_global',[]))
def write(name,data):
 if not data:return
 with(OUT/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
summary=[];components=[]
for name,spec in plan['cases'].items():
 wanted=set(spec['modules']);done=wanted.intersection(success)
 trials=[x for x in build if x['module']in wanted]
 old=next((x for x in reversed(rows) if x['operation']=='stream'and x['cohort']==name),None)
 stream=next((x for x in reversed(rows) if x['operation']=='matched_stream'and x['cohort']==name),None)
 btime=sum(x['wall_s']for x in trials)
 complete=wanted.issubset(success)
 stream_ok=stream is not None and stream['closure_complete']
 verified=wanted.intersection(global_oracle)
 # Older v1 oracle records are retained controls, not substituted for matched input.
 row=dict(cohort=name,root=spec['root'],closure_modules=len(wanted),constructed_modules=len(done),construction_complete=complete,
 source_compiler_work_s=btime,source_peak_rss_kib=max([x['peak_rss_kib']for x in trials],default=0),
 original_artifact_stream_s=old['wall_s']if old and old['closure_complete']else'',
 matched_artifact_stream_s=stream['wall_s']if stream_ok else'',
 matched_stream_peak_rss_kib=stream['peak_rss_kib']if stream else'',
 stream_over_full_construction=stream['wall_s']/btime if stream_ok and complete and btime else'',
 matched_oracle_modules=len(verified),acceptance_parity_complete=stream_ok and verified==wanted,
 status='complete'if stream_ok and complete and verified==wanted else 'pending',
 failed_attempts=sum(x['returncode']!=0 for x in trials))
 summary.append(row)
 if stream_ok:
  events=[json.loads(x)for x in(ROOT/(stream['key']+'.stdout')).read_text().splitlines()]
  tm=next((x for x in events if x['event']=='module_timing'and x['module']==spec['root']),None)
  producer=success.get(spec['root'])
  if tm and producer:
   cost=(tm['read_ns']+tm['map_ns']+tm['replay_ns'])/1e9
   components.append(dict(cohort=name,module=spec['root'],class_tag='computational'if name.startswith('compute')else'ordinary',
     root_compiler_s=producer['wall_s'],root_read_map_replay_s=cost,root_kernel_replay_s=tm['replay_ns']/1e9,
     component_over_construction=cost/producer['wall_s'],scope='increment after checked dependencies; excludes process startup and shared base'))
write('cohort-costs.csv',summary);write('root-components.csv',components)
write('source-module-costs.csv',[dict(module=x['module'],wall_s=round(x['wall_s'],6),user_s=round(x['user_s'],6),system_s=round(x['system_s'],6),
 peak_rss_kib=x['peak_rss_kib'],returncode=x['returncode'],class_tag=x['class_tag'],raw_key=x['key'])for x in build])
text=f"""# Decoupled native checking: measured status
Updated {time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}. Review: self-review.
Raw observations: {ROOT}. P cores0-7; shared lock; no Lean -M;
11.875GiB child cgroup plus128MiB parent reserve within O12GiB.
Fixed native kernel and compiler: Lean4.34.1, release5045d0056413266e57c625dcd7c365b10e377c52.

## Complete closure accounting
"""
for r in summary:
 text+=f"- {r['cohort']} ({r['root']}): constructed {r['constructed_modules']}/{r['closure_modules']}; source compiler work {r['source_compiler_work_s']:.6f}s; matched stream {r['matched_artifact_stream_s']}; ratio {r['stream_over_full_construction']}; matched oracle modules {r['matched_oracle_modules']}; parity complete={r['acceptance_parity_complete']}.\n"
text+="""
A blank ratio is pending, not zero. The primary numerator consumes the exact
newly constructed olean artifacts, not the original distributed cache.
The source denominator sums actual native compiler subprocess durations for
**every member** of the closure, including each member's imports, tactics,
kernel checks and standard olean/ilean/C output. Failed attempts remain charged.
This is serial compiler work, not parallel Lake wall time, C++ toolchain
bootstrap, a continuous cross-window clock, or an inferred population speedup.
One union source DAG is built; common immutable modules are measured once and
included once in each applicable closure total. Lock wait and orchestration
overhead are outside these native-process durations. Warm OS/cache conditions
and one-pass construction limit generalization.

## Ordinary versus computational root components
root-components.csv separates predeclared ordinary roots (Nat.Basic and
NearPinDeletion) from computational roots (Grid and Amplitudes). Its numerator
is that root's read/map/kernel-replay component **after dependencies are checked**.
It is not standalone process latency: shared library verification remains in
the whole-closure table. Neither component fraction nor sampled C++ producer
cycle fraction is a guaranteed end-to-end speedup.
"""
for r in components:text+=f"- {r['module']}: component {r['root_read_map_replay_s']:.6f}s / producer {r['root_compiler_s']:.6f}s = {r['component_over_construction']:.6f}.\n"
text+="""
## Correctness and trust scope
The preflight checks a real13-module closure against bundled leanchecker and
three malformed proofs in distinct real Nat theorems. All three are rejected
by the original kernel through both streaming and module-local paths.
Each completed measured cohort additionally requires a matched acceptance set
from independently finalized single-module import environments (source-equivalent
to the bundled checker), with no checked environment reused across modules.
Successful oracle records for identical, already-built immutable dependencies
can contribute to multiple enclosing closures; no failed/timeout record does.
This is differential evidence on these inputs, not a proof of universal
transparency. Upstream replay skips unsafe/partial declarations; counts remain
in raw module events. Axioms keep Lean's semantics. No external checker joins TCB.

## Retained non-successes
"""
bad=[x for x in rows if x['returncode']or x.get('sorry_warning')or('closure_complete'in x and not x['closure_complete'])]
if not bad:text+='No measured non-success recorded at this checkpoint.\n'
for x in bad:text+=f"- {x['key']}: operation={x['operation']}, rc={x['returncode']}, cgroup memory events={x['memory_events'].strip().replace(chr(10),'; ')}.\n"
if any(state.get(k)for k in ['build_failure','stream_failure','matched_failure','oracle_failure']):
 text+='\nCapture stopped on an actual incomplete/error cell; retained partials are not a completed cost comparison.\n'
(OUT/'results.md').write_text(text)
(ROOT/'reduction.json').write_text(json.dumps(dict(cohorts=summary,root_components=components,measured_non_successes=len(bad)),indent=2))
print(json.dumps(summary),flush=True)
