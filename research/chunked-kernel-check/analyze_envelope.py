"""Analyze the finite >=1s Envelope target curve, never impute missing cells."""
import os,pathlib,json,re,csv,statistics,filecmp,argparse
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
def write(name,rows):
 with (HERE/name).open('w') as f:
  w=csv.DictWriter(f,lineterminator='\n',fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 ap=argparse.ArgumentParser();ap.add_argument('--point',type=pathlib.Path,required=True);ap.add_argument('--prefix',default='envelope');args=ap.parse_args()
 point=args.point or RAW/'envelope-curve-v1'
 prefix=args.prefix
 term=json.loads((point/'terminal.json').read_text())
 locations={(r['k'],r['rep']):pathlib.Path(r['raw']) for r in json.loads((point/'manifest.json').read_text())} if (point/'manifest.json').exists() else {}
 assert set(locations)=={(k,rep) for k in [0,1,2,4,8] for rep in [1,2,3]},'exact Envelope manifest required'
 assert term['complete'] and term['completed']==15,'pending/failed is not complete evidence'
 rows=[];artifacts=[]
 for k in [0,1,2,4,8]:
  for rep in [1,2,3]:
   p=locations[(k,rep)]
   r=json.loads((p/'result.json').read_text());text=(p/'stdout').read_text()
   assert r['returncode']==0 and r['native_retired'] and r['cgroup_retired'] and not r['stop_reasons']
   command=json.loads((p/'command.json').read_text())
   commands=command['phase_commands'] if command.get('kind')=='sequential_native_phases' else [command]
   assert all(c['affinity']==list(range(8)) and c['measured'] and not any(a.startswith('-M') for a in c['argv']) for c in commands)
   assert r.get('cpu_accounting_complete',True)
   phases=[tuple(map(int,m)) for m in re.findall(r'^CK_KERNEL (\d+) (\d+) (\d+) (\d+)$',text,re.M)]
   assert len(phases)==max(1,k)
   assert all(end>=start and cpu>=0 for _,start,end,cpu in phases)
   assert all(cpu<=(end-start)*1.05+1000000 for _,start,end,cpu in phases),'thread CPU clock exceeds its wall interval'
   span=(max(x[2] for x in phases)-min(x[1] for x in phases))/1e9
   cpu=sum(x[3] for x in phases)/1e9
   assert cpu<=span*min(max(1,k),8)*1.05+0.01,'impossible measured active-core average'
   m=re.search(r'CK_RESULT (original|chunks) (\d+) (\d+) (\d+) (\d+)',text);assert m
   row=dict(k=k,rep=rep,native_wall_s=r['wall_s'],native_cpu_s=r['user_s']+r['system_s'],
     peak_rss_kib=r['peak_rss_kib'],pure_kernel_span_s=span,pure_kernel_worker_thread_cpu_s=cpu,
     pure_kernel_average_active_cores=cpu/span,check_and_write_span_s=int(m[2])/1e9,
     check_and_write_process_cpu_s=int(m[3])/1e9,merge_stage_wall_s=int(m[4])/1e9,merge_stage_cpu_s=int(m[5])/1e9)
   if k and command.get('kind')=='sequential_native_phases':
    merge=re.search(r'CK_MERGE_RESULT (\d+) (\d+)',text);assert merge
    row['merge_stage_wall_s']=int(merge[1])/1e9
    row['merge_stage_cpu_s']=int(merge[2])/1e9
   if k:
    assert f'CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={k}' in text
    parts=re.search(r'CK_MERGE_PARTS (\d+) (\d+) (\d+) (\d+)',text);assert parts
    for i,key in enumerate(['import','final_kernel_check','axiom_shape_audit','final_export']):
     row[key+'_wall_s']=int(parts[i+1])/1e9
   else:assert 'CK_ORIGINAL_AXIOMS [propext]' in text
   out=pathlib.Path(json.loads((p/'cell.json').read_text())['outputs'])
   paths=[out/'EnvelopeOriginal.olean'] if k==0 else [out/f'EnvelopeK{k}Part{i}.olean' for i in range(k)]+[out/'EnvelopeCombined.olean']
   expected={a.name for a in paths}
   paths=sorted(out.glob('*.olean*'))
   assert expected.issubset({a.name for a in paths}),'missing primary artifacts'
   reference_out=pathlib.Path(json.loads((locations[(k,1)]/'cell.json').read_text())['outputs'])
   assert {a.name for a in paths}=={a.name for a in reference_out.glob('*.olean*')},'olean part set differs across repetitions'
   for a in paths:
    assert a.exists()
    refrow=locations[(k,1)]
    ref=pathlib.Path(json.loads((refrow/'cell.json').read_text())['outputs'])/a.name
    artifacts.append(dict(k=k,rep=rep,artifact=a.name,bytes=a.stat().st_size,
       equal_same_k_rep1=filecmp.cmp(a,ref,shallow=False),
       scope='same configuration repetitions; proof restructuring changes artifact bytes across k'))
   row['raw']=str(p);rows.append(row)
 write(prefix+'-per-repeat.csv',rows);write(prefix+'-artifacts.csv',artifacts)
 summaries=[]
 for k in [0,1,2,4,8]:
  rr=[r for r in rows if r['k']==k]
  for metric in rr[0]:
   if not metric.endswith(('_s','_kib','_cores')):continue
   vals=[r[metric] for r in rr if r.get(metric) is not None]
   if vals:summaries.append(dict(k=k,metric=metric,n=len(vals),median=statistics.median(vals),min=min(vals),max=max(vals)))
 write(prefix+'-summary.csv',summaries)
 pairs=[]
 for row in rows:
  if row['k']==0:continue
  original=next(x for x in rows if x['k']==0 and x['rep']==row['rep'])
  pairs.append(dict(k=row['k'],rep=row['rep'],original_wall_s=original['native_wall_s'],
   chunk_wall_s=row['native_wall_s'],wall_speedup=original['native_wall_s']/row['native_wall_s'],
   kernel_speedup=original['pure_kernel_span_s']/row['pure_kernel_span_s'],
   extra_nonkernel_wall_s=(row['native_wall_s']-row['pure_kernel_span_s'])-(original['native_wall_s']-original['pure_kernel_span_s']),
   native_cpu_ratio=row['native_cpu_s']/original['native_cpu_s']))
 write(prefix+'-paired.csv',pairs)
 quality=dict(completed_native_cells=15,accepted=15,target_identical_to_original_extracted_input=True,
  axioms=['propext'],new_axioms=0,sorry=False,same_k_repeat_artifacts_equal=all(a['equal_same_k_rep1'] for a in artifacts),
  native_heartbeats='finite per child; no claim of aggregate budget transparency',
  source_frame='one real measured >=1s Envelope Fin31 goal; not whole-module compilation')
 leaves=[json.loads(f.read_text()) for f in (point/'runs').glob('*/result.json')]
 leaves=[x for x in leaves if x.get('kind')!='sequential_native_phases']
 assert all(x['native_retired'] and x['cgroup_retired'] for x in leaves)
 quality.update(all_olean_parts_compared=True,olean_part_comparisons=len(artifacts),
  raw_native_phases=len(leaves),positive_native_phases=sum(x['returncode']==0 for x in leaves),
  negative_kernel_rejection_phases=sum(x['key'].startswith('invalid-target') and x['returncode']==1 for x in leaves),
  all_native_retired_and_scopes_removed=True,code_commit=json.loads((point/'launch.json').read_text())['code_commit'],
  max_sampled_own_tree_bytes=max(x['sampled_tree_peak_bytes'] for x in leaves),
  max_charged_child_bytes=max(x['charged_peak_bytes'] for x in leaves),
  setup_scope='offline source generation/Base/merge-lemma compilation and original OAI production build excluded; full two native-phase runtime included')
 (HERE/(prefix+'-validation.json')).write_text(json.dumps(quality,indent=2)+'\n')
 print(json.dumps(quality))
if __name__=='__main__':main()
