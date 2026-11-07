from pathlib import Path
import os,sys,json,time,subprocess,datetime,collections
raw=Path(sys.argv[1]);repo=Path(sys.argv[2])
os.sched_setaffinity(0,{8,9})
sdk=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
clock=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/declaration-distribution-v1/clock.so')
cfg=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/checker-final-e000ed62-20261106T050828/matrix/config.json').read_text())
plan=json.loads((raw/'sample-plan.json').read_text());todo=list(plan['modules'])
# Cheap first module qualifies the measurement entry; it is retained as a sample.
first=min(todo,key=lambda r:float(r['cpu_s']));todo.remove(first)
todo=[first]+sorted(todo,key=lambda r:-float(r['cpu_s']))
env=dict(os.environ,PATH=str(sdk/'bin')+':'+os.environ.get('PATH',''),LEAN_SYSROOT=str(sdk),LEAN_PATH=str(sdk/'lib/lean')+':'+cfg['lean_path'],LEAN_NUM_THREADS='1',TMPDIR=str(raw/'tmp'))
(raw/'tmp').mkdir(exist_ok=True);(raw/'modules').mkdir(exist_ok=True)
mem=lambda:int(next(l.split()[1]for l in Path('/proc/meminfo').read_text().splitlines()if l.startswith('MemAvailable:')))*1024
reserve=8*1024**3;budget=min(mem()-reserve-256*1024**2,53*1024**3)
assert budget>4*1024**3
current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
group=current.parent/('generation-checking-'+str(os.getpid())+'.scope');group.mkdir()
(group/'memory.max').write_text(str(budget))
(group/'cgroup.subtree_control').write_text('+memory +cpu')
(raw/'sampler-scope.json').write_text(json.dumps(dict(cgroup=str(group),memory_max_bytes=budget,node_reserve_bytes=reserve,cpus=list(range(8)),workers_max=8,per_module_wall_limit_s=900,argv_policy='official Lean --run only; no target compilation'),indent=2)+'\n')
active={};done=[];qualified=False;started=time.monotonic();overall=started+max(0,datetime.datetime.fromisoformat(plan['campaign_deadline_utc']).timestamp()-time.time())-60;counter=0
def cpu(cg):
 v=dict(l.split()for l in(cg/'cpu.stat').read_text().splitlines());return {k:int(v.get(k+'_usec',0))/1e6 for k in ['usage','user','system']}
def events(path):
 result=[]
 for l in path.read_text().splitlines():
  try:j=json.loads(l)
  except ValueError:continue
  if isinstance(j,dict)and'event'in j:result.append(j)
 return result
def launch(row,core):
 global counter
 counter+=1;directory=raw/'modules'/str(counter).zfill(4);directory.mkdir()
 cg=group/str(counter).zfill(4);cg.mkdir();(cg/'memory.max').write_text(str(budget));(cg/'memory.oom.group').write_text('1')
 argv=[str(sdk/'bin/lean'),'--root='+str(raw),'-j1','--load-dynlib='+str(clock),'--run',str(raw/'Window.lean'),row['module'],row['olean_path']]
 def enter():
  (cg/'cgroup.procs').write_text('0');os.sched_setaffinity(0,{core})
 fo=(directory/'stdout').open('w');fe=(directory/'stderr').open('w')
 begin=time.monotonic();p=subprocess.Popen(argv,env=env,cwd=cfg['project'],stdout=fo,stderr=fe,preexec_fn=enter,start_new_session=True)
 rec=dict(module=row['module'],core=core,pid=p.pid,birth=Path('/proc',str(p.pid),'stat').read_text().rsplit(')',1)[1].split()[19],
   argv=argv,cgroup=str(cg),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),groups=row['sample_groups'])
 (directory/'command.json').write_text(json.dumps(rec,indent=2)+'\n')
 active[p.pid]=dict(process=p,row=row,core=core,cg=cg,out=directory,start=begin,fo=fo,fe=fe,peak=0,stop=None,rec=rec)
def finish(pid,status,ru):
 global qualified
 a=active.pop(pid);a['process'].returncode=os.waitstatus_to_exitcode(status);a['fo'].close();a['fe'].close()
 cg=a['cg'];ee=events(a['out']/'stdout');complete=[e for e in ee if e['event']=='complete'];imports=[e for e in ee if e['event']=='import_complete'];reads=[e for e in ee if e['event']=='read_complete'];maps=[e for e in ee if e['event']=='map_complete'];began=any(e['event']=='check_begin'for e in ee)
 mc=(cg/'memory.events').read_text();stat=cpu(cg)
 r=dict(module=a['row']['module'],groups=a['row']['sample_groups'],core=a['core'],returncode=a['process'].returncode,
  process_wall_s=time.monotonic()-a['start'],process_cpu_s=stat['usage'],process_user_s=stat['user'],process_system_s=stat['system'],
  peak_rss_kib=ru.ru_maxrss,sampled_tree_peak_bytes=a['peak'],charged_memory_peak_bytes=int((cg/'memory.peak').read_text()),
  stop_reason=a['stop'],memory_events=mc,check_started=began,events=ee,raw=str(a['out']))
 if imports:
  r.update(import_wall_s=int(imports[-1]['import_wall_ns'])/1e9,import_cpu_s=int(imports[-1]['import_cpu_ns'])/1e9)
 if reads:r.update(target_read_wall_s=int(reads[-1]['read_wall_ns'])/1e9,target_read_cpu_s=int(reads[-1]['read_cpu_ns'])/1e9)
 if maps:r.update(target_map_wall_s=int(maps[-1]['map_wall_ns'])/1e9,target_map_cpu_s=int(maps[-1]['map_cpu_ns'])/1e9)
 if len(complete)==1 and r['returncode']==0:
  r.update(status='accepted',check_wall_s=int(complete[0]['check_wall_ns'])/1e9,check_cpu_s=int(complete[0]['check_cpu_ns'])/1e9,
    eligible_entries=complete[0]['eligible_entries'],replay_wall_s=int(complete[0]['replay_wall_ns'])/1e9,replay_cpu_s=int(complete[0]['replay_cpu_ns'])/1e9)
 elif any(int(l.split()[1])for l in mc.splitlines()if l.split()[0]in ['oom_kill','oom_group_kill']):
  r['status']='resource_oom'
 elif a['stop']=='wall_900s':
  r['status']='timeout_check'if began else'timeout_import_or_setup'
 elif a['stop']:
  r['status']='resource_stop'
 elif any(e['event']=='kernel_reject'for e in ee):
  r['status']='kernel_rejected'
 else:r['status']='tool_or_import_error'
 r['right_censored']=r['status'].startswith('timeout')
 if 'check_base_cpu'in a:
  r['check_cpu_observed_lower_s']=max(0,stat['usage']-a['check_base_cpu'])
  r['check_wall_observed_lower_s']=r['check_cpu_observed_lower_s'] # one physical CPU
 (a['out']/'result.json').write_text(json.dumps(r,indent=2)+'\n')
 with(raw/'sample-results.jsonl').open('a')as f:f.write(json.dumps(r)+'\n');f.flush()
 done.append(r)
 for _ in range(20):
  try:cg.rmdir();break
  except OSError:time.sleep(.05)
 else:raise RuntimeError('own process cgroup did not retire')
 print('RETURN',r['module'],r['status'],r.get('import_wall_s'),r.get('check_wall_s'),flush=True)
 if not qualified:
  if r['status']!='accepted':raise RuntimeError('initial sample did not qualify the entry; retain and inspect')
  qualified=True
def estimate(row):return max(1536*1024**2,min(budget,int(float(row.get('cgroup_peak')or'0')*1.1)))
try:
 while todo or active:
  # Preflight permits only one live sample until its actual successful return.
  cores=[c for c in range(8)if c not in{a['core']for a in active.values()}]
  allocated=sum(estimate(a['row'])for a in active.values())
  while todo and cores and (qualified or not active)and time.monotonic()+900<overall and mem()>reserve+1024**3:
   candidates=[i for i,r in enumerate(todo)if allocated+estimate(r)<=budget]
   if not candidates:break
   i=candidates[0];row=todo.pop(i);core=cores.pop(0);allocated+=estimate(row);launch(row,core)
   if not qualified:break
  now=time.monotonic()
  for pid in list(active):
   a=active[pid]
   ids=(a['cg']/'cgroup.procs').read_text().split();rss=0
   for ident in ids:
    try:rss+=int(Path('/proc',ident,'statm').read_text().split()[1])*os.sysconf('SC_PAGE_SIZE')
    except FileNotFoundError:pass
   a['peak']=max(a['peak'],rss)
   if 'check_base_cpu'not in a and any(e['event']=='check_begin'for e in events(a['out']/'stdout')):
    a['check_base_cpu']=cpu(a['cg'])['usage']
   if now-a['start']>=900 and not a['stop']:
    a['stop']='wall_900s';(a['cg']/'cgroup.kill').write_text('1')
   p,status,ru=os.wait4(pid,os.WNOHANG)
   if p:finish(pid,status,ru)
  if active and mem()<reserve:
   a=max(active.values(),key=lambda x:int((x['cg']/'memory.current').read_text()))
   a['stop']='node_available_below_8GiB';(a['cg']/'cgroup.kill').write_text('1')
  if 1-os.statvfs(raw).f_bavail/os.statvfs(raw).f_blocks>=.85:raise RuntimeError('disk85')
  progress=dict(completed=len(done),total=plan['unique_modules'],statuses=dict(collections.Counter(r['status']for r in done)),
   active=[dict(module=a['row']['module'],core=a['core'],pid=a['process'].pid,elapsed_s=now-a['start'])for a in active.values()],
   queued=len(todo),node_available_bytes=mem(),elapsed_s=now-started)
  (raw/'sample-progress.json').write_text(json.dumps(progress)+'\n')
  if todo and not active and now+900>=overall:break
  time.sleep(.25)
finally:
 if active:
  for a in active.values():
   a['stop']='controller_failure';(a['cg']/'cgroup.kill').write_text('1')
  for pid in list(active):
   p,status,ru=os.wait4(pid,0);finish(pid,status,ru)
 group.rmdir()
 terminal=dict(complete=len(done)==plan['unique_modules'],returned=len(done),requested=plan['unique_modules'],
  not_started=[r['module']for r in todo],statuses=dict(collections.Counter(r['status']for r in done)),
  elapsed_s=time.monotonic()-started,cgroup_retired=not group.exists(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (raw/'sample-terminal.json').write_text(json.dumps(terminal,indent=2)+'\n');print('TERMINAL',json.dumps(terminal),flush=True)
