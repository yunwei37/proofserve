#!/usr/bin/env python3
"""Finite lock-per-task continuation. No missing artifact becomes a kernel verdict."""
import argparse,csv,importlib.util,json,os,subprocess,sys,time
from pathlib import Path
R=Path('/workspaces/repository');OWN=R/'research/decoupled-check'
B=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
O=B/'whole-library-20261102';F=B/'scale-study/falconer-project-20261101'
GROUPS=['OAI.Combinatorics.Ramsey','OAI.Analysis.MutuallyUnbiased','OAI.Analysis.PlanarPacking','OAI.MathematicalPhysics.Transonic','OAI.Algorithms.SubexponentialSAT']
def atomic(p,v):
 t=p.with_suffix('.pending')
 with t.open('w')as f:json.dump(v,f,indent=2);f.flush();os.fsync(f.fileno())
 t.replace(p)
def state(cohort):
 p=O/(cohort+'-state.json')
 return json.loads(p.read_text())if p.exists()else dict(cohort=cohort,windows=0,checks=0,
    accepted=[],built=[],blocked={},source_failures={},snapshot=None,terminal=False)
def append(v):
 with(O/'ledger.jsonl').open('a')as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
def data():
 frame=json.loads((O/'frame.json').read_text());return frame,{v['module']:v for v in frame}
def available(m):return O.joinpath('lib',*m.split('.')).with_suffix('.olean').exists()
def events(key):
 out=[];bad=[]
 for i,line in enumerate((O/(key+'.stdout')).read_text().splitlines()):
  if not line.startswith('{'):continue
  try:out.append(json.loads(line))
  except ValueError:bad.append(i)
 return out,bad
def window(cohort):
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 spec=importlib.util.spec_from_file_location('n',O/'native_whole.py')
 n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=O
 assert(O/'prepared.json').exists()
 frame,byname=data();selected=[v for v in frame if cohort=='all'or v['cohort']==cohort]
 wanted={v['module']for v in selected};s=state(cohort);assert not s['terminal']
 s['windows']+=1;start=time.monotonic()
 env=n.environment();env.update(LEAN_PATH=str(O/'lib'),TMPDIR=str(O/'tmp'))
 ready=[v['module']for v in selected if available(v['module'])and v['module']not in s['blocked']and v['module']not in s['source_failures']]
 if not(set(ready)-set(s['accepted'])):
  needed=set()
  def include(m):
   if m in needed:return
   needed.add(m)
   for q in byname[m]['imports']:
    if q in byname:include(q)
  decided=set(s['accepted'])|set(s['blocked'])|set(s['source_failures'])
  for v in selected:
   if v['module']not in decided:include(v['module'])
  built=0;attempted=0
  for v in frame:
   m=v['module']
   if m not in needed or available(m)or m in s['blocked']or m in s['source_failures']:continue
   missing=[q for q in v['imports']if not available(q)]
   if missing:
    s['blocked'][m]=dict(reason='missing_or_failed_import_artifact',imports=missing);continue
   if built>=500 or time.monotonic()-start>600:break
   output=O.joinpath('lib',*m.split('.')).with_suffix('.olean');output.parent.mkdir(parents=True,exist_ok=True)
   root=O/'sources'/v['source_root']
   c=n.run(cohort+'-build-'+str(s['windows'])+'-'+str(attempted),
     [n.SDK/'bin/lean','--root='+str(root),'-j8','-DautoImplicit=false','-o',output,O/'sources'/v['path']],
     600,True,env=env,cwd=root)
   attempted+=1
   text=(O/(c['key']+'.stdout')).read_text(errors='replace')+(O/(c['key']+'.stderr')).read_text(errors='replace')
   success=c['returncode']==0 and output.exists()
   append(dict(operation='source_production',cohort=cohort,module=m,source_success=success,
               sorry_warning="declaration uses 'sorry'"in text,cell=c))
   if success:s['built'].append(m);built+=1
   else:
    s['source_failures'][m]=dict(key=c['key'],returncode=c['returncode'],
        reason='source_compiler_error_or_operational_censor_not_kernel_rejection')
    for p in output.parent.glob(output.stem+'.*'):
     backup=O/'failed-source-artifacts'/c['key']/p.name;backup.parent.mkdir(parents=True,exist_ok=True);p.rename(backup)
   atomic(O/(cohort+'-state.json'),s)
  ready=[v['module']for v in selected if available(v['module'])and v['module']not in s['blocked']and v['module']not in s['source_failures']]
  classified=set(s['accepted'])|set(s['blocked'])|set(s['source_failures'])
  s['terminal']=wanted<=classified
  s['status']='incomplete_missing_typed_inputs'if s['terminal']else'source_production_progress'
  atomic(O/(cohort+'-state.json'),s);return 0
 roots=O/(cohort+'-roots-'+str(s['checks']).zfill(5)+'.txt');roots.write_text('\n'.join(ready)+'\n')
 chosen=env.copy();mod='Whole'+cohort.replace('.','_')+str(s['checks']).zfill(5);suffix=0
 while(O/(mod+'.olean')).exists():suffix+=1;mod='Whole'+cohort.replace('.','_')+str(s['checks']).zfill(5)+'Attempt'+str(suffix)
 chosen.update(DECOUPLED_CHECKPOINT_OUTPUT=str(O/(mod+'.olean')),DECOUPLED_CHECKPOINT_MODULE=mod,DECOUPLED_SEGMENT_MODULES='500')
 if s['snapshot']:chosen['DECOUPLED_CHECKPOINT_INPUT']=s['snapshot']
 chosen['LEAN_PATH']=str(O)+':'+str(O/'lib')
 c=n.run(cohort+'-check-'+str(s['checks']).zfill(5),[O/'checkpoint-audit','audit','none','@'+str(roots)],1400,True,env=chosen)
 es,bad=events(c['key']);accepted=[v['module']for v in es if v.get('event')=='accept']
 reject=[v for v in es if v.get('event')=='reject']
 cp=next((v for v in reversed(es)if v.get('event')=='checkpoint'),None)
 done=next((v for v in reversed(es)if v.get('event')=='complete'),None)
 valid=c['returncode']==0 and not bad and not reject and bool(cp or done)
 append(dict(operation='kernel_check',cohort=cohort,cell=c,valid=valid,accepted=accepted,
   rejected=reject,malformed=bad,checkpoint=cp,complete=done,previous_snapshot=s['snapshot'],snapshot=mod if cp else None))
 s['checks']+=1
 if valid:
  s['accepted']=sorted(set(s['accepted'])|set(accepted))
  if cp:
   s['snapshot']=mod;link=O/'lib'/(mod+'.olean')
   if not link.exists():os.link(O/(mod+'.olean'),link)
  s['terminal']=wanted<=set(s['accepted']);s['status']='complete_all_source_ids'if s['terminal']else'kernel_check_progress'
 else:
  s['terminal']=True;s['status']='native_incomplete_partition_or_repair_required'
  s['failure']=dict(key=c['key'],returncode=c['returncode'],reject=reject,malformed=bad)
 atomic(O/(cohort+'-state.json'),s);return 0 if valid else 2
def reduce():
 frame,_=data();source={v['module']for v in frame};accepted=set();costs=[]
 for line in(O/'ledger.jsonl').read_text().splitlines()if(O/'ledger.jsonl').exists()else[]:
  v=json.loads(line);c=v['cell']
  if v['operation']=='kernel_check'and v['valid']:accepted.update(v['accepted'])
  costs.append(dict(key=c['key'],operation=v['operation'],cohort=v['cohort'],returncode=c['returncode'],
      wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],peak_rss_kib=c['peak_rss_kib'],
      valid=v.get('valid',v.get('source_success',False)),native_accept_events=len(v.get('accepted',[]))))
 cover=[]
 for group in GROUPS+['remainder']:
  names={v['module']for v in frame if v['cohort']==group}
  cover.append(dict(cohort=group,source_modules=len(names),kernel_accepted_source_modules=len(names&accepted),missing=len(names-accepted)))
 for filename,rows in [('whole-library-coverage.csv',cover),('whole-library-segments.csv',costs)]:
  if rows:
   with(OWN/filename).open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
 checks=[v for v in costs if v['operation']=='kernel_check'];cpu=sum(v['cpu_s']for v in checks)
 text='# Whole-library native check: actual progress\n\nReview: 自审. P0–7/shared flock/no Lean -M/external11.5GiB child cgroup/512MiB parent reserve.\n\n'
 status=dict(source_modules=len(source),accepted_source_ids=len(source&accepted),accepted_dependency_ids=len(accepted-source),
    missing_source_ids=len(source-accepted),native_check_attempts=len(checks),
    kernel_wall_s=sum(v['wall_s']for v in checks),kernel_cpu_s=cpu,kernel_cpu_h=cpu/3600,
    kernel_peak_rss_gib=max((v['peak_rss_kib']for v in checks),default=0)/1024**2,complete=source<=accepted)
 valid_checks=[v for v in costs if v['operation']=='kernel_check'and v['valid']]
 source_attempts=[v for v in costs if v['operation']=='source_production']
 source_failures=sum(not v['valid']for v in source_attempts)
 current=checks[-1]['key']if checks else 'not_started'
 minimum=(len(source-accepted)+499)//500
 text+=f'**Accepted source: {len(source&accepted)} / {len(source)}; certified dependencies: {len(accepted-source)}; kernel CPU: {cpu/3600:.6f} h; current check: {current} (attempt {len(checks)}, successful {len(valid_checks)}); remaining: at least {minimum} source-equivalent500-module segments.**\n\n'
 text+='Missing typed inputs, new dependencies, resource failures and repeated work prevent a credible total-segment or ETA point estimate. The322-type number is only a source-count lower bound, not an extrapolated completion promise.\n\n'
 text+='\n'.join('- '+k+': '+str(v)for k,v in status.items())+'\n\n'
 text+=f'- source_failures_or_censors: {source_failures}\n'
 if(O/'all-state.json').exists():
  current_state=json.loads((O/'all-state.json').read_text())
  text+=f'- dependency_blocked_source_modules: {len(current_state["blocked"])}\n'
 distribution=OWN/'whole-library-source-error-distribution.csv'
 if distribution.exists():
  text+='\n## Source error classification (all retained logs)\n\n'
  for row in csv.DictReader(distribution.open()):
   text+='- '+row['category']+': '+row['count']+'\n'
  text+='These are producer/import configuration and data-layout errors, not qualified proof rejections. See whole-library-source-errors.md.\n\n'
 text+='All costs are observed prefixes until every source ID and required native dependency is covered. No claim of validating8.3–41.6CPUh is made from partial data. LatestWsource32 scenarios207.894666–630.701677construction/10.826785–41.839086modeled streamCPUh remain separate. Source production for missing typed inputs is recorded separately. Native snapshots include only successful preceding certification; startup/reload/export/exit are included. Checkpoint frequency does not bound live environment size: failure at12GiB requires partitioning, not merely a smaller quota. Native failures/timeouts/memory events remain raw, not false mathematical verdicts.\n\n'
 for p in sorted(O.glob('*-state.json')):
  s=json.loads(p.read_text())
  if p.name!=s['cohort']+'-state.json':continue
  text+='- '+s['cohort']+': '+s.get('status','pending')+'; source errors/censors='+str(len(s['source_failures']))+'; blocked='+str(len(s['blocked']))+'.\n'
 text+='\nRawPVC: '+str(O)+'. Commands: whole-library-run.py reduce; queue --cohort all; window --cohort <directory>. See whole-library-plan.md.\n'
 (OWN/'whole-library-progress.md').write_text(text);atomic(O/'reduced.json',status);return status
def publish():
 files=['research/decoupled-check/'+x for x in ['whole-library-progress.md','whole-library-coverage.csv','whole-library-segments.csv']if(OWN/x).exists()]
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=R,text=True).strip()=='main'
 subprocess.run(['git','add','--']+files,cwd=R,check=True)
 changed=subprocess.run(['git','diff','--cached','--quiet','--']+files,cwd=R).returncode!=0
 if changed:
  a=subprocess.check_output(['git','show','-s','--format=%an%n%ae','58ab893'],cwd=R,text=True).splitlines()
  subprocess.run(['git','-c','user.name='+a[0],'-c','user.email='+a[1],'commit','--only','-m','research: retain bounded whole-library original-kernel progress','--']+files,cwd=R,check=True)
 # A previous attempt may have committed and then lost DNS during push.
 # Even an unchanged reduction must publish that already-existing commit.
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=R)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 for attempt in range(3):
  try:
   subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=R,check=True)
   # Do not retry conflicts or non-ancestor history as network failures.
   subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R,check=True)
   subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=R,check=True)
   return
  except subprocess.CalledProcessError as error:
   with(O/'publication-errors.jsonl').open('a')as f:
    f.write(json.dumps(dict(attempt=attempt+1,returncode=error.returncode,
                           phase='git publication',raw_data_retained=True))+'\n')
   if 'merge-base'in error.cmd or attempt==2:raise
   time.sleep(5*(attempt+1))

def queue(cohort,limit):
 os.sched_setaffinity(0,{8})
 for i in range(limit):
  if state(cohort)['terminal']:break
  key=cohort+'-queue-'+str(time.monotonic_ns())
  args=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','taskset','-c','0-7','timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(O/'whole-library-run.py'),'window','--cohort',cohort]
  with(O/(key+'.log')).open('w')as f:
   locks=Path('/proc/locks').read_text();p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   atomic(O/(key+'.submission.json'),dict(pid=p.pid,args=args,locks_before=locks));rc=p.wait()
  reduce();publish()
  if rc:
   atomic(O/(key+'.exit.json'),dict(returncode=rc,status='stopped; prior certified state retained'));break
 atomic(O/(cohort+'-queue-terminal.json'),dict(state=state(cohort),iterations=i+1))
def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['window','reduce','queue']);p.add_argument('--cohort',default='all',choices=['all']+GROUPS+['remainder']);p.add_argument('--windows',type=int,default=1000);a=p.parse_args()
 if a.operation=='window':raise SystemExit(window(a.cohort))
 elif a.operation=='queue':queue(a.cohort,a.windows)
 else:os.sched_setaffinity(0,{8});print(json.dumps(reduce(),indent=2))
if __name__=='__main__':main()
