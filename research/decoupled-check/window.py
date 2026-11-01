#!/usr/bin/env python3
"""One <=29-minute locked window of the finite decoupled-check experiment."""
import os,json,time,sys,shutil
from pathlib import Path
from native import run,ROOT,SDK,environment
def load_events(path):
    return [json.loads(x)for x in path.read_text().splitlines()]
def compiler_flags(row):
    if row['module'].startswith('Mathlib.') or row['module']=='Mathlib':
        return json.loads((ROOT/'mathlib-options.json').read_text())['flags']
    if row['module'].startswith('OAI.'):return ['-DautoImplicit=false']
    return []
def append(row):
    with(ROOT/'measured.jsonl').open('a')as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
def checkpoint(state):
    target=ROOT/'progress.json';pending=ROOT/'progress.pending'
    with pending.open('w')as f:
        json.dump(state,f,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(pending,target)
def main():
    assert sorted(os.sched_getaffinity(0))==list(range(8))
    start=time.monotonic();deadline=start+1680
    state=json.loads((ROOT/'progress.json').read_text())if(ROOT/'progress.json').exists()else dict(streams=[],built=[],oracle_done=[],windows=0)
    state.setdefault('constructed_streams',[]);state.setdefault('oracle_verified',{});state.setdefault('constructed_oracle_done',[]);state.setdefault('oracle_global',[])
    state['windows']+=1;window=state['windows']
    (ROOT/f'window-{window:03d}-launch.json').write_text(json.dumps(dict(pid=os.getpid(),utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),locks=Path('/proc/locks').read_text(),affinity=sorted(os.sched_getaffinity(0))),indent=2))
    frame=json.loads((ROOT/'build-frame.json').read_text());cohorts=json.loads((ROOT/'cohort-plan.json').read_text())
    # Bring each complete cohort to a measured stream and full source construction
    # before moving on; dependencies already built are shared but charged to every
    # closure that contains them in the reduction.
    for name in ['math','compute-grid','compute-amplitudes','ordinary-oai']:
        spec=cohorts['cases'][name];root=spec['root'];wanted=set(spec['modules'])
        if name not in state['streams']:
            if deadline-time.monotonic()<spec['stream_limit_s']+10:break
            key='timed-stream-'+name
            r=run(key,[ROOT/'stream-check','stream','none',root],spec['stream_limit_s'],True)
            key=r['key'];events=load_events(ROOT/(key+'.stdout'))
            accepted=[x['module']for x in events if x.get('event')=='accept']
            r.update(operation='stream',cohort=name,root=root,accepted_modules=accepted,
                closure_complete=r['returncode']==0 and set(accepted)==wanted and events[-1].get('event')=='complete')
            append(r);state['streams'].append(name)
            if not r['closure_complete']:
                state['stream_failure']=name
                # Preserve real failure and stop rather than silently weaken the closure.
                break
        for index,row in enumerate(frame):
            module=row['module']
            if module not in wanted or module in state['built']:continue
            remaining=deadline-time.monotonic()
            limit=900 if module.endswith('.Grid') else 600 if module.endswith('.Amplitudes')else 180
            if remaining<limit+10:break
            out=ROOT/'constructed/lib'/Path(*module.split('.'));out.parent.mkdir(parents=True,exist_ok=True)
            leftovers=list(out.parent.glob(out.name+'.*'))
            if leftovers:
                backup=ROOT/'interrupted-artifacts'/(str(index)+'-'+str(time.monotonic_ns()))
                backup.mkdir(parents=True)
                for f in leftovers:shutil.move(str(f),str(backup/f.name))
            env=environment();env['LEAN_PATH']=str(ROOT/'constructed/lib')+':'+env['LEAN_PATH']
            cmd=[SDK/'bin/lean','--root='+row['source_root'],'-j8']+compiler_flags(row)+[
                '-o',str(out)+'.olean','-i',str(out)+'.ilean','-c',str(out)+'.c',row['source']]
            key=f'build-{index:05d}'
            r=run(key,cmd,min(limit,remaining-5),True,env=env,cwd=row['source_root'])
            key=r['key'];text=(ROOT/(key+'.stdout')).read_text(errors='replace')+(ROOT/(key+'.stderr')).read_text(errors='replace')
            outputs={s:Path(str(out)+s).exists()for s in ['.olean','.ilean','.c']}
            r.update(operation='build',module=module,source=row['source'],class_tag=row['class_tag'],outputs=outputs,
                sorry_warning="declaration uses 'sorry'"in text)
            append(r)
            if r['returncode']or not all(outputs.values())or r['sorry_warning']:
                state['build_failure']=module
                break
            state['built'].append(module)
            checkpoint(state)
        checkpoint(state)
        if state.get('build_failure')or state.get('stream_failure'):break
        if not wanted.issubset(state['built']):break
        # Primary consumption run reads the exact artifacts just constructed.
        if name not in state['constructed_streams']:
            if deadline-time.monotonic()<spec['stream_limit_s']+10:break
            key='timed-constructed-stream-'+name
            env=environment();env['LEAN_PATH']=str(ROOT/'constructed/lib')+':'+env['LEAN_PATH']
            r=run(key,[ROOT/'stream-check','stream','none',root],spec['stream_limit_s'],True,env=env)
            key=r['key'];events=load_events(ROOT/(key+'.stdout'));accepted=[e['module']for e in events if e.get('event')=='accept']
            r.update(operation='matched_stream',cohort=name,root=root,accepted_modules=accepted,
                closure_complete=r['returncode']==0 and set(accepted)==wanted and events[-1].get('event')=='complete')
            append(r);state['constructed_streams'].append(name)
            if not r['closure_complete']:state['matched_failure']=name;break
        # Every module is compared against freshly imported single-module replay.
        # Chunk boundaries share no checked environment and do not change acceptance.
        verified=state['oracle_verified'].setdefault(name,[])
        verified.extend(m for m in state['oracle_global']if m in wanted and m not in verified)
        modules=[x['module']for x in frame if x['module']in wanted]
        while not wanted.issubset(verified):
            remaining=deadline-time.monotonic()
            if remaining<70:break
            pending=[m for m in modules if m not in verified]
            chunk=pending[:32];key='oracle-'+name+'-'+str(len(verified)).zfill(5)
            env=environment();env['LEAN_PATH']=str(ROOT/'constructed/lib')+':'+env['LEAN_PATH']
            r=run(key,[ROOT/'stream-check','one','none']+chunk,min(600,remaining-10),True,env=env)
            key=r['key'];events=load_events(ROOT/(key+'.stdout'));accepted=[e['module']for e in events if e.get('event')=='accept']
            r.update(operation='matched_oracle',cohort=name,requested_modules=chunk,accepted_modules=accepted,
                closure_complete=r['returncode']==0 and set(accepted)==set(chunk))
            append(r)
            if r['closure_complete']:
                verified.extend(m for m in accepted if m not in verified)
                state['oracle_global'].extend(m for m in accepted if m not in state['oracle_global'])
            checkpoint(state)
            if not r['closure_complete']:
                state['oracle_failure']=name;break
        if wanted.issubset(verified) and name not in state['constructed_oracle_done']:
            state['constructed_oracle_done'].append(name)
        if state.get('oracle_failure') or name not in state['constructed_oracle_done']:break
    checkpoint(state)
    terminal=dict(window=window,elapsed_s=time.monotonic()-start,built_count=len(state['built']),stream_cohorts=state['streams'],oracle_cohorts=state['constructed_oracle_done'],
        failed=any(state.get(k)for k in ['build_failure','stream_failure','matched_failure','oracle_failure']),
        finished=all(n in state['constructed_oracle_done']for n in ['math','compute-grid','compute-amplitudes','ordinary-oai']))
    (ROOT/f'window-{window:03d}-terminal.json').write_text(json.dumps(terminal,indent=2))
    print(json.dumps(terminal),flush=True)
    return 2 if terminal['failed']else 0
if __name__=='__main__':raise SystemExit(main())
