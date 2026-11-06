"""Finite built-subset acquisition; native checker remains frozen."""
from __future__ import annotations
import csv,datetime,fcntl,gzip,json,os,signal,time
from pathlib import Path

class AdmissionDrain:
    """Freeze only the verified coordinator, let its existing child drain."""
    def __init__(self,deadline,grace=900):
        self.deadline=deadline;self.grace=grace;self.frozen=None;self.finished=False
    def step(self,now,members,coordinators,wrapper):
        if self.finished or now<self.deadline:return []
        if self.frozen is None:
            if len(coordinators)!=1:
                self.finished=True
                return [('kill','admission_deadline_no_unique_coordinator')]
            self.frozen=coordinators[0]
            return [('freeze',self.frozen)]
        active=set(members)-{wrapper,self.frozen}
        if not active or now>=self.deadline+self.grace:
            self.finished=True
            return [('kill','admission_deadline_drained'if not active else'admission_deadline_drain_expired')]
        return []

def _epoch(text):
    return datetime.datetime.fromisoformat(text.replace('Z','+00:00')).timestamp()

def progress(state):
    accepted=set();axioms=set();rejected=[];certified=0;uncommitted=[]
    for p in sorted(state.glob('batch-*/certified.json')):
        j=json.loads(p.read_text())['receipt']
        if j.get('status')!='complete':continue
        certified+=1;accepted.update(j.get('accepted',[]));axioms.update(j.get('axioms',[]))
    # A stopped outer coordinator may not have validated/committed its last
    # child's receipt. Preserve it separately and do not inflate certified counts.
    for p in sorted(state.glob('batch-*/receipt.json')):
        if (p.parent/'certified.json').exists():continue
        j=json.loads(p.read_text())
        if j.get('status')=='complete':
            uncommitted.append(dict(batch=p.parent.name,accepted=len(j.get('accepted',[])),receipt=str(p)))
        rejected.extend(j.get('rejected',[]))
    return accepted,axioms,rejected,certified,uncommitted

def run(raw,export,cfg,binary,source,env,names,missing,guard,write,qualification=False,retry_failed=False):
    deadline=_epoch(cfg['corpus_admission_deadline_utc'])
    grace=cfg.get('corpus_drain_seconds',900)
    cpus=cfg['corpus_cpus'];workers=cfg['corpus_workers']
    if workers!=len(cpus):raise ValueError('corpus workers/CPU set differ')
    matrix=raw.parent/'matrix'
    handoff=matrix/'matrix-collection-handoff.json'
    terminal=json.loads((handoff if handoff.exists()else matrix/'phase-terminal.json').read_text())
    if not(terminal.get('complete')or terminal.get('handoff_ready')):
        raise RuntimeError('matrix collection not retired')
    selected=Path(cfg['built_source_roots']).read_text().splitlines()
    deferred=Path(cfg['deferred_source_roots']).read_text().splitlines()
    if len(selected)!=162170 or len(set(selected))!=len(selected)or len(deferred)!=926:
        raise ValueError('wrong W built/deferred frame')
    if set(selected)&set(deferred)or set(selected)!=(set(names)-set(missing)):
        raise ValueError('selected built roots differ from actual available input frame')
    write(raw/'selection.json',dict(requested_built_modules=len(selected),deferred_source_modules=len(deferred),
        configuration_units=['lakefile'],source_frame_modules=163096,whole_input_units=len(names),
        built_root_file=cfg['built_source_roots'],deferred_root_file=cfg['deferred_source_roots'],
        source_data_commit=cfg['source_data_commit'],cpus=cpus,workers=workers,
        admission_deadline_utc=cfg['corpus_admission_deadline_utc'],drain_seconds=grace,
        kernel_checker_commit=source['native_commit'],whole_source_corpus_complete=False))
    roots=raw/'whole-roots.txt';roots.write_text('\n'.join(selected)+'\n')
    state=raw/'whole-state';state.mkdir(exist_ok=True)
    rows=[];result=None;capacity=[]
    env.update(LEAN_NUM_THREADS=str(workers),PARALLEL_ALLOWED_CPUS=json.dumps(cpus),
        PROOFSERVE_BENCH_CLASSIFICATION='built-subset coverage; mixed P/E cores, not a matrix speed point')
    initial=set(os.sched_getaffinity(0));previous=Path.cwd()
    def stage(name,argv,cap,drain=False):
        if time.time()>=deadline:raise RuntimeError('admission deadline reached; no new stage')
        old=sorted((raw/'runs').glob(name+'-attempt-*/command.json'))
        if old and not retry_failed:raise RuntimeError('existing stage retained; explicit retry required')
        key=name+'-attempt-'+str(len(old)+1)
        remain=(deadline+grace if drain else deadline)-time.time()
        r=guard.run(key,argv,min(cap,remain),True,env,
          admission_deadline=deadline if drain else None,drain_seconds=grace,
          coordinator_argv=[str(binary),str(cfg['project']),'--checkpoint-dir',str(state),'--root-file',str(roots)]if drain else None)
        rows.append(dict(phase=name,attempt=len(old)+1,returncode=r['returncode'],wall_s=r.get('wall_s'),
          cpu_s=r['cgroup_usage_s'],sampled_tree_peak_bytes=r['sampled_tree_peak_bytes'],
          charged_peak_bytes=r['charged_peak_bytes'],stop_reasons=';'.join(r.get('stop_reasons',[])),
          native_commit=source['native_commit']))
        write(raw/'workflow-results.json',rows)
        return r
    try:
        with Path(cfg['lease']).open('a+')as lease:
            print('WAIT_CORPUS_LEASE',flush=True);fcntl.flock(lease,fcntl.LOCK_EX)
            os.sched_setaffinity(0,set(cpus));os.chdir(cfg['project'])
            write(raw/'lease-acquired.json',dict(pid=os.getpid(),cpus=cpus,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
            for name in cfg.get('capacity_import_roots',['OAI']):
                if name in missing:
                    capacity.append(dict(module=name,status='not_completed',reason='deferred root has no compiled artifact; capacity not measurable',resource_failure=False))
                    write(raw/'capacity-precheck.json',capacity);continue
                meta=stage('capacity-metadata-'+name,[binary,'--internal-module-meta',name],1800)
                if meta['returncode']!=0:raise RuntimeError('capacity metadata did not complete')
                info=json.loads((raw/'runs'/('capacity-metadata-'+name+'-attempt-1')/'stdout').read_text())['module_metadata'][0]
                if not info['empty']:raise RuntimeError('capacity root is not a compiled-empty umbrella')
                check=stage('capacity-import-'+name,[binary,'--internal-empty-context',name],1800)
                capacity.append(dict(module=name,status='complete'if check['returncode']==0 else'not_completed',returncode=check['returncode']))
                write(raw/'capacity-precheck.json',capacity)
            argv=[binary,cfg['project'],'--workers',str(workers),'--root-file',roots,
                '--closure-roots',str(cfg.get('closure_roots',500)),'--checkpoint-dir',state,'--json']
            result=stage('whole-library',argv,max(1,deadline+grace-time.time()),True)
    finally:
        os.chdir(previous);os.sched_setaffinity(0,initial)
        accepted,axioms,rejected,batches,uncommitted=progress(state)
        source_accepted=set(selected)&accepted;unreached=set(selected)-source_accepted
        rejected_names={x.get('module')for x in rejected if isinstance(x,dict)and x.get('module')}
        # Native 'rejected' rows require diagnosis before being labelled kernel failures.
        coverage=dict(status='complete_built_subset'if result and result['returncode']==0 and not unreached else'incomplete',
          requested_built_modules=len(selected),accepted_built_source_modules=len(source_accepted),
          accepted_closure_modules=len(accepted),certified_complete_batches=batches,
          reported_rejected_modules=sorted(rejected_names),kernel_rejections_confirmed=None,
          not_certified_built_source_modules=len(unreached),uncommitted_complete_child_receipts=uncommitted,
          deferred_source_modules=len(deferred),configuration_units=['lakefile'],source_frame_modules=163096,
          whole_source_corpus_complete=False,axioms=sorted(axioms),capacity_precheck=capacity,
          native_commit=source['native_commit'],source_data_commit=cfg['source_data_commit'],
          final_returncode=None if result is None else result['returncode'],
          stop_reasons=[]if result is None else result.get('stop_reasons',[]),
          evidence='fresh native certified batches; uncommitted child receipts excluded from certified acceptance',
          rejected_diagnostics=rejected)
        write(raw/'whole-coverage.json',dict(coverage,accepted_built_source_names=sorted(source_accepted),not_certified_built_source_names=sorted(unreached)))
        write(export/'whole-coverage-summary.json',coverage)
        with gzip.open(raw/'module-status.csv.gz','wt',newline='')as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(['module','status','reason'])
            for name in sorted(selected):
                w.writerow([name,'accepted_certified'if name in source_accepted else'not_certified',
                  'native complete batch certificate'if name in source_accepted else'not reached or current batch uncommitted; see lifecycle'])
            for name in sorted(deferred):w.writerow([name,'deferred_build','user-deferred W source module'])
            w.writerow(['lakefile','configuration','excluded configuration unit'])
        if rows:
            with(export/'workflow-cells.csv').open('w',newline='')as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
        end=dict(complete=coverage['status']=='complete_built_subset',phase='corpus',coverage=coverage,
          native_commit=source['native_commit'],lease_returned=True)
        write(raw/'phase-terminal.json',end);write(export/'phase-terminal.json',end)
        print(json.dumps(end),flush=True)
    return end
