"""Finite stock-vs-wave original-kernel qualification and Barrier curve.
Run on P0-7 under the shared lease. Never automatically continue another capture.
"""
import os,json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from declaration_native import run,environment
BINARY=ROOT/'parallel-replay'
def events(key):
 return [json.loads(x) for x in (ROOT/'runs'/key/'stdout').read_text().splitlines() if x.startswith('{')]
def only(key,event):
 values=[x for x in events(key) if x.get('event')==event]
 assert len(values)==1,(key,event,len(values))
 return values[0]
def cell(key,target,k,mutation='none',measured=True,limit=300):
 """The baseline is direct stock replay. k>0 includes graph, wave imports/exports and final audit."""
 out=ROOT/'cells'/key;out.mkdir(parents=True,exist_ok=False)
 artifacts=out/'artifacts';artifacts.mkdir()
 env=environment();env.update(LEAN_NUM_THREADS=str(max(1,k)),LEAN_PATH=str(artifacts)+':'+env['LEAN_PATH'])
 config=out/'config.json'
 def cfg(**extra):
  config.write_text(json.dumps(dict(mutation=mutation,prior=[],**extra))+'\n')
 def invoke(stage,mode,cap=120):
  frozen_config=out/(stage+'-config.json');frozen_config.write_bytes(config.read_bytes())
  return run(key+'-'+stage,[BINARY,mode,target,frozen_config],min(cap,max(1,int(deadline-time.monotonic()))),measured=measured,env=env)
 begin=time.monotonic();deadline=begin+limit;records=[]
 cfg()
 if k==0:
  record=invoke('stock','stock',limit);records.append(record)
  ok=record['returncode']==0 and not record['stop_reasons']
  accepted=only(record['key'],'accepted') if ok else None
 else:
  record=invoke('plan','plan',90);records.append(record)
  if record['returncode'] or record['stop_reasons']:raise RuntimeError('plan failed')
  plan=only(record['key'],'plan');(out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
  prior=[];ok=True
  for wave,jobs in enumerate(plan['levels']):
   prefix='MDecl'+key.replace('-','_')+'L'+str(wave)
   config.write_text(json.dumps(dict(mutation=mutation,prior=prior,jobs=jobs,k=k,prefix=prefix,out=str(artifacts)))+'\n')
   record=invoke('L'+str(wave),'wave');records.append(record)
   if record['returncode'] or record['stop_reasons']:
    ok=False;break
   result=only(record['key'],'wave_complete')
   actual=[i for w in result['workers'] for i in w['indices']]
   assert len(actual)==len(set(actual)) and sorted(actual)==sorted(jobs)
   prior=[w['module'] for w in result['workers']]
   (out/('wave-'+str(wave)+'.json')).write_text(json.dumps(result,indent=2)+'\n')
  accepted=None
  if ok:
   config.write_text(json.dumps(dict(mutation=mutation,prior=prior))+'\n')
   record=invoke('audit','audit',90);records.append(record)
   ok=record['returncode']==0 and not record['stop_reasons']
   if ok:accepted=only(record['key'],'accepted')
 result=dict(key=key,k=k,mutation=mutation,accepted=bool(ok),acceptance=accepted,
   whole_pipeline_wall_s=time.monotonic()-begin,
   native_user_s=sum(x.get('user_s',0) for x in records),
   native_system_s=sum(x.get('system_s',0) for x in records),
   peak_rss_kib=max(x.get('peak_rss_kib',0) for x in records),
   charged_peak_bytes=max(x.get('charged_peak_bytes',0) for x in records),
   all_native_retired=all(x.get('native_retired') and x.get('cgroup_retired') for x in records),
   stage_keys=[x['key'] for x in records],meaning='source-independent replay of already compiled target; imported dependencies trusted as stock leanchecker')
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='acceptance'}),flush=True)
 return result
def qualification(fixture,measured=False):
 # Tiny finite native controls, not timing evidence.
 stock=cell('qual-stock',fixture,0,measured=measured,limit=90)
 wave=cell('qual-wave',fixture,4,measured=measured,limit=120)
 assert stock['accepted'] and wave['accepted']
 assert stock['acceptance']['names']==wave['acceptance']['names']
 negatives=[]
 for mutation in ['bvar','unknown','sort']:
  a=cell('qual-stock-'+mutation,fixture,0,mutation,measured=measured,limit=90)
  b=cell('qual-wave-'+mutation,fixture,4,mutation,measured=measured,limit=120)
  assert not a['accepted'] and not b['accepted']
  negatives.append(dict(mutation=mutation,stock_reject=True,wave_reject=True))
 result=dict(positive_typed_constants_and_names_equal=True,malformed_proof_rejections=negatives,
   note='no speed claim; artifacts produced only from original checked kernel branches and normal module imports')
 (ROOT/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 assert (ROOT/'qualification.json').exists()
 start=time.monotonic();target=json.loads((ROOT/'input.json').read_text())['olean']
 rows=[];baseline=None
 for repeat in range(3):
  for k in [0,1,2,4,8]:
   if time.monotonic()-start+300+20>1680:
    (ROOT/'budget-stop.json').write_text(json.dumps(dict(next_repeat=repeat,next_k=k,completed=len(rows)))+'\n')
    break
   result=cell(f'r{repeat}-k{k}',target,k,limit=300)
   assert result['accepted'] and result['all_native_retired']
   if baseline is None:baseline=result['acceptance']['names']
   assert baseline==result['acceptance']['names'],'acceptance order/set differs'
   rows.append(result)
   (ROOT/'completed.json').write_text(json.dumps(rows,indent=2)+'\n')
  else:continue
  break
 (ROOT/'terminal.json').write_text(json.dumps(dict(complete=len(rows)==15,planned=15,completed=len(rows),all_complete_accept=True))+'\n')
if __name__=='__main__':main()
