#!/usr/bin/env python3
"""One native memory-option comparison, inside an already acquired P-core lock."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import threading
import time


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def run(point, index, arm, wall_limit=None):
    assert os.sched_getaffinity(0) == set(range(8))
    plan = json.loads((point / "plan.json").read_text())
    case = dict(plan["cases"][index])
    if wall_limit is not None:
        case["self_wall_s"] = min(case["self_wall_s"], wall_limit)
    out = point / "runs" / (str(index).zfill(2) + "-" + arm)
    out.mkdir(parents=True, exist_ok=False)
    source = Path(case["args"][-1])
    assert source.read_bytes() == Path(case["pinned_source"]).read_bytes()
    # Both arms use identical output paths, snapshotted only after retirement.
    common = point / "working" / str(index).zfill(2)
    common.mkdir(parents=True, exist_ok=True)
    for item in common.iterdir():
        assert item.is_file()
        item.unlink()
    args = list(case["args"])
    for flag in ["-o", "-i", "-c"]:
        if flag in args:
            k = args.index(flag) + 1
            args[k] = str(common / Path(args[k]).name)
    if arm == "noM":
        args = [x for x in args if not x.startswith("-M")]
    assert sum(x.startswith("-M") for x in args) == (arm == "M")
    env = os.environ.copy()
    for key in ["GLIBC_TUNABLES", "LD_PRELOAD", "LEAN_NUM_THREADS"]:
        env.pop(key, None)
    env.update(case["env"])
    current = Path("/sys/fs/cgroup") / Path("/proc/self/cgroup").read_text().strip().split("::", 1)[1].lstrip("/")
    assert current.name.startswith("cri-containerd-") and "pod" in current.parent.name
    cg = current.parent / ("proofserve-W-memory-pair-" + str(os.getpid()) + ".scope")
    cg.mkdir()
    (cg / "memory.max").write_text(str(15 * 1024**3))
    settings = {name: (cg / name).read_text().strip()
                for name in ["memory.max", "memory.high", "memory.swap.max", "memory.oom.group"]}
    dump(out / "command.json", dict(args=args, env=case["env"],
         source=str(source), source_exact=True, cwd=case["cwd"],
         native_cgroup=str(cg), cgroup_settings=settings,
         self_wall_s=case["self_wall_s"], pcore_lock=True,
         affinity=sorted(os.sched_getaffinity(0))))
    sample_stop = threading.Event()
    child = None
    thread = None
    def terminate(signum, frame):
        raise InterruptedError("outer controller signal " + str(signum))
    signal.signal(signal.SIGTERM, terminate)
    samples = []
    try:
        def before_exec():
            (cg / "cgroup.procs").write_text(str(os.getpid()))
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            signal.setitimer(signal.ITIMER_REAL, case["self_wall_s"])

        with (out / "native.log").open("w") as log:
            start = time.monotonic()
            child = subprocess.Popen(args, cwd=case["cwd"], env=env,
                  stdout=log, stderr=subprocess.STDOUT, preexec_fn=before_exec)
            birth = Path("/proc", str(child.pid), "stat").read_text().rsplit(")", 1)[1].split()[19]
            dump(out / "native-identity.json", dict(pid=child.pid, birth_ticks=birth))

            def sample():
                with (out / "memory.jsonl").open("w") as mem:
                    while not sample_stop.is_set():
                        row = dict(elapsed_s=time.monotonic() - start,
                           cgroup_memory_current=int((cg / "memory.current").read_text()))
                        try:
                            st = Path("/proc", str(child.pid), "stat").read_text().rsplit(")", 1)[1].split()
                            row.update(birth_ticks=st[19], native_rss_bytes=int(st[21]) * os.sysconf("SC_PAGE_SIZE"))
                        except FileNotFoundError:
                            pass
                        row["controller_rss_bytes"] = int(Path("/proc/self/stat").read_text().rsplit(")", 1)[1].split()[21]) * os.sysconf("SC_PAGE_SIZE")
                        if row.get("native_rss_bytes", 0) + row["controller_rss_bytes"] > 16 * 1024**3:
                            row["rss_watchdog_kill"] = True
                            (cg / "cgroup.kill").write_text("1")
                        samples.append(row)
                        mem.write(json.dumps(row) + "\n")
                        mem.flush()
                        sample_stop.wait(1)
            thread = threading.Thread(target=sample)
            thread.start()
            _, status, usage = os.wait4(child.pid, 0)
            end = time.monotonic()
            child.returncode = os.waitstatus_to_exitcode(status)
            sample_stop.set()
            thread.join()
        raw = (out / "native.log").read_text(errors="replace")
        events = (cg / "memory.events").read_text()
        rc = child.returncode
        artifacts = list(common.iterdir())
        expected = [Path(args[args.index(flag) + 1]) for flag in ["-o", "-i", "-c"] if flag in args]
        classification = ("rss_watchdog_failure" if any(x.get("rss_watchdog_kill") for x in samples)
            else "cgroup_memory_failure" if int(dict(x.split() for x in events.splitlines())["oom_kill"])
            else "wall_budget_exceeded" if rc == -signal.SIGALRM
            else "native_process_failure" if rc < 0 or "INTERNAL PANIC" in raw
            else "compile_with_sorry" if rc == 0 and "declaration uses 'sorry'" in raw
            else "compile_ok" if rc == 0 and all(x.exists() for x in expected)
            else "missing_artifact" if rc == 0
            else "native_memory_failure" if any(x in raw.lower() for x in ["memory_exception", "excessive memory", "bad_alloc", "out of memory"])
            else "budget_exceeded" if any(x in raw.lower() for x in ["heartbeats", "deterministic timeout", "maximum recursion depth"])
            else "lean_error")
        (out / "artifacts").mkdir()
        for path in artifacts:
            shutil.copyfile(path, out / "artifacts" / path.name)
        result = dict(module=case["module"], stratum=case["stratum"], index=index,
            arm=arm, actual_self_wall_s=case["self_wall_s"], source_exact=True, status=classification, returncode=rc,
            wall_s=end-start, user_cpu_s=usage.ru_utime, system_cpu_s=usage.ru_stime,
            peak_rss_kib=usage.ru_maxrss, minor_faults=usage.ru_minflt, major_faults=usage.ru_majflt,
            voluntary_switches=usage.ru_nvcsw, involuntary_switches=usage.ru_nivcsw,
            pid=child.pid, birth_ticks=birth, cgroup_memory_events=events,
            cgroup_memory_peak_bytes=int((cg / "memory.peak").read_text()),
            sampled_native_rss_peak_bytes=max((x.get("native_rss_bytes", 0) for x in samples), default=0),
            artifact_bytes={p.name:p.stat().st_size for p in artifacts},
            native_retired=not Path("/proc", str(child.pid)).exists(),
            cgroup_retired=not (cg / "cgroup.procs").read_text().strip(),
            raw=str(out), args=args)
        dump(out / "result.json", result)
        print(json.dumps(result), flush=True)
        return 0
    finally:
        sample_stop.set()
        if thread is not None:
            thread.join()
        stop_reason = None
        if (cg / "cgroup.procs").read_text().strip():
            (cg / "cgroup.kill").write_text("1")
            for _ in range(100):
                if not (cg / "cgroup.procs").read_text().strip():
                    break
                time.sleep(.05)
            stop_reason = "native cgroup required cleanup"
        if child is not None and child.returncode is None:
            child.wait(timeout=5)
        if not (cg / "cgroup.procs").read_text().strip():
            cg.rmdir()
        else:
            stop_reason = "native cgroup not retired"
        dump(out / "cleanup.json", dict(cgroup_removed=not cg.exists(), stop_reason=stop_reason))
        if stop_reason:
            raise RuntimeError(stop_reason)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--point", type=Path, required=True)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--arm", choices=["M", "noM"], required=True)
    parser.add_argument("--wall-limit", type=float)
    args = parser.parse_args()
    if args.arm == "M":
        parser.error("current user policy forbids -M; historical frozen captures are methodology only")
    raise SystemExit(run(args.point, args.index, args.arm, args.wall_limit))
