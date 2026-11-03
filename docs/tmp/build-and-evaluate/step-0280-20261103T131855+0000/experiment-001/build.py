from pathlib import Path
import os,subprocess,time,resource,threading,json,re
r=Path('/workspaces/repository');os.chdir(r);s=Path(Path('/workspaces/.agent-state/gpu-smt-persistence-pmu-memory-root-step.txt').read_text().strip());e=s/'experiment-001'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
current=(r/'docs/paper/main.tex').read_text()
assert 'Checking or Recomputing?' in current and 'Independent Branches for' not in current
assert current.count('\\item[RQ')==4
assert current.count('\\paragraph{System-design implication.}')==4
assert current.count('\\missing{')>=10
assert current.count('\\measured{')>=20 and current.count('\\unproven{')>=1
bib=(r/'docs/paper/references.bib').read_text()
keys=set(re.findall(r'@\w+\{([^,]+),',bib))
cites={k for group in re.findall(r'\\cite\{([^}]+)\}',current) for k in group.split(',')}
assert cites<=keys, cites-keys
out=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-paper');out.mkdir(exist_ok=True)
env=os.environ.copy();env['XDG_CACHE_HOME']='/workspaces/.agent-state/tectonic-cache';env['TMPDIR']=str(out)
cmd=['/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/tectonic','--keep-logs','--keep-intermediates','--outdir',str(out),'main.tex']
def config():
 os.sched_setaffinity(0,{22,23});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
stop=threading.Event();samples=[];start=time.monotonic()
def sample(pid):
 while not stop.is_set():
  todo=[pid];seen=set();rss=0
  while todo:
   p=todo.pop()
   if p in seen:continue
   seen.add(p)
   try:
    rss+=sum(int(x.split()[1])*1024 for x in Path(f'/proc/{p}/status').read_text().splitlines() if x.startswith('VmRSS:'))
    todo.extend(map(int,Path(f'/proc/{p}/task/{p}/children').read_text().split()))
   except FileNotFoundError:pass
  samples.append({'elapsed_s':time.monotonic()-start,'rss_bytes':rss,'pids':sorted(seen)});stop.wait(1)
with (e/'tectonic.stdout').open('w') as so,(e/'tectonic.stderr').open('w') as se:
 child=subprocess.Popen(cmd,cwd=r/'docs/paper',env=env,stdout=so,stderr=se,preexec_fn=config);thread=threading.Thread(target=sample,args=(child.pid,),daemon=True);thread.start()
 try:rc=child.wait()
 finally:stop.set();thread.join()
receipt={'argv':cmd,'returncode':rc,'elapsed_s':time.monotonic()-start,'own_tree_sample_peak_rss_bytes':max(x['rss_bytes'] for x in samples),'compiler_AS_bytes':3*1024**3,'root_share_bytes':4*1024**3,'CPU_affinity':[22,23],'pod':os.uname().nodename,'node':'phobos-vt','output_directory':str(out),'retired':child.poll() is not None,'signal_watchdog_claimed':False,'samples':samples}
(e/'paper-build.json').write_text(json.dumps(receipt,indent=2)+'\n');print('BUILD',{k:v for k,v in receipt.items() if k!='samples'},flush=True)
assert rc==0 and (out/'main.pdf').exists()
log=(out/'main.log').read_text(errors='replace');assert 'Overfull' not in log and 'There were undefined' not in log
for name in ['step-report.md','outer-audit.md']:
 p=s/name;text=p.read_text();text+=f'\n\n## Actual completed verification\n\nRoot reanalysis takes {json.loads((e/"reanalysis.json").read_text())["root_analysis_seconds"]:.3f} s and peaks at {json.loads((e/"reanalysis.json").read_text())["root_analysis_maxrss_kib"]:,} KiB. No native verifier runs. Full Tectonic0.17.0 compilation exits0 in {receipt["elapsed_s"]:.3f} s; sampled own-tree peak is {receipt["own_tree_sample_peak_rss_bytes"]:,} bytes on CPUs22–23, below root4GiB. All citations resolve and no overfull boxes appear; underfull warnings remain. The compiler retires naturally. No new speedup or visual/publication acceptance is claimed.\n';p.write_text(text)
owned=['docs/paper/main.tex','docs/evaluation.md',str(s.relative_to(r))]
check=subprocess.run(['git','diff','--check','--']+owned,text=True,capture_output=True);print('DIFFCHECK',check.returncode,check.stdout,flush=True);assert check.returncode==0
print('READY_TO_COMMIT',s,flush=True)
