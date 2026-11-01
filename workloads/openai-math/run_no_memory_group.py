#!/usr/bin/env python3
"""Finite no-M dependency replay; defer rather than join any P-core wait queue."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--point", type=Path, required=True)
    a = p.parse_args()
    os.sched_setaffinity(0, set(range(8, 16)))
    point = a.point
    plan = json.loads((point / "plan.json").read_text())
    ready = set(plan.get("initial_ready", []))
    rows = []
    start = time.monotonic()
    stop = None
    for index, case in enumerate(plan["cases"]):
        remaining = 1700 - (time.monotonic() - start)
        if remaining < 15:
            stop = "group allowance exhausted; remaining jobs not started"
            break
        assert not any(x.startswith("-M") for x in case["args"])
        blockers = sorted(set(case.get("deps", [])) - ready)
        if blockers:
            result = dict(module=case["module"], path=case["path"],
                status="dependency_not_compiled", native_invoked=False,
                blockers=blockers, probability_sample_target=case["role"] == "original_probability_sample")
        else:
            command = ["python3", "/workspaces/repository/workloads/openai-math/pcore_launch.py",
                "--", "python3", "-u", str(point/"runner.py"), "--point", str(point),
                "--index", str(index), "--arm", "noM", "--wall-limit", str(remaining-10)]
            with (point/(str(index).zfill(4)+"-launcher.log")).open("w") as log:
                child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
                (point/"current.json").write_text(json.dumps(dict(index=index,
                    module=case["module"], pid=child.pid,
                    birth_ticks=Path("/proc", str(child.pid), "stat").read_text().rsplit(")", 1)[1].split()[19],
                    utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    command=command))+"\n")
                code = child.wait()
            if code != 0:
                stop = "deferred without queue/retry" if code == 75 else "runner operational error "+str(code)
                break
            receipt = point/"runs"/(str(index).zfill(2)+"-noM")/"result.json"
            result = json.loads(receipt.read_text())
            if not result["native_retired"] or not result["cgroup_retired"]:
                stop = "native or cgroup not retired"
                break
            if result["status"] == "compile_ok":
                assert result.get("cache_published_after_native_retirement")
                ready.add(case["module"])
        rows.append(result)
        with (point/"results.jsonl").open("a") as f:
            f.write(json.dumps(result)+"\n")
    terminal = dict(rows=len(rows), planned_jobs=len(plan["cases"]),
        native_rows=sum(x.get("native_invoked", False) for x in rows),
        elapsed_s=time.monotonic()-start, stop=stop,
        statuses={s:sum(x["status"]==s for x in rows) for s in {x["status"] for x in rows}},
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        complete=len(rows)==len(plan["cases"]))
    (point/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n")
    print(json.dumps(terminal),flush=True)
    return 0 if terminal["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
