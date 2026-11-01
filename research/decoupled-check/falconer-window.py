#!/usr/bin/env python3
"""One finite P-core window of the full Falconer project extension.
Common nodes reuse exact successfully built artifacts of the SAME capture;
their recorded compiler work is charged once to each containing closure.
"""
import os,json,time,sys,shutil
from pathlib import Path
from native_project import run,ROOT,SDK,environment
BASE=ROOT.parent.parent
BOUNDARY=ROOT.parent/'boundary-v4'
CHECKER=ROOT.parent/'measurement-v1/audited-stream'
def atomic(name,value):
 p=ROOT/name;tmp=p.with_suffix(p.suffix+'.pending')
 with tmp.open('w')as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
 tmp.replace(p)
def append(row):
 with(ROOT/'measured.jsonl').open('a')as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
def events(key):return [json.loads(x)for x in(ROOT/(key+'.stdout')).read_text().splitlines()if x.startswith('{')]
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 start=time.monotonic();deadline=start+1680
 frame=json.loads((ROOT/'build-frame.json').read_text());wanted={r['module']for r in frame}
 state=json.loads((ROOT/'progress.json').read_text())if(ROOT/'progress.json').exists()else dict(windows=0,built=[],reused=[],oracle_verified=[])
 state['windows']+=1;window=state['windows']
 # Original finite capture must actually retire before this extension writes.
 assert(BASE/'all-complete.json').is_file()
 assert(BOUNDARY/'qualified.json').is_file()
 assert(ROOT.parent/'measurement-v1/measurement-qualified.json').is_file()
 assert not json.loads((BASE/'progress.json').read_text()).get('build_failure')
 parent_state=json.loads((BASE/'progress.json').read_text())
 common=set(parent_state['built'])&wanted
 state['reused']=sorted(common)
 old_rows={r['module']:r for r in json.loads((BASE/'build-frame.json').read_text())}
 for row in frame:
  m=row['module']
  if m in common and row['source']!=old_rows[m]['source']:
   # Pinned source extraction moved paths for two already-built AI files.
   if Path(row['source']).read_bytes()!=Path(old_rows[m]['source']).read_bytes():
    raise RuntimeError('source identity differs from reused typed artifact: '+m)
 env=environment()
 lib=ROOT/'constructed/lib';lib.mkdir(parents=True,exist_ok=True)
 env['LEAN_PATH']=str(lib)+':'+str(BASE/'constructed/lib')+':'+env['LEAN_PATH']
 for i,row in enumerate(frame):
  m=row['module']
  if m in common or m in state['built']:continue
  remain=deadline-time.monotonic()
  if remain<310:break
  out=lib.joinpath(*m.split('.'));out.parent.mkdir(parents=True,exist_ok=True)
  leftovers=list(out.parent.glob(out.name+'.*'))
  if leftovers:
   backup=ROOT/'interrupted-artifacts'/(str(i)+'-'+str(time.monotonic_ns()))
   backup.mkdir(parents=True)
   for f in leftovers:shutil.move(str(f),str(backup/f.name))
  flags=json.loads((BASE/'mathlib-options.json').read_text())['flags']if m.startswith('Mathlib')else['-DautoImplicit=false']if m.startswith('OAI.')else[]
  cmd=[SDK/'bin/lean','--root='+row['source_root'],'-j8']+flags+['-o',str(out)+'.olean','-i',str(out)+'.ilean','-c',str(out)+'.c',row['source']]
  result=run('build-'+str(i).zfill(5),cmd,300,True,env=env,cwd=row['source_root'])
  text=(ROOT/(result['key']+'.stdout')).read_text(errors='replace')+(ROOT/(result['key']+'.stderr')).read_text(errors='replace')
  result.update(operation='build',module=m,source=row['source'],sorry_warning="declaration uses 'sorry'"in text)
  append(result)
  if result['returncode']or result['sorry_warning']or not all(Path(str(out)+s).is_file()for s in ['.olean','.ilean','.c']):
   state['failure']=dict(operation='source_construction',module=m,key=result['key']);break
  state['built'].append(m);atomic('progress.json',state)
 if wanted.issubset(set(state['built'])|common) and not state.get('failure'):
  roots_arg='@'+str(ROOT/'roots.txt')
  for phase in ['primary','memory_profile']:
   if state.get(phase):continue
   if deadline-time.monotonic()<1510:break
   chosen=env.copy()
   if phase=='memory_profile':chosen['DECOUPLED_MEMORY_PROFILE']='1'
   r=run(phase,[CHECKER,'audit','none',roots_arg],1500,True,env=chosen)
   es=events(r['key']);accepted={e['module']for e in es if e.get('event')=='accept'}
   finished=r['returncode']==0 and accepted==wanted and es[-1].get('event')=='complete'
   r.update(operation=phase,closure_complete=finished,accepted_modules=sorted(accepted))
   append(r)
   if not finished:state['failure']=dict(operation=phase,key=r['key']);break
   # The native artifact graph, not just a source import scanner, must match.
   headers={e['module']:e for e in es if e.get('event')=='module_header'}
   if set(headers)!=wanted or any(set(headers[row['module']]['imports'])!=set(row['imports'])for row in frame):
    state['failure']=dict(operation='native_graph_mismatch',key=r['key']);break
   state[phase]=r['key'];atomic('progress.json',state)
  if state.get('primary')and state.get('memory_profile')and not state.get('failure'):
   # Old qualification covers only exact shared artifacts, and is explicitly reused.
   old_verified=set(parent_state['oracle_global'])
   state['oracle_reused']=sorted(old_verified&common)
   pending=[r['module']for r in frame if r['module']not in set(state['oracle_verified'])|old_verified&common]
   while pending:
    remain=deadline-time.monotonic()
    if remain<70:break
    chunk=pending[:32]
    r=run('oracle-'+str(len(state['oracle_verified'])).zfill(5),[CHECKER,'one','none']+chunk,min(600,remain-10),True,env=env)
    es=events(r['key']);accepted={e['module']for e in es if e.get('event')=='accept'}
    complete=r['returncode']==0 and accepted==set(chunk)
    r.update(operation='module_oracle',requested_modules=chunk,closure_complete=complete);append(r)
    if not complete:state['failure']=dict(operation='module_oracle',key=r['key']);break
    state['oracle_verified'].extend(chunk);pending=pending[len(chunk):];atomic('progress.json',state)
   state['complete']=not pending and not state.get('failure')
 atomic('progress.json',state)
 terminal=dict(window=window,elapsed_s=time.monotonic()-start,built=len(state['built']),
  reused=len(common),complete=state.get('complete',False),failure=state.get('failure'))
 atomic('window-'+str(window).zfill(3)+'-terminal.json',terminal)
 print(json.dumps(terminal),flush=True)
 return 2 if state.get('failure')else 0
if __name__=='__main__':raise SystemExit(main())
