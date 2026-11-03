from pathlib import Path
import json,os,importlib.util,traceback
os.sched_setaffinity(0,{8})
A=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103')
audit=json.loads((A/'reboot-20261103T1448/audit.json').read_text())
assert Path('/proc/sys/kernel/random/boot_id').read_text().strip()==audit['current_boot']
spec=importlib.util.spec_from_file_location('s',A/'subexponential-run-resume-v2.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
assert s.state()['phase']=='source' and len(s.state()['built'])==13169
try:
 s.queue()
 s.atomic(A/'resume-terminal.json',dict(state=s.state(),reduced=s.reduce(),resume='host reboot20261103'))
except BaseException as error:
 s.atomic(A/'resume-after-reboot-failure.json',dict(error=repr(error),traceback=traceback.format_exc()))
 raise
