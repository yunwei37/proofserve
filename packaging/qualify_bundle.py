#!/usr/bin/env python3
"""Exercise a locally installed archive without build-host paths or a source tree."""
import argparse,json,os,subprocess
from pathlib import Path
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 a.out.mkdir(parents=True,exist_ok=False)
 cli=(a.prefix/'bin/proofserve').resolve(strict=True);root=cli.parents[1];project=a.out/'project with spaces';project.mkdir()
 toolchain=(root/'share/proofserve/lean-toolchain').read_text()
 (project/'lean-toolchain').write_text(toolchain)
 (project/'lakefile.toml').write_text('name = "bundle_qualification"\nversion = "0.1.0"\ndefaultTargets = ["Fixture"]\n[[lean_lib]]\nname = "Base"\n[[lean_lib]]\nname = "Fixture"\n')
 (project/'Base.lean').write_text('prelude\nimport Init.Prelude\ntheorem bundle_base : True := True.intro\n')
 (project/'Fixture.lean').write_text('prelude\nimport Base\ntheorem bundle_ok : True := bundle_base\n')
 env=os.environ.copy();env.pop('LEAN_PATH',None);env.update(PATH=str(root/'bin')+os.pathsep+env.get('PATH',''),LEAN_SYSROOT=str(root),LD_LIBRARY_PATH=str(root/'lib/lean'))
 results=[]
 def run(label,args,expected=0,extra=None):
  e=dict(env);e.update(extra or {})
  c=subprocess.run(list(map(str,args)),cwd=project,env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
  (a.out/(label+'.stdout')).write_text(c.stdout);(a.out/(label+'.stderr')).write_text(c.stderr)
  results.append(dict(label=label,args=list(map(str,args)),returncode=c.returncode))
  assert c.returncode==expected,(label,c.returncode,c.stderr[-2000:])
  return c
 run('version',[cli,'--version'])
 run('build',[root/'bin/lake','build'])
 check=run('project-check',[cli,'check',project,'--workers','1','--json'])
 receipt=json.loads(check.stdout)
 assert receipt['status']=='complete' and {'Base','Fixture'}<=set(receipt['accepted'])
 receipt_file=project/'.proofserve/receipt.json';assert receipt_file.is_file()
 audit=run('project-audit',[cli,'audit',project,'--json','-','--receipt',receipt_file])
 report=json.loads(audit.stdout)
 assert report['schema']=='proofserve-audit/v1'
 for mode in ['default','fresh']:
  args=[root/'bin/lake','env','leanchecker','-v']
  if mode=='fresh':args+=['--fresh']
  run('official-'+mode,args+['Base','Fixture'])
 # Invoke the installed original-kernel component's internal protocol directly.
 # A public CLI usage error is never accepted as proof rejection.
 lean_path=run('lean-path',[root/'bin/lake','env','printenv','LEAN_PATH']).stdout.strip()
 for mutation in ['bvar','unknown','sort']:
  c=run('bad-'+mutation,[root/'libexec/proofserve-check','--internal-segment','audit',mutation,'Fixture'],expected=1,extra=dict(LEAN_PATH=lean_path,DECOUPLED_MUTATE_MODULE='Fixture',PROOFSERVE_WORKERS='1'))
  events=[json.loads(line)for line in c.stdout.splitlines()if line.startswith('{')]
  assert any(e.get('event')=='reject'and e.get('module')=='Fixture'for e in events),(mutation,c.stdout)
  assert not any(e.get('event')=='accept'and e.get('module')=='Fixture'for e in events)
 (project/'lean-toolchain').write_text('leanprover/lean4:v0.0.0-proofserve-unsupported\n')
 unsupported=run('unsupported',[cli,'check',project],expected=2)
 assert 'unsupported'in(unsupported.stderr+unsupported.stdout).lower()or 'toolchain'in(unsupported.stderr+unsupported.stdout).lower()
 (project/'lean-toolchain').write_text(toolchain)
 result=dict(complete=True,bundle=json.loads((root/'share/proofserve/bundle.json').read_text()),installed_root=str(root),receipt=receipt,audit=report,commands=results,malformed_proofs_rejected=3,scope='relocated archive correctness; not performance or external-project evaluation')
 (a.out/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(complete=True,malformed_proofs_rejected=3,source_commit=result['bundle']['source_commit'])))
if __name__=='__main__':main()
