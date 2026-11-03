from pathlib import Path
import os,json,subprocess,gzip,shutil,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
roots=[r/'bench/lean-source-trace/.lake/build',r/'bench/lean-persistent/.lake/build'];protected=set()
for base in [r,r/'bench/lean-persistent/.lake/packages/lean4export']:
 if base.exists():
  protected.update(str(base/n)for n in subprocess.check_output(['git','-C',str(base),'ls-files','-z']).decode().split('\0')if n)
files=[p for root in roots for p in root.rglob('*')if p.is_file()and not p.is_symlink()and str(p)not in protected]
targets={str(p)for p in files}
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  cmd=(pr/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');assert not any(str(q)in cmd for q in roots)
  for fd in list((pr/'fd').iterdir())+[pr/'exe',pr/'cwd']:
   try:assert os.readlink(fd).removesuffix(' (deleted)')not in targets
   except OSError:pass
  for l in(pr/'maps').read_text().splitlines():
   a=l.split(None,5)
   if len(a)==6:assert a[5]not in targets
 except OSError:pass
records=[];saved=0
for p in files:
 assert any(p.resolve().is_relative_to(q.resolve())for q in roots)
 # These directories contain only compiler outputs; exclude any raw archives/logs/source-input snapshots.
 if p.suffix not in ['.olean','.ilean','.c','.o','.hash','.trace','.ir','.private','.server']and '/bin/'not in str(p):continue
 st=p.stat();rec=dict(path=str(p),bytes=st.st_size,blocks=st.st_blocks*512,nlink=st.st_nlink,mode=st.st_mode,reason='retired generated bench .lake/build output; original source/toolchain/lake configuration retained')
 p.unlink();saved+=st.st_blocks*512 if st.st_nlink==1 else 0;records.append(rec)
(e/'cleanup-bench-generated.json.gz').write_bytes(gzip.compress(json.dumps(records).encode()))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=len(records),reclaimed_lastlink_blocks_bytes=saved,tracked_deleted=0,raw_deleted=0,disk=shutil.disk_usage('/workspaces')._asdict());(e/'cleanup-bench-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
for folder in [r/'bench/lean-source-trace',r/'bench/lean-persistent']:print('RETAINED_SOURCE',[x.name for x in folder.iterdir()if x.name!='.lake'])
