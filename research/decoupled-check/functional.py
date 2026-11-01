import os,json,sys
from pathlib import Path
from native import run,ROOT,SDK
os.sched_setaffinity(0,{16,17,18,19})
for key,cmd in [
 ('prepare-lean-v3',[SDK/'bin/lean','-o',ROOT/'StreamCheck.olean','-c',ROOT/'StreamCheck.c',ROOT/'StreamCheck.lean']),
 ('prepare-leanc-v3',[SDK/'bin/leanc','-O3','-o',ROOT/'stream-check',ROOT/'StreamCheck.c'])]:
    r=run(key,cmd,300)
    if r['returncode']:raise SystemExit('preparation failed')
binary=ROOT/'stream-check';root='Init.Data.Nat.Basic'
r=run('functional-stream',[binary,'stream','none',root],120)
if r['returncode']:raise SystemExit('initial native streaming failed')
events=[json.loads(x)for x in(ROOT/(r['key']+'.stdout')).read_text().splitlines()]
assert events[-1]['event']=='complete'
modules=[e['module']for e in events if e['event']=='accept']
accepted=[];rejected=[]
for i,module in enumerate(modules):
    r=run(f'functional-oracle-{i:03d}',[SDK/'bin/leanchecker','-v',module],120)
    (accepted if r['returncode']==0 else rejected).append(module)
assert accepted==modules and not rejected
mutants=[]
for mutation in ['bvar','unknown','sort']:
    pair=[]
    for mode in ['stream','one']:
        key='functional-'+mode+'-'+mutation
        r=run(key,[binary,mode,mutation,root],120)
        e=[json.loads(x)for x in(ROOT/(r['key']+'.stdout')).read_text().splitlines()]
        rejects=[v for v in e if v.get('event')=='reject'and v.get('module')==root]
        pair.append(dict(mode=mode,mutation=mutation,returncode=r['returncode'],native_rejection=bool(rejects),error=rejects[-1]['error']if rejects else''))
        assert r['returncode']not in[0,124,137]and rejects
    mutants.append(pair)
result=dict(scope='E-core functional qualification only; no timing measurements',root=root,streaming_accepted_modules=modules,oracle_accepted_modules=accepted,oracle_rejected_modules=rejected,mutation_pairs=mutants,complete_event=events[-1])
(ROOT/'functional-controls.json').write_text(json.dumps(result,indent=2))
# Metadata preparation, not a measured checker result.
r=run('closure-manifest',[binary,'manifest','none','Mathlib.Data.Nat.Basic','OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17','OAI.MeasureTheory.Falconer.Estimates.NearPinDeletion'],300)
if r['returncode']:raise SystemExit('manifest preparation failed')
(ROOT/'preparation-terminal.json').write_text(json.dumps(dict(status='functional-qualified-and-manifest-ready')))
