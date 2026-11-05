#!/usr/bin/env python3
"""One installed-tool external-project cell; original inputs must be built first."""
from pathlib import Path
import argparse,json,os,subprocess,time,threading,csv,shutil,signal
LOCK=Path('/workspaces/.agent-state/gpu-smt-captures/pcore.lock')
ACTIVE=None
def abort(signum,frame):
 if ACTIVE is not None:
  try:(ACTIVE/'cgroup.kill').write_text('1')
  except OSError:pass
 raise SystemExit(128+signum)
signal.signal(signal.SIGTERM,abort)
signal.signal(signal.SIGINT,abort)
def main():
 global ACTIVE
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--source-audit',type=Path,required=True);p.add_argument('--project',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True);p.add_argument('--name',required=True)
 p.add_argument('--upstream-commit',required=True);p.add_argument('--checker-commit',required=True)
 p.add_argument('--workers',type=int,default=4)
 p.add_argument('--preview',action='store_true',help='E8-9 functional preview; not eligible as final system timing')
 p.add_argument('--closure-roots',type=int,default=0)
 p.add_argument('--timeout-seconds',type=int,default=1740,help='Per-command bound; final external window may request a longer uninterrupted native call')
 p.add_argument('--resume',action='store_true',help='Resume an interrupted preview on unchanged product checkpoints')
 a=p.parse_args();assert a.timeout_seconds>0;a.project=a.project.resolve(strict=True);a.out=a.out.resolve()
 assert sorted(os.sched_getaffinity(0))==([8,9]if a.preview else list(range(8))),'preview uses8-9; final uses outer P-core lock and0-7'
 source_audit=json.loads(a.source_audit.read_text())
 expected=set(source_audit['coverage']['covered_modules'])
 compiled={'.'.join(x.relative_to(a.project/'.lake/build/lib/lean').with_suffix('').parts)for x in(a.project/'.lake/build/lib/lean').rglob('*.olean')}
 assert expected and expected<=compiled,('default-source preparation incomplete',sorted(expected-compiled))
 assert not a.resume or a.preview,'final measurement never resumes an interrupted preview'
 a.out.mkdir(parents=True,exist_ok=a.resume)
 cli=(a.prefix/'bin/proofserve').resolve(strict=True);sdk=cli.parents[1]
 metadata=json.loads((sdk/'share/proofserve/bundle.json').read_text())
 assert (a.project/'lean-toolchain').read_text().strip()==metadata['lean_toolchain']
 env=os.environ.copy();env.update(PATH=str(sdk/'bin')+os.pathsep+env.get('PATH',''),LEAN_SYSROOT=str(sdk))
 env.pop('LEAN_PATH',None)
 rows=[]
 if a.resume:
  assert not(a.out/'result.json').exists(),'already complete; never repeat a qualified case'
  for path in sorted(a.out.glob('proofserve*.result.json')):
   old=json.loads(path.read_text())
   assert old['project']==a.name and old['upstream_commit']==a.upstream_commit and old['checker_commit']==a.checker_commit and old['bundle_commit']==metadata['source_commit']
   assert old['returncode']==124 and not old['resource_failure']and not old['disk_failure'],'only bounded preview timeout may resume'
   old=dict(old,cpu_s=None,cpu_accounting_valid=False)
   rows.append(old)
  assert rows,'no interrupted native invocation'
 def run(label,args):
  global ACTIVE
  assert shutil.disk_usage('/workspaces').used/shutil.disk_usage('/workspaces').total<.85,'disk ceiling; no native call started'
  # The independent Python parent owns both the sampled-RSS stop and cgroup.
  current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::')[1].lstrip('/')
  cg=current.parent/('proofserve-o-external-'+str(os.getpid())+'-'+label+'.scope')
  cg.mkdir();(cg/'memory.max').write_text(str(12*1024**3-256*1024**2));(cg/'memory.oom.group').write_text('1')
  def enter():(cg/'cgroup.procs').write_text('0')
  with(a.out/(label+'.stdout')).open('w')as fo,(a.out/(label+'.stderr')).open('w')as fe:
   start=time.monotonic()
   q=subprocess.Popen(['timeout','--signal=TERM','--kill-after=5',str(a.timeout_seconds)]+list(map(str,args)),cwd=a.project,env=env,stdout=fo,stderr=fe,preexec_fn=enter,start_new_session=True)
   ACTIVE=cg
   stop=threading.Event();sample=dict(peak_tree_rss=0,resource_failure=False,disk_failure=False)
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
     rss+=int(Path('/proc/self/stat').read_text().split(') ')[1].split()[21])*os.sysconf('SC_PAGE_SIZE')
     sample['peak_tree_rss']=max(sample['peak_tree_rss'],rss)
     if shutil.disk_usage('/workspaces').used/shutil.disk_usage('/workspaces').total>=.85:
      sample['disk_failure']=True;(cg/'cgroup.kill').write_text('1');return
     if rss>12*1024**3:
      sample['resource_failure']=True;(cg/'cgroup.kill').write_text('1');return
   thread=threading.Thread(target=watch);thread.start()
   _,status,usage=os.wait4(q.pid,0);q.returncode=os.waitstatus_to_exitcode(status)
   wall=time.monotonic()-start;stop.set();thread.join();ACTIVE=None
  row=dict(timing_stage='preview-cpu8-9'if a.preview else 'final-system',final_system_timing_eligible=not a.preview,project=a.name,upstream_commit=a.upstream_commit,bundle_commit=metadata['source_commit'],checker_commit=a.checker_commit,arm=label,repeat=1,returncode=q.returncode,cpu_s=(usage.ru_utime+usage.ru_stime)if q.returncode==0 else None,cpu_accounting_valid=q.returncode==0,wall_s=wall,wait4_peak_rss_kib=usage.ru_maxrss,cgroup_peak_bytes=int((cg/'memory.peak').read_text()),memory_events=(cg/'memory.events').read_text(),**sample)
  rows.append(row);(a.out/(label+'.result.json')).write_text(json.dumps(row,indent=2)+'\n')
  try:cg.rmdir()
  except OSError:pass
  return q.returncode
 native_args=[cli,'check',a.project,'--workers',str(a.workers),'--checkpoint-dir',a.out/'checkpoint','--json']
 if a.closure_roots:native_args+=['--closure-roots',str(a.closure_roots)]
 def completed_segments():
  done=0
  for path in(a.out/'checkpoint').glob('**/segment-*.json'):
   value=json.loads(path.read_text())
   if value.get('exit')==0:done+=1
  return done
 attempt=len(rows)
 while True:
  before=completed_segments()
  native_label='proofserve'if attempt==0 else'proofserve-resume-'+str(attempt)
  code=run(native_label,native_args)
  if code==0:break
  after=completed_segments()
  if not a.preview or code!=124 or rows[-1]['resource_failure']or rows[-1]['disk_failure']or after<=before:
   raise SystemExit('native checker did not complete; raw operational result retained')
  attempt+=1
 receipt=json.loads((a.out/(native_label+'.stdout')).read_text())
 assert receipt['status']=='complete'and receipt['execution_path']=='proofserve-parallel'
 roots=receipt['roots'];accepted=set(receipt['accepted'])
 assert expected<=set(roots),'never accept an unintentionally partial source build as the complete project'
 # Default leanchecker checks each named module while trusting imported proofs.
 # The common local-root set is exact; it is not full-closure checking parity.
 code=run('official-default',[sdk/'bin/lake','env',sdk/'bin/leanchecker','-v']+roots)
 text=(a.out/'official-default.stdout').read_text()
 observed={line.removeprefix('replaying ').strip()for line in text.splitlines()if line.startswith('replaying ')}
 root_equal=code==0 and observed==set(roots) and set(roots)<=accepted
 audit_file=a.out/'audit.json'
 code=run('audit',[cli,'audit',a.project,'--json',audit_file,'--receipt',a.out/'checkpoint/receipt.json'])
 audit=json.loads(audit_file.read_text())if audit_file.exists()else None
 result=dict(resumed_preview=a.resume or attempt>0,native_invocations=attempt+1,complete_native_cost_available=attempt==0,timing_stage='preview-cpu8-9'if a.preview else 'final-system',final_system_timing_eligible=not a.preview,complete=code==0 and root_equal,project=a.name,upstream_commit=a.upstream_commit,bundle=metadata,checker_commit=a.checker_commit,roots=roots,local_root_acceptance_equal=root_equal,native_closure_modules=len(accepted),official_default_modules=len(observed),timing_scope_equal=False,scope_note='ProofServe checks the transitive closure; official default replays named local roots and trusts imports. CPU/wall are user-facing costs, not a speedup over equal proof obligations. Fresh final-environment checks are a distinct protocol, evaluated by the checker matrix.',audit=audit,measurements=rows)
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 with(a.out/'measurements.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for row in rows for k in row)),lineterminator='\n');w.writeheader();w.writerows(rows)
 print(json.dumps(dict(complete=result['complete'],project=a.name,local_root_acceptance_equal=root_equal,native_closure_modules=len(accepted),timing_scope_equal=False)))
if __name__=='__main__':main()
