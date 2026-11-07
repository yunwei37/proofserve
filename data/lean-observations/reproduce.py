from pathlib import Path
import subprocess,os,json,csv,shutil,sys,time,datetime
sdk=Path(sys.argv[1]);raw=Path(sys.argv[2]);src=Path(sys.argv[3])
env=dict(os.environ,PATH=str(sdk/'bin')+':'+os.environ['PATH'],LEAN_NUM_THREADS='1',TMPDIR=str(raw/'tmp'))
(raw/'tmp').mkdir(exist_ok=True)
rows=[]
def run(label,args,cwd,limit=180):
 log=raw/'results'/label;log.mkdir(exist_ok=True)
 command=['taskset','-c','0-7','timeout','--kill-after=5',str(limit),*map(str,args)]
 (log/'command.json').write_text(json.dumps(dict(argv=command,cwd=str(cwd),LEAN_PATH=env.get('LEAN_PATH'),LEAN_NUM_THREADS=env['LEAN_NUM_THREADS']),indent=2)+'\n')
 with(log/'stdout').open('w')as fo,(log/'stderr').open('w')as fe:
  begin=time.monotonic();p=subprocess.Popen(command,cwd=cwd,env=env,stdout=fo,stderr=fe)
  _,status,ru=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status)
  usage=dict(wall_s=time.monotonic()-begin,user_s=ru.ru_utime,system_s=ru.ru_stime,peak_rss_kib=ru.ru_maxrss)
  (log/'usage.json').write_text(json.dumps(usage,indent=2)+'\n')
 row=dict(case=label,exit=p.returncode,**usage,stdout=(log/'stdout').read_text(),stderr=(log/'stderr').read_text())
 rows.append(row);(raw/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(label,p.returncode,row['stdout'][-300:],row['stderr'][-500:],flush=True)
 return row
def setup(name,names):
 p=raw/name;p.mkdir(exist_ok=True)
 for n in names:shutil.copyfile(src/(n+'.lean'),p/(n+'.lean'))
 env['LEAN_PATH']=str(p)
 for n in names:
  assert run('compile-'+name+'-'+n,[sdk/'bin/lean','-o',n+'.olean',n+'.lean'],p)['exit']==0
 return p
def pair(label,p,root):
 env['LEAN_PATH']=str(p)
 return [run(label+'-'+kind,[sdk/'bin/leanchecker','-v',*flags,root],p)for kind,flags in [('default',[]),('fresh',['--fresh'])]]
parts=setup('missing-private',['Parts'])
print('parts artifacts',sorted(f.name for f in parts.iterdir()),flush=True)
pair('parts-complete',parts,'Parts')
private=parts/'Parts.olean.private'
assert private.exists()
shutil.copyfile(private,raw/'Parts.olean.private.retained')
private.unlink()
pair('parts-missing-private',parts,'Parts')
shutil.copyfile(raw/'Parts.olean.private.retained',private)
evaluation=setup('evaluation',['F','Eval'])
pair('evaluation',evaluation,'Eval')
dups=setup('duplicates',['Base','A','B','C'])
pair('duplicates-good',dups,'C')
env['LEAN_PATH']=str(dups)
shutil.copyfile(dups/'B.olean',raw/'B.good.olean.retained')
assert run('mutate-B',[sdk/'bin/lean','--run',src/'Mutate.lean',dups/'B.olean','B',dups/'B.changed'],dups)['exit']==0
shutil.copyfile(dups/'B.changed',dups/'B.olean')
pair('bad-B-alone',dups,'B')
pair('duplicates-good-then-bad',dups,'C')
(dups/'Reverse.lean').write_text('prelude\nimport B\nimport A\n')
assert run('compile-reverse',[sdk/'bin/lean','-o','Reverse.olean','Reverse.lean'],dups)['exit']==0
pair('duplicates-bad-then-good',dups,'Reverse')
(dups/'OnlyBad.lean').write_text('prelude\nimport B\n')
assert run('compile-onlybad',[sdk/'bin/lean','-o','OnlyBad.olean','OnlyBad.lean'],dups)['exit']==0
pair('import-only-bad',dups,'OnlyBad')
with(raw/'cases.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['case','exit','wall_s','user_s','system_s','peak_rss_kib','stdout','stderr'],lineterminator='\n');w.writeheader();w.writerows(rows)
(raw/'fixtures-terminal.json').write_text(json.dumps(dict(complete=True,cases=len(rows),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))+'\n')
