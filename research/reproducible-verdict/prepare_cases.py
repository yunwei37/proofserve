"""Freeze selected retained source inputs; do not regenerate a healthy capture."""
import json,re
from pathlib import Path
ROOT=Path('/workspaces/repository')
OLD=ROOT/'research/mechanisms-2026-10-30'
def prepare(out):
    sources={x['id']:x for x in json.loads((OLD/'dag200-input.json').read_text()) if x['mode']=='control'}
    import csv
    with (OLD/'profiler-400-diagnostic.csv').open() as f:
        rows=list(csv.DictReader(f))
    print('csvfields',list(rows[0]))
    selected=[x['id'] for x in json.loads((OLD/'profiler-7-differences.json').read_text())]
    # Preserve representative cases by the retained diagnostic classification.
    for kind in ['no_lean_errors','ordinary_lean_error','diagnostic_budget_interruption']:
        for row in rows:
            if row.get('mode')=='control' and row.get('classification')==kind and row['id'] not in selected:
                selected.append(row['id'])
                if sum(1 for x in selected if x not in {a['id'] for a in json.loads((OLD/'profiler-7-differences.json').read_text())} and next((z.get('classification')for z in rows if z['id']==x and z['mode']=='control'),None)==kind)>=3:break
    cases=[]
    for key in selected:
        code=sources[key]['code']
        # Budget is an experimental treatment, not a silently retained source override.
        code=re.sub(r'(?m)^set_option maxHeartbeats \d+\s*$', '', code)
        target=re.search(r'\btheorem\s+([A-Za-z0-9_]+)',code)
        if not target:raise ValueError(key)
        cases.append(dict(id=key,code=code,target=target.group(1)))
    (out/'selected.json').write_text(json.dumps(cases,indent=2))
    return cases
if __name__=='__main__':
    import sys
    prepare(Path(sys.argv[1]))
