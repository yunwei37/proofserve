"""Offline extraction from completed Barrier worker receipts; no native run.
Worker elapsed maxima are not a global span: subtracting them from whole-stage
wall yields only an upper bound on work outside those worker intervals.
"""
from pathlib import Path
import argparse,csv,json
HERE=Path(__file__).resolve().parent
def analyze(point):
 assert json.loads((point/'terminal.json').read_text())['complete']
 rows=[]
 for rep in range(3):
  for k in [1,2,4,8]:
   for wave in range(6):
    data=json.loads((point/'cells'/f'r{rep}-k{k}'/f'wave-{wave}.json').read_text())
    receipt=json.loads((point/'runs'/f'r{rep}-k{k}-L{wave}'/'result.json').read_text())
    assert receipt['returncode']==0 and receipt['native_retired'] and receipt['cgroup_retired']
    workers=data['workers']
    checks=[int(w['check_wall_ns'])/1e9 for w in workers]
    exports=[int(w['export_wall_ns'])/1e9 for w in workers]
    durations=[c+e for c,e in zip(checks,exports)]
    residual=receipt['wall_s']-max(durations)
    assert residual>=0,'worker duration longer than complete native stage'
    rows.append(dict(k=k,rep=rep,wave=wave,jobs=data['jobs'],workers=len(workers),
     native_stage_wall_s=receipt['wall_s'],max_worker_check_and_export_wall_s=max(durations),
     outside_worker_wall_upper_bound_s=residual,
     max_worker_check_loop_wall_s=max(checks),min_worker_check_loop_wall_s=min(checks),
     min_jobs=min(len(w['indices']) for w in workers),max_jobs=max(len(w['indices']) for w in workers),
     max_export_wall_s=max(exports),
     metric_scope='loop includes per-job replay/map/audit and queue access; duration maxima are NOT exact global span; residual is only upper bound'))
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('point',type=Path);args=ap.parse_args()
 rows=analyze(args.point)
 with (HERE/'parallel-worker-analysis.csv').open('w') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 panel=list(csv.DictReader((HERE/'declaration-distribution.csv').open()))
 quality=json.loads((HERE/'declaration-estimate.json').read_text())
 assert quality['completed_timed_modules']==quality['planned_input_modules']==len(panel)
 weights={row['module']:float(row['all_kernel_call_cpu_s']) for row in panel}
 total=sum(weights.values());largest=max(weights,key=weights.get)
 loads=[0.0]*8
 for value in sorted(weights.values(),reverse=True):
  worker=min(range(8),key=lambda j:loads[j]);loads[worker]+=value
 rest=[v for k,v in weights.items() if not k.endswith('.BarrierData41')]
 bound=dict(scope='unweighted retained31-artifact panel only; not whole library or runtime experiment',
  units='original serial native checker-call threadCPU weights; imported dependencies/frontends excluded',
  modules=len(weights),total_serial_checker_work_s=total,largest_module=largest,
  largest_module_checker_work_s=weights[largest],
  module_granularity_8processor_work_lower_bound_s=total/8,
  module_granularity_8processor_straggler_lower_bound_s=max(total/8,max(weights.values())),
  modeled_LPT_8processor_makespan_s=max(loads),
  zero_cost_barrier_removal_straggler_bound_s=max(sum(rest)/8,max(rest)),
  assumptions='fixed serial costs, no startup/import/export/cache/memory/contention effects; no resource-admission model; not wall-clock prediction',
  conclusion='Barrier alone does not remove dominant module lower bound in this selected panel; stock module parallelism is a necessary library-scale baseline')
 (HERE/'module-granularity-bound.json').write_text(json.dumps(bound,indent=2)+'\n')
 print('Wrote',len(rows),'completed-wave observations and one explicit offline bound; no native process')
if __name__=='__main__':main()
