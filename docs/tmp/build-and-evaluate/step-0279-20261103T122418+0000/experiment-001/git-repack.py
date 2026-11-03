from pathlib import Path
import os,subprocess,json,gzip,time,shutil,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
before_objects=subprocess.check_output(['git','cat-file','--batch-all-objects','--batch-check=%(objectname)'],cwd=r)
(e/'git-object-ids-before.txt.gz').write_bytes(gzip.compress(before_objects))
before_count=subprocess.check_output(['git','count-objects','-v'],cwd=r,text=True)
def blocks():
 return sum(p.stat().st_blocks*512 for p in(r/'.git/objects').rglob('*')if p.is_file())
before_blocks=blocks();before_disk=shutil.disk_usage('/workspaces')._asdict();start=time.monotonic()
argv=['git','-c','pack.threads=2','repack','-a','-d','--keep-unreachable']
with(e/'git-repack.stdout').open('w')as so,(e/'git-repack.stderr').open('w')as se:
 q=subprocess.run(argv,cwd=r,stdout=so,stderr=se)
after_objects=subprocess.check_output(['git','cat-file','--batch-all-objects','--batch-check=%(objectname)'],cwd=r)
assert q.returncode==0 and set(before_objects.splitlines())<=set(after_objects.splitlines())
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
after_blocks=blocks();out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,returncode=q.returncode,seconds=time.monotonic()-start,object_count_before=len(before_objects.splitlines()),object_count_after=len(after_objects.splitlines()),all_old_objects_retained=True,prune=False,reflog_expiration=False,worktree_changes=False,before_blocks=before_blocks,after_blocks=after_blocks,reclaimed_bytes=before_blocks-after_blocks,before_count=before_count,after_count=subprocess.check_output(['git','count-objects','-v'],cwd=r,text=True),before_disk=before_disk,after_disk=shutil.disk_usage('/workspaces')._asdict())
(e/'git-repack-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
