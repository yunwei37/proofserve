from pathlib import Path
import os,ast,re,csv,json,gzip,subprocess,time,resource,urllib.request,tarfile,datetime
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-two-cost-regimes-paper-step.txt').read_text().strip());e=s/'experiment-001'
os.sched_setaffinity(0,{22,23});begin=time.monotonic()
rawdir=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-static');rawdir.mkdir(exist_ok=False)
url='https://codeload.github.com/openai/math/tar.gz/4eaee87548250b2682affda7d05d947c05554bae'
partial=rawdir/'source.tar.gz.partial';archive=rawdir/'source.tar.gz'
with urllib.request.urlopen(url,timeout=180) as response,partial.open('xb') as output:
 while True:
  chunk=response.read(1024*1024)
  if not chunk:break
  output.write(chunk)
partial.rename(archive)
print('DOWNLOADED',archive.stat().st_size,'seconds',time.monotonic()-begin,flush=True)
scanner=r/'workloads/openai-math/scan.py';tree=ast.parse(scanner.read_text())
nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='masks') or (isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SPECIAL' for x in n.targets))]
ns={'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(scanner),'exec'),ns)
pattern=re.compile(r'\bdecide\s*\+\s*kernel\b')
hits=[];maskedhits=[];summaries=[]
mathlib=Path('/workspaces/.agent-state/gpu-smt-workloads/mathlib4341')
pin=subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()
assert pin=='d13f23b723b8a846827a245b89c10fc7d3f11612'
assert not subprocess.check_output(['git','diff','--name-only','HEAD','--','Mathlib'],cwd=mathlib,text=True).strip()
def measure(name,items):
 files=bytes_=positive=occ=rawocc=rawpositive=0
 for path,data in items:
  files+=1;bytes_+=len(data)
  if b'decide' not in data or b'kernel' not in data:continue
  text=data.decode('utf-8');rn=len(pattern.findall(text))
  code=ns['masks'](text)[1];n=len(pattern.findall(code))
  rawocc+=rn;rawpositive+=rn>0
  if n:positive+=1;occ+=n;hits.append(dict(corpus=name,path=path,source_bytes=len(data),decide_plus_kernel=n))
  if rn!=n:maskedhits.append(dict(corpus=name,path=path,raw_occurrences=rn,masked_occurrences=n))
  if files%25000==0:print('PROGRESS',name,files,bytes_,flush=True)
 summary=dict(corpus=name,source_files=files,source_bytes=bytes_,raw_occurrences=rawocc,raw_positive_files=rawpositive,
  masked_occurrences=occ,masked_positive_files=positive,positive_file_fraction=positive/files,
  occurrences_per_decimal_MB=occ/(bytes_/1000000))
 summaries.append(summary);print('CORPUS',summary,flush=True)
measure('Mathlib',((str(p.relative_to(mathlib)),p.read_bytes()) for p in (mathlib/'Mathlib').rglob('*.lean')))
inv=r/'workloads/openai-math/static-4eaee875/files.csv.gz'
with gzip.open(inv,'rt') as f:expected={x['path']:int(x['size']) for x in csv.DictReader(f)}
assert len(expected)==163097
def members():
 seen=set()
 with tarfile.open(archive,'r|gz') as tar:
  for m in tar:
   path=m.name.partition('/')[2]
   if not m.isfile() or path not in expected:continue
   assert path not in seen;seen.add(path)
   data=tar.extractfile(m).read();assert len(data)==expected[path],path
   yield path,data
 assert seen==set(expected),(len(seen),len(expected))
measure('openai/math',members())
assert summaries[1]['source_files']==163097 and summaries[1]['source_bytes']==1785499363
for name,rows in [('lexical-corpus-comparison.csv',summaries),('lexical-positive-files.csv',hits),('masked-versus-raw-files.csv',maskedhits)]:
 with (e/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
j=dict(complete=True,corpora=summaries,density_ratio=summaries[1]['occurrences_per_decimal_MB']/summaries[0]['occurrences_per_decimal_MB'],
 units='decimal MB=1000000 source bytes',pattern=pattern.pattern,mask='exact existing W masks implementation',
 pins=dict(mathlib=pin,openai_math='4eaee87548250b2682affda7d05d947c05554bae'),raw_archive=str(archive),raw_archive_bytes=archive.stat().st_size,
 scope='Mathlib/ subtree and pinned whole openai/math Lean inventory; lexical, not native calls/costs/axiom audits',
 initial_partial_cache_discarded_as_population=True,native_calls=0,root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print('COMPLETE',json.dumps(j),flush=True)
