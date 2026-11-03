"""Dedicated inherited-count recorder, only after the original 16-cell sequence."""
import json,sys
from pathlib import Path

def main():
    point=Path(__file__).resolve().parent
    assert str(point).startswith('/workspaces/.agent-state/gpu-smt-captures/')
    state=json.loads((point/'foreground-terminal.json').read_text())
    assert state['state']=='all16_native_and_four_decodes_complete_requires_scientific_review'
    assert len(state['completed'])==16
    import perf_run
    original_run=perf_run.run
    n=int(sys.argv[1])
    assert n in [4,8]
    def count_only(key,argv,*args,**kwargs):
        assert key=='full-record-P'+str(n)+'-r2-count-only'
        assert argv.count('--compression-level=1')==1
        actual=list(argv)
        actual.remove('--compression-level=1')
        for flag,value in [('--call-graph','dwarf,16384'),('-F','99')]:
            index=actual.index(flag)
            assert actual[index+1]==value
            del actual[index:index+2]
        actual.insert(2,'--no-samples')
        return original_run(key,actual,*args,**kwargs)
    perf_run.run=count_only
    sys.argv=[str(point/'perf_run.py'),'record',str(n),'r2-count-only']
    perf_run.main()

if __name__=='__main__':
    main()
