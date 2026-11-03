"""One tail-drain counter control; no change inside the Lean native workload."""
import json,sys
from pathlib import Path

def main():
    p=Path(__file__).resolve().parent
    assert str(p).startswith('/workspaces/.agent-state/gpu-smt-captures/')
    assert json.loads((p/'foreground-terminal.json').read_text())['state']=='all16_native_and_four_decodes_complete_requires_scientific_review'
    assert json.loads((p/'full-record-P4-r2-count-only-terminal.json').read_text())['state']=='complete'
    import perf_run
    original=perf_run.run
    def drain(key,argv,*args,**kwargs):
        assert key=='full-record-P4-r3-count-only-drain5'
        actual=list(argv);actual.remove('--compression-level=1')
        for flag,value in [('--call-graph','dwarf,16384'),('-F','99')]:
            i=actual.index(flag);assert actual[i+1]==value;del actual[i:i+2]
        actual.insert(2,'--no-samples')
        i=actual.index('--')+1
        actual[i:i]=[sys.executable,str(p/'post_native_drain.py')]
        return original(key,actual,*args,**kwargs)
    perf_run.run=drain
    sys.argv=[str(p/'perf_run.py'),'record','4','r3-count-only-drain5']
    perf_run.main()
if __name__=='__main__':main()
