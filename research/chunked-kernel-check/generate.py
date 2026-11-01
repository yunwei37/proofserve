"""Generate a real Grid equality and record-field subgoals from pinned sources."""
from pathlib import Path
import re,json,os,argparse
HERE=Path(__file__).resolve().parent
RAW=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
ROOT=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875/lean')
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 ap=argparse.ArgumentParser();ap.add_argument('--partition',choices=['flat','components'],default='flat');args=ap.parse_args()
 out=RAW/('prototype' if args.partition=='flat' else 'prototype-components');out.mkdir(exist_ok=True)
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
 # Source-only heuristic: preserve complete explicitly exponential record
 # components; no timing oracle and no trusted mathematical assumption.
 calc=re.search(r'^def PointBox\.calc[^\n]*:=\s*\n\s*⟨([^\n]+)⟩',intervals,re.M).group(1)
 terms=[];stack=[];last=0;closers={')':'(',']':'[','}':'{','⟩':'⟨'}
 for pos,ch in enumerate(calc):
  if ch in '([{⟨':stack.append(ch)
  elif ch in closers:
   assert stack and stack.pop()==closers[ch]
  elif ch==',' and not stack:terms.append(calc[last:pos].strip());last=pos+1
 terms.append(calc[last:].strip())
 assert len(terms)==len(records['PointBox'])
 heavy=[field for (field,_),term in zip(records['PointBox'],terms) if re.search(r'\.exp\b',term)]
 def partition(k):
  if args.partition=='flat' or k==1:return [paths[len(paths)*i//k:len(paths)*(i+1)//k] for i in range(k)]
  blocks=[[p for p in paths if p.startswith('.'+field+'.')] for field in heavy]
  assert len(blocks)<=k
  groups=[[] for _ in range(k)]
  for i,block in enumerate(blocks):groups[i].extend(block)
  cheap=[p for p in paths if not any(p in block for block in blocks)]
  slots=list(range(len(blocks),k)) or list(range(k))
  for i,path in enumerate(cheap):groups[slots[i%len(slots)]].append(path)
  assert all(groups) and sorted(p for g in groups for p in g)==sorted(paths)
  return groups
 for k in [1,2,4,8]:
  groups=partition(k)
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
 (HERE/('generated-schema.json' if args.partition=='flat' else 'generated-components-schema.json')).write_text(json.dumps(dict(
  source_module='OAI.Analysis.PlanarPacking.Grid',original_target=target,
  source_definition=point,record_fields=records,leaf_paths=paths,
  strategy=('structural record equality; split leaves into balanced contiguous conjunctions' if args.partition=='flat' else 'keep source exponential components whole; distribute remaining leaves'),
  **(dict(partition_mode=args.partition,source_component_expressions=dict(zip([f for f,_ in records['PointBox']],terms)),preserved_components=heavy,groups={str(k):partition(k) for k in [1,2,4,8]}) if args.partition=='components' else {}),
  source_is_extracted=True,handwritten_target_numbers=False),indent=2)+'\n')
 # Small generated input is derived from the original public target.
 (HERE/('ChunkBase.lean' if args.partition=='flat' else 'ComponentBase.lean')).write_text('\n'.join(lines)+'\n')
 print('generated',len(paths),'field goals')
if __name__=='__main__':main()
