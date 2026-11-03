#!/usr/bin/env python3
"""One installed-tool external-project cell; original inputs must be built first."""
from pathlib import Path
import argparse,json,os,subprocess,time,threading,csv
LOCK=Path('/workspaces/.agent-state/gpu-smt-captures/pcore.lock')
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--project',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True);p.add_argument('--name',required=True)
 p.add_argument('--upstream-commit',required=True);p.add_argument('--checker-commit',required=True)
 p.add_argument('--workers',type=int,default=4)
 a=p.parse_args();a.project=a.project.resolve(strict=True);a.out=a.out.resolve()
 assert list(os.sched_getaffinity(0))==list(range(8)),'invoke with flock P-core lock and taskset0-7'
 a.out.mkdir(parents=True,exist_ok=False)
 cli=(a.prefix/'bin/proofserve').resolve(strict=True);sdk=cli.parents[1]
 metadata=json.loads((sdk/'share/proofserve/bundle.json').read_text())
 assert (a.project/'lean-toolchain').read_text().strip()==metadata['lean_toolchain']
 env=os.environ.copy();env.update(PATH=str(sdk/'bin')+os.pathsep+env.get('PATH',''),LEAN_SYSROOT=str(sdk))
 env.pop('LEAN_PATH',None)
 rows=[]
 def run(label,args):
  # The independent Python parent owns both the sampled-RSS stop and cgroup.
  current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::')[1].lstrip('/')
  cg=current.parent/('proofserve-o-external-'+str(os.getpid())+'-'+label+'.scope')
  cg.mkdir();(cg/'memory.max').write_text(str(12*1024**3-256*1024**2));(cg/'memory.oom.group').write_text('1')
  def enter():(cg/'cgroup.procs').write_text('0')
  with(a.out/(label+'.stdout')).open('w')as fo,(a.out/(label+'.stderr')).open('w')as fe:
   start=time.monotonic()
   q=subprocess.Popen(['timeout','--signal=TERM','--kill-after=5','1740']+list(map(str,args)),cwd=a.project,env=env,stdout=fo,stderr=fe,preexec_fn=enter,start_new_session=True)
   stop=threading.Event();sample=dict(peak_tree_rss=0,resource_failure=False)
   def watch():
    while not stop.wait(1):
     rss=0
     try:pids=(cg/'cgroup.procs').read_text().split()
     except OSError:break
     for pid in pids:
      try:
       fields=Path('/proc',pid,'stat').read_text().split(') ')[1].split()
       rss+=int(fields[21])*os.sysconf('SC_PAGE_SIZE')
      except (OSError,ValueError,IndexError):pass
     sample['peak_tree_rss']=max(sample['peak_tree_rss'],rss)
     if rss>12*1024**3-128*1024**2:
      sample['resource_failure']=True;(cg/'cgroup.kill').write_text('1');return
   thread=threading.Thread(target=watch);thread.start()
   _,status,usage=os.wait4(q.pid,0);q.returncode=os.waitstatus_to_exitcode(status)
   wall=time.monotonic()-start;stop.set();thread.join()
  row=dict(project=a.name,upstream_commit=a.upstream_commit,bundle_commit=metadata['source_commit'],checker_commit=a.checker_commit,arm=label,repeat=1,returncode=q.returncode,cpu_s=usage.ru_utime+usage.ru_stime,wall_s=wall,wait4_peak_rss_kib=usage.ru_maxrss,cgroup_peak_bytes=int((cg/'memory.peak').read_text()),memory_events=(cg/'memory.events').read_text(),**sample)
  rows.append(row);(a.out/(label+'.result.json')).write_text(json.dumps(row,indent=2)+'\n')
  try:cg.rmdir()
  except OSError:pass
  return q.returncode
 code=run('proofserve',[cli,'check',a.project,'--workers',str(a.workers),'--checkpoint-dir',a.out/'checkpoint','--json'])
 if code:raise SystemExit('native checker did not complete; raw operational result retained')
 receipt=json.loads((a.out/'proofserve.stdout').read_text())
 assert receipt['status']=='complete'and receipt['execution_path']=='proofserve-parallel'
 roots=receipt['roots'];accepted=set(receipt['accepted'])
 # Default leanchecker checks each named module while trusting imported proofs.
 # The common local-root set is exact; it is not full-closure checking parity.
 code=run('official-default',[sdk/'bin/lake','env',sdk/'bin/leanchecker','-v']+roots)
 text=(a.out/'official-default.stdout').read_text()
 observed={line.removeprefix('replaying ').strip()for line in text.splitlines()if line.startswith('replaying ')}
 root_equal=code==0 and observed==set(roots) and set(roots)<=accepted
 audit_file=a.out/'audit.json'
 code=run('audit',[cli,'audit',a.project,'--json',audit_file,'--receipt',a.out/'checkpoint/receipt.json'])
 audit=json.loads(audit_file.read_text())if audit_file.exists()else None
 result=dict(complete=code==0 and root_equal,project=a.name,upstream_commit=a.upstream_commit,bundle=metadata,checker_commit=a.checker_commit,roots=roots,local_root_acceptance_equal=root_equal,native_closure_modules=len(accepted),official_default_modules=len(observed),timing_scope_equal=False,scope_note='ProofServe checks the transitive closure; official default replays named local roots and trusts imports. CPU/wall are user-facing costs, not a speedup over equal proof obligations. Fresh final-environment checks are a distinct protocol, evaluated by the checker matrix.',audit=audit,measurements=rows)
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 with(a.out/'measurements.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
 print(json.dumps(dict(complete=result['complete'],project=a.name,local_root_acceptance_equal=root_equal,native_closure_modules=len(accepted),timing_scope_equal=False)))
if __name__=='__main__':main()
