"""Generate a real Grid equality and record-field subgoals from pinned sources."""
from pathlib import Path
import re,json,os
HERE=Path(__file__).resolve().parent
RAW=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
ROOT=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875/lean')
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 out=RAW/'prototype';out.mkdir(exist_ok=True)
 intervals=(ROOT/'OAI/Analysis/PlanarPacking/Intervals.lean').read_text()
 records={}
 for m in re.finditer(r'structure (RBox|CBox|PointBox) where\n(.*?)\n  deriving',intervals,re.S):
  records[m[1]]=[tuple(x) for x in re.findall(r'^\s+(\w+)\s*:\s*(\w+|ℤ)\s*$',m[2],re.M)]
 assert [len(records[k]) for k in ['RBox','CBox','PointBox']]==[2,2,5]
 source=(ROOT/'OAI/Analysis/PlanarPacking/Grid.lean').read_text()
 detected=re.search(r'have\s+\w+\s*:\s*(PointBox\.calc\s+(\w+)\.t\s*=\s*\2)\s*:=\s*by decide \+kernel',source)
 if detected is None:raise ValueError('unsupported: no source PointBox.calc equality; use original path')
 target=detected.group(1);point=detected.group(2)
 definition=re.search(r'^def '+re.escape(point)+r' : PointBox := .*$',source,re.M).group()
 lines=['import OAI.Analysis.PlanarPacking.Fejer','import Lean','set_option maxHeartbeats 2000000',
        'set_option maxRecDepth 20000','namespace ChunkBase',
        'open OAI.SharpPlanar.IntegerIntervals OAI.SharpPlanar.IntegerCompact',
        definition, 'def rootGoal : Prop := '+target]
 for name,fields in records.items():
  hs=' '.join(f'(h{i} : a.{f} = b.{f})' for i,(f,t) in enumerate(fields))
  proof='; '.join(['cases a','cases b']+[f'cases h{i}' for i in range(len(fields))]+['rfl'])
  lines.append(f'theorem ext_{name} (a b : {name}) {hs} : a = b := by {proof}')
 def leaves(name,path=''):
  rr=[]
  for f,t in records[name]:
   sub=path+'.'+f
   rr.extend(leaves(t,sub) if t in records else [sub])
  return rr
 paths=leaves('PointBox');assert len(paths)==18
 for k in [1,2,4,8]:
  groups=[paths[len(paths)*i//k:len(paths)*(i+1)//k] for i in range(k)]
  locations={}
  for i,g in enumerate(groups):
   goals=[f'((PointBox.calc {point}.t){p} = {point}{p})' for p in g]
   lines.append(f'def goal_{k}_{i} : Prop := '+' ∧ '.join(goals))
   for j,p in enumerate(g):locations[p]=f'h{i}'+'.2'*j+('.1' if j<len(g)-1 else '')
  def build(name,path):
   a=f'(PointBox.calc {point}.t)'+path;b=point+path
   proof=f'ext_{name} ({a}) ({b})'
   for f,t in records[name]:
    sub=path+'.'+f
    proof+=' ('+(build(t,sub) if t in records else locations[sub])+')'
   return proof
  hs=' '.join(f'(h{i} : goal_{k}_{i})' for i in range(k))
  lines.append(f'theorem merge_{k} {hs} : rootGoal :=\n  '+build('PointBox',''))
 lines+=['end ChunkBase']
 (out/'ChunkBase.lean').write_text('\n'.join(lines)+'\n')
 (HERE/'generated-schema.json').write_text(json.dumps(dict(
  source_module='OAI.Analysis.PlanarPacking.Grid',original_target=target,
  source_definition=point,record_fields=records,leaf_paths=paths,
  strategy='structural record equality; split leaves into balanced contiguous conjunctions',
  source_is_extracted=True,handwritten_target_numbers=False),indent=2)+'\n')
 # Small generated input is derived from the original public target.
 (HERE/'ChunkBase.lean').write_text('\n'.join(lines)+'\n')
 print('generated',len(paths),'field goals')
if __name__=='__main__':main()
