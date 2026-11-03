"""Aggregate original READ records; counting-only perf report-T has no histogram."""
import collections,csv,json,sys
from pathlib import Path

def workers(point,key):
    c=json.loads((point/(key+'-terminal.json')).read_text())['cell']
    d=point/('decode-'+key);totals=collections.Counter()
    ids=collections.defaultdict(set);all_ids=collections.defaultdict(set)
    records=collections.Counter()
    with (d/'read-times.csv').open() as f:
        for x in csv.DictReader(f):
            tid=int(x['TID']);ev=x['event']
            totals[tid,ev]+=int(x['value'])
            if ev.startswith('cpu_core/'):
                ids[tid,ev].add(x['id']);all_ids[ev].add(x['id'])
                records[tid,ev,x['id']]+=1
    assert len(all_ids)==7 and all(len(v)==len(c['affinity']) for v in all_ids.values())
    work=collections.defaultdict(collections.Counter)
    with (point/'runs'/key/'stdout').open() as f:
        for line in f:
            if not line.startswith('{'):continue
            e=json.loads(line)
            if e.get('event')!='profile_module':continue
            for x in e['metrics']['workers']:
                w=work[x['tid']]
                w['checks']+=x['checks'];w['units']+=x['raw_HB'];w['CPU_ns']+=x['cpu_ns']
    rows=[]
    def value(tid,ev):
        return totals[tid,'cpu_core/'+ev+(',period=0/u' if ev!='cpu-cycles' else '/u')]
    for tid,w in sorted(work.items()):
        assert all(ids[tid,ev]==v for ev,v in all_ids.items()),'partial worker READ set'
        assert all(records[tid,ev,i]==1 for ev,v in all_ids.items() for i in v)
        cyc=value(tid,'cpu-cycles');ins=value(tid,'instructions')
        rows.append(dict(key=key,workers=c['workers'],TID=tid,checks=w['checks'],
            allocation_units=w['units'],kernel_CPU_s=w['CPU_ns']/1e9,
            cycles=cyc,instructions=ins,IPC=ins/cyc,
            reference_cycles=value(tid,'ref-cycles'),
            cycles_per_reference_cycle=cyc/value(tid,'ref-cycles'),
            retired_L3_miss_loads=value(tid,'mem_load_retired.l3_miss'),
            locked_loads=value(tid,'mem_inst_retired.lock_loads'),
            modified_line_forwarding=value(tid,'mem_load_l3_hit_retired.xsnp_hitm'),
            RFO_snoop_HITM=value(tid,'ocr.demand_rfo.l3_hit.snoop_hitm'),
            all_expected_READ_shards_present=True,
            scope='PMU thread lifetime; C CPU original-call interval; not sample normalization'))
    assert sum(x['checks']for x in rows)==c['ordinary_checks']==237863
    assert sum(x['allocation_units']for x in rows)==c['ordinary_allocation_units']==3283925639
    return rows

def main():
    data=workers(Path(sys.argv[1]),sys.argv[2])
    with Path(sys.argv[3]).open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator=chr(10))
        w.writeheader();w.writerows(data)
    print('qualified checking TIDs',len(data),'IPC',min(x['IPC']for x in data),max(x['IPC']for x in data))
if __name__=='__main__':main()
