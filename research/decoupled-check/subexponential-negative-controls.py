#!/usr/bin/env python3
"""Six untimed E-core native rejections; independent of complete reference parity."""
from pathlib import Path
import datetime
import importlib.util
import json
import os
import threading

A = Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103")
B = A / "correctness-cpu89-20261104"
C = A / "negative-controls-cpu89-20261104"
F = A.parent / "scale-study/falconer-project-20261101"


def atomic(path, value):
    temp = path.with_name(path.name + ".write-" + str(os.getpid()))
    temp.write_text(json.dumps(value, indent=2) + "\n")
    temp.replace(path)


def main():
    assert sorted(os.sched_getaffinity(0)) == [8, 9]
    claim = C / "controller.json"
    C.mkdir(exist_ok=True)
    with claim.open("x") as out:
        json.dump(dict(pid=os.getpid(),
                       birth=Path("/proc/self/stat").read_text().split(") ")[1].split()[19],
                       affinity=[8, 9], measured=False), out)
    old_proc = Path("/proc/235183/stat")
    assert not old_proc.exists() or old_proc.read_text().split(") ")[1].split()[19] != "4693501"
    failure = json.loads((B / "failure.json").read_text())
    assert failure["resource_observation"]["rss_budget_stop"]
    frame = json.loads((A / "frame.json").read_text())
    state = json.loads((A / "state.json").read_text())
    expected = {v["module"] for v in frame}
    assert len(expected) == 14721 and set(state["stream_ids"]) == expected
    plan = json.loads((B / "negative-control-plan.json").read_text())
    prefix = set()
    for line in (A / "ledger.jsonl").open():
        row = json.loads(line)
        if row["operation"] != "stream":
            continue
        assert row["valid"]
        prefix.update(row["accepted"])
        if row["snapshot"] == plan["certified_predecessor"]:
            break
    else:
        raise AssertionError("certified predecessor missing")
    assert len(prefix) == plan["certified_prefix_modules"] == 10500
    assert len(plan["roots"]) == 3 and not prefix.intersection(plan["roots"])

    spec = importlib.util.spec_from_file_location("native", F / "native_project.py")
    n = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(n)
    n.ROOT = C
    stop = threading.Event()
    resources = dict(peak_tree_rss=0, rss_budget_stop=False,
                     scope="this control invocation; health sample, no CPU/wall metric")
    def watch():
        while not stop.wait(1):
            active = n.ACTIVE
            if active is None:
                continue
            cg, _ = active
            try:
                pids = (cg / "cgroup.procs").read_text().split()
            except OSError:
                continue
            rss = 0
            for pid in pids + [str(os.getpid())]:
                try:
                    rss += int(Path("/proc", pid, "stat").read_text().split(") ")[1].split()[21]) * os.sysconf("SC_PAGE_SIZE")
                except (OSError, ValueError, IndexError):
                    pass
            resources["peak_tree_rss"] = max(resources["peak_tree_rss"], rss)
            if rss > 12 * 1024**3:
                resources["rss_budget_stop"] = True
                try:
                    (cg / "cgroup.kill").write_text("1")
                except OSError:
                    pass
    thread = threading.Thread(target=watch)
    thread.start()
    controls = []
    try:
        for i, module in enumerate(plan["roots"]):
            for mode in ("one", "audit"):
                env = n.environment()
                env["LEAN_PATH"] = str(A) + ":" + str(A / "check-lib")
                for key in ("DECOUPLED_TIMING", "DECOUPLED_CHECKPOINT_INPUT",
                            "DECOUPLED_CHECKPOINT_OUTPUT", "DECOUPLED_CHECKPOINT_MODULE",
                            "DECOUPLED_SEGMENT_MODULES", "DECOUPLED_MUTATE_MODULE"):
                    env.pop(key, None)
                env["DECOUPLED_MUTATE_MODULE"] = module
                binary = F.parent / "measurement-v1/audited-stream"
                if mode == "audit":
                    binary = A / "checkpoint-audit"
                    env["DECOUPLED_CHECKPOINT_INPUT"] = plan["certified_predecessor"]
                key = f"negative-{i}-{mode}"
                cell = n.run(key, [binary, mode, "bvar", module], 120, False, env=env)
                events = [json.loads(line) for line in (C / (key + ".stdout")).read_text().splitlines()
                          if line.startswith("{")]
                valid = (cell["returncode"] == 1 and not resources["rss_budget_stop"]
                         and any(v.get("event") == "reject" and v.get("module") == module
                                 and "loose bound variables" in v.get("error", "") for v in events)
                         and not any(v.get("event") == "accept" and v.get("module") == module for v in events))
                item = dict(module=module, mode=mode, mutation="bvar", cell=cell,
                            events=events, valid=valid, measured=False,
                            performance_eligible=False, resource_observation=dict(resources))
                atomic(C / (key + ".json"), item)
                controls.append(item)
                assert valid, ("native rejection not established", key)
        result = dict(review="自审", complete=True, malformed_theorem_bodies=3,
                      native_rejections=6, mutation_classes=1, measured=False,
                      affinity=[8, 9], pcore_lease=False, controls=controls,
                      full_reference_parity=False, reference_resource_failure_retained=True,
                      resource_observation=resources)
        atomic(C / "terminal.json", result)
        print(json.dumps(dict(complete=True, native_rejections=6,
                              full_reference_parity=False)), flush=True)
    except BaseException as error:
        atomic(C / "failure.json", dict(error=repr(error),
               completed_valid_controls=sum(v["valid"] for v in controls),
               resources=resources, performance_eligible=False))
        raise
    finally:
        stop.set()
        thread.join()


if __name__ == "__main__":
    main()
