from pathlib import Path
import os,json,subprocess,struct,collections,csv,gzip,tarfile,time,resource,re,datetime
os.sched_setaffinity(0,{22,23})
resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
start=time.monotonic();r=Path('/workspaces/repository');b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103')
s=Path(Path('/workspaces/.agent-state/gpu-smt-worker-pmu-root-step.txt').read_text().strip());e=s/'experiment-001'
keys=['full-record-P8-r2-count-only','full-record-P4-r2-count-only','full-record-P4-r3-count-only-drain5']
names=['cpu-cycles','instructions','ref-cycles','mem_load_retired.l3_miss','mem_inst_retired.lock_loads','mem_load_l3_hit_retired.xsnp_hitm','ocr.demand_rfo.l3_hit.snoop_hitm']
configs=[0x3c,0xc0,0x13c,0x20d1,0x21d0,0x4d2,0x12a]
ref=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/runs/barrier-full-reference1-r1/stdout')
reference={}
for line in ref.read_text().splitlines():
 if line.startswith('{'):
  x=json.loads(line)
  if x.get('event')=='accept':
   assert x['module'] not in reference
   reference[x['module']]=(x['constants'],x['imports'])
assert len(reference)==4449
def writecsv(name,rows):
 with (e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
identities=set();cells=[];workers=[];coverage=[];vectors=[];freeze={ref};rawreceipts=[]
for key in keys:
 d=b/'runs'/key;c=json.loads((d/'command.json').read_text());v=json.loads((d/'result.json').read_text());term=json.loads((b/(key+'-terminal.json')).read_text());launch=json.loads((b/(key+'-launch.json')).read_text())
 assert term['state']=='complete' and term['cell']['returncode']==v['returncode']==0
 assert c['argv']==v['argv']==term['cell']['argv']
 assert c['affinity']==list(range(8)) and c['wall_limit_s']==1100 and c['cgroup_charged_memory_max_gib']==14 and c['own_rss_sample_stop_gib']==14
 assert all(not str(a).startswith('-M') for a in c['argv']) and '--no-samples'in c['argv'] and '--call-graph'not in c['argv'] and '--compression-level=1'not in c['argv']
 assert v['wait4_usage_complete'] and not v['stop_reasons'] and not Path(v['cgroup']).exists()
 assert all(int(q.split()[1])==0 for q in v['memory_events'].splitlines()if q.split()[0]in ['oom','oom_kill','oom_group_kill'])
 assert launch['argv'][:2]==['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock']
 identities|={(int(v['pid']),str(v['birth'])),(int(launch['pid']),str(launch['birth']))}
 samplepeak=0
 for line in (d/'memory.jsonl').read_text().splitlines():
  x=json.loads(line);samplepeak=max(samplepeak,x['rss_bytes'])
  identities.update((int(y['pid']),str(y['birth']))for y in x['processes'])
 assert samplepeak==v['sampled_tree_peak_bytes']
 heads={};accept={};prof={};work=collections.defaultdict(collections.Counter);complete=[];marks={}
 for line in (d/'stdout').read_text().splitlines():
  if not line.startswith('{'):continue
  x=json.loads(line);ev=x.get('event')
  if ev in ['module_header','accept']:
   dest=heads if ev=='module_header' else accept
   assert x['module'] not in dest;dest[x['module']]=(x['constants'],x['imports'])
  if ev=='profile_module':
   assert x['module']not in prof
   m=x['metrics'];prof[x['module']]=(m['checks'],m['raw_HB'])
   assert sum(z['checks']for z in m['workers'])==m['checks']
   assert sum(z['raw_HB']for z in m['workers'])==m['raw_HB']
   assert sum(z['cpu_ns']for z in m['workers'])==m['kernel_cpu_ns']
   for z in m['workers']:
    assert z['cpu'] in range(term['cell']['workers'])
    for src,dst in [('checks','checks'),('raw_HB','units'),('cpu_ns','CPU_ns')]:work[z['tid']][dst]+=z[src]
  if ev=='complete':complete.append(x)
  if ev in ['post_native_drain_begin','post_native_drain_end']:marks[ev]=x
 assert heads==accept==reference and len(prof)==4449 and len(complete)==1
 assert complete[0]['constants']==425463 and complete[0]['skipped_unsafe_partial']==3595 and complete[0]['module_local_fallbacks']==0
 assert sum(z[0]for z in prof.values())==237863 and sum(z[1]for z in prof.values())==3283925639
 vectors.append(prof)
 raw=b/(key+'.perf.data');data=raw.read_bytes();magic,hsize,asz,ao,alen,do,dl,*_=struct.unpack_from('<8s9Q',data)
 assert magic==b'PERFILE2' and asz==152 and alen==8*asz
 expected={};idname={}
 for i,name in enumerate(names):
  offset=ao+i*asz;typ,sz,config=struct.unpack_from('<IIQ',data,offset)
  assert typ==4 and sz==136 and config==configs[i]
  fmt=struct.unpack_from('<Q',data,offset+32)[0];assert fmt==23
  ido,idl=struct.unpack_from('<QQ',data,offset+asz-16);ids=struct.unpack_from('<'+'Q'*(idl//8),data,ido)
  assert len(ids)==len(set(ids))==8;expected[name]=set(ids)
  for ident in ids:assert ident not in idname;idname[ident]=name
  if i==6:assert struct.unpack_from('<Q',data,offset+56)[0]==0x10003c0002
 # Independent direct binary READ parser: read_format=enabled|running|ID|lost, non-group.
 rows=[];pos=do;counts=collections.Counter()
 while pos<do+dl:
  typ,misc,size=struct.unpack_from('<IHH',data,pos);assert size>=8 and pos+size<=do+dl
  counts[typ]+=1
  if typ==8:
   assert size==80
   pid,tid,value,enabled,running,ident,lost=struct.unpack_from('<IIQQQQQ',data,pos+8)
   assert enabled>=running>=0 and lost==0
   rows.append(dict(PID=pid,TID=tid,value=value,time_enabled=enabled,time_running=running,id=ident,lost=lost))
  pos+=size
 assert pos==do+dl and counts[9]==0 and rows
 command=['perf','report','-D','--stdio','--stats','-i',str(raw)]
 q=subprocess.run(command,text=True,capture_output=True,check=True)
 (e/(key+'-fresh-report-D.stdout.gz')).write_bytes(gzip.compress(q.stdout.encode()))
 (e/(key+'-fresh-report-D.stderr.gz')).write_bytes(gzip.compress(q.stderr.encode()))
 # Fresh tool dump, preserved binary and owner CSV independently agree on every READ field.
 rx=re.compile(r'PERF_RECORD_READ:\s+(\d+)\s+(\d+)\s+(.+?)\s+(\d+)\s*\n\.\.\. time enabled\s*:\s*(\d+)\n\.\.\. time running\s*:\s*(\d+)\n\.\.\. id\s*:\s*(\d+)\n\.\.\. lost\s*:\s*(\d+)')
 parsed=[dict(PID=int(m[1]),TID=int(m[2]),value=int(m[4]),time_enabled=int(m[5]),time_running=int(m[6]),id=int(m[7]),lost=int(m[8]))for m in rx.finditer(q.stdout)]
 assert parsed==rows,(key,len(rows),len(parsed))
 owner=list(csv.DictReader((b/('decode-'+key)/'read-times.csv').open()))
 assert len(owner)==len(rows)
 for x,y in zip(rows,owner):
  assert all(x[k]==int(y[k])for k in x)
  if x['id']in idname:
   name=idname[x['id']];assert y['event']=='cpu_core/'+name+('/u'if name=='cpu-cycles'else ',period=0/u')
 bytid=collections.defaultdict(list)
 for row in rows:
  if row['id']in idname:bytid[row['TID']].append(row)
 valid=0
 for tid,w in sorted(work.items()):
  sums={};ok=True
  for name,ids in expected.items():
   rr=[z for z in bytid[tid]if z['id']in ids];observed=collections.Counter(z['id']for z in rr)
   good=set(observed)==ids and all(v==1 for v in observed.values())
   ok &= good
   coverage.append(dict(key=key,TID=tid,event=name,expected_shards=len(ids),actual_unique=len(observed),records=len(rr),complete_unique=good,missing_IDs=';'.join(map(str,sorted(ids-set(observed)))),duplicate_IDs=';'.join(str(i)for i,n in observed.items()if n>1)))
   sums[name]=sum(z['value']for z in rr) if good else None
  valid+=ok
  workers.append(dict(key=key,requested_workers=term['cell']['workers'],TID=tid,checks=w['checks'],allocation_units=w['units'],observer_CPU_s=w['CPU_ns']/1e9,READ_complete=ok,**{n:(sums[n]if ok else '')for n in names},IPC=(sums['instructions']/sums['cpu-cycles']if ok else ''),scope='PMU checking-thread lifetime; CPU observer bracket incl HB/timing; not gated PMU'))
 assert len(work)==(9 if term['cell']['workers']==8 else 5)
 if key.endswith('P4-r2-count-only'):assert valid==1
 else:assert valid==len(work)
 if marks:
  assert set(marks)=={'post_native_drain_begin','post_native_drain_end'} and marks['post_native_drain_begin']['child_returncode']==0
  drain=(marks['post_native_drain_end']['monotonic_ns']-marks['post_native_drain_begin']['monotonic_ns'])/1e9
 else:drain=0
 cells.append(dict(key=key,requested_workers=term['cell']['workers'],native_rc=v['returncode'],guard_wall_s=v['wall_s'],wait4_CPU_s=v['user_s']+v['system_s'],application_wall_s=float(term['cell']['application_time']['wall_s']),historical_checking_TIDs=len(work),complete_TIDs=valid,accepted_modules=len(accept),checks=237863,allocation_units=3283925639,observer_CPU_s=sum(w['CPU_ns']for w in work.values())/1e9,HWM_KiB=v['peak_rss_kib'],sampled_peak_bytes=v['sampled_tree_peak_bytes'],charged_peak_bytes=v['charged_peak_bytes'],raw_perf_bytes=len(data),READ_records=len(rows),post_native_drain_s=drain,cgroup_absent=True))
 rawreceipts.append(dict(key=key,fresh_decode_argv=command,fresh_decode_rc=q.returncode,binary_parser_READs=len(rows),owner_CSV_exact=True,hardware_attrs=7,IDs_per_hardware_attr=8,PERF_RECORD_SAMPLE=counts[9]))
 freeze.update(d.iterdir());freeze.update((b/('decode-'+key)).iterdir());freeze|={raw,b/(key+'-terminal.json'),b/(key+'-launch.json'),b/(key+'-application.time'),b/(key+'-controller.log')}
assert vectors[0]==vectors[1]==vectors[2]
retirement=[]
for pid,birth in sorted(identities):
 p=Path('/proc')/str(pid)/'stat';live=p.read_text().rsplit(')',1)[1].split()[19]if p.exists()else None
 assert live!=birth,(pid,birth)
 retirement.append(dict(pid=pid,birth=birth,same_identity_alive=False))
completekeys=[keys[2],keys[0]];totals={}
for key in completekeys:
 rr=[z for z in workers if z['key']==key];assert all(x['READ_complete']for x in rr)
 totals[key]={name:sum(x[name]for x in rr)for name in names}
 totals[key]['observer_CPU_s']=sum(x['observer_CPU_s']for x in rr)
 totals[key]['IPC']=totals[key]['instructions']/totals[key]['cpu-cycles']
 totals[key]['cycles_per_ref']=totals[key]['cpu-cycles']/totals[key]['ref-cycles']
delta=[dict(metric=name,P4=totals[completekeys[0]][name],P8=totals[completekeys[1]][name],change_percent=100*(totals[completekeys[1]][name]/totals[completekeys[0]][name]-1))for name in totals[completekeys[0]]]
# Compare all fourteen complete per-TID counters with existing published output without borrowing its aggregation.
for key,f in [(keys[2],'P4-drain-worker-counters.csv'),(keys[0],'P8-count-only-worker-counters.csv')]:
 owner={int(x['TID']):x for x in csv.DictReader((r/'research/parallel-stream-check/perf/results'/f).open())}
 for x in workers:
  if x['key']!=key:continue
  y=owner[x['TID']]
  for n,src in [('cycles','cpu-cycles'),('instructions','instructions'),('reference_cycles','ref-cycles'),('retired_L3_miss_loads','mem_load_retired.l3_miss'),('locked_loads','mem_inst_retired.lock_loads'),('modified_line_forwarding','mem_load_l3_hit_retired.xsnp_hitm'),('RFO_snoop_HITM','ocr.demand_rfo.l3_hit.snoop_hitm')]:assert int(y[n])==x[src]
for name in ['native.py','perf_run.py','counter_repair.py','counter_drain.py','post_native_drain.py','attribution.py','read_times.py','read_worker_counts.py','read_worker_counts_with_reference.py']:freeze.add(b/name)
for name in ['full-matrix-report.md','supplemental-worker-report.md','event-semantics.md','P4-counter-partial.md']:freeze.add(r/'research/parallel-stream-check/perf'/name)
source=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2/source');freeze.update(source.iterdir())
archive=e/'supplemental-three-raw-and-source.tar.gz'
with tarfile.open(archive,'w:gz')as tf:
 for p in sorted(freeze):
  if p.is_file():tf.add(p,arcname=str(p).removeprefix('/workspaces/'))
writecsv('three-attempts.csv',cells);writecsv('checking-workers.csv',workers);writecsv('READ-coverage.csv',coverage);writecsv('checking-thread-P4-P8.csv',delta)
(e/'PIDbirth-retirement.json').write_text(json.dumps(retirement,indent=2)+'\n')
a=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native_attempts=3,accepted_each=4449,checks=237863,allocation_units=3283925639,identities_retired=len(identities),cgroups_absent=3,complete_checking_TIDs=14,partial_attempt_complete_TIDs=1,partial_attempt_total_TIDs=5,totals=totals,delta=delta,raw_receipts=rawreceipts,archive_bytes=archive.stat().st_size,root_analysis_seconds=time.monotonic()-start,root_analysis_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,native_runs=0,agents=0,HWM_KiB=max(x['HWM_KiB']for x in cells),sampled_peak_bytes=max(x['sampled_peak_bytes']for x in cells),charged_peak_bytes=max(x['charged_peak_bytes']for x in cells))
(e/'reanalysis.json').write_text(json.dumps(a,indent=2)+'\n')
print(json.dumps(a))
