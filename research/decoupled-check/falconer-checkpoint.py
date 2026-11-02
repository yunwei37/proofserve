#!/usr/bin/env python3
"""One native checkpoint segment, or bounded qualification; outputs stay on PVC."""
import os,json,sys,time,importlib.util
from pathlib import Path
D=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
O=D/'checkpoint-recheck-v2'
spec=importlib.util.spec_from_file_location('n',D/'native_project.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=O
def events(key):
 es=[];bad=[]
 for i,s in enumerate((O/(key+'.stdout')).read_text().splitlines()):
  if not s.startswith('{'):continue
  try:es.append(json.loads(s))
  except ValueError:bad.append(i)
 return es,bad
def write(name,data):
 p=O/name;t=p.with_suffix('.pending')
 with t.open('w')as f:json.dump(data,f,indent=2);f.flush();os.fsync(f.fileno())
 t.replace(p)
def env():
 e=n.environment();e['LEAN_PATH']=str(O)+':'+str(D/'constructed/lib')+':'+str(D.parent.parent/'constructed/lib')+':'+e['LEAN_PATH'];return e
def runpart(key,roots,e,previous=None,quota=500,mutation='none'):
 chosen=e.copy();base_mod='Verified'+key.replace('-','_');mod=base_mod;attempt=0
 while(O/(mod+'.olean')).exists():
  attempt+=1;mod=base_mod+'Retry'+str(attempt)
 chosen.update(DECOUPLED_CHECKPOINT_OUTPUT=str(O/(mod+'.olean')),DECOUPLED_CHECKPOINT_MODULE=mod,DECOUPLED_SEGMENT_MODULES=str(quota))
 if previous:chosen['DECOUPLED_CHECKPOINT_INPUT']=previous
 r=n.run(key,[O/'checkpoint-audit','audit',mutation]+roots,1400,sys.argv[1]!='controls',env=chosen)
 es,bad=events(r['key'])
 checkpoint=next((x for x in reversed(es)if x.get('event')=='checkpoint'),None)
 complete=next((x for x in reversed(es)if x.get('event')=='complete'),None)
 row=dict(previous_snapshot=previous,quota_modules=quota,cell=r,accepted=[x['module']for x in es if x.get('event')=='accept'],rejected=[x['module']for x in es if x.get('event')=='reject'],checkpoint=checkpoint,complete=complete,malformed=bad,snapshot=mod if checkpoint else None)
 write(r['key']+'-terminal.json',row);return row
def main():
 if sys.argv[1]!='controls':assert sorted(os.sched_getaffinity(0))==list(range(8))
 if sys.argv[1]=='controls':
  e=env();e['LEAN_PATH']=str(D.parent/'boundary-v4/fixtures')+':'+e['LEAN_PATH']
  cases=[('duplicates','none',None,['DupA','DupB'],0),('bad_duplicate','bvar','DupB',['DupA','DupB'],1),('sibling','sibling','ExtraB',['ExtraA','ExtraB'],1),('definitions','none',None,['DefA','DefB'],0),('private','none',None,['PrivateA','PrivateB'],0)]
  results=[]
  for tag,mutation,target,roots,expected in cases:
   chosen=e.copy()
   if target:chosen['DECOUPLED_MUTATE_MODULE']=target
   previous=None;accepted=[];last=None
   for part in range(6):
    last=runpart('control_'+tag+'_'+str(part),roots,chosen,previous,1,mutation)
    accepted+=last['accepted']
    if last['cell']['returncode']or last['complete']:break
    assert last['checkpoint']and not last['malformed']
    previous=last['snapshot']
   ok=not last['malformed']and last['cell']['returncode']==expected
   if expected:ok=ok and roots[-1]in last['rejected']
   else:ok=ok and last['complete']is not None and set(roots)<=set(accepted)
   results.append(dict(case=tag,qualified=ok,parts=part+1,last_key=last['cell']['key']))
   if not ok:break
  write('checkpoint-controls.json',dict(complete=len(results)==5 and all(x['qualified']for x in results),results=results))
  return 0 if len(results)==5 and all(x['qualified']for x in results)else 2
 assert json.loads((O/'checkpoint-controls.json').read_text())['complete']
 # Independent restarts read only successful prior segment terminals.
 tag='math-segment'if sys.argv[1]=='math-segment'else'segment'
 prior=[]
 for p in sorted(O.glob(tag+'-*-terminal.json')):
  v=json.loads(p.read_text())
  if v['cell']['returncode']==0 and not v['malformed']and(v['checkpoint']or v['complete']):prior.append(v)
 if prior and prior[-1]['complete']:print('already complete');return 0
 previous=prior[-1]['snapshot']if prior else None
 number=len(prior)
 roots=['Mathlib.Data.Nat.Basic']if tag=='math-segment'else['@'+str(D/'roots.txt')]
 row=runpart(tag+'-'+str(number).zfill(3),roots,env(),previous,500)
 return 0 if row['cell']['returncode']==0 and not row['malformed']and(row['checkpoint']or row['complete'])else 2
if __name__=='__main__':raise SystemExit(main())
