from pathlib import Path
import os,time,json,datetime,subprocess,gzip,tarfile,csv,collections,math,resource
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=r/'docs/tmp/build-and-evaluate'/('step-0261-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000'));e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-budget-scope-root-step.txt').write_text(str(s))
for n in ['docs/paper/main.tex','docs/paper/references.bib','docs/user-instruction.md','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md']:(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
# Independent theorem-command range reconstruction, not a budget-threshold sweep.
b=Path('/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v5');observations=collections.defaultdict(list);pairs=0;diff=0;vector=0;verdict=0
for rep in [0,1]:
 cells={}
 for k in [1,2,4,8]:
  rows=[json.loads(l[5:])['result']for l in(b/f'runs/math-r{rep}-j{k}/stdout').open()if l.startswith('MATH ')]
  assert len(rows)==32
  cells[k]={(x['id'],x['budget']):x for x in rows}
  for key,x in cells[k].items():observations[key].append({'repeat':rep,'workers':k,'HB':x['command_raw_heartbeats'][1],'verdict':x['verdict']})
 for k in [2,4,8]:
  for key,a in cells[1].items():
   z=cells[k][key];pairs+=1;diff+=a['command_raw_heartbeats'][1]!=z['command_raw_heartbeats'][1];vector+=a['command_raw_heartbeats']!=z['command_raw_heartbeats'];verdict+=a['verdict']!=z['verdict']
ranges=[]
for key,vals in observations.items():
 hb=[x['HB']for x in vals];assert len(vals)==8
 ranges.append({'source':key[0],'budget':key[1],'min_raw_HB':min(hb),'max_raw_HB':max(hb),'range_percent':100*(max(hb)/min(hb)-1),'observed_verdicts':sorted({x['verdict']for x in vals})})
maxrange=max(x['range_percent']for x in ranges);assert pairs==192 and diff==83 and vector==84 and verdict==0 and abs(maxrange-2.333868)<1e-6
# Reconstruct W assumptions using the retained raw source observations and original strata.
root=r/'workloads/openai-math';frame=list(csv.DictReader((root/'noM-original-c-suffix48/sample-costs.csv').open()))
strata={';'.join(x[k]for k in ['size_percentile_bin','import_depth_bin','has_decide_kernel']):int(x['population_modules'])for x in csv.DictReader((root/'build-planning-4eaee875/strata.csv').open())}
known=[];missing=[];values=collections.defaultdict(list);freeze=set()
for x in frame:
 h=x['stratum'];d='marked'if h.endswith(';1')else'ordinary';weight=strata[h]/2
 if x['status']=='completed_cost':
  p=Path(x['source_file']);a=json.loads(p.read_text().splitlines()[int(x['source_line'])-1]);assert a['status']=='compile_ok'and a['lean_memory_option_MiB']==0 and a['source_exact']
  cpu=a['user_cpu_s']+a['system_cpu_s'];known.append((d,weight,cpu));values[d].append(cpu);freeze.add(p)
 else:missing.append((d,weight,x['module']))
assert len(known)==31 and len(missing)==11
cal={x['calibration']:float(x['CPU_factor'])for x in csv.DictReader((root/'cost_staircase/calibration.csv').open())}
ratios={'ordinary':(cal['ordinary-oai'],cal['math']),'marked':(cal['compute-amplitudes'],cal['compute-grid'])}
scenarios=[]
for name,mult,side in [('min',1,'min'),('max',1,'max'),('ten_times_max',10,'max')]:
 costs={d:mult*(min(v)if side=='min'else max(v))for d,v in values.items()}
 source=sum(w*y for d,w,y in known)+sum(w*costs[d]for d,w,m in missing)
 streamlow=sum(w*y*ratios[d][0]for d,w,y in known)+sum(w*costs[d]*ratios[d][0]for d,w,m in missing)
 streamhigh=sum(w*y*ratios[d][1]for d,w,y in known)+sum(w*costs[d]*ratios[d][1]for d,w,m in missing)
 missingcost=sum(w*costs[d]for d,w,m in missing);knownhigh=sum(w*y*ratios[d][1]for d,w,y in known)
 scenarios.append({'assumption':name,'source_CPU_h':source/3600,'stream_low_CPU_h':streamlow/3600,'stream_high_CPU_h':streamhigh/3600,'missing_no_saving_stream_CPU_h':(knownhigh+missingcost)/3600,'missing_twice_source_stream_CPU_h':(knownhigh+2*missingcost)/3600,'missing_checker_source_break_even':(source-knownhigh)/missingcost})
assert abs(scenarios[0]['source_CPU_h']-178.22569632027776)<1e-8
assert abs(scenarios[1]['source_CPU_h']-627.348203)<1e-6 and abs(scenarios[0]['stream_low_CPU_h']-8.322086223934205)<1e-8 and abs(scenarios[1]['stream_high_CPU_h']-41.555143)<1e-6
# Previously root-qualified finite controls and independent repeated capture are reused, not rerun.
p260=r/'docs/tmp/build-and-evaluate/step-0260-20261102T020415+0000/experiment-001/reanalysis.json'
j260=json.loads(p260.read_text());assert j260['M_native_phases']==86 and j260['M_stage_rows']==504
m12=Path('/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v12');launch=json.loads((m12/'census-launch.json').read_text());p=Path('/proc')/str(launch['pid'])
live=p.exists()and p.joinpath('stat').read_text().rsplit(')',1)[1].split()[19]==str(launch['birth'])
m12state={'controller':launch,'PID_birth_live':live,'terminal_files':[p.name for p in m12.glob('*terminal*.json')],'census_outcome_adopted':False}
for n in ['module-terminal.json','all-helper-terminal.json','census-terminal.json']:
 if(m12/n).exists():m12state[n]=json.loads((m12/n).read_text()).get('state')
with(e/'theorem-command-ranges.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(ranges[0]),lineterminator='\n');w.writeheader();w.writerows(ranges)
with(e/'missing-cost-scenarios.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(scenarios[0]),lineterminator='\n');w.writeheader();w.writerows(scenarios)
for rep in [0,1]:
 for k in [1,2,4,8]:freeze.add(b/f'runs/math-r{rep}-j{k}/stdout')
for n in ['missing_draw_stress.py','missing_draw_stress/README.md','missing_draw_stress/receipt.json','missing_draw_stress/source-vs-stream-scenarios.csv','cost_staircase/calibration.csv','build-planning-4eaee875/strata.csv','noM-original-c-suffix48/sample-costs.csv','native-replay31/README.md']:freeze.add(root/n)
for n in ['module-results-v11/results.md','coexecution-analysis/results.md']:freeze.add(r/'research/reproducible-verdict'/n)
freeze.add(p260)
with tarfile.open(e/'reused-evidence-and-new-sensitivity-reduction.tar.gz','w:gz')as tf:
 for p in sorted(freeze):tf.add(p,arcname=str(p).removeprefix('/workspaces/'),recursive=False)
j={'theorem_command_pairs':pairs,'theorem_command_count_changes':diff,'command_vector_changes':vector,'verdict_changes':verdict,'maximum_theorem_command_range_percent':maxrange,'scenarios':scenarios,'M12_latest_qualification':m12state,'reused_root0260_for_M11_W31':True,'new_root_native':0,'root_analysis_seconds':time.monotonic()-start,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n');print('STEP',s);print(json.dumps(j))
