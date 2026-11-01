#!/usr/bin/env python3
"""Build the complete Falconer source frame after a stock artifact manifest.
The external manifest is not a successful-build or proof acceptance record.
"""
import json,sys
from pathlib import Path
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
PLAN=BASE/'scale-study/falconer-plan.json'
def prepare(external_manifest, output):
 output=Path(output);output.mkdir(exist_ok=True)
 q=json.loads(PLAN.read_text())
 old=json.loads((BASE/'build-frame.json').read_text())
 roots=sorted({r['source_root']for r in old if not r['module'].startswith('OAI.')})
 graph={}
 for line in Path(external_manifest).read_text().splitlines():
  e=json.loads(line)
  if e.get('event')=='manifest':graph[e['module']]=e
 if not set(q['external_frontier']).issubset(graph):
  raise RuntimeError('external native manifest incomplete')
 for m in q['internal_closure']:
  graph[m]=dict(module=m,imports=['Init']+q['source_imports'][m],constants=None)
 order=[];seen=set();pending=set()
 def visit(m):
  if m in seen:return
  if m in pending:raise RuntimeError('cyclic graph '+m)
  if m not in graph:raise RuntimeError('missing import '+m)
  pending.add(m)
  for dep in graph[m]['imports']:visit(dep)
  pending.remove(m);seen.add(m);order.append(m)
 for mod in q['target_modules']:visit(mod)
 frame=[];missing=[]
 for mod in order:
  if mod in q['source_paths']:
   srcroot=BASE/'scale-study/falconer-source/lean'
   source=srcroot/(mod.replace('.','/')+'.lean')
  else:
   candidates=[Path(root)/(mod.replace('.','/')+'.lean')for root in roots]
   found=[x for x in candidates if x.is_file()]
   if len(found)!=1:
    missing.append(dict(module=mod,source_candidates=[str(x)for x in found]))
    continue
   source=found[0];srcroot=source.parents[len(mod.split('.'))-1]
  if not source.is_file():missing.append(dict(module=mod,source_candidates=[]));continue
  frame.append(dict(module=mod,source=str(source),source_root=str(srcroot),
   source_bytes=source.stat().st_size,imports=graph[mod]['imports'],
   constants=graph[mod].get('constants'),class_tag='ai-mathematics'if mod in q['source_paths']else'dependency'))
 receipt=dict(status='prepared'if not missing else'missing_sources',source_revision=q['source_revision'],
  ai_source_modules=len(q['target_modules']),complete_closure_modules=len(order),
  source_frame_rows=len(frame),missing_sources=missing,roots=q['target_modules'],
  scope='predeclared complete project, actual native external graph plus source internal imports; final compiled graph must match')
 (output/'build-frame.json').write_text(json.dumps(frame,indent=2))
 (output/'cohort-plan.json').write_text(json.dumps(receipt,indent=2))
 (output/'roots.txt').write_text('\n'.join(q['target_modules'])+'\n')
 if missing:raise RuntimeError('missing source; preserve plan and do not impute denominator')
 print(json.dumps({k:v for k,v in receipt.items()if k!='roots'}))
 return frame,receipt
if __name__=='__main__':prepare(*sys.argv[1:])
