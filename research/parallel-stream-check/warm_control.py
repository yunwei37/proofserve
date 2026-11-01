from native import ROOT,run,environment,SDK
import os,json
os.sched_setaffinity(0,set(range(8)))
e=environment();e['LEAN_PATH']=str(ROOT/'fixtures')+':'+str(SDK/'lib/lean')
rows=[]
for mutation,expected in [('none',0),('bvar',1)]:
 key='warm-control-'+mutation
 rr=run(key,[ROOT/'warm-curve','Waves',mutation],90,False,e)
 events=[json.loads(l)for l in(ROOT/'runs'/key/'stdout').read_text().splitlines()if l.startswith('{')]
 assert rr['returncode']==expected and rr['native_retired'] and rr['cgroup_retired']
 if mutation=='none':assert sum(x.get('event')=='curve_cell'for x in events)==5
 else:assert any(x.get('event')=='reject'and 'loose bound variables'in x['error']for x in events)
 rows.append(dict(mutation=mutation,result=rr,events=events))
(ROOT/'warm-controls-qualified.json').write_text(json.dumps(rows,indent=2))
