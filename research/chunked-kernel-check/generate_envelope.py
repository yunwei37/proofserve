"""Generate the eligible Fin-universal Envelope split, preserving each whole CI.exp per index."""
import argparse,csv,json,re
from pathlib import Path
def generate(directory,source,top_goals):
 csv.field_size_limit(10_000_000)
 goals=list(csv.DictReader(top_goals.open()))
 candidates=[r for r in goals if r['module'].endswith('.EnvelopePsiB') and float(r['cpu_s'])>=1 and 'envelopeExpB' in r['names'] and '_calc.' in r['names']]
 if not candidates:raise ValueError('no measured >=1s Envelope helper')
 selected=max(candidates,key=lambda r:float(r['cpu_s']))
 name=re.search(r'(envelopeExpB\d+_calc)\.',selected['names'])[1]
 pattern=r'lemma '+re.escape(name)+r' \(j : Fin (\d+)\) : (.*?) := by\s+revert j\s+decide \+kernel'
 match=re.search(pattern,source.read_text(),re.S)
 if not match:raise ValueError('supported direct source shape absent')
 n,body=match.groups();n=int(n)
 if '\n' in body or n<=0:raise ValueError('ambiguous source capture')
 lines=['import OAI.Analysis.Triangular.Envelope.EnvelopePsiB','namespace MEnvelopeBase',
  'open OAI OAI.AtomicTriangular OAI.AtomicTriangular.Interval OAI.AtomicTriangular.FiniteCertificate',
  'set_option maxHeartbeats 2000000','set_option maxRecDepth 20000',
  f'def predicate (j : Fin {n}) : Prop := {body}',
  f'def rootGoal : Prop := ∀ j : Fin {n}, predicate j']
 bounds={}
 for k in [1,2,4,8]:
  groups=[(i*n//k,(i+1)*n//k) for i in range(k)];bounds[str(k)]=groups
  for i,(lo,hi) in enumerate(groups):
   lines.append(f'def goal_{k}_{i} : Prop := ∀ j : Fin {n}, {lo} ≤ j.val → j.val < {hi} → predicate j')
  lines.append(f'theorem merge_{k} '+' '.join(f'(p{i} : goal_{k}_{i})' for i in range(k))+' : rootGoal := by')
  lines+=['  intro j','  have hj := j.isLt']
  for i,(lo,hi) in enumerate(groups):
   if i<k-1:lines += [f'  by_cases h{i} : j.val < {hi}',f'  · exact p{i} j (by omega) h{i}']
   else:lines.append(f'  exact p{i} j (by omega) (by omega)')
 lines+=['end MEnvelopeBase','']
 return '\n'.join(lines),dict(original_source=str(source),original_lemma=name,n=n,target_body=body,
   partition_bounds=bounds,selection='largest measured >=1s helper; entire predicate per j retained',
   original_measurement_row=selected,measurement_is_not_curve_denominator=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--top-goals',type=Path,required=True)
 ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 text,schema=generate(args.out,args.source,args.top_goals)
 args.out.mkdir(parents=True,exist_ok=True)
 (args.out/'EnvelopeBase.lean').write_text(text)
 (args.out/'envelope-schema.json').write_text(json.dumps(schema,indent=2)+'\n')
