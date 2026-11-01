import os,pathlib,json,subprocess,datetime,signal
BASE=pathlib.Path(__file__).resolve().parent
RAW=BASE.parent
os.sched_setaffinity(0,set(range(8,16)))
rows=[]
try:
 for rep in [1,2,3]:
  for k in ([8,4,2,1,0] if rep==2 else [0,1,2,4,8]):
   label=f'grid-v3-k{k}-r{rep}'
   cp=subprocess.run(['python3','-u',str(BASE/'run.py'),label,str(k)],check=True)
   value=json.loads((RAW/'runs'/label/'result.json').read_text());rows.append(value)
   (BASE/'progress.json').write_text(json.dumps(dict(planned=15,completed=len(rows),last=label),indent=2)+'\n')
   if value['returncode']!=0:raise RuntimeError('failed native cell; later cells not started')
 (BASE/'terminal.json').write_text(json.dumps(dict(complete=True,planned=15,completed=len(rows)),indent=2)+'\n')
except BaseException as e:
 (BASE/'terminal.json').write_text(json.dumps(dict(complete=False,completed=len(rows),error=repr(e)),indent=2)+'\n')
 raise
