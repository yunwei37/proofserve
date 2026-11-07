from pathlib import Path
import sys,os,csv,gzip,json,subprocess,statistics,concurrent.futures,collections,time,tarfile
raw=Path(sys.argv[1]);repo=Path(sys.argv[2]);archive=Path(sys.argv[3]);out=repo/'data/generation-vs-checking'
os.sched_setaffinity(0,set(range(8,16)))
sys.path.insert(0,str(raw/'python-packages'))
os.environ['TIKTOKEN_CACHE_DIR']=str(raw/'tiktoken-cache')
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
rows=list(csv.DictReader(gzip.open(repo/'data/openai-math-4eaee875/census/modules.csv.gz','rt')))
rows=[r for r in rows if r['source_unit'].endswith('.lean')and r['source_unit']!='lean/lakefile.lean']
assert len(rows)==163096 and len({r['source_unit']for r in rows})==163096
revision='4eaee87548250b2682affda7d05d947c05554bae'
by_source={r['source_unit']:r for r in rows};seen=set()
start=time.monotonic();ratios=[];total_bytes=total_tokens=0;done=0
def encode(row,data):
 text=data.decode('utf-8');tokens=len(enc.encode_ordinary(text))
 return dict(module=row['module'],source_unit=row['source_unit'],bytes=len(data),tokens=tokens)
pending=collections.deque()
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool,gzip.open(out/'tokens.csv.gz','wt',newline='')as f:
 writer=csv.DictWriter(f,fieldnames=['module','source_unit','bytes','tokens'],lineterminator='\n');writer.writeheader()
 def emit():
  global total_bytes,total_tokens,done
  r=pending.popleft().result();writer.writerow(r);total_bytes+=r['bytes'];total_tokens+=r['tokens'];done+=1
  if r['tokens']:ratios.append(r['bytes']/r['tokens'])
  if done%5000==0:
   progress=dict(completed=done,total=163096,bytes=total_bytes,tokens=total_tokens,elapsed_s=time.monotonic()-start)
   (raw/'token-progress.json').write_text(json.dumps(progress)+'\n');print(progress,flush=True)
 with tarfile.open(archive,'r|gz')as tar:
  for member in tar:
   if not member.isfile():continue
   prefix='math-'+revision+'/'
   if not member.name.startswith(prefix):raise ValueError(member.name)
   path=member.name[len(prefix):]
   if path not in by_source:continue
   assert path not in seen;seen.add(path)
   data=tar.extractfile(member).read();assert len(data)==member.size
   pending.append(pool.submit(encode,by_source[path],data))
   if len(pending)>=16:emit()
 assert seen==set(by_source),(len(seen),len(by_source))
 while pending:emit()
result=dict(complete=True,source_revision=revision,tokenizer='tiktoken',tokenizer_version=tiktoken.__version__,encoding='o200k_base',
 tokenization='encode_ordinary, complete UTF-8 file including comments/whitespace; no chat framing',
 modules=done,total_bytes=total_bytes,total_tokens=total_tokens,median_module_bytes_per_token=statistics.median(ratios),
 aggregate_bytes_per_token=total_bytes/total_tokens,elapsed_s=time.monotonic()-start,
 source_scope='original GitHub source archive at pinned revision; excludes lean/lakefile.lean configuration unit')
(raw/'token-summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
