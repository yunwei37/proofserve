from pathlib import Path
import os,subprocess,time,resource,json,csv,gzip,collections,tarfile,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cpu-coverage-root-step.txt').read_text().strip());e=s/'experiment-001'
start=time.monotonic();b=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031');o=b/'scale-study/falconer-project-20261101/checkpoint-recheck-v2'
costrows=list(csv.DictReader((r/'research/decoupled-check/falconer-source-costs.csv').open()))
measured=[json.loads(v)for v in (b/'measured.jsonl').read_text().splitlines()]
oldmath=next(v for v in measured if v.get('operation')=='matched_stream' and v.get('cohort')=='math')
mathids=set(oldmath['accepted_modules']);assert len(mathids)==1330
src=[];inputs=[]
for row in costrows:
 p=Path(row['source_cell_root'])/(row['source_cell']+'.result.json');c=json.loads(p.read_text());inputs.append(p)
 assert c['returncode']==0 and c['measured'] and not any(x.startswith('-M')for x in c['args'])
 assert c['user_s']==float(row['source_user_s'])and c['system_s']==float(row['source_system_s'])
 assert abs(c['wall_s']-float(row['source_compiler_wall_s']))<1e-9
 src.append(dict(module=row['module'],key=c['key'],cpu_s=c['user_s']+c['system_s'],wall_s=c['wall_s'],raw=str(p)))
assert len(src)==13205 and len({v['module']for v in src})==13205
mathsrc=[v for v in src if v['module']in mathids];assert len(mathsrc)==1330
segments={}
for tag,n in [('segment',27),('math-segment',3)]:
 rr=[]
 for p in sorted(o.glob(tag+'-*-terminal.json')):
  v=json.loads(p.read_text());c=v['cell'];raw=o/(c['key']+'.result.json');actual=json.loads(raw.read_text())
  assert actual==c and c['returncode']==0 and not any(x.startswith('-M')for x in c['args'])
  rr.append(dict(key=c['key'],modules=len(v['accepted']),cpu_s=c['user_s']+c['system_s'],wall_s=c['wall_s'],raw=str(raw)))
  inputs.extend([p,raw])
 assert len(rr)==n
 segments[tag]=rr
def sums(rows):return {k:sum(v[k]for v in rows)for k in ['cpu_s','wall_s']}
results=[]
for label,ss,tag in [('Falconer',src,'segment'),('Mathlib Nat.Basic',mathsrc,'math-segment')]:
 a=sums(ss);c=sums(segments[tag]);results.append(dict(closure=label,modules=len(ss),segments=len(segments[tag]),source_cpu_s=a['cpu_s'],check_cpu_s=c['cpu_s'],cpu_ratio=c['cpu_s']/a['cpu_s'],source_wall_s=a['wall_s'],check_wall_s=c['wall_s'],wall_ratio=c['wall_s']/a['wall_s']))
assert abs(results[0]['cpu_ratio']-0.06312417401157776)<1e-12
assert round(results[1]['cpu_ratio']*100,2)==8.95
whole=b/'whole-library-20261102';ledger=[json.loads(v)for v in (whole/'ledger.jsonl').read_text().splitlines()]
source=[v for v in ledger if v['operation']=='source_production'];counts=collections.Counter(v['cell']['returncode']for v in source);assert counts[1]==9124
progress=(r/'research/decoupled-check/whole-library-progress.md').read_text()
for token in ['2488','10744','160609','9124','False']:assert token in progress
state=json.loads((whole/'all-state.json').read_text())
accepted=state['accepted'];print('STATE_TYPES',{k:type(state[k]).__name__ for k in state})
# Final published source coverage; raw ledger preserves 9124 unclassified production returns.
coverage=dict(source_frame=163097,accepted_source=2488,accepted_dependencies=10744,missing_source=160609,compilation_rc1_unattributed=counts[1],complete=False,source_return_counts=dict(counts),attribution='pending O owner investigation; not kernel/mathematical rejection')
st=os.statvfs(r);disk=dict(total_bytes=st.f_blocks*st.f_frsize,used_bytes=(st.f_blocks-st.f_bfree)*st.f_frsize,available_bytes=st.f_bavail*st.f_frsize);disk['used_percent']=100*disk['used_bytes']/disk['total_bytes']
inv=Path('/workspaces/.agent-state/root-owned-cleanup-20261102-inventory.json')
(e/'cleanup-candidate-inventory.json.gz').write_bytes(gzip.compress(inv.read_bytes()))
(e/'whole-library-progress.md.gz').write_bytes(gzip.compress(progress.encode()))
(e/'whole-library-ledger.jsonl.gz').write_bytes(gzip.compress((whole/'ledger.jsonl').read_bytes()))
(e/'whole-library-all-state.json.gz').write_bytes(gzip.compress((whole/'all-state.json').read_bytes()))
# Selected raw numeric records frozen without SDK/build trees or large native objects.
with tarfile.open(e/'cpu-raw-inputs.tar.gz','w:gz')as tf:
 for p in inputs:tf.add(p,arcname=str(p.relative_to('/workspaces/.agent-state')))
 tf.add(r/'research/decoupled-check/falconer-source-costs.csv',arcname='falconer-source-costs.csv')
# measured file held as exact compressed source for Mathlib membership and historical wall record.
(e/'original-measured.jsonl.gz').write_bytes(gzip.compress((b/'measured.jsonl').read_bytes()))
for name,rows in [('closure-cpu-wall.csv',results),('checkpoint-processes.csv',segments['segment']+segments['math-segment']),('source-cpu-wall.csv',src)]:
 with (e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result=dict(results=results,historical_math_wall_s=oldmath['wall_s'],historical_math_wall_ratio=oldmath['wall_s']/results[1]['source_wall_s'],coverage=coverage,disk=disk,cache_deletion_executed=False,cleanup_target_already_met=disk['used_percent']<85,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
