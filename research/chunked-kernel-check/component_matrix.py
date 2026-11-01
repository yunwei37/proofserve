"""One finite common-lock window: qualify and measure component-preserving groups."""
import os,pathlib,json,sys,datetime
BASE=pathlib.Path(__file__).resolve().parent
RAW=BASE.parent
os.sched_setaffinity(0,set(range(8,16)))
sys.path.insert(0,str(BASE))
import run
def main():
 previous=json.loads((RAW/'frozen-grid-v3-continuation/terminal.json').read_text())
 assert previous['complete'] and previous['completed']==15,'review/complete the flat matrix first'
 fd=int(os.environ['CK_PCORE_LOCK_FD'])
 rows=[]
 try:
  sdk=str(run.SDK/'bin/lean');root='--root='+str(BASE)
  common=[sdk,root,'-j8','-DmaxHeartbeats=2000000']
  q1=run.cell('components-base-qualification',-1,
      argv=common+['-o',str(BASE/'ChunkBase.olean'),str(BASE/'ChunkBase.lean')])
  assert q1['returncode']==0
  q2=run.cell('components-equivalence-qualification',-1,
      argv=common+[str(BASE/'TargetEquivalence.lean')])
  assert q2['returncode']==0
  (BASE/'qualification.json').write_text(json.dumps(dict(base=q1,equivalence=q2),indent=2)+'\n')
  for rep in [1,2,3]:
   for k in ([8,4,2,1,0] if rep==2 else [0,1,2,4,8]):
    label=f'grid-components-v1-k{k}-r{rep}'
    r=run.cell(label,k)
    assert r['returncode']==0 and r['retired'] and not r['stop_reasons']
    rows.append(dict(k=k,rep=rep,raw=r['raw']))
    (BASE/'progress.json').write_text(json.dumps(dict(completed=len(rows),planned=15,last=label),indent=2)+'\n')
  (BASE/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
  (BASE/'terminal.json').write_text(json.dumps(dict(complete=True,completed=15,planned=15,qualified=True),indent=2)+'\n')
 except BaseException as e:
  (BASE/'terminal.json').write_text(json.dumps(dict(complete=False,completed=len(rows),error=repr(e)),indent=2)+'\n')
  raise
if __name__=='__main__':main()
