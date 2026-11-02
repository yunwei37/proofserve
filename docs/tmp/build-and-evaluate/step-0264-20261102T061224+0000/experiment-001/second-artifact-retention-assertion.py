from pathlib import Path
import os,json,csv,subprocess,time,resource,gzip,tarfile,collections,re
os.sched_setaffinity(0,{22,23})
r=Path('/workspaces/repository');assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
s=Path(Path('/workspaces/.agent-state/gpu-smt-falconer-root-step.txt').read_text().strip());e=s/'experiment-001'
for n in ['docs/paper/main.tex','docs/paper/main.pdf','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','docs/evaluation.md','docs/novelty-20261101.md','research/README.md']:
 p=r/n;(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress(p.read_bytes()))
(e/'initial-inspection-anchor-failure.txt').write_text('Read-only inspection used a prose substring absent from the current TeX, raising ValueError. No files/data/native processes modified. Located the actual Falconer paragraph by line search instead.\n')
began=time.monotonic();base=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031');b=base/'scale-study/falconer-project-20261101';o=b/'checkpoint-recheck-v2';q=b/'bounded-recheck-v1'
inputs=set();records=[];frames=json.loads((b/'build-frame.json').read_text());frame={x['module']:x for x in frames};assert len(frame)==len(frames)==13205
def J(p):
 inputs.add(p);return json.loads(p.read_text())
def events(p):
 inputs.add(p);out=[]
 for line in p.read_text().splitlines():
  if line.startswith('{'):out.append(json.loads(line))
 return out
def qualify(c):
 assert c['returncode']==0 and c['affinity']==list(range(8)) and c['measured']
 assert not any(x.startswith('-M')for x in c['args'])
 assert not Path(c['cgroup']).exists(),c['cgroup']
 me=dict(x.split()for x in c['memory_events'].splitlines());assert int(me.get('oom',0))==int(me.get('oom_kill',0))==0
 records.append(c)
def series(tag,expected):
 seen=[];headers={};prev=None;rows=[]
 terms=sorted(o.glob(tag+'-*-terminal.json'))
 for i,p in enumerate(terms):
  v=J(p);c=v['cell'];qualify(c);assert c==J(o/(c['key']+'.result.json'));command=J(o/(c['key']+'.command.json'));assert all(c[k]==val for k,val in command.items())
  assert not v['rejected']and not v['malformed']and v['previous_snapshot']==prev
  es=events(o/(c['key']+'.stdout'));a=[z['module']for z in es if z['event']=='accept'];hs=[z for z in es if z['event']=='module_header']
  assert a==v['accepted']and len(a)==len(set(a))and not set(a)&set(seen)
  assert [z['module']for z in hs]==a
  for z in hs:headers[z['module']]=z
  seen+=a
  if i<len(terms)-1:
   assert len(a)==500 and v['checkpoint']['modules']==len(seen)and v['complete']is None
   assert Path(v['checkpoint']['snapshot']).name==v['snapshot']+'.olean'
   assert (o/(v['snapshot']+'.olean')).stat().st_size>0
  else:assert v['complete']['modules']==len(expected)and v['checkpoint']is None
  prev=v['snapshot'];rows.append(dict(key=c['key'],modules=len(a),wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],maxRSS_KiB=c['peak_rss_kib'],charged_peak_B=c['cgroup_peak_bytes']))
 assert set(seen)==expected and set(headers)==expected
 return dict(modules=len(seen),segments=len(rows),wall_s=sum(x['wall_s']for x in rows),cpu_s=sum(x['cpu_s']for x in rows),maxRSS_KiB=max(x['maxRSS_KiB']for x in rows),charged_peak_B=max(x['charged_peak_B']for x in rows),rows=rows,complete=J(terms[-1])['complete']),headers
f,heads=series('segment',set(frame))
assert f['segments']==27
count_differences=[]
for m,z in heads.items():
 assert set(z['imports'])==set(frame[m]['imports'])
 if z['constants']!=frame[m]['constants']:count_differences.append(dict(module=m,prepared=frame[m]['constants'],actual=z['constants']))
roots=set((b/'roots.txt').read_text().splitlines());todo=list(roots);seen=set()
while todo:
 m=todo.pop()
 if m in seen:continue
 seen.add(m);todo+=frame[m]['imports']
assert seen==set(frame)
plan=J(base/'cohort-plan.json');mathset=set(plan['cases']['math']['modules']);math,mheads=series('math-segment',mathset);assert math['segments']==3
# Reconstruct same-capture original module-local common qualification from all161 raw blocks.
old=J(base/'progress.json');common=set(J(b/'progress.json')['reused']);assert len(common)==5077 and common<=set(frame)
measured=[json.loads(x)for x in (base/'measured.jsonl').read_text().splitlines()];inputs.add(base/'measured.jsonl')
oldaccepted=set();oldcells=[]
for c in measured:
 if c.get('operation')!='matched_oracle':continue
 qualify(c)
 es=events(base/(c['key']+'.stdout'));a=[z['module']for z in es if z.get('event')=='accept']
 wanted=c['args'][c['args'].index('none')+1:];assert len(a)==len(set(a))and set(a)==set(wanted)
 oldaccepted.update(a);oldcells.append(c['key']);inputs.add(base/(c['key']+'.result.json'));inputs.add(base/(c['key']+'.command.json'))
assert len(oldcells)==161 and len(oldaccepted)==5085 and common<=oldaccepted
ref=set(common);refrows=[]
for p in sorted(q.glob('oracle-*-terminal.json')):
 v=J(p);c=v['cell'];qualify(c);assert v['complete']and not c['malformed_json_lines']
 es=events(q/(c['key']+'.stdout'));a=[z['module']for z in es if z.get('event')=='accept'];assert a==v['requested']==v['accepted']and not(set(a)&ref)
 assert 'one'in c['args']and 'none'in c['args'];ref.update(a)
 refrows.append(dict(key=c['key'],modules=len(a),wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s']))
 for suffix in ['.result.json','.command.json','.stderr','-parsed.json']:inputs.add(q/(c['key']+suffix))
assert len(refrows)==16 and ref==set(frame)
# Every source row is joined to its actual successful process record and output objects.
src=list(csv.DictReader((r/'research/decoupled-check/falconer-source-costs.csv').open()));assert {x['module']for x in src}==set(frame)and len(src)==13205
source_stats=[];caps=collections.Counter();reused=0;new=0;commonfiles=0;sourcebytes=0;sourceframes=[]
original=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875')
for row in src:
 m=row['module'];d=Path(row['source_cell_root']);c=J(d/(row['source_cell']+'.result.json'));qualify(c);args=c['args'];assert '-j8'in args
 assert args[-1]==frame[m]['source']or Path(args[-1]).read_bytes()==Path(frame[m]['source']).read_bytes()
 assert abs(c['wall_s']-float(row['source_compiler_wall_s']))<1e-9 and c['user_s']==float(row['source_user_s'])and c['system_s']==float(row['source_system_s'])
 assert Path(args[-1]).stat().st_size==frame[m]['source_bytes'];sourcebytes+=frame[m]['source_bytes']
 if m.startswith('OAI.'):
  assert Path(args[-1]).read_bytes()==(original/('/'.join(m.split('.'))+'.lean')).read_bytes()
 for flag in ['-o','-i','-c']:assert Path(args[args.index(flag)+1]).stat().st_size>0
 if row['reused_exact_artifact']=='True':
  reused+=1;obj=Path(args[args.index('-o')+1]);rel=obj.relative_to(base/'constructed/lib');copy=b/'constructed/lib'/rel
  for p in obj.parent.glob(obj.stem+'.*'):
   target=copy.parent/p.name
   if target.exists():
    a=p.stat();z=target.stat();assert (a.st_dev,a.st_ino,a.st_size)==(z.st_dev,z.st_ino,z.st_size);commonfiles+=1
 else:new+=1
 caps[c['memory_max_bytes']]+=1
 for suffix in ['.command.json','.stdout','.stderr']:inputs.add(d/(c['key']+suffix))
 source_stats.append(c);sourceframes.append(dict(module=m,source=frame[m]['source'],bytes=frame[m]['source_bytes'],cell=c['key'],source_cell_root=str(d),reused=row['reused_exact_artifact']))
assert (reused,new)==(5077,8128)
sourcewall=sum(c['wall_s']for c in source_stats);sourcecpu=sum(c['user_s']+c['system_s']for c in source_stats)
mathsrc=[c for row,c in zip(src,source_stats)if row['module']in mathset];assert len(mathsrc)==1330
mswall=sum(c['wall_s']for c in mathsrc)
# Five checkpoint/restore cases; expected bad proofs reject only after restoring a successful prefix.
controls=J(o/'checkpoint-controls.json');assert controls['complete']and len(controls['results'])==5
controlrows=[]
for case in controls['results']:
 assert case['qualified']
 for p in sorted(o.glob('control_'+case['case']+'_*'+'-terminal.json')):
  v=J(p);c=v['cell'];es=events(o/(c['key']+'.stdout'));assert c['returncode']in [0,1]and not v['malformed']
  assert not Path(c['cgroup']).exists()
  if c['returncode']==1:assert v['previous_snapshot']and v['rejected']
  controlrows.append(dict(key=c['key'],returncode=c['returncode'],previous=v['previous_snapshot'],rejected=v['rejected']))
  for suffix in ['.command.json','.result.json','.stderr']:inputs.add(o/(c['key']+suffix))
assert len(controlrows)==18 and sum(c['returncode']==1 for c in controlrows)==2
# Failed full attempts never contribute accepted modules to the successful chain.
failed=[]
for d,key in [(b,'primary'),(q,'stream')]:
 c=J(d/(key+'.result.json'));assert c['returncode']==124 and not Path(c['cgroup']).exists()
 raw=(d/(key+'.stdout')).read_bytes();lines=raw.splitlines(keepends=True);complete_lines=[json.loads(x)for x in lines if x.endswith(b'\n')and x.startswith(b'{')]
 accepted=[x['module']for x in complete_lines if x.get('event')=='accept'];fragment=len(lines[-1])if lines and not lines[-1].endswith(b'\n')else 0
 failed.append(dict(key=key,wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],complete_accepts=len(set(accepted)),last_unterminated_bytes=fragment,returncode=c['returncode']))
 for suffix in ['.command.json','.stdout','.stderr']:inputs.add(d/(key+suffix))
# Audit only identities that were actually emitted with a birth value.
identities={};missingbirth=[]
for d in [b,o,q]:
 for p in list(d.glob('*submit*.json'))+list(d.glob('*submission*.json')):
  v=J(p)
  if 'pid'in v:
   if 'birth'in v:identities[(int(v['pid']),int(v['birth']))]=str(p)
   else:missingbirth.append(dict(pid=v['pid'],record=str(p)))
identities[(244727,761148374)]='previous raw-root controller identity'
for (pid,birth),origin in identities.items():
 p=Path('/proc',str(pid),'stat')
 assert not p.exists()or int(p.read_text().rsplit(')',1)[1].split()[19])!=birth,(pid,birth,origin)
for p in [b/'build-frame.json',b/'cohort-plan.json',b/'roots.txt',b/'source-reference.json',b/'native_project.py',b/'primary.result.json',q/'oracle-complete.json',q/'oracle-progress.json',o/'CheckpointAudit.lean',o/'falconer-checkpoint.py',o/'math-checkpoint-worker.py',o/'segmented-progress.json',q/'oracle-reference-worker.py',q/'IndexedAudit.lean']:inputs.add(p)
for p in (r/'research/decoupled-check').glob('falconer-*'):
 if p.suffix in ['.md','.csv','.py']:inputs.add(p)
# Freeze exact raw/source/logs, not Lean objects or build trees.
archive=e/'falconer-source-segments-reference-and-failures.tar.gz'
with tarfile.open(archive,'w:gz')as t:
 for p in sorted(inputs):
  if p.exists()and p.is_file():t.add(p,arcname=str(p.relative_to('/workspaces')))
j=dict(source_modules=len(src),new_source_cells=new,reused_source_cells=reused,common_hardlinked_files_checked=commonfiles,source_input_bytes=sourcebytes,source_wall_s=sourcewall,source_cpu_s=sourcecpu,source_caps=dict(caps),prepared_declcount_differences=count_differences,source_maxRSS_KiB=max(c['peak_rss_kib']for c in source_stats),source_charged_peak_B=max(c['cgroup_peak_bytes']for c in source_stats),falconer=f,mathlib=math,math_source_wall_s=mswall,reference_new_chunks=refrows,common_reference_raw_blocks=len(oldcells),reference_ids_equal=True,checkpoint_controls=controlrows,failed_full_attempts=failed,recorded_PID_birth_retired=[dict(pid=p,birth=z,origin=v)for(p,z),v in identities.items()],PID_only_records_not_birth_audited=missingbirth,all_performance_cgroups_absent=True,independent_RSS_sampling_recorded=False,native_child_PID_birth_recorded=False,root_analysis_seconds=time.monotonic()-began,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,raw_freeze_bytes=archive.stat().st_size)
j['falconer_ratio']=f['wall_s']/sourcewall;j['math_ratio']=math['wall_s']/mswall;j['successful_plus_failed_wall_s']=f['wall_s']+sum(x['wall_s']for x in failed)
(e/'reanalysis.json').write_text(json.dumps(j,indent=2)+'\n')
for name,rows in [('segmented-costs.csv',f['rows']+math['rows']),('source-costs.csv',sourceframes),('reference-new-costs.csv',refrows)]:
 with(e/name).open('w',newline='')as z:
  w=csv.DictWriter(z,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
print('ANALYZED',s,json.dumps({k:v for k,v in j.items()if k not in ['falconer','mathlib','reference_new_chunks','checkpoint_controls','recorded_PID_birth_retired','PID_only_records_not_birth_audited']}))
