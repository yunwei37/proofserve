"""Per-stage matched comparisons; incomplete cells never become stable observations."""
from pathlib import Path
import json,csv,collections
def analyze(point,out):
 terminal=json.loads((point/'module-terminal.json').read_text())
 modules=json.loads((point/'modules.json').read_text())
 complete={};missing=[]
 for rep in [0,1]:
  for x in modules:
   short=x['module'].split('.')[-1]
   for mode in (['front','kernel']if x['regime']=='mathematical'else['kernel']):
    for j in [1,2,4,8]:
     key=f'{mode}-{short}-r{rep}-j{j}';p=point/'runs'/key
     if not(p/'result.json').exists():missing.append(key);continue
     result=json.loads((p/'result.json').read_text())
     prefix='FRONT 'if mode=='front'else'KERNEL '
     rr=[json.loads(s[len(prefix):])for s in(p/'stdout').read_text().splitlines()if s.startswith(prefix)]
     if result['returncode']or len(rr)!=(8 if mode=='front'else(rr[0]['selected']if rr else -1)) or not result['native_retired']or not result.get('cgroup_retired'):
      missing.append(key);continue
     unit={}
     for r in rr:
      if mode=='kernel':
       z=r['result'];uid=z['target'];hb=[z['rawHB']];cpu=z['cpuNS'];verdict=z['verdict'];errors=z['error']
      else:
       uid=r['index'];hb=[z['rawHB']for z in r['commands']]
       cpu=sum(z['cpuNS']for z in r['commands']);verdict=r['verdict'];errors=r['errors']
      if uid in unit:raise ValueError('duplicate unit '+key)
      unit[uid]=dict(module=x['module'],regime=x['regime'],stage=mode,repeat=rep,workers=j,
        unit=uid,heartbeats=hb,total_HB=sum(hb),cpu_ns=cpu,verdict=verdict,errors=errors,
        tid=r['result']['tid']if mode=='kernel'else r['tid'])
     complete[(x['module'],mode,rep,j)]=unit
 comparisons=[];ranges=[]
 for x in modules:
  for mode in (['front','kernel']if x['regime']=='mathematical'else['kernel']):
   for rep in [0,1]:
    baseline=complete.get((x['module'],mode,rep,1))
    for j in [2,4,8]:
     current=complete.get((x['module'],mode,rep,j))
     if baseline is None or current is None:continue
     if baseline.keys()!=current.keys():raise ValueError('unmatched targets')
     for uid,a in baseline.items():
      z=current[uid]
      comparisons.append(dict(module=x['module'],regime=x['regime'],stage=mode,repeat=rep,
       workers=j,unit=uid,verdict_equal=a['verdict']==z['verdict'],diagnostic_equal=a['errors']==z['errors'],
       heartbeat_equal=a['heartbeats']==z['heartbeats'],baseline_HB=a['total_HB'],current_HB=z['total_HB']))
   units=collections.defaultdict(list)
   for key,rows in complete.items():
    if key[:2]==(x['module'],mode):
     for uid,r in rows.items():units[uid].append(r)
   for uid,rr in units.items():
    h=[r['total_HB']for r in rr];c=[r['cpu_ns']/1e9 for r in rr]
    ranges.append(dict(module=x['module'],regime=x['regime'],stage=mode,unit=uid,
     observations=len(rr),min_HB=min(h),max_HB=max(h),
     HB_relative_range=(max(h)-min(h))/min(h)if min(h)else None,
     min_cpu_s=min(c),max_cpu_s=max(c),all_accepted=all(r['verdict']=='accepted'for r in rr)))
 summary=[]
 for x in modules:
  for mode in ['front','kernel']:
   cc=[r for r in comparisons if r['module']==x['module']and r['stage']==mode]
   if not cc:continue
   rr=[r for r in ranges if r['module']==x['module']and r['stage']==mode]
   summary.append(dict(module=x['module'],regime=x['regime'],stage=mode,pairs=len(cc),
    verdict_differences=sum(not r['verdict_equal']for r in cc),
    diagnostic_differences=sum(not r['diagnostic_equal']for r in cc),
    heartbeat_differences=sum(not r['heartbeat_equal']for r in cc),
    min_HB=min(r['min_HB']for r in rr),max_HB=max(r['max_HB']for r in rr),
    maximum_unit_relative_range=max((r['HB_relative_range']or 0)for r in rr)))
 out.mkdir(exist_ok=True)
 result=dict(raw=str(point),state=terminal['state'],complete_cells=len(complete),missing_cells=missing,
   summary=summary,ranges=ranges,comparisons=comparisons,
   scope='allocation heartbeats per executing worker; kernel-only CPU separate from source command CPU; native kernel poll count unobserved')
 (out/'summary.json').write_text(json.dumps(result,indent=2))
 for name,rr in [('pairs',comparisons),('ranges',ranges),('module-summary',summary)]:
  if rr:
   with(out/(name+'.csv')).open('w')as f:
    w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
 return result
if __name__=='__main__':
 import sys
 r=analyze(Path(sys.argv[1]),Path(sys.argv[2]))
 print(json.dumps({k:r[k]for k in ['state','complete_cells','missing_cells','summary']},indent=2))
