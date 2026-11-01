from pathlib import Path
import os,subprocess,json,gzip,time,resource,csv,re,statistics,math,datetime
os.sched_setaffinity(0,{22,23});begin=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-envelope-paper-step.txt').read_text().strip());e=s/'experiment-001'
def freeze(p,name):
 b=Path(p).read_bytes();q=e/(name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(q.read_bytes())==b;return b
for f in ['docs/paper/main.tex','docs/research-status.md','docs/research-plan.md','research/README.md','docs/questions-for-author.md']:
 freeze(r/f,'entry-'+Path(f).name)
freeze(r/'docs/paper/main.tex','paper-front.template.tex')
# Read current authority; keep the verbatim user log unchanged.
authority=(r/'docs/user-instruction.md').read_text();assert '按这个主线推进' in authority
p=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/envelope-curve-v3');m=r/'research/chunked-kernel-check'
for f in ['terminal.json','manifest.json','launch.json','preparation.json','envelope_matrix.py','declaration_native.py','EnvelopeDriver.lean','EnvelopeMerger.lean','EnvelopeBase.lean','EnvelopeTargetEquivalence.lean']:
 freeze(p/f,'raw-'+f)
for f in ['envelope-result.md','envelope-validation.json','envelope-per-repeat.csv','envelope-summary.csv','envelope-paired.csv','envelope-artifacts.csv','step-015-report.md','step-015-audit.md']:
 freeze(m/f,'published-'+f)
def live(pid,birth):
 q=Path('/proc')/str(pid)/'stat'
 return q.exists() and q.read_text().rsplit(')',1)[1].split()[19]==str(birth)
launch=json.loads((p/'launch.json').read_text());assert not live(launch['pid'],launch['birth'])
term=json.loads((p/'terminal.json').read_text());assert term==dict(complete=True,planned=15,completed=15)
manifest=json.loads((p/'manifest.json').read_text());assert {(x['k'],x['rep']) for x in manifest}=={(k,j) for k in [0,1,2,4,8] for j in [1,2,3]} and len(manifest)==15
rows=[];packet=[];maxrss=maxsample=maxcharged=0;native_count=negative=0
for q in sorted((p/'runs').glob('*/result.json')):
 z=json.loads(q.read_text())
 if z.get('kind')=='sequential_native_phases':continue
 d=q.parent;cmd=json.loads((d/'command.json').read_text())
 assert z['native_retired'] and z['cgroup_retired'] and not z['stop_reasons']
 assert not live(z['pid'],z['birth']) and not Path(z['cgroup']).exists()
 assert z['affinity']==list(range(8)) and z['measured'] and z['cgroup_charged_memory_max_gib']==14
 assert z['argv']==cmd['argv'] and not any(x.startswith('-M') for x in z['argv'])
 assert all(int(line.split()[1])==0 for line in z['memory_events'].splitlines())
 assert z['returncode']==(1 if z['key'].startswith('invalid-target') else 0)
 if z['key'].startswith('invalid-target'):
  assert 'original C++ kernel rejected declaration' in (d/'stdout').read_text()+(d/'stderr').read_text();negative+=1
 packet.append(dict(key=z['key'],command=cmd,result=z))
 for f in ['stdout','stderr','memory.jsonl']:freeze(d/f,z['key']+'-'+f)
 native_count+=1;maxrss=max(maxrss,z['peak_rss_kib']);maxsample=max(maxsample,z['sampled_tree_peak_bytes']);maxcharged=max(maxcharged,z['charged_peak_bytes'])
assert native_count==28 and negative==1
bykey={x['key']:x['result'] for x in packet}
for cell in manifest:
 d=Path(cell['raw']);z=json.loads((d/'result.json').read_text());k=cell['k'];rep=cell['rep'];txt=(d/'stdout').read_text()
 assert z['returncode']==0 and z['native_retired'] and z['cgroup_retired'] and z['cpu_accounting_complete']
 phases=[bykey[v] for v in z['phase_keys']];assert len(phases)==(1 if k==0 else 2)
 assert math.isclose(z['user_s']+z['system_s'],sum(v['user_s']+v['system_s'] for v in phases),abs_tol=1e-9)
 assert z['wall_s']>=sum(v['wall_s'] for v in phases)
 clocks=[tuple(map(int,x)) for x in re.findall(r'^CK_KERNEL (\d+) (\d+) (\d+) (\d+)$',txt,re.M)]
 assert len(clocks)==max(1,k) and len({x[0] for x in clocks})==max(1,k)
 assert all(b>=a and c>=0 and c<=(b-a)*1.05+1000000 for _,a,b,c in clocks)
 span=(max(x[2] for x in clocks)-min(x[1] for x in clocks))/1e9;cpu=sum(x[3] for x in clocks)/1e9
 row=dict(k=k,rep=rep,whole_wall_s=z['wall_s'],native_cpu_s=z['user_s']+z['system_s'],kernel_span_s=span,checker_thread_CPU_s=cpu)
 if k:
  assert f'CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={k}' in txt
  a=re.search(r'CK_MERGE_PARTS (\d+) (\d+) (\d+) (\d+)',txt);assert a
  row.update(dict(zip(['import_s','final_check_s','audit_s','export_s'],[int(a[i])/1e9 for i in range(1,5)])))
 else:assert 'CK_ORIGINAL_AXIOMS [propext]' in txt
 rows.append(row)
# Verify published clock rows against raw calculations, not just their summary.
published=list(csv.DictReader((m/'envelope-per-repeat.csv').open()))
assert len(published)==15
for z in rows:
 a=next(x for x in published if int(x['k'])==z['k'] and int(x['rep'])==z['rep'])
 for ours,theirs in [('whole_wall_s','native_wall_s'),('native_cpu_s','native_cpu_s'),('kernel_span_s','pure_kernel_span_s'),('checker_thread_CPU_s','pure_kernel_worker_thread_cpu_s')]:
  assert math.isclose(z[ours],float(a[theirs]),abs_tol=1e-9)
artifacts=list(csv.DictReader((m/'envelope-artifacts.csv').open()));assert len(artifacts)==84
for z in artifacts:
 assert z['equal_same_k_rep1']=='True'
 f=p/'outputs'/f"envelope-k{z['k']}-r{z['rep']}"/z['artifact'];assert f.stat().st_size==int(z['bytes'])
# The prior full byte-comparison receipt is retained, not rerun on all large objects.
quality=json.loads((m/'envelope-validation.json').read_text());assert quality['same_k_repeat_artifacts_equal'] and quality['olean_part_comparisons']==84
prep=Path(json.loads((p/'preparation.json').read_text())['source'])
freeze(prep/'preparation-terminal.json','qualified-preparation-terminal.json')
prepterm=json.loads((prep/'preparation-terminal.json').read_text());assert prepterm['driver_and_separate_merger_compiled'] and prepterm['whole_curve_unrun']
for f in ['EnvelopeDriver.lean','EnvelopeMerger.lean','EnvelopeBase.lean','EnvelopeTargetEquivalence.lean']:
 assert (p/f).read_bytes()==(prep/f).read_bytes()
 driver=(p/'EnvelopeDriver.lean').read_text();merger=(p/'EnvelopeMerger.lean').read_text()
assert '.addDeclCore' in driver and '.addDeclCore' in merger and 'final.type == goal.value' in merger
assert 'finalizeImport state imports {} 0 false false' in merger and 'collectAxioms' in merger
med={str(k):{key:statistics.median(x[key] for x in rows if x['k']==k) for key in ['whole_wall_s','native_cpu_s','kernel_span_s','checker_thread_CPU_s']} for k in [0,1,2,4,8]}
pairs=[]
for rep in [1,2,3]:
 a=next(x for x in rows if x['k']==0 and x['rep']==rep);b=next(x for x in rows if x['k']==8 and x['rep']==rep)
 pairs.append(dict(rep=rep,whole_ratio=a['whole_wall_s']/b['whole_wall_s'],extra_nonkernel_s=(b['whole_wall_s']-b['kernel_span_s'])-(a['whole_wall_s']-a['kernel_span_s'])))
metrics=dict(kernel_ratio=med['0']['kernel_span_s']/med['8']['kernel_span_s'],whole_ratio=med['0']['whole_wall_s']/med['8']['whole_wall_s'],wall_reduction_percent=100*(1-med['8']['whole_wall_s']/med['0']['whole_wall_s']),native_CPU_increase_percent=100*(med['8']['native_cpu_s']/med['0']['native_cpu_s']-1))
j=dict(medians=med,paired8=pairs,metrics=metrics,raw_native_phases=28,positive_native_phases=27,negative_rejections=1,performance_cells=15,all_identities_and_scopes_retired=True,max_RSS_KiB=maxrss,max_sampled_RSS_bytes=maxsample,max_charged_bytes=maxcharged,external_charged_cap_GiB=14,same_k_artifact_metadata_checked=84,prior_byte_comparison_receipt_retained=True,root_analysis_s=time.monotonic()-begin,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_native_runs=0)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
(e/'raw-native-packet.json.gz').write_bytes(gzip.compress(json.dumps(packet).encode(),mtime=0))
with (e/'per-repeat.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(key for row in rows for key in row)),lineterminator='\n');w.writeheader();w.writerows(rows)
print('STEP',s,'METRICS',json.dumps(metrics),'PAIRS',json.dumps(pairs),'ROOT',j['root_analysis_s'],j['root_analysis_maxrss_kib'])
