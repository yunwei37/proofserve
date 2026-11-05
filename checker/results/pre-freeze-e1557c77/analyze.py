#!/usr/bin/env python3
"""Reduce retained pre-freeze previews; never launches native work."""
import argparse,collections,csv,json
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('raw',type=Path)
a=ap.parse_args();raw=a.raw
out=Path(__file__).resolve().parent
launch=json.loads((raw/'launch.json').read_text())
old=Path(launch['old_preview'])
def read(p):return json.loads(p.read_text())
def events(state):
    # Only successful committed segments contribute final acceptance evidence.
    result=[]
    for p in sorted(state.glob('segment-*.json')):
        r=read(p)
        if r['exit']==0:result.extend(r['events'])
    return result
def table(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[];reasons=[];sets={};inputs={}
legacy_csv=Path(__file__).resolve().parents[1]/'loaded-preview-cells.csv'
legacy={r['key']:r for r in csv.DictReader(legacy_csv.open())}
for dataset,oldkey in [('nat','math-P2-r1'),('grid','grid-P2-r1')]:
    for source in ['ba316991','3fe83c5a','e1557c77']:
        if source=='ba316991':
            receipt=read(old/(oldkey+'-receipt.json'));state=old/oldkey
            r=legacy[oldkey];attempts=[oldkey]
            cpu=float(r['cpu_s']);user=float(r['cpu_user_s']);system=float(r['cpu_system_s'])
            wall=[float(r['wall_s'])];peak=int(r['rss_sample_bytes'])
            affinity='P0-7';disrupted=False
        else:
            ref=source=='3fe83c5a'
            key=dataset+('-3fe-reference' if ref else '-e155')
            receipt=read(raw/(key+'-receipt.json'));state=raw/(key+'-state')
            attempts=[key]
            if not ref and dataset=='grid':attempts+=['grid-e155-resume1']
            runs=[read(raw/'runs'/k/'result.json') for k in attempts]
            assert all(r['native_retired'] and r['cgroup_retired'] for r in runs)
            assert runs[-1]['returncode']==0
            cpu=sum(r['cgroup_usage_s'] for r in runs)
            user=sum(r['cgroup_user_s'] for r in runs)
            system=sum(r['cgroup_system_s'] for r in runs)
            peak=max(r['sampled_tree_peak_bytes'] for r in runs)
            wall=[r['wall_s'] for r in runs];affinity='E8-9'
            disrupted=len(attempts)>1
        assert receipt['status']=='complete' and not receipt['rejected']
        accepted=set(receipt['accepted']);axioms=set(receipt['axioms'])
        es=events(state)
        local={e['module']:e for e in es if e.get('event')=='accept' and e.get('context')=='module_local'}
        all_events={e['module'] for e in es if e.get('event')=='accept'}
        assert all_events==accepted,(dataset,source,len(all_events),len(accepted))
        counts=collections.Counter(e.get('fallback_reason','unknown').split(':',1)[0] for e in local.values())
        for reason,count in sorted(counts.items()):
            reasons.append(dict(dataset=dataset,source=source,reason=reason,whole_module_serial_replays=count))
        sets[dataset,source]=dict(accepted=accepted,axioms=axioms)
        inputs[dataset,source]=dict(read(state/'identity.json')['inputs'])
        rows.append(dict(dataset=dataset,source=source,affinity=affinity,workers=2,status=receipt['status'],
            accepted=len(accepted),declared_axioms=len(axioms),whole_module_serial_replays=len(local),
            segments=len(receipt['segments']),sampled_peak_rss_gib=peak/1024**3,
            actual_attempt_cpu_s=cpu,actual_attempt_user_s=user,actual_attempt_system_s=system,
            attempt_wall_s=json.dumps(wall),attempts=len(attempts),interrupted=disrupted,
            complete_segment_cpu_s=int(receipt['cumulative_segment_cpu_ns'])/1e9,
            binary_hash=receipt.get('checker_binary_hash','not-recorded'),paper_eligible=False))
comparisons=[]
for dataset in ['nat','grid']:
    target=sets[dataset,'e1557c77']
    for baseline in ['ba316991','3fe83c5a']:
        ref=sets[dataset,baseline]
        old_inputs=inputs[dataset,baseline];new_inputs=inputs[dataset,'e1557c77']
        mismatch=[k for k,v in old_inputs.items() if new_inputs.get(k)!=v]
        comparisons.append(dict(dataset=dataset,reference=baseline,
            accepted_missing=sorted(ref['accepted']-target['accepted']),
            accepted_added=sorted(target['accepted']-ref['accepted']),
            axioms_missing=sorted(ref['axioms']-target['axioms']),
            axioms_added=sorted(target['axioms']-ref['axioms']),
            prior_recorded_input_pairs=len(old_inputs),prior_input_mismatches=mismatch,
            additional_inventory_pairs=len(new_inputs)-len(old_inputs)))
table(out/'closures.csv',rows);table(out/'fallback-reasons.csv',reasons)
summary=dict(native_source_commit=launch['source_commit'],raw=str(raw),paper_eligible=False,
    verdict='frozen with known performance regression; user-authorized correctness-first exception, not threshold pass',
    comparisons=comparisons,rows=rows,
    declared_axioms={d:sorted(sets[d,'e1557c77']['axioms']) for d in ['nat','grid']},
    interrupted_grid_clock_note='attempt CPU includes interrupted work; clocks are not an uninterrupted performance sample',
    fallback_count_scope='module_local accept records in successful committed segments; internal complex-prefix replay and overwritten partial events are not counted',
    data_quality='See data-quality.md: first uncommitted Grid event file was not archived before native resume.')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+chr(10))
print(json.dumps(summary,indent=2))

by={(r['dataset'],r['source']):r for r in rows}
def row(d,src):
    r=by[d,src]
    return f"| {d} | {src} | {r['affinity']} | {r['accepted']} | {r['declared_axioms']} | {r['whole_module_serial_replays']} | {r['segments']} | {r['sampled_peak_rss_gib']:.3f} | {r['actual_attempt_cpu_s']:.2f} | {r['complete_segment_cpu_s']:.2f} |"
md="""# Real-closure regression and native-source freeze

> Superseded freeze decision: the coordinator replaced this default on
> 2026-11-05 with shared-checked plus an explicit strict mode. The measurements
> below remain unchanged historical e1557c77 data. See ../theorem-body-policy/.

Native source is frozen at e1557c770fcc585e722399e56a3c3be77b2f0e7f.
The freeze uses the coordinator's explicit correctness-first exception:
**the fallback-growth performance threshold did not pass**. This is not a
release, an independent execution review, or a qualified speedup claim.

## Actual closure checks

The fixed e155 binary ran with two workers on E cores 8–9, at most 12 GiB
of its own native group, no Lean -M and no P-core lock while W's census continued.
Both roots used fresh checkpoint directories initially. Nat.Basic is its
1,330-module dependency closure, not the complete Mathlib library.
Grid is the retained 3,793-module dependency closure.

The retained 3fe83c5a binary was run on exactly these roots and E-core settings
to separate the old axiom-report correction from this repair. Its known
small-fixture correctness defects make it a diagnostic reference, not a release
candidate. The ba316991 row shows one retained P-core preview for each root;
its CPU must not be divided into E-core CPU and called a source speedup.

| Root | Source | CPUs | Accepted | Declared axioms | Whole-module serial replay | Segments | Peak tree GiB | Attempt CPU s | Complete-segment CPU s |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
"""
for d in ['nat','grid']:
    for src in ['ba316991','3fe83c5a','e1557c77']:md+=row(d,src)+'\n'
md+="""
Both new acceptance sets equal their retained ba316991 and same-root 3fe83c5a
sets. The new 15-name declared axiom sets equal the same-root 3fe83c5a sets.
The earlier ba316991 report listed only seven; the eight additional names
(Quot.lcInv, isScalarObj, lcAny, lcCast, lcErased, lcProof, lcUnreachable,
lcVoid) were already in the unchanged inputs and were omitted by that older
report. They are not new assumptions inserted by this qualification.

All previously recorded input path/hash pairs match the new inventories;
the new inventory additionally validates IR presence and bytes. See
summary.json for exact comparison counts and declared names. These 64-bit
identities detect ordinary changes, not deliberately constructed collisions.

Module-local counts use successful committed-segment accept records and
their unique module names; those two counts agree in this run. They do not
count internal complex-prefix declaration replay or unknown overwritten
partial events. fallback-reasons.csv gives the exact recorded reason categories.

## Why the threshold fails

"""
for d in ['nat','grid']:
    new=by[d,'e1557c77'];ref=by[d,'3fe83c5a']
    md+=f"- {d}: whole-module replay rose from {ref['whole_module_serial_replays']} to {new['whole_module_serial_replays']}, exceeding the allowed 10% growth.\n"
md+="""
The real first divergent theorem is List.drop.eq_def in Init.Data.List.TakeDrop.
The two bodies mention different private splitter constants. Removing metadata
and let nondependency annotations does not make them equal; a bounded beta/zeta
diagnostic also did not equate them. diagnosis.json records the actual output.

A same-interface or imported-ancestor exemption is not a safe small repair:
the upstream importer can replace a theorem body with a later imported body,
and the genuine WellFounded/Acc regressions show that retaining the wrong
body can change downstream checking. No unqualified proof-body normalization,
alias substitution or correctness rollback is shipped to recover throughput.
Context-aware optimization remains unimplemented; this is a known cost, not
a claim that a safe optimization is impossible.

The quarantine causes subsequent missing-frontier and segregated-dependency
fallbacks. CPU is reported as a preview under the census, not an isolated
causal measurement of this one code branch or a quiet-machine performance result.

## Interruption, memory and evidence

Nat.Basic finished in one invocation. Grid reached the first 1,800-second
finite window and then completed from the same binary/checkpoint. Its two
wall-clock intervals remain separate. Attempt CPU includes interrupted work,
revalidation and repeated work; complete-segment CPU is reported separately.
All guarded native processes and cgroups retired. There were no memory,
node-reserve or OOM stops. See data-quality.md for the unarchived first partial
Grid event file; do not claim every partial event survived.

Raw binaries, receipts, complete segments, memory samples and failed attempts:
"""
md+='\n'+str(raw)+'\n'
md+="""
The public small tables can be regenerated with:

    python3 checker/results/pre-freeze-e1557c77/analyze.py RAW_DIRECTORY

## Freeze and remaining work

freeze.json binds the native source files, binary receipt identity and CI
evidence. Both code-only independent reviews have regression repairs; the
repaired source has no independent execution review. The current execution and
result interpretation are self-review (自审). The earlier repair's CI passed
the core contract plus 90 earlier and 109 new review command records; these
are command counts, not counts of distinct defects or theorems.

After freeze, only real defects justify native changes, and relevant results
must be rerun after a change. Documents and new evaluation results may still
be added. No tag or public release is created.

Still pending: the post-census quiet-machine final matrix and official controls,
O's external-project acceptance/timings, the repaired-source 14,721-module replay
and bounded corpus checking. Earlier ABI 4 large results do not qualify ABI 5.
The final closeout order and deadlines supersede the historical capacity-first
driver; see ../../docs/release-evaluation.md. There is no PlanarPacking-only
comparison and no new performance number from this preview enters the paper.
"""
(out/'README.md').write_text(md)
