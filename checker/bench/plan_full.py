#!/usr/bin/env python3
"""Static closure planning only; never runs Lean or changes W outputs."""
from __future__ import annotations
import argparse,collections,csv,heapq,json,re,runpy,statistics,sys
from pathlib import Path
def dump(p,v):p.write_text(json.dumps(v,indent=2)+"\n")
def has_prelude(path):
 depth=0
 with Path(path).open()as source:
  for line in source:
   i=0
   while i<len(line):
    if line.startswith("/-",i):depth+=1;i+=2;continue
    if depth:
     if line.startswith("-/",i):depth-=1;i+=2
     else:i+=1
     continue
    if line.startswith("--",i):break
    if line[i].isspace()or line[i]=="\ufeff":i+=1;continue
    word=re.match(r"[A-Za-z_]+",line[i:])
    if word and word[0]=="module":i+=len(word[0]);continue
    return bool(word and word[0]=="prelude")
 return False

def analyze(manifest,out,repository):
 M=json.loads(manifest.read_text());rows=M["modules"];by={r["module"]:r for r in rows}
 if len(by)!=len(rows):raise ValueError("ambiguous module names")
 out.mkdir(parents=True,exist_ok=False);sys.dont_write_bytecode=True
 lib=runpy.run_path(str(repository/"tools/audit/audit.py"));mask,IMPORT,NAME=(lib[k] for k in ("mask","IMPORT","NAME"))
 sdk=Path(M["lean_binary"]).parent.parent
 artifacts=[Path(p)for p in M["env"]["LEAN_PATH"].split(":")]
 sources=[p.parents[3]for p in artifacts if str(p).endswith("/.lake/build/lib/lean")]+[sdk/"src/lean"]
 graph={n:set(r["deps"])|set(r["external"])|(set() if has_prelude(r["source"]) else {"Init"})for n,r in by.items()}
 unresolved=[];metadata=collections.Counter();done=set(by);todo=list({d for ds in graph.values()for d in ds if d not in graph})
 while todo:
  n=todo.pop()
  if n in done:continue
  done.add(n);rel=Path(*n.split("."))
  src=next((p/rel.with_suffix(".lean")for p in sources if(p/rel.with_suffix(".lean")).is_file()),None)
  if src:
   code=mask(src.read_text());deps={x for m in IMPORT.finditer(code)for x in re.findall(NAME,m[1])if x not in("all","in")}
   if not re.search(r"(?m)^\s*prelude\b",code):deps.add("Init")
   metadata["source"]+=1
  else:
   il=next((p/rel.with_suffix(".ilean")for p in artifacts if(p/rel.with_suffix(".ilean")).is_file()),None)
   if il:
    info=json.loads(il.read_text());deps={i[0]if isinstance(i,list)else i for i in info["directImports"]};metadata["ilean_directImports"]+=1
   else:deps=set();unresolved.append(n);metadata["unresolved_leaf"]+=1
  graph[n]=deps;todo.extend(d for d in deps if d not in done)
 reverse=collections.defaultdict(list);degree={n:len(ds)for n,ds in graph.items()}
 for n,ds in graph.items():
  for d in ds:reverse[d].append(n)
 ready=[n for n,d in degree.items()if not d];heapq.heapify(ready);order=[]
 while ready:
  n=heapq.heappop(ready);order.append(n)
  for q in reverse[n]:
   degree[q]-=1
   if degree[q]==0:heapq.heappush(ready,q)
 cyclic=[n for n,d in degree.items()if d]
 if cyclic:
  dump(out/"unresolved.json",unresolved);dump(out/"cycles.json",cyclic)
  raise ValueError(f"non-DAG static import graph: {len(cyclic)} nodes")
 index={n:i for i,n in enumerate(order)};closures={}
 for n in order:
  bits=1<<index[n]
  for d in graph[n]:bits|=closures[d]
  closures[n]=bits
 roots=sorted(by);empty=[]
 candidates=[n for i,n in enumerate(roots[:-1])if roots[i+1].startswith(n+".")]
 for n in candidates:
  code=mask(Path(by[n]["source"]).read_text());remainder=IMPORT.sub("",code)
  remainder=re.sub(r"(?m)^\s*(?:prelude|module)\s*$","",remainder)
  if not remainder.strip():empty.append(n)
 empties=set(empty);proof=[n for n in roots if n not in empties];strategies=[]
 def evaluate(name,selected,quota):
  covered=tot=maximum=batches=offset=max_new=0;max_roots=[];sizes=[]
  while offset<len(selected):
   while offset<len(selected)and covered>>index[selected[offset]]&1:offset+=1
   if offset==len(selected):break
   stop=min(len(selected),offset+quota);batch=[n for n in selected[offset:stop]if not(covered>>index[n]&1)]
   bits=0
   for n in batch:bits|=closures[n]
   size=bits.bit_count();max_new=max(max_new,(bits&~covered).bit_count());sizes.append(size);tot+=size;batches+=1
   if size>maximum:maximum=size;max_roots=batch
   covered|=bits;offset=stop
  missing=[n for n in roots if not(covered>>index[n]&1)and n not in empties]
  row=dict(strategy=name,root_limit=quota,requested_source_modules=len(roots),planned_proof_roots=len(selected),
   lexical_import_only_assumptions=len(empty),batches=batches,max_closure_modules=maximum,sum_closure_modules=tot,
   sum_over_163097=tot/len(roots),unique_closure_modules=covered.bit_count(),omitted_nonempty_roots=len(missing),
   max_new_modules_per_batch=max_new,max_batch_roots=max_roots[:8],batch_p50=statistics.median(sizes)if sizes else 0,unresolved_external_leaves=len(unresolved))
  strategies.append(row)
 evaluate("unexpanded_lexical_order_500",roots,500)
 evaluate("compiled_empty_assumption_order_500",proof,500)
 evaluate("compiled_empty_assumption_order_1",proof,1)
 terminal=[n for n in proof if not any(q in by and q not in empties for q in reverse[n])]
 terminal.sort(key=lambda n:(-closures[n].bit_count(),n));terminal_set=set(terminal)
 ordered=terminal+[n for n in reversed(order)if n in by and n not in empties and n not in terminal_set]
 evaluate("largest_terminal_closure_first_1",ordered,1)
 source_degree={n:sum(d in by for d in graph[n])for n in by}
 source_ready=[n for n,d in source_degree.items()if not d];heapq.heapify(source_ready);source_order=[]
 while source_ready:
  n=heapq.heappop(source_ready)
  if n not in empties:source_order.append(n)
  for child in reverse[n]:
   if child not in source_degree:continue
   source_degree[child]-=1
   if source_degree[child]==0:heapq.heappush(source_ready,child)
 if len(source_order)!=len(proof):raise ValueError("source-only dependency order is incomplete")
 evaluate("dependency_order_500",source_order,500)

 context_rows=[]
 for root,count in collections.Counter(r["root"]for r in rows).items():
  requested=sorted(r["module"]for r in rows if r["root"]==root)
  bits=0
  for n in requested:bits|=closures[n]
  ident="source-context-"+str(len(context_rows))
  (out/(ident+"-roots.txt")).write_text("\n".join(requested)+"\n")
  context_rows.append(dict(context=ident,source_compile_root=root,requested_roots=count,
    static_closure_modules=bits.bit_count(),request_file=ident+"-roots.txt",
    execution_environment="shared manifest toolchain/options/search-path"))
 dump(out/"contexts.json",context_rows)

 import_only_contexts=sorted([dict(module=n,static_context_modules=closures[n].bit_count())for n in empty],key=lambda r:(-r["static_context_modules"],r["module"]))
 dump(out/"import-only-contexts.json",import_only_contexts)
 max_import_only=max((r["static_context_modules"]for r in import_only_contexts),default=0)
 for row in strategies:row["max_import_only_context_modules"]=max_import_only
 costs=[dict(name="Nat.Basic_loaded_preview_1worker",modules=1330,cpu_s=83.089953,rss_gib=1757626368/1024**3),
  dict(name="whole_Mathlib_loaded_scale_4workers",modules=10744,cpu_s=1860.420947,rss_gib=8133361664/1024**3),
  dict(name="SubexponentialSAT_prototype",modules=14721,cpu_s=3399.302946,rss_gib=14.73128890991211)]
 rates=[c["cpu_s"]/c["modules"]for c in costs];memory=[c["rss_gib"]/c["modules"]for c in costs]
 union=0
 for n in roots:union|=closures[n]
 unique=union.bit_count()
 current=next(r for r in strategies if r["strategy"]=="dependency_order_500")
 strategies.append(dict(strategy="dependency_completed_module_certificates_500",root_limit=500,
  requested_source_modules=len(roots),planned_proof_roots=len(proof),
  lexical_import_only_assumptions=len(empty),batches=current["batches"],
  max_closure_modules=current["max_closure_modules"],max_new_modules_per_batch=current["max_new_modules_per_batch"],sum_closure_modules=unique,
  sum_over_163097=unique/len(roots),unique_closure_modules=unique,omitted_nonempty_roots=0,
  max_batch_roots=current["max_batch_roots"],batch_p50=current["batch_p50"],
  unresolved_external_leaves=len(unresolved),
  interpretation="sum counts first kernel replay only; import loads still total "+str(current["sum_closure_modules"]),
  import_load_module_entries=current["sum_closure_modules"]))

 for row in strategies:
  row["max_import_only_context_modules"]=max_import_only
  row.update(cpu_hours_low=row["sum_closure_modules"]*min(rates)/3600,cpu_hours_high=row["sum_closure_modules"]*max(rates)/3600,
   ideal_8worker_wall_hours_high=row["sum_closure_modules"]*max(rates)/3600/8,
   observed_2x_wall_hours_high=row["sum_closure_modules"]*max(rates)/3600/2,
   linear_peak_gib_high=row["max_closure_modules"]*max(memory))
  row["linear_empty_context_gib_high"]=max_import_only*max(memory)
  row["design_fails_threshold"]=row["observed_2x_wall_hours_high"]>72 or row["linear_peak_gib_high"]>53 or row["linear_empty_context_gib_high"]>53
 summary=dict(classification="static planning estimate; no final timing",source_revision=M["source_revision"],
  source_modules=len(rows),unique_module_names=len(by),source_compile_roots=dict(collections.Counter(r["root"]for r in rows)),
  build_environment_contexts=1,context_meaning="one pinned toolchain/options/search-path; two --root source mappings; unique module names",
  source_compile_context_groups=context_rows,context_requires_final_artifact_binding=True,nodes=len(graph),edges=sum(map(len,graph.values())),external_metadata=dict(metadata),
  unresolved_external_modules=unresolved,lexical_import_only_count=len(empty),lexical_empty_is_not_kernel_qualification=True,
  calibration=costs,strategy_rows=strategies,decision="planning only; unresolved imports and changed build contexts require recomputation")
 dump(out/"summary.json",summary);dump(out/"lexical-empty.json",empty);dump(out/"root-lists.json",dict(original=roots,proof=proof,largest_first=ordered))
 with(out/"strategies.csv").open("w")as f:
  fields=list(dict.fromkeys(k for row in strategies for k in row if k!="max_batch_roots"));w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(strategies)
 dump(out/"graph.json",{n:sorted(ds)for n,ds in graph.items()})
 print(json.dumps({k:v for k,v in summary.items()if k!="strategy_rows"},indent=2));print(json.dumps(strategies,indent=2))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--manifest",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
 p.add_argument("--repository",type=Path,default=Path(__file__).resolve().parents[2]);a=p.parse_args();analyze(a.manifest,a.out,a.repository)
