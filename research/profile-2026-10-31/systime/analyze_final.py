"""Summarize the completed, frozen 90-cell matrix; no new native experiments."""
import os,json,csv,re,statistics,filecmp,collections,subprocess,argparse
from pathlib import Path
from decode_grid_stacks import classify
HERE=Path(__file__).resolve().parent
B=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
OUT=HERE/'final'
def write(name,rows):
    if not rows:return
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
        w.writeheader();w.writerows(rows)
def summary(rows,keys,metric='value'):
    out=[]
    for key in sorted({tuple(r[k] for k in keys) for r in rows}):
        vals=[r[metric] for r in rows if tuple(r[k] for k in keys)==key and r[metric] is not None]
        out.append({**dict(zip(keys,key)),'n':len(vals),'median':statistics.median(vals) if vals else None,
                    'min':min(vals) if vals else None,'max':max(vals) if vals else None})
    return out
def native():
    assert json.loads((B/'matrix-v3/terminal.json').read_text())['complete']
    cells=list(csv.DictReader((B/'matrix-v3/matrix.csv').open()))
    assert len(cells)==90
    inp=json.loads((B/'matrix-v3/inputs.json').read_text())
    rows=[];artifacts=[];traces=[];quality=[];counters=[]
    for c in cells:
        module,config,mode,rep=[c[k] for k in ['module','config','mode','rep']]
        folder=B/'runs'/f'{module}-{config}-{mode}-r{rep}'
        r=json.loads((folder/'result.json').read_text())
        assert r['returncode']==0 and r['retired'] and r['native_cgroup_retired'] and r['stop_reason'] is None
        assert not re.search(r'\berror:|INTERNAL PANIC|declaration uses .sorry.',(folder/'native.log').read_text())
        ref=B/'runs'/f'{module}-baseline-plain-r1'
        diag=filecmp.cmp(folder/'native.log',ref/'native.log',shallow=False)
        assert diag
        rel=Path(*inp['modules'][module]['module'].split('.'))
        for ext in inp['modules'][module]['outputs']:
            own=folder/'artifact'/rel.with_suffix(ext);base=ref/'artifact'/rel.with_suffix(ext)
            equal=filecmp.cmp(own,base,shallow=False)
            artifacts.append(dict(module=module,config=config,mode=mode,rep=int(rep),artifact=ext,
                bytes=own.stat().st_size,equal_baseline=equal,diagnostic_equal=diag))
        for metric in ['wall_s','user_s','system_s','peak_rss_kib','sampled_tree_peak_bytes','minor_faults','major_faults','voluntary_switches','involuntary_switches']:
            rows.append(dict(module=module,config=config,mode=mode,rep=int(rep),metric=metric,value=r[metric]))
        for metric,value in [('system_cpu_share',r['system_s']/(r['system_s']+r['user_s'])),
                             ('effective_cores',(r['system_s']+r['user_s'])/r['wall_s'])]:
            rows.append(dict(module=module,config=config,mode=mode,rep=int(rep),metric=metric,value=value))
        if mode=='stat':
            ev={}
            for line in (folder/'perf-stat.csv').read_text().splitlines():
                cc=line.split(';')
                if len(cc)<5 or line.startswith('#'):continue
                try:v=float(cc[0])
                except ValueError:v=None
                ev[cc[2]]=v
                counters.append(dict(module=module,config=config,rep=int(rep),metric=cc[2],value=v,running_percent=cc[4]))
            for d in ['u','k']:
                counters.append(dict(module=module,config=config,rep=int(rep),metric='IPC/'+d,
                    value=ev['cpu_core/instructions/'+d]/ev['cpu_core/cycles/'+d],running_percent=''))
        if mode=='trace':
            text=(folder/'perf-trace.txt').read_text(errors='replace');comm='';tid=''
            sums=collections.defaultdict(lambda:dict(calls=0,errors=0,elapsed_ms=0.))
            tids=set()
            for line in text.splitlines():
                h=re.match(r'\s*(.*?)\s+\((\d+)\),\s+\d+\s+events',line)
                if h:comm,tid=h.groups()
                h=re.match(r'\s+(\w+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',line)
                if h and comm=='lean':
                    name,n,e,t,*_=h.groups();tids.add(tid)
                    sums[name]['calls']+=int(n);sums[name]['errors']+=int(e);sums[name]['elapsed_ms']+=float(t)
            assert sums
            quality.append(dict(module=module,config=config,rep=int(rep),
                lost_events=sum(map(int,re.findall(r'LOST (\d+) events',text))),
                lean_thread_summaries=len(tids),exact_census=False))
            # Absent rows are unobserved, never imputed as exact zero.
            for name,v in sums.items():
                for metric,value in v.items():
                    traces.append(dict(module=module,config=config,rep=int(rep),syscall=name,metric=metric,value=value))
    assert len({(x['module'],x['config'],x['mode'],x['rep']) for x in artifacts})==90
    assert all(x['equal_baseline'] for x in artifacts)
    write('native-per-repeat.csv',rows);ss=summary(rows,['module','config','mode','metric']);write('native-summary.csv',ss)
    write('artifacts.csv',artifacts);write('stat-per-repeat.csv',counters);write('stat-summary.csv',summary(counters,['module','config','metric']))
    write('syscalls-per-repeat.csv',traces);write('syscalls-summary.csv',summary(traces,['module','config','syscall','metric']))
    write('trace-quality.csv',quality)
    ratios=[]
    for s in ss:
        if s['mode']=='plain' or s['metric'] not in ['wall_s','user_s','system_s']:continue
        ref=next(x for x in ss if x['module']==s['module'] and x['config']==s['config'] and x['mode']=='plain' and x['metric']==s['metric'])
        ratios.append(dict(module=s['module'],config=s['config'],mode=s['mode'],metric=s['metric'],
                           profile_median=s['median'],plain_median=ref['median'],ratio=s['median']/ref['median']))
    write('profiler-overhead.csv',ratios)
    plain=[x for x in ss if x['mode']=='plain']
    print(json.dumps({'plain_metric_summaries':len(plain),'artifact_checks':len(artifacts),
                      'non_olean_mismatches':[x for x in artifacts if not x['equal_baseline']],'trace_quality':quality},indent=2),flush=True)
def decode(module,rep):
    folder=B/'runs'/f'{module}-baseline-record-r{rep}'
    tag=folder.name;raw=B/'final-analysis';raw.mkdir(exist_ok=True)
    if module=='Grid':
        for suffix in ['operations.csv','top20.csv','decode.json']:
            (OUT/(tag+'-'+suffix)).write_bytes((HERE/'grid-interim'/(tag+'-'+suffix)).read_bytes())
        return
    if (OUT/(tag+'-decode.json')).exists():return
    flat=raw/(tag+'-flat.txt')
    with flat.open('w') as f:
        subprocess.run(['perf','report','--stdio','--no-inline','--no-children','--show-nr-samples','--show-total-period',
                        '--field-separator',';','--sort','comm,dso,symbol','-i',str(folder/'perf.data')],
                       stdout=f,stderr=subprocess.PIPE,text=True,check=True)
    expectedperiod=0;expectedsamples=0
    for line in flat.read_text().splitlines():
        cc=[s.strip() for s in line.split(';')]
        if len(cc)>=6 and cc[0].endswith('%') and cc[3]=='lean':
            expectedperiod+=int(cc[2]);expectedsamples+=int(cc[1])
    assert expectedperiod>0
    totals=collections.Counter();categories=collections.Counter();hot=collections.Counter()
    samples=0;ignored=0;bad=[];depth=collections.Counter()
    def block(lines):
        nonlocal samples,ignored
        if not lines:return
        header=lines[0];h=re.search(r'\s(\d+)\s+(?:cpu_core/)?cycles[^:]*:',header)
        if not h:bad.append(header);return
        period=int(h[1])
        if not header.lstrip().startswith('lean '):ignored+=1;return
        frames=[]
        for line in lines[1:]:
            if ' (' not in line or not line.endswith(')'):continue
            left,dso=line.rsplit(' (',1);pair=left.split(None,1)
            if len(pair)==2 and re.fullmatch('[0-9a-fA-F]+',pair[0]):frames.append((int(pair[0],16),pair[1],dso[:-1]))
        if not frames:bad.append(header);return
        ip,name,dso=frames[0];domain='kernel' if 'kernel' in dso or ip>=0xffff800000000000 else 'user'
        samples+=1;totals[domain]+=period;categories[(domain,classify(frames,domain))]+=period
        hot[(domain,name,dso)]+=period;depth[len(frames)]+=1
    cmd=['perf','script','--no-inline','--ns','--max-stack','48','-i',str(folder/'perf.data'),
         '-F','comm,pid,tid,time,event,period,ip,sym,dso']
    with (raw/(tag+'-stderr.txt')).open('w') as err:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True)
        lines=[]
        for line in p.stdout:
            line=line.rstrip('\n')
            if line:lines.append(line)
            else:block(lines);lines=[]
        block(lines);code=p.wait()
    assert code==0 and not bad,(code,bad[:3])
    assert sum(totals.values())==expectedperiod and samples==expectedsamples
    write(tag+'-operations.csv',[dict(domain=d,operation=k,period=v,within_domain_fraction=v/totals[d],
        of_native_fraction=v/sum(totals.values())) for (d,k),v in sorted(categories.items())])
    tops=[]
    for domain in ['user','kernel']:
        tops.extend(dict(domain=d,symbol=s,dso=l,period=v,within_domain_fraction=v/totals[d])
            for (d,s,l),v in sorted(((k,v) for k,v in hot.items() if k[0]==domain),key=lambda x:-x[1])[:20])
    write(tag+'-top20.csv',tops)
    (OUT/(tag+'-decode.json')).write_text(json.dumps(dict(native_samples=samples,ignored_helper_samples=ignored,
        periods=dict(totals),all_native_period_and_sample_totals_equal_independent_flat_report=True,
        sample_stack_depth_counts=dict(depth),method='v2 imported Grid classifier; no inline expansion; 48 frames',
        argv=cmd),indent=2)+'\n')
    print('decoded',tag,samples,flush=True)
def aggregate():
    rr=[];tops=[]
    for module in ['Grid','UMoments9','EnvelopePsiB']:
        for rep in [1,2,3]:
            tag=f'{module}-baseline-record-r{rep}'
            for x in csv.DictReader((OUT/(tag+'-operations.csv')).open()):
                rr.append(dict(module=module,rep=rep,domain=x['domain'],operation=x['operation'],value=float(x['within_domain_fraction'])))
            for x in csv.DictReader((OUT/(tag+'-top20.csv')).open()):
                tops.append(dict(module=module,rep=rep,**x))
    full=[]
    for module in ['Grid','UMoments9','EnvelopePsiB']:
        for domain,op in sorted({(x['domain'],x['operation']) for x in rr if x['module']==module}):
            for rep in [1,2,3]:
                val=next((x['value'] for x in rr if (x['module'],x['rep'],x['domain'],x['operation'])==(module,rep,domain,op)),0.)
                full.append(dict(module=module,rep=rep,domain=domain,operation=op,value=val))
    write('operations-per-repeat.csv',full);write('operations-summary.csv',summary(full,['module','domain','operation']))
    write('top20-per-repeat.csv',tops)
if __name__=='__main__':
    os.sched_setaffinity(0,set(range(8,16)));OUT.mkdir(exist_ok=True)
    native()
    for module in ['Grid','UMoments9','EnvelopePsiB']:
        for rep in [1,2,3]:decode(module,rep)
    aggregate()
