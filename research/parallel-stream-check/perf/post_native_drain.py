"""Keep only the perf workload parent alive after the measured child exits."""
import json,subprocess,sys,time
from pathlib import Path
assert str(Path(__file__).resolve()).startswith('/workspaces/.agent-state/gpu-smt-captures/')
result=subprocess.run(sys.argv[1:])
print(json.dumps(dict(event='post_native_drain_begin',child_returncode=result.returncode,
                     monotonic_ns=time.monotonic_ns(),seconds=5)),flush=True)
time.sleep(5)
print(json.dumps(dict(event='post_native_drain_end',monotonic_ns=time.monotonic_ns())),flush=True)
raise SystemExit(result.returncode)
