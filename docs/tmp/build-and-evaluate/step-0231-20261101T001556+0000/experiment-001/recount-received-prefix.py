from pathlib import Path
import os,ast,re,csv,json,gzip,subprocess,time,resource,urllib.request,tarfile,datetime
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-two-cost-regimes-paper-step.txt').read_text().strip());e=s/'experiment-001'
os.sched_setaffinity(0,{22,23});begin=time.monotonic()
rawdir=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-static')
archive=rawdir/'source.tar.gz.partial'
if not archive.exists():archive=rawdir/'source.tar.gz'
initial_bytes=archive.stat().st_size
class LimitedReader:
 def __init__(self,p,n):self.file=p.open('rb');self.left=n;self.used=0
 def read(self,n=-1):
  n=self.left if n<0 else min(n,self.left)
  v=self.file.read(n);self.left-=len(v);self.used+=len(v);return v
limited=LimitedReader(archive,initial_bytes)
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
 with tarfile.open(fileobj=limited,mode='r|gz') as tar:
  for m in tar:
   path=m.name.partition('/')[2]
   if not m.isfile() or path not in expected:continue
   assert path not in seen;seen.add(path)
   data=tar.extractfile(m).read();assert len(data)==expected[path],path
   yield path,data
   if len(seen)==len(expected):break
 assert seen==set(expected),(len(seen),len(expected))
measure('openai/math',members())
assert summaries[1]['source_files']==163097 and summaries[1]['source_bytes']==1785499363
for name,rows in [('lexical-corpus-comparison.csv',summaries),('lexical-positive-files.csv',hits),('masked-versus-raw-files.csv',maskedhits)]:
 with (e/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
j=dict(complete=True,corpora=summaries,density_ratio=summaries[1]['occurrences_per_decimal_MB']/summaries[0]['occurrences_per_decimal_MB'],
 units='decimal MB=1000000 source bytes',pattern=pattern.pattern,mask='exact existing W masks implementation',
 pins=dict(mathlib=pin,openai_math='4eaee87548250b2682affda7d05d947c05554bae'),raw_archive=str(archive),raw_archive_bytes=initial_bytes,compressed_prefix_bytes_read=limited.used,source_census_complete_archive_may_be_partial=True,
 scope='Mathlib/ subtree and pinned whole openai/math Lean inventory; lexical, not native calls/costs/axiom audits',
 initial_partial_cache_discarded_as_population=True,native_calls=0,root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

# The necessary source census is complete; retire only our redundant download.
import signal
target=str(e/'recount-pinned-source.py');events=[]
for d in Path('/proc').iterdir():
 if not d.name.isdigit():continue
 try:
  argv=(d/'cmdline').read_bytes().split(b'\0')
  if target.encode() not in argv:continue
  assert (d/'status').read_text().split('Uid:',1)[1].split()[0]==str(os.getuid())
  birth=(d/'stat').read_text().rsplit(')',1)[1].split()[19]
  assert (d/'stat').read_text().rsplit(')',1)[1].split()[19]==birth
  os.kill(int(d.name),signal.SIGTERM)
  events.append(dict(pid=int(d.name),birth=birth,action='TERM own redundant archive-download process only',reason='all163097inventory source members independently received/scanned; unrelated trailing archive unnecessary'))
 except FileNotFoundError:pass
(e/'source-download-retirement.json').write_text(json.dumps({'owned_events':events,'raw_prefix_retained':True,'native_jobs_affected':0},indent=2)+'\n')
limited.file.close()
if not archive.exists() and (rawdir/'source.tar.gz').exists():j['raw_archive']=str(rawdir/'source.tar.gz')
j['download_cleanup']='extra full-archive download stopped only after complete source-frame census; retained rawprefix is not a complete archive claim'

(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
print('COMPLETE',json.dumps(j),flush=True)
