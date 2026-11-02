#!/usr/bin/env python3
"""Independent finite Falconer verification cells; no long-lived state is required."""
import os,json,sys,time,importlib.util
from pathlib import Path
D=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
ROOT=D/'bounded-recheck-v1'
spec=importlib.util.spec_from_file_location('native',D/'native_project.py')
native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native);native.ROOT=ROOT
CHECKER=ROOT/'indexed-audit'
def parse(path):
 good=[];malformed=[]
 for i,line in enumerate(path.read_text().splitlines(),1):
  if not line.startswith('{'):continue
  try:good.append(json.loads(line))
  except json.JSONDecodeError:malformed.append(i)
 return good,malformed
def save(name,value):
 p=ROOT/name;pending=p.with_suffix('.pending')
 with pending.open('w')as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
 pending.replace(p)
def cell(key,args,limit,env):
 r=native.run(key,args,limit,True,env=env)
 es,bad=parse(ROOT/(r['key']+'.stdout'))
 r.update(accepted=[x['module']for x in es if x.get('event')=='accept'],
  rejected=[x['module']for x in es if x.get('event')=='reject'],
  malformed_json_lines=bad,complete_event=next((x for x in reversed(es)if x.get('event')=='complete'),None))
 save(r['key']+'-parsed.json',r);return r,es
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 task=sys.argv[1]
 env=native.environment()
 base=D.parent.parent
 env['LEAN_PATH']=str(D/'constructed/lib')+':'+str(base/'constructed/lib')+':'+env['LEAN_PATH']
 began=time.time()
 if task=='controls':
  env['LEAN_PATH']=str(D.parent/'boundary-v4/fixtures')+':'+env['LEAN_PATH']
  cases=[('ordinary-duplicates','none',None,['DupA','DupB'],0),
   ('corrupt-duplicate','bvar','DupB',['DupA','DupB'],1),
   ('unimported-sibling','sibling','ExtraB',['ExtraA','ExtraB'],1),
   ('conflicting-definitions','none',None,['DefA','DefB'],0),
   ('private-names','none',None,['PrivateA','PrivateB'],0)]
  rows=[]
  for name,mutation,target,roots,expected in cases:
   for mode in ['one','audit']:
    chosen=env.copy()
    if target:chosen['DECOUPLED_MUTATE_MODULE']=target
    r,es=cell('qualification-'+name+'-'+mode,[CHECKER,mode,mutation]+roots,60,chosen)
    ok=r['returncode']==expected and not r['malformed_json_lines']
    if expected:ok=ok and roots[-1]in r['rejected']
    rows.append(dict(case=name,mode=mode,qualified=ok,key=r['key']))
  save('controls-terminal.json',dict(complete=all(r['qualified']for r in rows),rows=rows))
  return 0 if all(r['qualified']for r in rows)else 2
 assert json.loads((ROOT/'controls-terminal.json').read_text())['complete']
 frame=json.loads((D/'build-frame.json').read_text());wanted={r['module']for r in frame}
 if task in ['stream','memory','math']:
  if task=='math':
   roots=['Mathlib.Data.Nat.Basic']
   plan=json.loads((base/'cohort-plan.json').read_text())
   wanted=set(plan['cases']['math']['modules'])
  else:roots=['@'+str(D/'roots.txt')]
  if task=='memory':env['DECOUPLED_MEMORY_PROFILE']='1'
  r,es=cell(task,[CHECKER,'audit','none']+roots,1500,env)
  headers={e['module']:set(e['imports'])for e in es if e.get('event')=='module_header'}
  graph_match=task=='math' or (set(headers)==wanted and all(headers[x['module']]==set(x['imports'])for x in frame))
  complete=r['returncode']==0 and set(r['accepted'])==wanted and r['complete_event']is not None and not r['malformed_json_lines']and graph_match
  save(task+'-terminal.json',dict(complete=complete,cell=r,graph_match=graph_match,expected_modules=len(wanted),began_epoch=began))
  return 0 if complete else 2
 if task=='oracle':
  # Earlier exact common artifacts already have complete module-local qualification.
  common=set(json.loads((D/'progress.json').read_text())['reused'])
  old=set(json.loads((base/'progress.json').read_text())['oracle_global'])
  done=common&old
  for p in ROOT.glob('oracle-*-terminal.json'):
   done.update(json.loads(p.read_text())['accepted'])
  pending=[r['module']for r in frame if r['module']not in done]
  if not pending:
   save('oracle-complete.json',dict(complete=True,modules=len(done),reused_qualified_common=len(common&old)));return 0
  chunk=pending[:512];key='oracle-'+str(len(done)).zfill(5)
  r,es=cell(key,[D.parent/'measurement-v1/audited-stream','one','none']+chunk,1400,env)
  # Complete accept events survive an interrupted chunk; no truncated or missing item is accepted.
  accepted=[m for m in r['accepted']if m in chunk]
  complete=r['returncode']==0 and accepted==chunk and not r['malformed_json_lines']
  save(key+'-terminal.json',dict(complete=complete,accepted=accepted,requested=chunk,cell=r,remaining=len(pending)-len(accepted)))
  print(json.dumps(dict(task=key,accepted=len(accepted),remaining=len(pending)-len(accepted))),flush=True)
  return 0 if complete else 2
 raise SystemExit('unknown task')
if __name__=='__main__':raise SystemExit(main())
