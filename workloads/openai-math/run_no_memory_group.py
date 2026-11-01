#!/usr/bin/env python3
"""Finite no-M replay: queue one stock flock command, release after each case."""
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
    native_wall = 0.
    start = time.monotonic()
    stop = None
    for index, case in enumerate(plan["cases"]):
        remaining = 1700 - native_wall
        if remaining < 15:
            stop = "native-work allowance exhausted; remaining jobs not started"
            break
        assert not any(x.startswith("-M") for x in case["args"])
        blockers = sorted(set(case.get("deps", [])) - ready)
        if blockers:
            result = dict(module=case["module"], path=case["path"],
                status="dependency_not_compiled", native_invoked=False,
                blockers=blockers, probability_sample_target=case["role"] == "original_probability_sample")
        else:
            command = ["flock", "/workspaces/.agent-state/gpu-smt-captures/pcore.lock",
                "taskset", "-c", "0-7", "python3", "-u", str(point/"runner.py"),
                "--point", str(point), "--index", str(index), "--arm", "noM",
                "--wall-limit", str(min(case["self_wall_s"], remaining-10))]
            submitted = time.monotonic()
            with (point/(str(index).zfill(4)+"-launcher.log")).open("w") as log:
                child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
                current=dict(index=index, module=case["module"], pid=child.pid,
                    birth_ticks=Path("/proc", str(child.pid), "stat").read_text().rsplit(")", 1)[1].split()[19],
                    utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    submitted_monotonic_s=submitted, command=command,
                    one_outstanding_W_request=True)
                (point/"current.json").write_text(json.dumps(current)+"\n")
                code = child.wait()
            if code != 0:
                stop = "runner operational error "+str(code)
                break
            receipt = point/"runs"/(str(index).zfill(2)+"-noM")/"result.json"
            result = json.loads(receipt.read_text())
            if not result["native_retired"] or not result["cgroup_retired"]:
                stop = "native or cgroup not retired"
                break
            result["probability_sample_target"] = case["role"] == "original_probability_sample"
            result["queue_plus_setup_cleanup_s"] = time.monotonic()-submitted-result["wall_s"]
            result["queue_scope"] = "not pure wait: includes interpreter/setup/snapshot/cleanup; excluded from native cost"
            native_wall += result["wall_s"]
            if result["status"] == "compile_ok":
                assert result.get("cache_published_after_native_retirement")
                ready.add(case["module"])
        rows.append(result)
        with (point/"results.jsonl").open("a") as f:
            f.write(json.dumps(result)+"\n")
    terminal = dict(rows=len(rows), planned_jobs=len(plan["cases"]),
        native_rows=sum(x.get("native_invoked", False) for x in rows),
        elapsed_including_queue_s=time.monotonic()-start, native_wall_sum_s=native_wall,
        stop=stop, native_allowance_s=1700, one_request_at_a_time=True,
        statuses={s:sum(x["status"]==s for x in rows) for s in {x["status"] for x in rows}},
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        complete=len(rows)==len(plan["cases"]))
    (point/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n")
    print(json.dumps(terminal),flush=True)
    return 0 if terminal["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
