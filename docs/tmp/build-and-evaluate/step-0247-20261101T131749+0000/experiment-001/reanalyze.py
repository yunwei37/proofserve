from pathlib import Path
import os,json,gzip,time,resource,csv,subprocess,datetime,functools
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0247-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-module-baseline-paper-step.txt').write_text(str(s)+'\n')
def freeze(p,name):
 raw=Path(p).read_bytes();(e/(name+'.gz')).write_bytes(gzip.compress(raw,mtime=0));return raw
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
assert '按这个主线推进' in (r/'docs/user-instruction.md').read_text()
src=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux/src/lean/LeanChecker.lean')
code=freeze(src,'upstream-LeanChecker.lean').decode()
local=code[code.index('unsafe def replayFromImports'):code.index('unsafe def replayFromFresh')]
main=code[code.index('unsafe def main'):]
assert 'importModulesCore mod.imports' in local and 'env.toKernelEnv.replay newConstants' in local
assert 'let mut tasks := #[]' in main
spawn=main[main.index('let mut tasks := #[]'):main.index('for (m, t) in tasks do')]
assert 'IO.asTask (replayFromImports m)' in spawn and '.get' not in spawn
assert 'if let .error e := t.get then' in main
assert 'target.isPrefixOf m' in main
b=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
rows=[];paths=[];edges=[]
for c in ['math','ordinary-oai','compute-grid','compute-amplitudes']:
 raw=freeze(b/('timed-constructed-stream-'+c+'.stdout'),c+'-timed-native.stdout')
 ev=[json.loads(line)for line in raw.decode().splitlines()]
 accepted=[x for x in ev if x.get('event')=='accept'];names=[x['module']for x in accepted]
 graph={x['module']:list(dict.fromkeys(x['imports']))for x in accepted}
 w={x['module']:int(x['replay_ns'])for x in ev if x.get('event')=='module_timing'}
 assert len(names)==len(set(names))==len(graph)==len(w)
 assert set(w)==set(graph) and len([x for x in ev if x.get('event')=='complete'])==1
 rank={n:i for i,n in enumerate(names)}
 for name,deps in graph.items():
  assert all(dep in graph and rank[dep]<rank[name]for dep in deps)
  edges.extend(dict(cohort=c,imported_module=dep,module=name)for dep in deps)
 root=names[-1];todo=[root];seen=set()
 while todo:
  v=todo.pop()
  if v in seen:continue
  seen.add(v);todo.extend(graph[v])
 assert seen==set(graph)
 pred={}
 @functools.lru_cache(None)
 def span(v):
  p=max(graph[v],key=span)if graph[v]else None;pred[v]=p
  return w[v]+(span(p)if p else 0)
 S=span(root);W=sum(w.values());path=[];v=root
 while v is not None:path.append(v);v=pred[v]
 path=path[::-1];assert sum(w[v]for v in path)==S
 assert all(path[i]in graph[path[i+1]]for i in range(len(path)-1))
 # These are alternative static scheduling assumptions on observed stream-call weights, NOT native leanchecker performance.
 rows.append(dict(cohort=c,modules=len(w),replay_work_s=W/1e9,fully_checked_imports_span_s=S/1e9,strict_import_model_W_over_S=W/S,largest_single_module_replay_s=max(w.values())/1e9,independent_task_fixed_weight_W_over_max=W/max(w.values()),critical_path_modules=len(path),native_baseline_speedup='not measured'))
 paths.extend(dict(cohort=c,path_index=i,module=v,replay_ns=w[v],source='existing timed shared stream; not module-local import/replay latency')for i,v in enumerate(path))
for name,rs in [('assumption-dependent-models.csv',rows),('strict-import-critical-paths.csv',paths),('import-edges.csv',edges)]:
 with(e/name).open('w',newline='')as f:
  q=csv.DictWriter(f,fieldnames=list(rs[0]),lineterminator='\n');q.writeheader();q.writerows(rs)
j=dict(models=rows,upstream_source=str(src),source_scope='Lean4.34.1 installed official LeanChecker source; module-local replayFromImports task API',decision='reject interpreting fully-checked-import weighted DAG as an upper bound on stock leanchecker or on arbitrary proof checking; expose missing native module-task comparison',why='upstream spawns independent module-local replay tasks before collecting task results; imported declarations loaded through stock importer are assumed within each task',input_scope='CLI target selection is prefix-based; exact closure ID set must not be silently broadened for a comparison',new_native_runs=0,root_analysis_s=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'step':str(s),**j},indent=2))
