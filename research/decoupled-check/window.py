#!/usr/bin/env python3
"""One <=29-minute locked window of the finite decoupled-check experiment."""
import os,json,time,sys
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
def main():
    assert sorted(os.sched_getaffinity(0))==list(range(8))
    start=time.monotonic();deadline=start+1680
    state=json.loads((ROOT/'progress.json').read_text())if(ROOT/'progress.json').exists()else dict(streams=[],built=[],oracle_done=[],windows=0)
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
            events=load_events(ROOT/(key+'.stdout'))
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
            if remaining<min(limit,180)+10:break
            out=ROOT/'constructed/lib'/Path(*module.split('.'));out.parent.mkdir(parents=True,exist_ok=True)
            env=environment();env['LEAN_PATH']=str(ROOT/'constructed/lib')+':'+env['LEAN_PATH']
            cmd=[SDK/'bin/lean','--root='+row['source_root'],'-j8']+compiler_flags(row)+[
                '-o',str(out)+'.olean','-i',str(out)+'.ilean','-c',str(out)+'.c',row['source']]
            key=f'build-{index:05d}'
            r=run(key,cmd,min(limit,remaining-5),True,env=env,cwd=row['source_root'])
            text=(ROOT/(key+'.stdout')).read_text(errors='replace')+(ROOT/(key+'.stderr')).read_text(errors='replace')
            outputs={s:Path(str(out)+s).exists()for s in ['.olean','.ilean','.c']}
            r.update(operation='build',module=module,source=row['source'],class_tag=row['class_tag'],outputs=outputs,
                sorry_warning="declaration uses 'sorry'"in text)
            append(r)
            if r['returncode']or not all(outputs.values())or r['sorry_warning']:
                state['build_failure']=module
                break
            state['built'].append(module)
            (ROOT/'progress.json').write_text(json.dumps(state,indent=2))
        (ROOT/'progress.json').write_text(json.dumps(state,indent=2))
        if state.get('build_failure')or state.get('stream_failure'):break
        if not wanted.issubset(state['built']):break
        # One native process, freshly finalized imported environment per module.
        # Upstream freeRegions runs after each module; no checked env is shared.
        if name not in state['oracle_done']:
            if deadline-time.monotonic()<610:break
            key='timed-oracle-'+name
            modules=[x['module']for x in frame if x['module']in wanted]
            r=run(key,[ROOT/'stream-check','one','none']+modules,600,True)
            events=load_events(ROOT/(key+'.stdout'));accepted=[x['module']for x in events if x.get('event')=='accept']
            r.update(operation='oracle',cohort=name,accepted_modules=accepted,
                closure_complete=r['returncode']==0 and set(accepted)==wanted)
            append(r);state['oracle_done'].append(name)
            if not r['closure_complete']:
                state['oracle_failure']=name;break
    (ROOT/'progress.json').write_text(json.dumps(state,indent=2))
    terminal=dict(window=window,elapsed_s=time.monotonic()-start,built_count=len(state['built']),stream_cohorts=state['streams'],oracle_cohorts=state['oracle_done'],
        failed=any(state.get(k)for k in ['build_failure','stream_failure','oracle_failure']),
        finished=all(n in state['oracle_done']for n in ['math','compute-grid','compute-amplitudes','ordinary-oai']))
    (ROOT/f'window-{window:03d}-terminal.json').write_text(json.dumps(terminal,indent=2))
    print(json.dumps(terminal),flush=True)
    return 2 if terminal['failed']else 0
if __name__=='__main__':raise SystemExit(main())
