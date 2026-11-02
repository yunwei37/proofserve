#!/usr/bin/env python3
"""Recompute paper-facing Falconer evidence from retained native records; no Lean run."""
import csv
import json
import os
from pathlib import Path

B = Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
D = B / 'scale-study/falconer-project-20261101'
C = D / 'checkpoint-recheck-v2'
OWN = Path(__file__).resolve().parent


def events(path):
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.startswith('{')]


def main():
    os.sched_setaffinity(0, {8})  # Offline reduction, no timed/native workload.
    frame = json.loads((D / 'build-frame.json').read_text())
    wanted = {row['module'] for row in frame}
    source = list(csv.DictReader((OWN / 'falconer-source-costs.csv').open()))
    assert len(source) == len(wanted) == 13205
    assert {row['module'] for row in source} == wanted
    for row in source:
        raw = Path(row['source_cell_root']) / (row['source_cell'] + '.result.json')
        cell = json.loads(raw.read_text())
        assert cell['returncode'] == 0 and cell['measured']
        assert cell['affinity'] == list(range(8))
        assert abs(cell['wall_s'] - float(row['source_compiler_wall_s'])) < 1e-12
    segments = sorted(C.glob('segment-*-terminal.json'))
    assert len(segments) == 27
    accepted, headers = set(), {}
    previous = None
    wall = cpu = 0.0
    peak = snapshot_bytes = 0
    snapshots = restores = 0
    complete = None
    for i, path in enumerate(segments):
        v = json.loads(path.read_text())
        cell = v['cell']
        raw = events(C / (cell['key'] + '.stdout'))
        assert cell['returncode'] == 0 and cell['measured']
        assert cell['affinity'] == list(range(8))
        assert cell['memory_max_bytes'] == 12616466432
        assert '-M' not in cell['args'] and not any(a.startswith('-M') for a in cell['args'])
        assert not v['malformed'] and not v['rejected']
        assert v['previous_snapshot'] == previous
        new = [e['module'] for e in raw if e.get('event') == 'accept']
        assert new == v['accepted']
        assert len(new) == len(set(new)) == (500 if i < 26 else 205)
        assert not accepted.intersection(new)
        accepted.update(new)
        for e in raw:
            if e.get('event') == 'module_header':
                name, imports = e['module'], set(e['imports'])
                assert name not in headers or headers[name] == imports
                headers[name] = imports
        if i < 26:
            assert v['checkpoint'] and not v['complete']
            assert v['checkpoint']['modules'] == (i + 1) * 500
            snapshot = C / (v['snapshot'] + '.olean')
            assert snapshot.is_file()
            snapshot_bytes += snapshot.stat().st_size
            snapshots += 1
        else:
            assert not v['checkpoint'] and v['complete']['modules'] == 13205
            complete = v['complete']
        restores += int(previous is not None)
        previous = v['snapshot']
        wall += cell['wall_s']
        cpu += cell['user_s'] + cell['system_s']
        peak = max(peak, cell['peak_rss_kib'])
        assert all(int(line.split()[1]) == 0
                   for line in cell['memory_events'].splitlines()
                   if line.split()[0] in {'max', 'oom', 'oom_kill', 'oom_group_kill'})
    assert accepted == wanted == set(headers)
    assert all(headers[v['module']] == set(v['imports']) for v in frame)
    # Reconstruct the independently run, original module-local reference union.
    reference = set(json.loads((B / 'progress.json').read_text())['oracle_global']) & wanted
    common = len(reference)
    assert common == 5077
    retained_common = set()
    for line in (B / 'measured.jsonl').open():
        v = json.loads(line)
        if v.get('operation') != 'matched_oracle':
            continue
        assert v['returncode'] == 0 and v['closure_complete']
        native = {e['module'] for e in events(B / (v['key'] + '.stdout'))
                  if e.get('event') == 'accept'}
        assert native == set(v['accepted_modules']) == set(v['requested_modules'])
        retained_common.update(native)
    assert reference <= retained_common
    chunks = sorted((D / 'bounded-recheck-v1').glob('oracle-*-terminal.json'))
    assert len(chunks) == 16
    for path in chunks:
        v = json.loads(path.read_text())
        cell = v['cell']
        assert v['complete'] and cell['returncode'] == 0
        native = {e['module'] for e in events(path.parent / (cell['key'] + '.stdout'))
                  if e.get('event') == 'accept'}
        assert native == set(v['accepted']) == set(v['requested'])
        assert not reference.intersection(v['accepted'])
        reference.update(v['accepted'])
    assert reference == wanted
    controls = json.loads((C / 'checkpoint-controls.json').read_text())
    assert controls['complete'] and all(v['qualified'] for v in controls['results'])
    assert sum(v['parts'] for v in controls['results']) == 18
    assert (C / 'CheckpointAudit.lean').read_bytes() == (OWN / 'CheckpointAudit.lean').read_bytes()
    source_wall = sum(float(v['source_compiler_wall_s']) for v in source)
    out = dict(
        source_revision='4eaee87548250b2682affda7d05d947c05554bae',
        lean_release='4.34.1',
        lean_commit='5045d0056413266e57c625dcd7c365b10e377c52',
        mathlib_commit='d13f23b723b8a846827a245b89c10fc7d3f11612',
        modules=len(wanted), segments=len(segments),
        full_segments=26, final_segment_modules=205,
        source_wall_sum_s=source_wall, check_wall_sum_s=wall,
        check_cpu_sum_s=cpu, ratio=wall/source_wall,
        peak_rss_gib=peak/1024**2,
        snapshots=snapshots, restores=restores, snapshot_file_bytes=snapshot_bytes,
        input_declaration_entries=complete['constants'],
        unique_shared_kernel_declarations=complete['unique_shared_kernel_declarations'],
        upstream_skipped_unsafe_partial=complete['skipped_unsafe_partial'],
        module_local_fallbacks=complete['module_local_fallbacks'],
        native_graph_equal=True, original_reference_equal=True,
        reference_common=common, reference_chunks=len(chunks),
        controls_native_processes=18,
        checkpoint_io_in_process_wall=True,
        separately_measured_checkpoint_io_s=None,
    )
    (OWN / 'falconer-paper-evidence.json').write_text(json.dumps(out, indent=2) + '\n')
    rows = list(csv.DictReader((OWN / 'falconer-final-costs.csv').open()))
    falc = next(v for v in rows if v['cohort'] == 'Falconer')
    assert abs(float(falc['wall_s']) - wall) < 1e-9
    assert abs(float(falc['source_wall_sum_s']) - source_wall) < 1e-9
    original_math = json.loads((B / 'timed-constructed-stream-math.result.json').read_text())
    assert original_math['returncode'] == 0
    math = next(v for v in rows if v['cohort'] == 'Mathlib')
    table = []
    for cohort, protocol, modules, count, cost, denom, rss in [
        ('Falconer closure', 'checkpointed', 13205, 27, wall, source_wall, peak/1024**2),
        ('Mathlib Nat.Basic closure', 'unsegmented historical', 1330, 1,
         original_math['wall_s'], float(math['source_wall_sum_s']),
         original_math['peak_rss_kib']/1024**2),
        ('Mathlib Nat.Basic closure', 'checkpointed matched protocol', 1330, 3,
         float(math['wall_s']), float(math['source_wall_sum_s']), float(math['peak_rss_gib'])),
    ]:
        table.append(dict(cohort=cohort, protocol=protocol, modules=modules, segments=count,
                          check_wall_sum_s=cost, source_wall_sum_s=denom,
                          check_over_source=cost/denom, peak_rss_gib=rss))
    with (OWN / 'falconer-paper-table.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=table[0], lineterminator='\n')
        w.writeheader()
        w.writerows(table)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
