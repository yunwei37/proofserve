"""Strict completed-cell tables; never turn missing/failed cells into timing."""
import json,csv,statistics
from pathlib import Path
CAP=Path('/workspaces/.agent-state/gpu-smt-captures')
OUT=Path(__file__).resolve().parent
def stats(xs):return(dict(median=statistics.median(xs),minimum=min(xs),maximum=max(xs)))
def stream_tables(only=None):
 P=CAP/'parallel-stream-wall-20261103'
 if only is None:assert json.loads((P/'matrix-terminal.json').read_text())['complete']
 rows=[];summary=[]
 for dataset,count,arms in[('math',1330,['reference','parallel1','parallel8']),('grid',3793,['reference','parallel1','parallel4','parallel8'])]:
  if only is not None and dataset!=only:continue
  reference=None
  for arm in arms:
   group=[]
   for rep in[1,2,3]:
    c=json.loads((P/(dataset+'-'+arm+'-r'+str(rep)+'-terminal.json')).read_text())
    assert c['qualified']and c['returncode']==0 and not c['stop_reasons']and c['native_retired']and c['cgroup_retired']
    assert len(c['accepted_IDs'])==count
    if reference is None:reference=c['accepted_IDs']
    assert c['accepted_IDs']==reference
    row=dict(dataset=dataset,arm=arm,repeat=rep,wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],
      peak_rss_GiB=c['peak_rss_kib']/1024**2,sampled_tree_peak_GiB=c['sampled_tree_peak_bytes']/1024**3,
      checked_modules=count,source='default-persistent plain, no-M/no-profile')
    rows.append(row);group.append(row)
   item=dict(dataset=dataset,arm=arm,repeats=3,checked_modules=count)
   for metric in['wall_s','cpu_s','peak_rss_GiB']:
    for stat,value in stats([x[metric]for x in group]).items():item[metric+'_'+stat]=value
   summary.append(item)
  base=next(x for x in summary if x['dataset']==dataset and x['arm']=='reference')
  for x in summary:
   if x['dataset']==dataset:x['strong_serial_speedup']=base['wall_s_median']/x['wall_s_median']
 for name,data in[('corrected-stream-repeats.csv',rows),('corrected-stream-summary.csv',summary)]:
  with(OUT/(((only+'-')if only else'')+name)).open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 print(json.dumps(summary,indent=2))
def barrier_tables():
 P=CAP/'parallel-stream-barrier-corrected-20261103';old=CAP/'chunked-kernel-check/parallel-barrier-v1'
 assert json.loads((P/'terminal.json').read_text())['complete']
 data=[];reference=None
 for phase,source in[('unmarked-old',old),('default-persistent-new',P)]:
  rows=json.loads((source/'completed.json').read_text());assert len(rows)==15
  for c in rows:
   c['native_cpu_s']=c['native_user_s']+c['native_system_s']
   if reference is None:reference=c['acceptance']['names']
   assert c['acceptance']['names']==reference and c['acceptance']['typed_constants_identical']
  for k in[0,1,2,4,8]:
   group=[x for x in rows if x['k']==k]
   assert len(group)==3 and all(x['accepted']and x['all_native_retired']for x in group)
   assert all(x['acceptance']['count']==3425 for x in group)
   r=dict(phase=phase,k=k,repeats=3,scope='single original module, imports trusted; wave export/reimport and final original CI audit')
   for metric in['whole_pipeline_wall_s','native_cpu_s','native_user_s','native_system_s','peak_rss_kib']:
    for stat,value in stats([x[metric]for x in group]).items():r[metric+'_'+stat]=value
   data.append(r)
  base=next(x for x in data if x['phase']==phase and x['k']==0)
  for x in data:
   if x['phase']==phase:x['direct_stock_speedup']=base['whole_pipeline_wall_s_median']/x['whole_pipeline_wall_s_median']
 with(OUT/'corrected-historical-barrier.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 print(json.dumps(data,indent=2))
if __name__=='__main__':
 import sys
 if sys.argv[1]=='stream':stream_tables()
 elif sys.argv[1]=='stream-math':stream_tables('math')
 elif sys.argv[1]=='stream-grid':stream_tables('grid')
 elif sys.argv[1]=='barrier':barrier_tables()
