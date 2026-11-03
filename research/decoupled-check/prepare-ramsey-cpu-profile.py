#!/usr/bin/env python3
"""Generate an observation-only copy of the qualified checkpoint adapter.

Primary Ramsey timing does not use this copy. The later paired profile
separates exclusive per-module CPU from process startup/checkpoint overhead.
"""
from pathlib import Path
import shutil

D = Path(__file__).resolve().parent
A = Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102/cpu-profile")
def main():
    A.mkdir(exist_ok=True)
    text = (D / "CheckpointAudit.lean").read_text()
    prefix = "open Lean\n"
    assert text.count(prefix) == 1
    text = text.replace(prefix, prefix + """
@[extern "proofserve_process_cpu_ns"]
opaque processCpuNanos : IO UInt64
""")
    before_read = "  let parts ← moduleParts mod\n"
    # localReplay also reads parts; only the visit body receives timing.
    first, visit = text.split("partial def visit ", 1)
    assert visit.count(before_read) == 1
    visit = visit.replace(before_read, "  let cpuBegin ← processCpuNanos\n" + before_read)
    imports = "  for imp in first.imports do visit mode mutation mutateOnly imp.module\n"
    assert visit.count(imports) == 1
    visit = visit.replace(imports, "  let cpuBeforeImports ← processCpuNanos\n" + imports +
                          "  let cpuAfterImports ← processCpuNanos\n")
    tail = "  maybeCheckpoint s\n"
    assert visit.count(tail) == 1
    visit = visit.replace(tail, """  let cpuEnd ← processCpuNanos
  let exclusive := (cpuBeforeImports - cpuBegin) + (cpuEnd - cpuAfterImports)
  event [("event", toJson "module_cpu"), ("module", toJson mod.toString),
    ("exclusive_process_cpu_ns", toJson exclusive)]
""" + tail)
    (A / "CheckpointAuditCpu.lean").write_text(first + "partial def visit " + visit)
    shutil.copy2(D / "process-cpu-clock.c", A / "process-cpu-clock.c")
    print(A)
if __name__ == "__main__":
    main()
