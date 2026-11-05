#!/usr/bin/env python3
"""Release backend correctness contract; no machine-specific paths."""
import contextlib,sys,json,os,subprocess,tempfile,shutil,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'tests/test_release.py')],check=True)
BINARY=Path(os.environ.get('PROOFSERVE_CHECK',str(ROOT/'.lake/build/bin/proofserve-check'))).resolve()
def invoke(args,expected=0,env=None):
 r=subprocess.run([str(BINARY),*map(str,args)],text=True,capture_output=True,timeout=60,env=env)
 assert r.returncode==expected,(r.returncode,r.stdout,r.stderr)
 return json.loads(r.stdout)
owned=os.environ.get('PROOFSERVE_CONTRACT_WORK')
if owned:Path(owned).mkdir(parents=True,exist_ok=False)
with(contextlib.nullcontext(owned)if owned else tempfile.TemporaryDirectory(prefix='proofserve-contract-'))as td:
 d=Path(td);project=d/'project';project.mkdir()
 for f in ['Base.lean','Parts.lean','Fixture.lean','ShadowLeft.lean','ShadowRight.lean','All.lean','Pkg.lean','Pkg/Child.lean','lakefile.lean','lean-toolchain']:
  (project/f).parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(ROOT/'tests'/f,project/f)
 version=subprocess.check_output(['lean','--version'],text=True).split('version ',1)[1].split(',',1)[0]
 (project/'lean-toolchain').write_text('leanprover/lean4:v'+version+'\n')
 subprocess.run(['lake','build'],cwd=project,check=True,timeout=60)
 full=invoke([project,'--workers','1','--checkpoint-dir',d/'full'])
 assert full['status']=='complete'and set(full['accepted'])=={'Base','Fixture'}
 assert full['theorem_body_policy']=='shared-checked'
 strict_full=invoke([project,'--workers','1','--checkpoint-dir',d/'strict-full','--strict-theorem-bodies'])
 assert strict_full['theorem_body_policy']=='strict'
 assert strict_full['accepted']==full['accepted'] and strict_full['axioms']==full['axioms']
 for state,flags in [(d/'full',['--strict-theorem-bodies']),(d/'strict-full',[])]:
  changed=subprocess.run([str(BINARY),str(project),'--workers','1','--checkpoint-dir',str(state),*flags],text=True,capture_output=True,timeout=60)
  assert changed.returncode==2 and 'checkpoint configuration changed' in changed.stderr
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
 strict_batches=invoke([project,'--workers','1','--closure-roots','1','--checkpoint-dir',d/'strict-batches','--strict-theorem-bodies'])
 assert strict_batches['theorem_body_policy']=='strict' and strict_batches['accepted']==full['accepted']
 for state,flags in [(d/'batches',['--strict-theorem-bodies']),(d/'strict-batches',[])]:
  changed=subprocess.run([str(BINARY),str(project),'--workers','1','--closure-roots','1','--checkpoint-dir',str(state),*flags],text=True,capture_output=True,timeout=60)
  assert changed.returncode==2 and 'checkpoint configuration changed' in changed.stderr

 # A genuine certificate from the other policy is invalid even if the
 # receiving directory's own policy identity was never edited.
 certificate=d/'batches/batch-0/certified.json'
 original_certificate=certificate.read_bytes()
 try:
  certificate.write_bytes((d/'strict-batches/batch-0/certified.json').read_bytes())
  transplanted=subprocess.run([str(BINARY),str(project),'--workers','1','--closure-roots','1','--checkpoint-dir',str(d/'batches')],text=True,capture_output=True,timeout=60)
  assert transplanted.returncode==2 and 'closure certificate configuration differs' in transplanted.stderr
 finally:certificate.write_bytes(original_certificate)
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
 assert partitioned['reuse_checked_imports'] is True
 assert partitioned['module_check_entries']==len(full['accepted'])
 assert partitioned['trusted_import_entries']>=1
 cached_events=json.loads((d/'batches/batch-1/segment-0.json').read_text())['events']
 assert any(e.get('event')=='trusted_import' and e.get('module')=='Base'for e in cached_events)
 assert not any(e.get('event')=='accept' and e.get('module')=='Base'for e in cached_events)
 legacy=invoke([project,'--workers','1','--closure-roots','1','--replay-shared-imports','--checkpoint-dir',d/'legacy-replay'])
 assert legacy['accepted']==full['accepted'] and legacy['module_check_entries']==3

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
 for strict in ['0','1']:
  for mutation in ['bvar','unknown','sort']:
   e=dict(os.environ,LEAN_PATH=paths,DECOUPLED_MUTATE_MODULE='Fixture',PROOFSERVE_WORKERS='2',PROOFSERVE_STRICT_THEOREM_BODIES=strict)
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
 assert all_batches['axioms']==all_plain['axioms'] and len(all_batches['batches'])==2
 assert 'All'in all_batches['import_only_modules']


 # A nonempty early root covers later roots; it is not an empty aggregator.
 (project/'AFirst.lean').write_text('prelude\nimport Fixture\ntheorem earlyProof : TinyTruth := fixtureProof\n')
 with(project/'lakefile.lean').open('a')as f:f.write('\nlean_lib AFirst\n')
 subprocess.run(['lake','build','AFirst'],cwd=project,check=True,timeout=60)
 first_roots=[project,'--workers','1','--root','AFirst','--root','Base','--root','Fixture']
 first_plain=invoke([*first_roots,'--closure-roots','0','--checkpoint-dir',d/'first-plain'])
 first_batched=invoke([*first_roots,'--closure-roots','1','--checkpoint-dir',d/'first-batched'])
 assert first_batched['accepted']==first_plain['accepted'] and len(first_batched['batches'])==3
 assert json.loads((d/'first-batched/closure-plan.json').read_text())['order']=='dependencies-first'
 covered_legacy=invoke([*first_roots,'--closure-roots','1','--replay-shared-imports','--checkpoint-dir',d/'covered-legacy'])
 assert covered_legacy['accepted']==first_plain['accepted'] and len(covered_legacy['batches'])==1
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
   assert incompatible.returncode==1,(limit,incompatible.stdout,incompatible.stderr)
   if incompatible.stdout:
    assert json.loads(incompatible.stdout).get('status')!='complete'
 finally:pkg_artifact.write_bytes(original_pkg)

 # A bad proof inside a dependency must not gain a first certificate. A
 # previously certified dependency changed later must invalidate a resumed run.
 (project/'ZAfter.lean').write_text('prelude\nimport Fixture\ntheorem finalProof : TinyTruth := fixtureProof\n')
 with(project/'lakefile.lean').open('a')as f:f.write('\nlean_lib ZAfter\n')
 subprocess.run(['lake','build','ZAfter'],cwd=project,check=True,timeout=60)
 proof_file=project/'.lake/build/lib/lean/Fixture.olean'
 original_proof=proof_file.read_bytes()
 z_roots=[project,'--workers','1','--root','Fixture','--root','ZAfter','--closure-roots','1']
 z_partial=invoke([*z_roots,'--max-segments','1','--checkpoint-dir',d/'z-resume'],2)
 assert z_partial['batches'][0]['status']=='complete'
 try:
  bad_file=d/'cached-bad-dependency.olean'
  subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(proof_file),'Fixture',str(bad_file),'bvar'],check=True,text=True,capture_output=True,timeout=30)
  os.replace(bad_file,proof_file)
  changed=subprocess.run([str(BINARY),*map(str,[*z_roots,'--checkpoint-dir',d/'z-resume'])],text=True,capture_output=True,timeout=60)
  assert changed.returncode==2 and 'certified closure input changed'in changed.stderr
  hidden=invoke([project,'--workers','1','--root','Base','--root','ZAfter','--closure-roots','1','--checkpoint-dir',d/'hidden-bad'],1)
  assert any(e['module']=='Fixture'for e in hidden['rejected'])
 finally:proof_file.write_bytes(original_proof)
 z_done=invoke([*z_roots,'--checkpoint-dir',d/'z-resume'])
 assert z_done['module_check_entries']==3 and z_done['trusted_import_entries']>=2
 assert set(z_done['accepted'])=={'Base','Fixture','ZAfter'}
 # Dependency order within a batch differs from the child's sorted argument
 # order. Binding must compare the same root set rather than reject a permutation.
 permuted=invoke([project,'--workers','1','--root','AFirst','--root','Base','--root','Fixture','--root','ZAfter','--closure-roots','3','--checkpoint-dir',d/'permuted-batch'])
 assert set(permuted['accepted'])=={'Base','Fixture','AFirst','ZAfter'}
 assert permuted['module_check_entries']==4



 # A cached base must survive a successful segment boundary. Its declarations
 # were deliberately omitted from the new checkpoint's constant delta.
 for name,body in [
  ('ZMid','prelude\nimport Fixture\ntheorem midProof : TinyTruth := fixtureProof\n'),
  ('ZZLast','prelude\nimport ZMid\ntheorem lastProof : TinyTruth := midProof\n')]:
  (project/(name+'.lean')).write_text(body)
  with(project/'lakefile.lean').open('a')as f:f.write('\nlean_lib '+name+'\n')
  subprocess.run(['lake','build',name],cwd=project,check=True,timeout=60)
 chain_args=[project,'--workers','1','--root','Base','--root','Fixture','--root','ZMid','--root','ZZLast']
 chain_plain=invoke([*chain_args,'--closure-roots','0','--checkpoint-dir',d/'chain-plain'])
 chain_split=invoke([*chain_args,'--closure-roots','2','--segment-modules','1','--checkpoint-dir',d/'chain-split'])
 assert chain_split['accepted']==chain_plain['accepted']
 assert chain_split['module_check_entries']==4 and chain_split['trusted_import_entries']>=2
 assert len(chain_split['segments'])>=4

 # A completed dependency changed between live batches must be checked again
 # against its recorded bytes, not merely trusted until a process restart.
 bad_live=d/'bad-live.olean'
 subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(proof_file),'Fixture',str(bad_live),'bvar'],check=True,text=True,capture_output=True,timeout=30)
 changed_live=[]
 def change_after_first_certificate():
  deadline=time.monotonic()+60
  while time.monotonic()<deadline:
   if(d/'live-change/batch-0/certified.json').exists():
    os.replace(bad_live,proof_file);changed_live.append(True);return
   time.sleep(.001)
 thread=threading.Thread(target=change_after_first_certificate);thread.start()
 try:
  live_change=subprocess.run([str(BINARY),*map(str,[*z_roots,'--checkpoint-dir',d/'live-change'])],text=True,capture_output=True,timeout=60)
  thread.join(1)
  assert changed_live and not thread.is_alive()
  assert live_change.returncode!=0
  assert not live_change.stdout or json.loads(live_change.stdout).get('status')!='complete'
 finally:proof_file.write_bytes(original_proof)

 # Valid contexts that conflict in their union must fall back to module-local
 # checking, without replaying already certified import proof bodies.
 for side in ['Left','Right']:
  name='ZUse'+side
  (project/(name+'.lean')).write_text('prelude\nimport Shadow'+side+'\ndef alias'+side+' : Shade := chosen\n')
  with(project/'lakefile.lean').open('a')as f:f.write('\nlean_lib '+name+'\n')
  subprocess.run(['lake','build',name],cwd=project,check=True,timeout=60)
 incompatible_roots=[project,'--workers','1','--root','ShadowLeft','--root','ShadowRight','--root','ZUseLeft','--root','ZUseRight']
 unrelated_plain=invoke([*incompatible_roots,'--closure-roots','0','--checkpoint-dir',d/'unrelated-plain'])
 unrelated_cached=invoke([*incompatible_roots,'--closure-roots','2','--checkpoint-dir',d/'unrelated-cached'])
 assert set(unrelated_cached['accepted'])==set(unrelated_plain['accepted'])
 assert unrelated_cached['module_check_entries']==4
 fallback_events=json.loads((d/'unrelated-cached/batch-1/segment-0.json').read_text())['events']
 assert any(e.get('event')=='certified_context_fallback'for e in fallback_events)
 # A completed input need not be imported by a later batch. The final union
 # must still revalidate it, rather than silently reporting current acceptance.
 changed_unused=[]
 def change_unused_after_certificate():
  deadline=time.monotonic()+60
  while time.monotonic()<deadline:
   if(d/'unused-change/batch-0/certified.json').exists():
    artifact.write_bytes(old+b'changed after completed batch');changed_unused.append(True);return
   time.sleep(.001)
 thread=threading.Thread(target=change_unused_after_certificate);thread.start()
 try:
  unused=subprocess.run([str(BINARY),*map(str,[project,'--workers','1','--root','Base','--root','ZUseRight','--closure-roots','1','--checkpoint-dir',d/'unused-change'])],text=True,capture_output=True,timeout=60)
  thread.join(1)
  assert changed_unused and not thread.is_alive()
  assert unused.returncode==2 and 'certified closure input changed'in unused.stderr
 finally:artifact.write_bytes(old)


 # A checked sibling brought into a combined cache is still invisible to a
 # module that did not import it. Its ill-scoped proof must reach native reject.
 scope_sources={
  'Shared':'prelude\nimport Base\nnamespace Shared\ntheorem externalProof : TinyTruth := fixtureAssumption\nend Shared\n',
  'ZAllowed':'prelude\nimport Shared\ntheorem allowedProof : TinyTruth := Shared.externalProof\n',
  'ZBlocked':'prelude\nimport Base\ntheorem blockedProof : TinyTruth := fixtureAssumption\n'}
 for name,text in scope_sources.items():
  (project/(name+'.lean')).write_text(text)
  with(project/'lakefile.lean').open('a')as f:f.write('\nlean_lib '+name+'\n')
  subprocess.run(['lake','build',name],cwd=project,check=True,timeout=60)
 blocked=project/'.lake/build/lib/lean/ZBlocked.olean';original_blocked=blocked.read_bytes()
 try:
  invalid=d/'bad-sibling.olean'
  subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(blocked),'ZBlocked',str(invalid),'sibling'],check=True,text=True,capture_output=True,timeout=30)
  os.replace(invalid,blocked)
  blocked_plain=invoke([project,'--workers','1','--root','ZBlocked','--closure-roots','0','--checkpoint-dir',d/'blocked-plain'],1)
  blocked_roots=[project,'--workers','1','--root','Base','--root','Shared','--root','ZAllowed','--root','ZBlocked','--closure-roots','2','--checkpoint-dir',d/'blocked-cached']
  blocked_cached=invoke(blocked_roots,1)
  assert any(r.get('module')=='ZBlocked'for r in blocked_plain['rejected'])
  assert any(r.get('module')=='ZBlocked'for r in blocked_cached['rejected'])
  assert 'unimported_reference'in(d/'blocked-cached/batch-1/segment-0.events').read_text()
 finally:blocked.write_bytes(original_blocked)
 # O's unchanged-certificate cases: project identity and optional-part inventory.
 subprocess.run(['lake','build','Parts'],cwd=project,check=True,timeout=60)
 part_args=[project,'--workers','1','--root','Parts','--closure-roots','1']
 part_file=project/'.lake/build/lib/lean/Parts.olean'
 staged=d/'optional-parts.olean'
 subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(part_file),'Parts',str(staged),'staged-good'],check=True,capture_output=True,text=True,timeout=30)
 for suffix in ['', '.server', '.private']:shutil.copy2(Path(str(staged)+suffix),Path(str(part_file)+suffix))
 part_state=d/'part-certificate'
 good_parts=invoke([*part_args,'--checkpoint-dir',part_state])
 cert_bytes=(part_state/'batch-0/certified.json').read_bytes()
 for label,section,field,value in [
  ('identity-lean','input_identity','lean','Lean (version 4.35.0)\\n'),
  ('receipt-lean','receipt','lean_version','Lean (version 4.35.0)\\n'),
  ('child-abi','input_identity','checker_checkpoint_abi',999)]:
  state=d/label;shutil.copytree(part_state,state)
  cert=state/'batch-0/certified.json';v=json.loads(cert.read_text())
  v[section][field]=value;cert.write_text(json.dumps(v))
  failure=subprocess.run([str(BINARY),*map(str,[*part_args,'--checkpoint-dir',state])],text=True,capture_output=True,timeout=60)
  assert failure.returncode==2 and not failure.stdout,(label,failure.stdout,failure.stderr)
 foreign=d/'foreign-project';shutil.copytree(project,foreign)
 foreign_part=foreign/'.lake/build/lib/lean/Parts.olean'
 invalid=d/'foreign-invalid.olean'
 subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(foreign_part),'Parts',str(invalid),'staged'],check=True,text=True,capture_output=True,timeout=30)
 for suffix in ['', '.server', '.private']:shutil.copy2(Path(str(invalid)+suffix),Path(str(foreign_part)+suffix))
 transplant=d/'authentic-transplant';(transplant/'batch-0').mkdir(parents=True)
 shutil.copy2(part_state/'batch-0/certified.json',transplant/'batch-0/certified.json')
 transplanted=subprocess.run([str(BINARY),str(foreign),'--workers','1','--root','Parts','--closure-roots','1','--checkpoint-dir',str(transplant)],text=True,capture_output=True,timeout=60)
 assert transplanted.returncode==2 and not transplanted.stdout and 'project'in transplanted.stderr
 assert (transplant/'batch-0/certified.json').read_bytes()==cert_bytes
 fresh_foreign=invoke([foreign,'--workers','1','--root','Parts','--closure-roots','1','--checkpoint-dir',d/'foreign-fresh'],1)
 assert fresh_foreign['status']=='rejected'
 original_part=part_file.read_bytes()
 subprocess.run(['lean','--run',str(ROOT/'tests/Mutate.lean'),str(part_file),'Parts',str(staged),'staged'],check=True,capture_output=True,text=True,timeout=30)
 for suffix in ['.server','.private']:
  shutil.copy2(Path(str(staged)+suffix),Path(str(part_file)+suffix))
 try:
  unchanged=subprocess.run([str(BINARY),*map(str,[*part_args,'--checkpoint-dir',part_state])],text=True,capture_output=True,timeout=60)
  assert unchanged.returncode==2 and not unchanged.stdout and 'certified closure input changed'in unchanged.stderr,(unchanged.returncode,unchanged.stdout,unchanged.stderr)
  assert part_file.read_bytes()==original_part and (part_state/'batch-0/certified.json').read_bytes()==cert_bytes
  private_fresh=invoke([*part_args,'--checkpoint-dir',d/'parts-fresh'],1)
  assert private_fresh['status']=='rejected'
  native_official=subprocess.run(['lake','env','leanchecker','-v','Parts'],cwd=project,text=True,capture_output=True,timeout=60)
  assert native_official.returncode!=0
 finally:
  for suffix in ['.server','.private']:Path(str(part_file)+suffix).unlink()
 # Inject the kernel's ENOSPC result into the final pending receipt only.
 # This works on ordinary Linux CI without mount or root privileges.
 if Path('/dev/full').exists():
  full_seed=d/'receipt-seed'
  full_args=[project,'--workers','1','--root','Base','--closure-roots','1']
  invoke([*full_args,'--checkpoint-dir',full_seed])
  full_state=d/'receipt-full';shutil.copytree(full_seed,full_state)
  old_receipt=(full_state/'receipt.json').read_bytes()
  (full_state/'receipt.json.pending').symlink_to('/dev/full')
  disk_full=subprocess.run([str(BINARY),*map(str,[*full_args,'--checkpoint-dir',full_state])],text=True,capture_output=True,timeout=60)
  assert disk_full.returncode==2 and not disk_full.stdout and 'publish checkpoint'in disk_full.stderr,(disk_full.returncode,disk_full.stdout,disk_full.stderr)
  assert (full_state/'receipt.json').read_bytes()==old_receipt
  json.loads(old_receipt)
 (project/'lean-toolchain').write_text('leanprover/lean4:not-supported\\n')
 badversion=subprocess.run([str(BINARY),str(project)],text=True,capture_output=True,timeout=10)
 assert badversion.returncode==2 and 'unsupported'in badversion.stderr
 print(json.dumps(dict(correct=True,axioms=True,resume=True,bad_proofs=3,closure_batches=True,batch_resume=True,changed_input_rejected=True,root_file=True,covered_roots_skipped=True,empty_root_file_rejected=True,empty_umbrella=True,empty_umbrella_bad_proofs=3,default_empty_umbrella=True,stale_empty_plan_rejected=True,incompatible_empty_imports_not_accepted=True,checked_import_reuse=True,hidden_bad_dependency_rejected=True,changed_completed_dependency_rejected=True,live_changed_dependency_rejected=True,incompatible_cached_contexts=True,unused_completed_input_change_rejected=True,leaf_empty_aggregator_detected=True,sibling_scope_rejected=True,dependency_root_order=True,permuted_batch_roots=True,cached_segment_base_restored=True,authentic_cross_project_certificate_refused=True,optional_part_inventory_refused=True,receipt_lean_refused=True,child_abi_refused=True,disk_full_fails_closed=True)))

# Explicitly validate the proof-body check that upstream duplicate replay skips.
subprocess.run(['lake','env','lean','--run',str(ROOT/'tests/DuplicateBodyCheck.lean')],cwd=ROOT,check=True,timeout=60)

# All code-review regressions are part of this existing CI entry point.
subprocess.run([sys.executable,str(ROOT/'tests/review_e0.py')],check=True,timeout=1800)

# Second supplied review: context, IR, exit, receipt and discovery regressions.
subprocess.run([sys.executable,str(ROOT/"tests/review_2628.py")],check=True,timeout=1800)
