"""Small publication tables from the original complete native matrix only."""
import collections,csv,json,sys
from decimal import Decimal
from pathlib import Path

def rows(p):
    with p.open() as f:return list(csv.DictReader(f))
def write(p,data):
    assert data
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator=chr(10))
        w.writeheader();w.writerows(data)

def main():
    root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True,parents=True)
    original={'full-'+arm+'-P'+str(n)+'-'+rep for n in [1,2,4,8]
              for arm,rep in [('plain','r1-before'),('stat','r1'),('record','r1'),('plain','r1-after')]}
    native=[r for r in rows(root/'native-timings.csv') if r['key'] in original]
    assert len(native)==16 and {r['key']for r in native}==original
    assert all(r['accepted_count']=='4449' and r['accepted_reference_equal']=='True'
               and r['checks']=='237863' and r['allocation_units']=='3283925639' for r in native)
    cats=rows(root/'category-by-workers.csv')
    counted=collections.Counter()
    for r in cats:
        if r['key'] in original:
            counted[int(r['workers']),r['scope'],r['category']]+=int(r['sampled_cycles'])
    categories=sorted({k[2] for k in counted})
    families=[]
    for scope in ['ordinary_kernel_anchored','ordinary_worker_kernel_unanchored']:
        for cat in categories:
            vals=[counted[n,scope,cat] for n in [1,2,4,8]]
            if not any(vals):continue
            families.append(dict(scope=scope,category=cat,P1_Gcycles=vals[0]/1e9,
                P2_Gcycles=vals[1]/1e9,P4_Gcycles=vals[2]/1e9,P8_Gcycles=vals[3]/1e9,
                P8_minus_P4_Gcycles=(vals[3]-vals[2])/1e9,
                meaning='period-weighted samples; inline RC may appear in other families'))
    write(out/'kernel-family-comparison.csv',families)
    whole=[]
    for n in [1,2,4,8]:
        ss=[r for r in rows(root/'stat-counters.csv') if r['key']=='full-stat-P'+str(n)+'-r1']
        assert len(ss)==7 and all(float(r['pcnt_running'])==100 for r in ss)
        counts={r['event'].split('/')[1]:int(Decimal(r['counter_value']))for r in ss}
        whole.append(dict(workers=n,cycles=counts['cpu-cycles'],instructions=counts['instructions'],
            IPC=counts['instructions']/counts['cpu-cycles'],ref_cycles=counts['ref-cycles'],
            cycles_per_ref_cycle=counts['cpu-cycles']/counts['ref-cycles'],
            retired_L3_miss_loads=counts['mem_load_retired.l3_miss'],
            retired_locked_loads=counts['mem_inst_retired.lock_loads'],
            L3_modified_line_forwarding=counts['mem_load_l3_hit_retired.xsnp_hitm'],
            RFO_snoop_HITM=counts['ocr.demand_rfo.l3_hit.snoop_hitm'],
            scope='whole stat command, user only; not exact original-check interval'))
    write(out/'whole-command-comparison.csv',whole)
    w=[r for r in rows(root/'record-thread-counters.csv')
       if r['key']in original and r['observed_original_check_worker']=='True']
    write(out/'observed-worker-counters.csv',w)
    scope_totals=collections.Counter()
    for (n,scope,cat),v in counted.items():scope_totals[n,scope]+=v
    coverage=[]
    for n in [1,2,4,8]:
        strict=scope_totals[n,'ordinary_kernel_anchored']
        wide=scope_totals[n,'ordinary_worker_kernel_unanchored']
        total=sum(v for (nn,scope),v in scope_totals.items()if nn==n)
        coverage.append(dict(workers=n,strict_Gcycles=strict/1e9,unanchored_worker_kernel_Gcycles=wide/1e9,
            strict_fraction_of_both=strict/(strict+wide),total_sampled_Gcycles=total/1e9,
            interpretation='stack coverage indicator, not fraction of all original-check CPU'))
    write(out/'stack-scope-coverage.csv',coverage)
    print(json.dumps(dict(original_native_points=len(native),ordinary_verdicts_equal=True,
                         output=str(out)),sort_keys=True))

if __name__=='__main__':main()
