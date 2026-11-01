#!/usr/bin/env python3
"""Freeze existing native labels and compute source-only features. Never starts Lean."""
import os,sys,json,csv,gzip,re,math,importlib.util,collections
from pathlib import Path
os.sched_setaffinity(0,{8})
sys.setrecursionlimit(10000)
REPO=Path('/workspaces/repository')
CAP=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
OUT=Path('/workspaces/.agent-state/gpu-smt-captures/cost-prediction-20261101-v2')
INV=REPO/'workloads/openai-math/static-4eaee875'
SDK=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(REPO/'workloads/openai-math'))
import scan
def lines(path):
 for i,line in enumerate(path.open(),1):
  try:yield i,json.loads(line)
  except json.JSONDecodeError:excluded['partial_json_line']+=1
def writecsv(path,rows):
 if not rows:return
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
excluded=collections.Counter()
source_by_module={};frames={}
for p in [CAP/'build-frame.json',CAP/'scale-study/falconer-project-20261101/build-frame.json']:
 if p.exists():
  for row in json.loads(p.read_text()):
   source_by_module[row['module']]=row['source'];frames[row['module']]=row
winputs=sorted(Path('/workspaces/.agent-state/gpu-smt-captures/workloads').glob('openai4341-noM-*/results.jsonl'))
wrows={};source_repeats=[];freeze=[]
for p in winputs:
 for line,row in lines(p):
  args=row.get('args',[])
  if row.get('lean_memory_option_MiB')!=0 or row.get('threads')!=8 or not row.get('pcore_lock') or row.get('profiled') or row.get('compilation_outputs')!='olean_ilean_c' or row.get('source_exact')is not True:
   excluded['W_incompatible_or_unqualified']+=1;continue
  if any(re.match(r'-M',str(x))for x in args):
   excluded['W_M_flag']+=1;continue
  if row.get('status')!='compile_ok' or row.get('returncode',0)!=0:
   freeze.append(dict(source_file=str(p),source_line=line,module=row.get('module'),status=row.get('status'),
    cpu_observed_s=row.get('user_cpu_s',0)+row.get('system_cpu_s',0),
    wall_observed_s=row.get('wall_s'),label='not completed compiler-cost target; preserve censor/operational status'))
   continue
  mod=row['module'];src=next((str(x)for x in reversed(args)if str(x).endswith('.lean')),None)
  if src:source_by_module[mod]=src
  item=dict(module=mod,source_file=str(p),source_line=line,protocol='W_noM_three_outputs',
   compiler_cpu_s=float(row['user_cpu_s'])+float(row['system_cpu_s']),compiler_wall_s=float(row['wall_s']),
   path=row.get('path',''),status='compile_ok')
  if mod not in wrows:wrows[mod]=item
  else:source_repeats.append(item)
# The committed W sample-cost table fixes primary membership and exact label source.
primary={};frame42={}
for row in csv.DictReader((REPO/'workloads/openai-math/build-planning-4eaee875/phaseA-targets.csv').open()):
 if row['role']=='probability_sample':frame42[row['module']]=row
for row in csv.DictReader((REPO/'workloads/openai-math/noM-original-c-suffix48/sample-costs.csv').open()):
 if row['status']!='completed_cost':continue
 path=Path(row['source_file']);want=int(row['source_line'])
 raw=next(j for i,j in lines(path)if i==want)
 mod=row['module'];args=raw.get('args',[])
 src=next((str(x)for x in reversed(args)if str(x).endswith('.lean')),None)
 if src:source_by_module[mod]=src
 assert raw['lean_memory_option_MiB']==0 and raw['threads']==8 and raw['pcore_lock']and raw['compilation_outputs']=='olean_ilean_c'
 primary[mod]=dict(module=mod,source_file=str(path),source_line=want,protocol='W_noM_three_outputs',
  compiler_cpu_s=float(raw['user_cpu_s'])+float(raw['system_cpu_s']),compiler_wall_s=float(raw['wall_s']),
  path=raw['path'],status='compile_ok')
 wrows[mod]=primary[mod] # Never choose a faster repeat for the primary.
assert len(frame42)==42 and len(primary)==31
allrows=dict(wrows)
for p in [CAP/'measured.jsonl',CAP/'scale-study/falconer-project-20261101/measured.jsonl']:
 for line,row in lines(p):
  if row.get('operation')!='build':continue
  if row.get('returncode')or row.get('sorry_warning')or row.get('affinity')!=list(range(8)):
   excluded['O_failed_or_nonprimary_source_cell']+=1;continue
  mod=row['module'];source_by_module[mod]=row['source']
  if mod in allrows:
   excluded['same_module_repeat_not_independent']+=1;continue
  allrows[mod]=dict(module=mod,source_file=str(p),source_line=line,protocol='O_noM_three_outputs',
   compiler_cpu_s=float(row['user_s'])+float(row['system_s']),compiler_wall_s=float(row['wall_s']),
   path=row['source'],status='compile_ok')
# First source-reconstructed kernel component per module; repeats remain a diagnostic,
# never cross validation rows for the same module.
kernel={};kernel_repeats=[]
for cohort in ['math','compute-grid','compute-amplitudes','ordinary-oai']:
 p=CAP/('timed-constructed-stream-'+cohort+'.stdout')
 for line,row in lines(p):
  if row.get('event')!='module_timing':continue
  item=dict(module=row['module'],kernel_replay_wall_s=row['replay_ns']/1e9,source_file=str(p),source_line=line,protocol='O_stream_component')
  if item['module']not in kernel:kernel[item['module']]=item
  else:kernel_repeats.append(item)
# Load static source-name edges, not runtime import events.
ai_graph=collections.defaultdict(list);ai_sizes={}
with gzip.open(INV/'content/imports.csv.gz','rt')as f:
 for row in csv.DictReader(f):ai_graph[row['module']].append(row['imports'])
with gzip.open(INV/'content/file-metrics.csv.gz','rt')as f:
 for row in csv.DictReader(f):
  m=row['path'][5:-5].replace('/','.');ai_sizes[m]=int(row['bytes'])
roots=[SDK/'src/lean',SDK/'src/lean/lake',Path('/workspaces/.agent-state/gpu-smt-workloads/mathlib4341')]
roots += [x for x in(roots[-1]/'.lake/packages').iterdir()if x.is_dir()]
# The configured public dependency has a checked-in compatibility source receipt.
for row in csv.DictReader((REPO/'workloads/openai-math/rellich-build-context/context.csv').open()):
 roots.append(Path(row['patched_source_directory']))

ORIG=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875/lean')
def resolve(m):
 old=source_by_module.get(m)
 if old and Path(old).is_file():return Path(old)
 if m.startswith('OAI.')or m.startswith('Comparator'):
  p=ORIG/(m.replace('.','/')+'.lean')
  if p.is_file():source_by_module[m]=str(p);return p
 for root in roots:
  p=root/(m.replace('.','/')+'.lean')
  if p.is_file():source_by_module[m]=str(p);return p
 return None
graph={};sizes={};ids={};memo={};depth={};visiting=set();unresolved=set();cycles=set()
def idx(m):
 if m not in ids:ids[m]=len(ids)
 return ids[m]
def deps(m):
 if m in graph:return graph[m]
 if m in ai_graph:
  graph[m]=list(dict.fromkeys(['Init']+ai_graph[m]));sizes[m]=ai_sizes.get(m,0)
 else:
  path=resolve(m)
  if not path:
   graph[m]=[];sizes[m]=0;unresolved.add(m);return []
  text=path.read_text(errors='replace');_,code=scan.masks(text)
  imps=[]
  for mat in scan.IMPORT.finditer(code):
   imps.extend(x for x in re.findall(r"[A-Za-z_][\w'.]*",mat.group(1))if x not in ('all','in'))
  if not re.search(r'(?m)^\s*prelude\b',code):imps.insert(0,'Init')
  graph[m]=list(dict.fromkeys(imps));sizes[m]=path.stat().st_size
 return graph[m]
def closure(m):
 if m in memo:return memo[m]
 if m in visiting:cycles.add(m);return 0
 visiting.add(m);bits=1<<idx(m);level=1
 for n in deps(m):
  if n==m:continue
  bits|=closure(n);level=max(level,depth.get(n,0)+1)
 visiting.remove(m);memo[m]=bits;depth[m]=level
 return bits
DECL=re.compile(r"(?m)^\s*(?:@\[[^\n]*\]\s*)*(?:(?:private|protected|noncomputable|unsafe|partial|local|scoped)\s+)*(theorem|lemma|def|abbrev|instance|opaque|axiom|inductive|structure|class)\b")
features=[]
wanted=sorted(set(allrows)|set(kernel)|set(frame42))
for pos,m in enumerate(wanted):
 path=resolve(m)
 if path is None:
  excluded['missing_source_features']+=1;continue
 text=path.read_text(errors='replace');_,code=scan.masks(text)
 matches=list(DECL.finditer(code));headers=[]
 for i,match in enumerate(matches):
  if match.group(1)not in ('lemma','theorem'):continue
  chunk=code[match.end():matches[i+1].start()if i+1<len(matches)else len(code)]
  headers.append(chunk.split(':=',1)[0].split('where',1)[0])
 shapes={k:sum(bool(re.search(pat,h))for h in headers)/max(1,len(headers))for k,pat in [
  ('goal_eq_fraction',r'(?<![:<>])=(?!=|>)'),('goal_quant_fraction',r'∀|∃|\bforall\b'),
  ('goal_arith_fraction',r'≤|≥|<|>|\bNat\b|\bInt\b|ℕ|ℤ|ℝ'),('goal_logic_fraction',r'∧|∨|↔|→')]}
 marker=len(re.findall(r'\bdecide\s*\+\s*kernel\b|\bnative_decide\b|\bbv_decide\b|\bofReduceBool\b',code))
 nums=list(re.finditer(r'\b[0-9]+\b',code));max_digits=max((len(x.group())for x in nums),default=0)
 ranges=[int(x.group(1))for x in re.finditer(r'\b(?:Finset|List)\.range\s+([0-9]{1,10})\b',code)]
 bits=closure(m);reachable=[];v=bits
 while v:
  low=v&-v;reachable.append(low.bit_length()-1);v-=low
 inverse={v:k for k,v in ids.items()}
 modules=[inverse[i]for i in reachable]
 row=dict(module=m,source_path=str(path),project='.'.join(m.split('.')[:3]if m.startswith('OAI.')else m.split('.')[:2]),
  source_bytes=path.stat().st_size,direct_imports=len(deps(m)),transitive_files=len(modules),
  closure_source_bytes=sum(sizes.get(x,0)for x in modules),import_depth=depth[m],
  unresolved_imports=sum(x in unresolved for x in modules),source_declarations=len(matches),source_theorems=len(headers),
  explicit_kernel_sites=marker,kernel_density_kib=1024*marker/max(1,path.stat().st_size),
  regime=int(marker>0),max_numeral_digits=max_digits,max_range_literal=max(ranges,default=0),
  large_decidable_risk=int(marker>0 and(max_digits>=3 or bool(ranges))),**shapes,
  source_shape_scope='lexical proxies; no elaborated goals or kernel declarations')
 features.append(row)
 if pos%1000==0:print('static feature modules',pos,flush=True)
by={r['module']:r for r in features}
records=[]
for m,f in by.items():
 row=dict(f,primary_42=m in frame42,primary_completed=m in primary,ai_module=m.startswith('OAI.'),
  compiler_cpu_s=allrows[m]['compiler_cpu_s']if m in allrows else '',
  compiler_wall_s=allrows[m]['compiler_wall_s']if m in allrows else '',
  kernel_replay_wall_s=kernel[m]['kernel_replay_wall_s']if m in kernel else '',
  compiler_label_file=allrows[m]['source_file']if m in allrows else '',
  compiler_label_line=allrows[m]['source_line']if m in allrows else '',
  protocol=allrows[m]['protocol']if m in allrows else '',
  kernel_label_file=kernel[m]['source_file']if m in kernel else '',
  primary_cost_available=m in primary)
 records.append(row)
writecsv(OUT/'features-and-costs.csv',records)
writecsv(OUT/'noncompleted-native-records.csv',freeze)
writecsv(OUT/'repeated-source-cells.csv',source_repeats)
writecsv(OUT/'repeated-kernel-cells.csv',kernel_repeats)
(OUT/'dataset-receipt.json').write_text(json.dumps(dict(
 source_revision='4eaee87548250b2682affda7d05d947c05554bae',frozen_git_head=os.popen('cd /workspaces/repository && git rev-parse HEAD').read().strip(),
 primary_frame=42,primary_completed=len(primary),feature_rows=len(records),all_compiler_modules=len(allrows),kernel_modules=len(kernel),
 auxiliary_ai_compiler_modules=sum(m.startswith('OAI.')for m in allrows),native_noncompleted_records=len(freeze),
 excluded=dict(excluded),unresolved_source_imports=sorted(unresolved),cycles=sorted(cycles),
 frozen_raw_sources=list(map(str,winputs)),no_Lean_launched=True,
 scope='current CPU/build target and conditional replay components kept separate; missing primary costs remain missing'),indent=2))
print((OUT/'dataset-receipt.json').read_text(),flush=True)
