from pathlib import Path
import json,os,subprocess,time,sys,datetime
sdk=Path(sys.argv[1]);raw=Path(sys.argv[2]);examples=Path(sys.argv[3]);cfg=json.loads(Path(sys.argv[4]).read_text())
env=dict(os.environ,PATH=str(sdk/'bin')+':'+os.environ['PATH'],LEAN_NUM_THREADS='8',LEAN_PATH=cfg['lean_path'],TMPDIR=str(raw/'tmp'))
rows=[]
def run(name,args,limit=900):
 d=raw/'results'/name;d.mkdir()
 process_env=dict(env)
 if name.startswith('discovery-'):process_env['LEAN_PATH']=cfg['lean_path']
 cmd=['taskset','-c','0-7','timeout','--kill-after=5',str(limit),*map(str,args)]
 (d/'command.json').write_text(json.dumps(dict(argv=cmd,LEAN_PATH=process_env['LEAN_PATH'],LEAN_NUM_THREADS=env['LEAN_NUM_THREADS']),indent=2)+'\n')
 with(d/'stdout').open('w')as fo,(d/'stderr').open('w')as fe:
  start=time.monotonic();p=subprocess.Popen(cmd,cwd=raw,env=process_env,stdout=fo,stderr=fe)
  _,status,ru=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status)
 r=dict(case=name,exit=p.returncode,wall_s=time.monotonic()-start,user_s=ru.ru_utime,system_s=ru.ru_stime,peak_rss_kib=ru.ru_maxrss)
 (d/'usage.json').write_text(json.dumps(r,indent=2)+'\n');rows.append(r)
 (raw/'timing-results.json').write_text(json.dumps(rows,indent=2)+'\n');print(r,flush=True)
 return r,d
r,d=run('nat-closure',[sdk/'bin/lean','--run',examples/'Closure.lean','Mathlib.Data.Nat.Basic'],180)
assert r['exit']==0,(d/'stderr').read_text()
closure=json.loads((d/'stdout').read_text());compact=raw/'compact';compact.mkdir()
bound=[]
for row in closure:
 n=row['module'];source=Path(row['path'])
 for suffix in ['','.server','.private']:
  f=Path(str(source)+suffix)
  if f.exists():
   dest=compact/Path(*n.split('.'));dest=Path(str(dest)+'.olean'+suffix)
   dest.parent.mkdir(parents=True,exist_ok=True);os.link(f,dest)
   assert (dest.stat().st_dev,dest.stat().st_ino)==(f.stat().st_dev,f.stat().st_ino);bound.append(dict(link=str(dest),target=str(f.resolve())))
 for suffix in ['.ir','.ir.sig']:
  f=source.with_suffix(suffix)
  if f.exists():
   dest=compact/Path(*n.split('.'));dest=Path(str(dest)+suffix)
   dest.parent.mkdir(parents=True,exist_ok=True);os.link(f,dest)
   assert (dest.stat().st_dev,dest.stat().st_ino)==(f.stat().st_dev,f.stat().st_ino);bound.append(dict(link=str(dest),target=str(f.resolve())))
(raw/'compact-binding.json').write_text(json.dumps(dict(modules=len(closure),links=bound),indent=2)+'\n')
large=env['LEAN_PATH'];env['LEAN_PATH']=str(compact)
r,_=run('nat-small-default',[sdk/'bin/leanchecker','-v','Mathlib.Data.Nat.Basic'])
assert r['exit']==0
r,_=run('discovery-small',[sdk/'bin/lean','--run',examples/'Discovery.lean','Mathlib.Data.Nat.Basic',env['LEAN_PATH']])
assert r['exit']==0
env['LEAN_PATH']=large
r,_=run('nat-large-default',[sdk/'bin/leanchecker','-v','Mathlib.Data.Nat.Basic'])
assert r['exit']==0
r,_=run('discovery-large',[sdk/'bin/lean','--run',examples/'Discovery.lean','Mathlib.Data.Nat.Basic',env['LEAN_PATH']])
assert r['exit']==0
(raw/'timing-terminal.json').write_text(json.dumps(dict(complete=True,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows))+'\n')
