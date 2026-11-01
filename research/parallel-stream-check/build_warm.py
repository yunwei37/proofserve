"""Untimed optional stock-import diagnostic, never an independent closure."""
import os
from pathlib import Path
from native import ROOT,SDK,run,environment
repo=Path('/workspaces/repository/research/parallel-stream-check')
source=(ROOT/'source/ParallelStream.lean').read_text()
reader=source[:source.index('partial def visit')]
target=ROOT/'warm-source';target.mkdir(exist_ok=True)
file=target/'WarmCurve.lean'
file.write_text(reader+(repo/'WarmCurve.lean.in').read_text())
os.sched_setaffinity(0,set(range(8,16)))
e=environment();e['LEAN_PATH']=str(ROOT)+':'+str(SDK/'lib/lean')
for i,command in enumerate([
 [SDK/'bin/lean','--root='+str(target),'-c',ROOT/'WarmCurve.c',file],
 [SDK/'bin/leanc','-O2','-o',ROOT/'warm-curve',ROOT/'WarmCurve.c',ROOT/'ParallelCore.c',ROOT/'checked_commit.o']]):
 r=run('warm-build-'+str(i),command,180,False,e)
 if r['returncode']:raise RuntimeError('warm build failed; preserve raw')
