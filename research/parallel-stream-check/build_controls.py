"""Build a native control using exactly the production certificate-loader text."""
import os
from pathlib import Path
from native import ROOT,SDK,run,environment
repo=Path('/workspaces/repository/research/parallel-stream-check')
text=(ROOT/'source/ParallelStream.lean').read_text()
start=text.index('/-- Read a prepared untrusted')
end=text.index('partial def visit',start)
# This section has no main or client elaboration. Do not maintain a second loader.
generated='import ParallelCore\nopen Lean\n'+text[start:end]+(repo/'CertificateControl.lean.in').read_text()
target=ROOT/'certificate-control-source';target.mkdir(exist_ok=True)
file=target/'CertificateControls.lean';file.write_text(generated)
os.sched_setaffinity(0,set(range(8,16)))
e=environment();e['LEAN_PATH']=str(ROOT)+':'+str(SDK/'lib/lean')
for i,c in enumerate([
 [SDK/'bin/lean','--root='+str(target),'-c',ROOT/'CertificateControls.c',file],
 [SDK/'bin/leanc','-O2','-o',ROOT/'certificate-controls',ROOT/'CertificateControls.c',
  ROOT/'ParallelCore.c',ROOT/'checked_commit.o']]):
 r=run('control-build-'+str(i),c,180,False,e)
 if r['returncode']:raise RuntimeError('control build failed')
