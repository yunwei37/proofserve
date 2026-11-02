#!/usr/bin/env python3
"""Small real import/compiler differential and complete external-closure metadata."""
import os,json,importlib.util
from pathlib import Path
B=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
A=B/'ramsey-20261102'
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 spec=importlib.util.spec_from_file_location('n',B/'scale-study/falconer-project-20261101/native_project.py')
 n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.ROOT=A
 env=n.environment();env['LEAN_PATH']=':'.join(json.loads((A/'prepare.json').read_text())['production_providers'])
 controls=['ComparatorChallenges.AbhyankarSathaye','ComparatorChallenges.AffineBernstein','ComparatorChallenges.AlgorithmicThinTrees']
 root=A/'sources/lean';out=A/'qualification';out.mkdir(exist_ok=True)
 (root/'InitDataControl.lean').write_text('prelude\nimport Init.Data.Iterators.Lemmas.Monadic.Basic\nexample : (1 : Nat) = 1 := rfl\n')
 controls.append('InitDataControl');results=[]
 for i,m in enumerate(controls):
  src=root.joinpath(*m.split('.')).with_suffix('.lean')
  dest=out/('case'+str(i))
  c=n.run('qualified-producer-'+str(i),[n.SDK/'bin/lean','--root='+str(root),'-j8','-DautoImplicit=false',
      '-o',str(dest)+'.olean','-i',str(dest)+'.ilean','-c',str(dest)+'.c',src],300,True,env=env,cwd=root)
  text=(A/(c['key']+'.stdout')).read_text(errors='replace')+(A/(c['key']+'.stderr')).read_text(errors='replace')
  ok=c['returncode']==0
  results.append(dict(module=m,returncode=c['returncode'],qualified=ok,key=c['key'],sorry_warning="declaration uses 'sorry'"in text))
  if not ok:print(text[-3000:]);break
 (A/'producer-qualification-v2.json').write_text(json.dumps(dict(complete=len(results)==4 and all(v['qualified']for v in results),results=results),indent=2))
 print(json.dumps(results,indent=2))
 if not(len(results)==4 and all(v['qualified']for v in results)):return 2
 # The fixed original manifest binary reads compiled terms; it does not execute
 # copied Meta/IR. This probe namespace selects exact already measured B/F terms.
 chosen=env.copy();chosen['LEAN_PATH']=str(B/'whole-library-20261102/lib')
 roots=json.loads((A/'external-roots.json').read_text())
 c=n.run('external-native-manifest',[B/'stream-check','manifest','none']+roots,300,True,env=chosen)
 print('manifest',c['returncode'])
 return c['returncode']
if __name__=='__main__':raise SystemExit(main())
