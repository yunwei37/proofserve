"""Whole-pipeline Barrier curve; refuses pending or failed matrices."""
from pathlib import Path
import json,csv,statistics,argparse
HERE=Path(__file__).resolve().parent
def write(name,rows):
 with (HERE/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('point',type=Path);args=ap.parse_args();p=args.point
 terminal=json.loads((p/'terminal.json').read_text())
 assert terminal['complete'] and terminal['completed']==15,'partial not a complete curve'
 cells=json.loads((p/'completed.json').read_text());assert len(cells)==15
 baseline=cells[0]['acceptance'];rows=[];stage_rows=[]
 for cell in cells:
  assert cell['accepted'] and cell['all_native_retired']
  assert cell['acceptance']==baseline,'typed audit/name/order parity failed'
  rep=int(cell['key'].split('-')[0][1:]);k=cell['k']
  stages=[]
  for key in cell['stage_keys']:
   result=json.loads((p/'runs'/key/'result.json').read_text())
   assert result['returncode']==0 and result['native_retired'] and result['cgroup_retired']
   assert result['measured'] and result['affinity']==list(range(8)) and not result['stop_reasons']
   assert all(not str(a).startswith('-M') for a in result['argv'])
   stage=dict(k=k,rep=rep,key=key,wall_s=result['wall_s'],user_s=result['user_s'],system_s=result['system_s'],
     peak_rss_kib=result['peak_rss_kib'],raw=str(p/'runs'/key))
   stage_rows.append(stage);stages.append(stage)
  rows.append(dict(k=k,rep=rep,whole_pipeline_wall_s=cell['whole_pipeline_wall_s'],
    native_cpu_s=cell['native_user_s']+cell['native_system_s'],
    native_user_s=cell['native_user_s'],native_system_s=cell['native_system_s'],
    peak_rss_kib=cell['peak_rss_kib'],charged_peak_bytes=cell['charged_peak_bytes'],
    native_stage_wall_s=sum(x['wall_s'] for x in stages),
    python_and_interstage_wall_s=cell['whole_pipeline_wall_s']-sum(x['wall_s'] for x in stages),
    checked_declarations=baseline['count'],raw=str(p/'cells'/cell['key'])))
 summary=[]
 for k in [0,1,2,4,8]:
  rr=[r for r in rows if r['k']==k];assert len(rr)==3
  for metric in ['whole_pipeline_wall_s','native_cpu_s','native_user_s','native_system_s','peak_rss_kib','charged_peak_bytes','python_and_interstage_wall_s']:
   vals=[r[metric] for r in rr]
   summary.append(dict(k=k,metric=metric,n=3,median=statistics.median(vals),minimum=min(vals),maximum=max(vals)))
 ratios=[]
 for row in rows:
  direct=next(r for r in rows if r['k']==0 and r['rep']==row['rep'])
  ratios.append(dict(k=row['k'],rep=row['rep'],stock_over_wave_wall_ratio=direct['whole_pipeline_wall_s']/row['whole_pipeline_wall_s']))
 write('parallel-per-repeat.csv',rows);write('parallel-stages.csv',stage_rows)
 write('parallel-summary.csv',summary);write('parallel-paired-ratios.csv',ratios)
 quality=dict(complete_cells=15,accepted=15,typed_constants_and_original_name_order_equal=True,
    declarations=baseline['count'],source=str(p),
    scope='single compiled-module replay over trusted imports; not source frontend or full library',
    trust='stock original kernel check plus checked module export/normal import; no unchecked join',
    ordering='physical insertion order inside independent frontier differs; final audit visits original array order',
    baseline='k0 direct official serial replay; k1 is wave-pipeline overhead control, not strong baseline')
 (HERE/'parallel-validation.json').write_text(json.dumps(quality,indent=2)+'\n')
 print(json.dumps(quality))
if __name__=='__main__':main()
