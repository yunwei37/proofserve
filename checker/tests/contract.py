#!/usr/bin/env python3
"""Release backend correctness contract; no machine-specific paths."""
import json,os,subprocess,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BINARY=Path(os.environ.get('PROOFSERVE_CHECK',str(ROOT/'.lake/build/bin/proofserve-check'))).resolve()
def invoke(args,expected=0,env=None):
 r=subprocess.run([str(BINARY),*map(str,args)],text=True,capture_output=True,timeout=60,env=env)
 assert r.returncode==expected,(r.returncode,r.stdout,r.stderr)
 return json.loads(r.stdout)
with tempfile.TemporaryDirectory(prefix='proofserve-contract-')as td:
 d=Path(td);project=d/'project';project.mkdir()
 for f in ['Base.lean','Fixture.lean','lakefile.lean','lean-toolchain']:shutil.copyfile(ROOT/'tests'/f,project/f)
 version=subprocess.check_output(['lean','--version'],text=True).split('version ',1)[1].split(',',1)[0]
 (project/'lean-toolchain').write_text('leanprover/lean4:v'+version+'\n')
 subprocess.run(['lake','build'],cwd=project,check=True,timeout=60)
 full=invoke([project,'--workers','1','--checkpoint-dir',d/'full'])
 assert full['status']=='complete'and set(full['accepted'])=={'Base','Fixture'}
 assert 'fixtureAssumption'in full['axioms']
 fallback=invoke([project,'--official','--checkpoint-dir',d/'official'])
 assert fallback['execution_path']=='official-leanchecker' and fallback['parallel']is False
 assert set(fallback['accepted_roots'])=={'Base','Fixture'} and fallback['accepted']is None
 for n in [2,4]:
  other=invoke([project,'--workers',n,'--checkpoint-dir',d/('workers'+str(n))])
  assert other['accepted']==full['accepted'] and other['axioms']==full['axioms']
 official=subprocess.run(['lake','env','leanchecker','-v','Base','Fixture'],cwd=project,text=True,capture_output=True,timeout=60)
 assert official.returncode==0,(official.stdout,official.stderr)
 assert {s.split('replaying ')[1]for s in official.stdout.splitlines()if s.startswith('replaying ')}==set(full['accepted'])
 partial=invoke([project,'--workers','1','--segment-modules','1','--max-segments','1','--checkpoint-dir',d/'resume'],2)
 assert partial['status']=='incomplete'
 resumed=invoke([project,'--workers','1','--segment-modules','1','--checkpoint-dir',d/'resume'])
 assert resumed['accepted']==full['accepted']and resumed['axioms']==full['axioms']
 assert resumed['module_set_hash']==full['module_set_hash']
 paths=subprocess.check_output(['lake','env','printenv','LEAN_PATH'],cwd=project,text=True).strip()
 paths=':'.join(str((project/p).resolve())for p in paths.split(':'))
 for mutation in ['bvar','unknown','sort']:
  e=dict(os.environ,LEAN_PATH=paths,DECOUPLED_MUTATE_MODULE='Fixture',PROOFSERVE_WORKERS='2')
  rr=subprocess.run([str(BINARY),'--internal-segment','audit',mutation,'Fixture'],env=e,text=True,capture_output=True,timeout=60)
  assert rr.returncode!=0,(mutation,rr.stdout,rr.stderr)
  assert 'reject'in rr.stdout and 'Fixture'in rr.stdout,(mutation,rr.stderr)
  assert ('kernel_reject:'in(rr.stdout+rr.stderr) or ('while replaying declaration'in(rr.stdout+rr.stderr) and '(kernel)'in(rr.stdout+rr.stderr))),(mutation,rr.stdout,rr.stderr)
 (project/'lean-toolchain').write_text('leanprover/lean4:not-supported\\n')
 badversion=subprocess.run([str(BINARY),str(project)],text=True,capture_output=True,timeout=10)
 assert badversion.returncode==2 and 'unsupported'in badversion.stderr
 print(json.dumps(dict(correct=True,axioms=True,resume=True,bad_proofs=3)))
