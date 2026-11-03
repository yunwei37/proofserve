from pathlib import Path
import os,json,csv,gzip,tarfile,time,resource,subprocess,collections,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-producer-errors-root-step.txt').read_text().strip());e=s/'experiment-001'
start=time.monotonic();b=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031');w=b/'whole-library-20261102';q=b/'ramsey-20261102'
ledger=[json.loads(x)for x in(w/'ledger.jsonl').read_text().splitlines()]
failed=[x for x in ledger if x['operation']=='source_production'and x['cell']['returncode']==1]
assert len(failed)==9124 and len({x['cell']['key']for x in failed})==9124
inputs={w/'ledger.jsonl',w/'all-state.json',w/'source-error-classification-v2.json',w/'source-error-classification-v2.csv',q/'producer-qualification-v1.json',q/'producer-qualification-v2.json',q/'qualification.log',q/'qualification-v2.log',q/'ramsey-qualify-v1.py',q/'ramsey-qualify-v2.py',q/'prepare.json'}
counts=collections.Counter();costs=collections.defaultdict(lambda:[0.,0.]);rows=[];no_line1=[];maxrss=0;charged=0
published={x['key']:x for x in csv.DictReader((w/'source-error-classification-v2.csv').open())}
for row in failed:
 c=row['cell'];key=c['key'];actual=json.loads((w/(key+'.result.json')).read_text());assert actual==c
 cmd=json.loads((w/(key+'.command.json')).read_text());assert all(c[k]==v for k,v in cmd.items())
 assert c['affinity']==list(range(8))and c['measured']and '-j8'in c['args']and not any(x.startswith('-M')for x in c['args'])
 assert c['limit_s']==600 and c['memory_max_bytes']==12348030976 and not Path(c['cgroup']).exists()
 ev=dict(x.split()for x in c['memory_events'].splitlines());assert int(ev['oom'])==int(ev['oom_kill'])==0
 stdout=(w/(key+'.stdout')).read_text(errors='strict');stderr=(w/(key+'.stderr')).read_text(errors='strict');text=stdout+stderr
 if '(interpreter) unknown declaration'in text:category='interpreter_unknown_declaration'
 elif 'Could not find native implementation of external declaration'in text:category='missing_native_external_implementation'
 elif 'missing data file for module'in text:category='missing_module_data_file'
 elif 'compiler IR check failed'in text and 'no executable code'in text:category='compiler_IR_missing_executable_code_unqualified_environment'
 elif '(interpreter) IR of declaration'in text and 'not available'in text:category='interpreter_missing_IR'
 else:raise AssertionError((key,text[:300]))
 assert published[key]['category']==category and published[key]['module']==row['module']
 if category in ['interpreter_unknown_declaration','missing_native_external_implementation']and ':1:0: error:'not in text:no_line1.append(key)
 cpu=c['user_s']+c['system_s'];counts[category]+=1;costs[category][0]+=cpu;costs[category][1]+=c['wall_s']
 maxrss=max(maxrss,c['peak_rss_kib']);charged=max(charged,c['cgroup_peak_bytes'])
 rows.append(dict(module=row['module'],key=key,category=category,cpu_s=cpu,wall_s=c['wall_s']))
 for suffix in ['.result.json','.command.json','.stdout','.stderr']:inputs.add(w/(key+suffix))
print('DIAGNOSTICS_NOT_LINE1',len(no_line1),no_line1[:5])
assert dict(counts)==json.loads((w/'source-error-classification-v2.json').read_text())['counts']
controls=[];srcbytes=0;source_matches=[];artifact_rows=[]
qual=json.loads((q/'producer-qualification-v2.json').read_text());assert qual['complete']and len(qual['results'])==4
failed_by_module={x['module']:x for x in failed}
for row in qual['results']:
 key=row['key'];c=json.loads((q/(key+'.result.json')).read_text());cmd=json.loads((q/(key+'.command.json')).read_text())
 assert c['returncode']==0 and c['limit_s']==300 and c['affinity']==list(range(8))and c['memory_max_bytes']==12616466432
 assert all(c[k]==v for k,v in cmd.items())and not any(x.startswith('-M')for x in c['args'])and '-j8'in c['args']
 assert not Path(c['cgroup']).exists()
 ev=dict(x.split()for x in c['memory_events'].splitlines());assert int(ev['oom'])==int(ev['oom_kill'])==0
 text=(q/(key+'.stdout')).read_text()+(q/(key+'.stderr')).read_text();assert "declaration uses 'sorry'"not in text
 src=Path(c['args'][-1]);assert src.exists();inputs.add(src)
 if row['module']!='InitDataControl':
  old=failed_by_module[row['module']]['cell'];oldsrc=Path(old['args'][-1]);assert not oldsrc.exists() or oldsrc.read_bytes()==src.read_bytes();inputs.add(oldsrc)
  source_matches.append(row['module']);srcbytes+=src.stat().st_size
 else:assert src.read_text()=='prelude\nimport Init.Data.Iterators.Lemmas.Monadic.Basic\nexample : (1 : Nat) = 1 := rfl\n'
 for flag in ['-o','-i','-c']:
  p=Path(c['args'][c['args'].index(flag)+1]);assert p.stat().st_size>0;artifact_rows.append(dict(module=row['module'],facet=flag,path=str(p),bytes=p.stat().st_size))
 controls.append(dict(module=row['module'],key=key,returncode=0,wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],maxRSS_KiB=c['peak_rss_kib'],charged_peak_B=c['cgroup_peak_bytes']))
 for suffix in ['.result.json','.command.json','.stdout','.stderr']:inputs.add(q/(key+suffix))
# Compare the three present controls with the retained fixed full-source archive.
# Historical duplicate source copies were retired by their owner; do not recreate them.
archive=Path('/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz')
wanted={'lean/'+m.replace('.','/')+'.lean':m for m in source_matches};found=set();archive_start=time.monotonic()
with tarfile.open(archive,'r|gz')as tf:
 for member in tf:
  if not member.isfile():continue
  for suffix,m in wanted.items():
   if member.name.endswith('/'+suffix):
    current=q/'sources/lean'/Path(*m.split('.')).with_suffix('.lean')
    data=tf.extractfile(member).read();assert data==current.read_bytes()
    found.add(m)
assert found==set(source_matches)
(e/'source-archive-comparison.json').write_text(json.dumps(dict(archive=str(archive),archive_bytes=archive.stat().st_size,selected_sources_compared=len(found),selected_source_bytes=srcbytes,all_current_control_sources_byte_equal=True,historical_source_copies_available=False,historical_per_invocation_byte_comparison='unavailable; duplicate source namespace retired before root audit; original source archive retained',elapsed_s=time.monotonic()-archive_start,scope='three selected controls only, no corpus census/download'),indent=2)+'\n')
old_retry=json.loads((q/'qualified-producer-0.result.json').read_text());assert old_retry['returncode']==1 and not Path(old_retry['cgroup']).exists()
for suffix in ['.result.json','.command.json','.stdout','.stderr']:inputs.add(q/('qualified-producer-0'+suffix))
# The controls carry no per-native PID/birth or independent RSS sample fields.
identity_fields={x:sum(x in json.loads((q/(v['key']+'.result.json')).read_text())for v in controls)for x in ['pid','birth','birth_ticks','sampled_native_rss_peak_bytes']}
# Preserve actual environment construction/source rather than asserting unlogged per-open providers.
for p in [r/'research/decoupled-check/ramsey-qualify.py',r/'research/decoupled-check/ramsey-qualification.md',r/'research/decoupled-check/whole-library-source-errors.md',r/'research/decoupled-check/whole-library-source-error-distribution.csv',r/'research/decoupled-check/whole-library-source-error-examples.json',b/'scale-study/falconer-project-20261101/native_project.py',r/'research/decoupled-check/whole-library-run.py']:inputs.add(p)
with tarfile.open(e/'producer-error-raw-and-controls.tar.gz','w:gz')as tf:
 for p in sorted(inputs):
  if p.exists():tf.add(p,arcname=str(p).removeprefix('/workspaces/'))
with (e/'failure-classification.csv.gz').open('wb')as f:
 import io
 buf=io.StringIO();cw=csv.DictWriter(buf,list(rows[0]),lineterminator='\n');cw.writeheader();cw.writerows(rows);f.write(gzip.compress(buf.getvalue().encode()))
summary=[dict(category=k,count=counts[k],cpu_s=costs[k][0],wall_s=costs[k][1])for k in sorted(counts)]
for name,rs in [('failure-categories.csv',summary),('producer-controls.csv',controls),('control-artifacts.csv',artifact_rows)]:
 with (e/name).open('w',newline='')as f:
  cw=csv.DictWriter(f,list(rs[0]),lineterminator='\n');cw.writeheader();cw.writerows(rs)
state=json.loads((w/'all-state.json').read_text());accepted=state['accepted'];assert len(accepted)==len(set(accepted))==13232
a=dict(failures=9124,classified_counts=dict(counts),initialization_errors=counts['interpreter_unknown_declaration']+counts['missing_native_external_implementation'],initialization_all_line1=not no_line1,initialization_not_line1_count=len(no_line1),failed_source_cpu_s=sum(v['cpu_s']for v in rows),failed_source_wall_s=sum(v['wall_s']for v in rows),failed_source_maxRSS_KiB=maxrss,failed_source_charged_peak_B=charged,failed_source_charged_cap_B=12348030976,failed_source_timeout_s=600,qualified_control_charged_cap_B=12616466432,qualified_control_timeout_s=300,controls=controls,current_controls_match_fixed_archive=source_matches,historical_source_copies_available=False,source_bytes_compared=srcbytes,metadata_copy_retry_rc=1,control_identity_fields=identity_fields,accepted_source=sum(x.startswith('OAI.')for x in accepted),accepted_dependencies=sum(not x.startswith('OAI.')for x in accepted),accepted_total=len(accepted),source_frame=163097,failed_control_is_not_source_proof_rejection=True,all_failures_pass_after_repair='unproven',single_runtime_facet_cause='not isolated',producer_search_paths='reported by frozen construction code; command records omit per-open path trace and environment fields',root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n');print('STEP',s);print(json.dumps(a,indent=2))
