"""Recompute complete Grid target k-curve; setup and merged end-to-end scopes separate."""
import os,pathlib,json,re,csv,statistics
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
def write(name,rows):
 with (HERE/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 rows=[]
 for k in [0,1,2,4,8]:
  for rep in [1,2,3]:
   p=RAW/'runs'/f'grid-v1-k{k}-r{rep}'
   r=json.loads((p/'result.json').read_text());s=(p/'native.log').read_text()
   assert r['returncode']==0 and r['retired'] and not r['stop_reasons']
   assert 'sorry' not in s or 'sorry=false' in s
   m=re.search(r'CK_RESULT (original|chunks) (\d+) (\d+) (\d+) (\d+)',s);assert m
   if k:assert f'CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={k}' in s
   else:assert 'CK_ORIGINAL_AXIOMS [propext]' in s
   command=json.loads((p/'command.json').read_text())
   assert not any(x.startswith('-M') for x in command['argv'])
   row=dict(k=k,rep=rep,decision='accepted',native_wall_s=r['wall_s'],native_cpu_s=r['user_s']+r['system_s'],
    user_s=r['user_s'],system_s=r['system_s'],peak_rss_kib=r['peak_rss_kib'],
    chunk_check_and_write_wall_s=int(m[2])/1e9,chunk_check_and_write_cpu_s=int(m[3])/1e9,
    import_merge_audit_write_wall_s=int(m[4])/1e9,import_merge_audit_write_cpu_s=int(m[5])/1e9)
   setup=re.search(r'CK_SETUP (\d+) (\d+)',s)
   row['proof_setup_wall_s']=int(setup[1])/1e9 if setup else None
   row['proof_setup_cpu_s']=int(setup[2])/1e9 if setup else None
   row['raw']=str(p);rows.append(row)
 write('grid-per-repeat.csv',rows)
 sums=[]
 for k in [0,1,2,4,8]:
  rr=[r for r in rows if r['k']==k]
  for metric in [key for key in rr[0] if key.endswith('_s') or key=='peak_rss_kib']:
   vals=[r[metric] for r in rr if r[metric] is not None]
   if vals:sums.append(dict(k=k,metric=metric,n=len(vals),median=statistics.median(vals),min=min(vals),max=max(vals)))
 write('grid-summary.csv',sums)
 log=(RAW/'native-census-v2.log').read_text();counts=[]
 for mod,category,n in re.findall(r'^CK_NATIVE_COUNT (\S+) (\S+) (\d+)$',log,re.M):
  counts.append(dict(module=mod,native_shape=category,checked_auxiliary_types=int(n),
    shape_split_possible=category.startswith(('record_equality:','conjunction:')),
    scope='compiled mkDecideProof-headed auxiliaries only; not all source sites or exclusive CPU'))
 write('native-shapes.csv',counts)
 negative=RAW/'runs/negative-k2-v4'
 nr=json.loads((negative/'result.json').read_text());nl=(negative/'native.log').read_text()
 assert nr['returncode']==1 and 'original C++ kernel rejected declaration' in nl
 assert not (negative/'ChunkCombined.olean').exists()
 (HERE/'prototype-validation.json').write_text(json.dumps(dict(
   completed_cells=15,original_accepts=3,chunked_accepts=12,original_axioms=['propext'],
   final_axioms=['propext'],new_axioms=0,all_final_targets_identical=True,sorry=False,
   false_first_chunk_rejected=True,no_false_combined_artifact=True,raw=str(RAW),
   limits='one real Grid target, field splitting; no complete Grid module acceleration claim',
   native_coverage='native-shapes.csv; syntax extracted field layout independently accepted by Lean'),indent=2)+'\n')
 print(json.dumps(sums,indent=2))
if __name__=='__main__':main()
