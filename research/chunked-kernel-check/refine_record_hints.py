"""Refine equality candidates in known interval-certificate families, lexically."""
from pathlib import Path
import os,tarfile,re,json,csv,collections,signal
from classify_shapes import mask,SITES,header,classify
HERE=Path(__file__).resolve().parent
RAW=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
PREFIXES=('OAI/Analysis/PlanarPacking/','OAI/MathematicalPhysics/Transonic/')
DEFINITION=re.compile(r'^(?:noncomputable\s+)?def\s+(\w+)[^\n]*?:\s*(RBox|CBox|PointBox|Box)\s*:=',re.M)
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 signal.alarm(1800)
 layouts=json.loads((HERE/'generated-schema.json').read_text())['record_fields']
 core=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875/lean/OAI/MathematicalPhysics/Transonic/Core.lean').read_text()
 match=re.search(r'structure Box where\n(.*?)\n  deriving',core,re.S)
 layouts['Box']=re.findall(r'^\s+(\w+)\s*:\s*(\w+|ℤ)\s*$',match[1],re.M)
 projections={name:dict(fields) for name,fields in layouts.items()}
 def hint(side,unambiguous):
  h=re.match(r'\s*\(?\s*([A-Za-z_]\w*)\b',side)
  if not h or h[1] not in unambiguous:return None
  typ=unambiguous[h[1]];rest=side[h.end():].strip()
  path=re.fullmatch(r'\)*((?:\.\w+)+)\)*',rest)
  if path:
   for field in path[1].split('.')[1:]:
    typ=projections.get(typ,{}).get(field)
    if typ is None:return None
  elif '.' in rest:return None
  elif rest and any(c in rest for c in ['=','+','-','*','/','^','<','>']):return None
  return typ if typ in projections else None
 rows=[];examples=[];counts=collections.Counter();files=0
 with tarfile.open(RAW/'openai-math-4eaee875.tar.gz','r|gz') as tar:
  for member in tar:
   rel=member.name.split('/',1)[-1].removeprefix('lean/')
   if not member.isfile() or not rel.endswith('.lean') or not rel.startswith(PREFIXES):continue
   text=tar.extractfile(member).read().decode();code=mask(text);sites=list(SITES.finditer(code))
   if not sites:continue
   files+=1;types=collections.defaultdict(set)
   for name,typ in DEFINITION.findall(code):types[name].add(typ)
   unambiguous={name:next(iter(ts)) for name,ts in types.items() if len(ts)==1}
   total=0;bytype=collections.Counter()
   for m in sites:
    target,known=header(code,m.start());cat,_=classify(target,known)
    if cat!='equality_unresolved_type':continue
    total+=1
    # Deliberately narrow: simple application/constant heads, no notation inference.
    eq=target.find('=')
    if eq<0:continue
    candidates=set()
    for side in [target[:eq],target[eq+1:]]:
     typ=hint(side,unambiguous)
     if typ is not None:candidates.add(typ)
    if len(candidates)==1:
     typ=next(iter(candidates));bytype[typ]+=1;counts[typ]+=1
     if len(examples)<12:examples.append(dict(path=rel,target=target[:400],type_hint=typ))
   rows.append(dict(module='.'.join(Path(rel).with_suffix('').parts),source_sites=len(sites),
       equality_headers=total,record_hint_candidates=sum(bytype.values()),
       CBox=bytype['CBox'],RBox=bytype['RBox'],PointBox=bytype['PointBox'],Box=bytype['Box']))
 with (HERE/'record-hint-candidates.csv').open('w') as f:
  w=csv.DictWriter(f,lineterminator='\n',fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 result=dict(prefixes=PREFIXES,files_with_sites=files,source_sites=sum(r['source_sites'] for r in rows),
  equality_headers=sum(r['equality_headers'] for r in rows),record_hint_candidates=sum(counts.values()),
  by_type=dict(counts),global_site_denominator=1354379,
  global_fraction=sum(counts.values())/1354379,
  evidence='lexical type annotations in the same file; known record projections resolved from original schemas; namespace/shadowing not resolved; conditional on successful elaboration',
  semantic_status='not a certified global splittable fraction; automation still demonstrated only on the tested Grid goal',
  examples=examples)
 (HERE/'record-hint-summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
