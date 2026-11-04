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
 for f in ['Base.lean','Fixture.lean','ShadowLeft.lean','ShadowRight.lean','All.lean','Pkg.lean','Pkg/Child.lean','lakefile.lean','lean-toolchain']:
  (project/f).parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(ROOT/'tests'/f,project/f)
 version=subprocess.check_output(['lean','--version'],text=True).split('version ',1)[1].split(',',1)[0]
 (project/'lean-toolchain').write_text('leanprover/lean4:v'+version+'\n')
 subprocess.run(['lake','build'],cwd=project,check=True,timeout=60)
 full=invoke([project,'--workers','1','--checkpoint-dir',d/'full'])
 assert full['status']=='complete'and set(full['accepted'])=={'Base','Fixture'}
 assert 'fixtureAssumption'in full['axioms']
 fallback=invoke([project,'--official','--checkpoint-dir',d/'official'])
 assert fallback['execution_path']=='official-leanchecker' and fallback['parallel']is False
 assert set(fallback['accepted_roots'])=={'Base','Fixture'} and fallback['accepted']is None
 for flag in ['--no-persistence','--no-split-fallback']:
  ablated=invoke([project,'--workers','2','--checkpoint-dir',d/flag[2:],flag])
  assert ablated['accepted']==full['accepted'] and ablated['axioms']==full['axioms']
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

 # Independent closure batches retain certificates, not all historical environments.
 partitioned=invoke([project,'--workers','1','--closure-roots','1','--checkpoint-dir',d/'batches'])
 assert partitioned['context_strategy']=='independent-closures'
 (d/'requested-roots.txt').write_text('Base\nFixture\n')
 from_file=invoke([project,'--workers','1','--closure-roots','1','--root-file',d/'requested-roots.txt','--checkpoint-dir',d/'root-file'])
 assert from_file['accepted']==full['accepted'] and from_file['roots']==full['roots']
 (d/'official-roots.txt').write_text('Fixture\n')
 official_file=invoke([project,'--official','--root-file',d/'official-roots.txt','--checkpoint-dir',d/'official-file'])
 assert set(official_file['accepted_roots'])=={'Fixture'}
 (d/'empty-roots.txt').write_text('\n')
 empty_roots=subprocess.run([str(BINARY),str(project),'--workers','1','--root-file',str(d/'empty-roots.txt'),'--checkpoint-dir',str(d/'empty-roots')],text=True,capture_output=True,timeout=10)
 assert empty_roots.returncode==2 and 'root-file contains no module names' in empty_roots.stderr



 assert partitioned['accepted']==full['accepted'] and partitioned['axioms']==full['axioms']
 assert partitioned['module_set_hash']==full['module_set_hash'] and len(partitioned['batches'])==2
 assert len(list((d/'batches').glob('batch-*/certified.json')))==2
 assert not list((d/'batches').glob('batch-*/*.olean'))
 again=invoke([project,'--workers','1','--closure-roots','1','--checkpoint-dir',d/'batches'])
 assert again['accepted']==full['accepted'] and all(b['reused'] for b in again['batches'])
 assert all(s['reused'] for s in again['segments'])
 stopped=invoke([project,'--workers','1','--closure-roots','1','--max-segments','1','--checkpoint-dir',d/'batch-resume'],2)
 assert stopped['status']=='incomplete'
 batch_resumed=invoke([project,'--workers','1','--closure-roots','1','--checkpoint-dir',d/'batch-resume'])
 assert batch_resumed['accepted']==full['accepted'] and batch_resumed['axioms']==full['axioms']
 assert batch_resumed['batches'][0]['reused'] is True
 artifact=project/'.lake/build/lib/lean/Base.olean'
 old=artifact.read_bytes()
 try:
  artifact.write_bytes(old+b'changed')
  stale=subprocess.run([str(BINARY),str(project),'--workers','1','--closure-roots','1','--checkpoint-dir',str(d/'batches')],text=True,capture_output=True,timeout=10)
  assert stale.returncode==2 and 'certified closure input changed' in stale.stderr
 finally:artifact.write_bytes(old)
 paths=subprocess.check_output(['lake','env','printenv','LEAN_PATH'],cwd=project,text=True).strip()
 paths=':'.join(str((project/p).resolve())for p in paths.split(':'))
 for mutation in ['bvar','unknown','sort']:
  e=dict(os.environ,LEAN_PATH=paths,DECOUPLED_MUTATE_MODULE='Fixture',PROOFSERVE_WORKERS='2')
  rr=subprocess.run([str(BINARY),'--internal-segment','audit',mutation,'Fixture'],env=e,text=True,capture_output=True,timeout=60)
  assert rr.returncode!=0,(mutation,rr.stdout,rr.stderr)
  assert 'reject'in rr.stdout and 'Fixture'in rr.stdout,(mutation,rr.stderr)
  assert ('kernel_reject:'in(rr.stdout+rr.stderr) or ('while replaying declaration'in(rr.stdout+rr.stderr) and '(kernel)'in(rr.stdout+rr.stderr))),(mutation,rr.stdout,rr.stderr)


 # Later roots already covered by an earlier closure must not be checked again.
 subprocess.run(['lake','build','All'],cwd=project,check=True,timeout=60)
 all_roots=[project,'--workers','1','--root','All','--root','Base','--root','Fixture']
 all_plain=invoke([*all_roots,'--closure-roots','0','--checkpoint-dir',d/'all-plain'])
 all_batches=invoke([*all_roots,'--closure-roots','1','--checkpoint-dir',d/'all-batches'])
 assert all_batches['accepted']==all_plain['accepted']
 assert all_batches['axioms']==all_plain['axioms'] and len(all_batches['batches'])==1

 # Conflicting declarations in unrelated modules must retain their own contexts.
 for target in ['ShadowLeft','ShadowRight']:
  subprocess.run(['lake','build',target],cwd=project,check=True,timeout=60)
 common=[project,'--workers','1','--root','ShadowLeft','--root','ShadowRight']
 shadow_plain=invoke([*common,'--closure-roots','0','--checkpoint-dir',d/'shadow-plain'])
 shadow_batches=invoke([*common,'--closure-roots','1','--checkpoint-dir',d/'shadow-batches'])
 assert set(shadow_plain['accepted'])=={'ShadowLeft','ShadowRight'}
 assert shadow_batches['accepted']==shadow_plain['accepted']
 assert shadow_batches['axioms']==shadow_plain['axioms']

 # An actual compiled empty namespace module is accepted only after its imports.
 subprocess.run(['lake','build','Pkg'],cwd=project,check=True,timeout=60)
 pkg_roots=[project,'--workers','1','--root','Pkg','--root','Pkg.Child']
 pkg_plain=invoke([*pkg_roots,'--closure-roots','0','--checkpoint-dir',d/'pkg-plain'])
 pkg_batches=invoke([*pkg_roots,'--closure-roots','1','--checkpoint-dir',d/'pkg-batches'])
 assert pkg_batches['accepted']==pkg_plain['accepted'] and pkg_batches['axioms']==pkg_plain['axioms']
 assert 'Pkg' in pkg_batches['import_only_modules'] and len(pkg_batches['batches'])==1

 pkg_default=invoke([project,'--workers','1','--root','Pkg','--checkpoint-dir',d/'pkg-default'])
 assert pkg_default['accepted']==pkg_plain['accepted'] and 'Pkg' in pkg_default['import_only_modules']
 pkg_artifact=project/'.lake/build/lib/lean/Pkg.olean'
 original_pkg=pkg_artifact.read_bytes()
 try:
  pkg_artifact.write_bytes(original_pkg+b'changed')
  stale_pkg=subprocess.run([str(BINARY),str(project),'--workers','1','--root','Pkg','--root','Pkg.Child','--closure-roots','1','--checkpoint-dir',str(d/'pkg-batches')],text=True,capture_output=True,timeout=10)
  assert stale_pkg.returncode==2 and 'certified closure input changed' in stale_pkg.stderr
 finally:pkg_artifact.write_bytes(original_pkg)
 child=project/'.lake/build/lib/lean/Pkg/Child.olean'
 original_child=child.read_bytes()
 for mutation in ['bvar','unknown','sort']:
  try:
   child.write_bytes(original_child)
   bad_file=d/(mutation+'.olean')
   subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(child),'Pkg.Child',str(bad_file),mutation],check=True,text=True,capture_output=True,timeout=30)
   os.replace(bad_file,child)
   for limit in ['0','1']:
    rejected=invoke([project,'--workers','1','--root','Pkg','--closure-roots',limit,'--checkpoint-dir',d/('pkg-bad-'+mutation+'-'+limit)],1)
    assert rejected['status']=='rejected' and any(x.get('module')=='Pkg.Child'for x in rejected['rejected'])
  finally:child.write_bytes(original_child)

 # Empty does not imply that independently valid imports can be combined.
 original_pkg=pkg_artifact.read_bytes()
 try:
  bad_context=d/'bad-context.olean'
  subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(pkg_artifact),'Pkg',str(bad_context),'imports'],check=True,text=True,capture_output=True,timeout=30)
  os.replace(bad_context,pkg_artifact)
  for limit in ['0','1']:
   incompatible=subprocess.run([str(BINARY),str(project),'--workers','1','--root','Pkg','--closure-roots',limit,'--checkpoint-dir',str(d/('bad-context-'+limit))],text=True,capture_output=True,timeout=60)
   assert incompatible.returncode!=0,(limit,incompatible.stdout,incompatible.stderr)
   if incompatible.stdout:
    assert json.loads(incompatible.stdout).get('status')!='complete'
 finally:pkg_artifact.write_bytes(original_pkg)
 (project/'lean-toolchain').write_text('leanprover/lean4:not-supported\\n')
 badversion=subprocess.run([str(BINARY),str(project)],text=True,capture_output=True,timeout=10)
 assert badversion.returncode==2 and 'unsupported'in badversion.stderr
 print(json.dumps(dict(correct=True,axioms=True,resume=True,bad_proofs=3,closure_batches=True,batch_resume=True,changed_input_rejected=True,root_file=True,covered_roots_skipped=True,empty_root_file_rejected=True,empty_umbrella=True,empty_umbrella_bad_proofs=3,default_empty_umbrella=True,stale_empty_plan_rejected=True,incompatible_empty_imports_not_accepted=True)))
