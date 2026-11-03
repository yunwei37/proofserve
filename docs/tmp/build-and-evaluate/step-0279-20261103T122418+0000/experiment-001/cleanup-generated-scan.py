from pathlib import Path
import os,subprocess,json,gzip,collections,shutil,stat,datetime
os.sched_setaffinity(0,{22,23})
r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-native427-20261017-recovery')
s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
old=json.loads(gzip.decompress((r/'docs/tmp/build-and-evaluate/step-0268-20261102T190628+0000/experiment-001/cleanup-candidate-inventory.json.gz').read_bytes()))
protected=set()
for root in [r]+[p.parent for p in b.rglob('.git')]:
 try:
  for n in subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split('\0'):
   if n:protected.add(str(root/n))
 except subprocess.CalledProcessError:pass
candidates={}
def add(p,reason):
 if str(p)in protected or p.is_symlink()or not p.is_file():return
 st=p.stat();candidates[str(p)]={'path':str(p),'bytes':st.st_size,'blocks':st.st_blocks*512,'dev':st.st_dev,'ino':st.st_ino,'nlink':st.st_nlink,'mtime_ns':st.st_mtime_ns,'reason':reason}
for x in old['builds']:
 root=Path(x['path'])
 for dp,dn,fn in os.walk(root):
  for n in fn:
   p=Path(dp)/n
   if p.suffix in ['.olean','.ilean','.private','.server','.ir','.o','.a','.so','.c','.bc','.hash','.trace'] or '/bin/'in str(p):
    add(p,'retired reproducible Lean build cache; source and raw archives retained')
lib=b/'goedel427/lean-4.27.0-linux/lib'
for dp,dn,fn in os.walk(lib):
 for n in fn:add(Path(dp)/n,'retired stock Lean4.27.0 distribution library; pinned source/version/build commands retained')
# Other historical executable/object outputs: magic rather than names or suffix.
for root in [b,r/'artifacts']:
 for dp,dn,fn in os.walk(root):
  dn[:]=[n for n in dn if n!='.git']
  for n in fn:
   p=Path(dp)/n
   if str(p)in candidates or str(p)in protected or p.is_symlink():continue
   st=p.stat()
   if st.st_size<100000:continue
   try:
    with p.open('rb')as f:magic=f.read(8)
    if magic.startswith(b'\x7fELF'):add(p,'retired reproducible ELF executable/library/object; historical source/build logs and results retained')
    elif p.suffix in ['.rlib','.rmeta'] and ('/target/'in str(p)):add(p,'retired reproducible Rust target cache')
   except OSError:pass
rows=list(candidates.values())
# Inspect every currently visible command, fd, executable, cwd and mapped file without printing command data.
live=[]
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  cmd=(pr/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
  if any(x in cmd for x in [str(b),str(r/'artifacts')]):live.append((pr.name,'command refers to target root'))
  for f in [pr/'exe',pr/'cwd']+list((pr/'fd').iterdir()):
   try:
    name=os.readlink(f).removesuffix(' (deleted)')
    if name in candidates:live.append((pr.name,name))
   except OSError:pass
  for line in (pr/'maps').read_text().splitlines():
   name=line.split(None,5)[-1] if len(line.split(None,5))==6 else ''
   if name in candidates:live.append((pr.name,name))
 except (OSError,PermissionError):pass
assert not live,live
# Exact inventory protects every Git-tracked path, including nested checkout sources.
(e/'cleanup-generated-candidates.json.gz').write_bytes(gzip.compress(json.dumps(rows).encode()))
(e/'cleanup-protected-tracked-paths.txt.gz').write_bytes(gzip.compress(('\n'.join(sorted(protected))+'\n').encode()))
groups=collections.Counter()
for x in rows:groups[x['reason']]+=x['blocks']
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_files':len(rows),'candidate_path_blocks':sum(x['blocks']for x in rows),'reasons':dict(groups),'tracked_protected':len(protected),'live_conflicts':live,'executed':False,'disk':shutil.disk_usage('/workspaces')._asdict()}
(e/'cleanup-generated-preflight.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt),flush=True)
