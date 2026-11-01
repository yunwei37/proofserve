"""Untimed extraction of the complete selected AI mathematical project."""
import os,json,tarfile,urllib.request
from pathlib import Path
os.sched_setaffinity(0,{8})
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study')
plan=json.loads((ROOT/'falconer-plan.json').read_text())
expected={p:plan['source_sizes'][m]for m,p in plan['source_paths'].items()}
out=ROOT/'falconer-source';out.mkdir(exist_ok=True)
finished=set()
for path,size in expected.items():
 f=out/path
 if f.exists():
  if f.stat().st_size!=size:raise RuntimeError('partial existing source; preserve before retry: '+path)
  finished.add(path)
if len(finished)!=len(expected):
 url='https://codeload.github.com/openai/math/tar.gz/'+plan['source_revision']
 with urllib.request.urlopen(url,timeout=180)as stream:
  # Python3.13 stream=True avoids retaining 163k TarInfo objects.
  with tarfile.open(fileobj=stream,mode='r|gz',stream=True)as archive:
   for member in archive:
    if not member.isfile():continue
    path=member.name.partition('/')[2]
    if path not in expected or path in finished:continue
    f=out/path;f.parent.mkdir(parents=True,exist_ok=True)
    data=archive.extractfile(member).read()
    if len(data)!=expected[path]:raise RuntimeError('source byte-count mismatch '+path)
    pending=f.with_suffix(f.suffix+'.partial');pending.write_bytes(data);pending.replace(f)
    finished.add(path)
    if len(finished)%250==0:print(json.dumps(dict(extracted=len(finished),expected=len(expected))),flush=True)
    if len(finished)==len(expected):break
if len(finished)!=len(expected):raise RuntimeError('incomplete pinned archive')
(ROOT/'falconer-source-terminal.json').write_text(json.dumps(dict(status='complete',source_revision=plan['source_revision'],
 files=len(finished),bytes=sum(expected.values()),root=str(out),scope='untimed source preparation, originals unchanged'),indent=2))
print((ROOT/'falconer-source-terminal.json').read_text(),flush=True)
