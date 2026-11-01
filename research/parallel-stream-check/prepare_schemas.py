"""Prepare all source/profile-supported >=1s Fin-universal Envelope schemas."""
import csv,json,re
from pathlib import Path
def prepare(out):
 inputs=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/inputs.json').read_text())
 source=Path(inputs['modules']['EnvelopePsiB']['source'])
 text=source.read_text();csv.field_size_limit(10_000_000)
 rows=list(csv.DictReader(Path('/workspaces/repository/research/chunked-kernel-check/large-goal-source-nominations.csv').open()))
 rows=[dict(r,names=r['name'])for r in rows if r['module'].endswith('.EnvelopePsiB')and float(r['cpu_s'])>=1]
 lines=['import OAI.Analysis.Triangular.Envelope.EnvelopePsiB','namespace MEnvelopeStream',
 'open OAI OAI.AtomicTriangular OAI.AtomicTriangular.Interval OAI.AtomicTriangular.FiniteCertificate',
 'set_option maxHeartbeats 2000000','set_option maxRecDepth 20000']
 specs=[];unsupported=[]
 for idx,row in enumerate(rows):
  match=re.search(r'(envelopeExpB\d+_calc)',row['names'])
  if not match:unsupported.append(row);continue
  lemma=match[1]
  m=re.search(r'lemma '+re.escape(lemma)+r' \(j : Fin (\d+)\) : (.*?) := by\s+revert j\s+decide \+kernel',text,re.S)
  if not m or '\n'in m[2]:unsupported.append(row);continue
  n=int(m[1]);body=m[2];ident='b'+str(idx)
  specs.append(dict(id=ident,original_name=row['names'],source_lemma=lemma,n=n,profile_cpu_s=float(row['cpu_s'])))
  lines += [f'abbrev predicate_{ident} (j : Fin {n}) : Prop := {body}',
   f'def rootGoal_{ident} : Prop := ∀ j : Fin {n}, predicate_{ident} j']
  for k in [1,2,4,8]:
   groups=[(i*n//k,(i+1)*n//k)for i in range(k)]
   for i,(lo,hi)in enumerate(groups):
    lines.append(f'def goal_{ident}_{k}_{i} : Prop := ∀ j : Fin {n}, {lo} ≤ j.val → j.val < {hi} → predicate_{ident} j')
   lines.append(f'theorem merge_{ident}_{k} '+' '.join(f'(p{i} : goal_{ident}_{k}_{i})'for i in range(k))+f' : rootGoal_{ident} := by')
   lines+=['  intro j','  have hj := j.isLt']
   for i,(lo,hi)in enumerate(groups):
    lower='(Nat.zero_le _)'if i==0 else f'(Nat.le_of_not_lt h{i-1})'
    if i<k-1:lines += [f'  by_cases h{i} : j.val < {hi}',f'  · exact p{i} j {lower} h{i}']
    else:lines.append(f'  exact p{i} j {lower} hj')
 lines+=['end MEnvelopeStream','']
 out.mkdir(exist_ok=True);(out/'EnvelopeStreamBase.lean').write_text('\n'.join(lines))
 (out/'schemas.json').write_text(json.dumps(dict(source=str(source),specs=specs,unsupported=unsupported,
  qualification='source/profile nomination only until native generator and stream check complete',
  trust='prepared terms are untrusted and rechecked by original kernel in stream'),indent=2)+'\n')
 print('nominated',len(specs),'unsupported',len(unsupported))
if __name__=='__main__':
 import sys;prepare(Path(sys.argv[1]))
