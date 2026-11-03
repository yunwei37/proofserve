"""One-variable recorder control, only after the original 16-cell sequence."""
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
    def uncompressed(key,argv,*args,**kwargs):
        assert key=='full-record-P'+str(n)+'-r2-uncompressed'
        assert argv.count('--compression-level=1')==1
        actual=[x for x in argv if x!='--compression-level=1']
        return original_run(key,actual,*args,**kwargs)
    perf_run.run=uncompressed
    sys.argv=[str(point/'perf_run.py'),'record',str(n),'r2-uncompressed']
    perf_run.main()

if __name__=='__main__':
    main()
