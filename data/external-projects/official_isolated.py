#!/usr/bin/env python3
"""Finish official common-root parity after the retained batch resource stop."""
from pathlib import Path
import argparse, csv, json, os, shutil, signal, subprocess, threading, time
ACTIVE = None
def abort(signum, frame):
    if ACTIVE is not None:
        try: (ACTIVE / "cgroup.kill").write_text("1")
        except OSError: pass
    raise SystemExit(128 + signum)
signal.signal(signal.SIGTERM, abort)
signal.signal(signal.SIGINT, abort)

def main():
    global ACTIVE
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", type=Path, required=True)
    p.add_argument("--prefix", type=Path, required=True)
    p.add_argument("--original", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    assert sorted(os.sched_getaffinity(0)) == list(range(8))
    old = json.loads((a.original / "result.json").read_text())
    assert old["project"] == "CrocSwap/integer-mult-bounds"
    assert old["measurements"][1]["resource_failure"]
    assert old["measurements"][0]["returncode"] == 0
    sdk = (a.prefix / "bin/proofserve").resolve(strict=True).parents[1]
    env = os.environ.copy()
    env.update(PATH=str(sdk / "bin") + os.pathsep + env.get("PATH", ""), LEAN_SYSROOT=str(sdk))
    env.pop("LEAN_PATH", None)
    a.out.mkdir(exist_ok=True)
    rows, observed = [], set()
    for i, root in enumerate(old["roots"]):
        record = a.out / (str(i).zfill(3) + ".json")
        stdout = a.out / (str(i).zfill(3) + ".stdout")
        stderr = a.out / (str(i).zfill(3) + ".stderr")
        if record.exists():
            row = json.loads(record.read_text())
            assert row["root"] == root and row["returncode"] == 0
        else:
            assert shutil.disk_usage("/workspaces").used / shutil.disk_usage("/workspaces").total < .85
            current = Path("/sys/fs/cgroup") / Path("/proc/self/cgroup").read_text().strip().split("::")[1].lstrip("/")
            cg = current.parent / ("proofserve-o-isolated-" + str(os.getpid()) + "-" + str(i) + ".scope")
            cg.mkdir()
            (cg / "memory.max").write_text(str(12 * 1024**3 - 256 * 1024**2))
            (cg / "memory.oom.group").write_text("1")
            def enter(): (cg / "cgroup.procs").write_text("0")
            with stdout.open("x") as fo, stderr.open("x") as fe:
                begin = time.monotonic()
                q = subprocess.Popen(["timeout", "--signal=TERM", "--kill-after=5", "180",
                    str(sdk / "bin/lake"), "env", str(sdk / "bin/leanchecker"), "-v", root],
                    cwd=a.project, env=env, stdout=fo, stderr=fe, preexec_fn=enter, start_new_session=True)
                ACTIVE = cg
                stop = threading.Event()
                sample = dict(peak_tree_rss=0, stop_reason=None)
                def watch():
                    while not stop.wait(1):
                        rss = 0
                        for pid in (cg / "cgroup.procs").read_text().split() + [str(os.getpid())]:
                            try: rss += int(Path("/proc", pid, "stat").read_text().split(") ")[1].split()[21]) * os.sysconf("SC_PAGE_SIZE")
                            except (OSError, ValueError, IndexError): pass
                        sample["peak_tree_rss"] = max(sample["peak_tree_rss"], rss)
                        if rss > 12 * 1024**3: sample["stop_reason"] = "RSS"
                        if shutil.disk_usage("/workspaces").used / shutil.disk_usage("/workspaces").total >= .85: sample["stop_reason"] = "disk"
                        if sample["stop_reason"]:
                            (cg / "cgroup.kill").write_text("1")
                            return
                monitor = threading.Thread(target=watch); monitor.start()
                _, status, usage = os.wait4(q.pid, 0)
                q.returncode = os.waitstatus_to_exitcode(status)
                wall = time.monotonic() - begin
                stop.set(); monitor.join(); ACTIVE = None
            row = dict(root=root, returncode=q.returncode, cpu_s=usage.ru_utime+usage.ru_stime,
                wall_s=wall, wait4_peak_rss_kib=usage.ru_maxrss,
                cgroup_peak_bytes=int((cg / "memory.peak").read_text()),
                memory_events=(cg / "memory.events").read_text(), **sample)
            record.write_text(json.dumps(row, indent=2) + "\n")
            try: cg.rmdir()
            except OSError: pass
        rows.append(row)
        actual = {line.removeprefix("replaying ").strip()
                  for line in stdout.read_text().splitlines() if line.startswith("replaying ")}
        assert row["returncode"] == 0 and actual == {root}, row
        observed |= actual
    assert observed == set(old["roots"])
    result = dict(complete=True, original_batch_failure_retained=str(a.original),
        project=old["project"], upstream_commit=old["upstream_commit"],
        bundle_commit=old["bundle"]["source_commit"], checker_commit=old["checker_commit"],
        arm="official-default-isolated", repeat=1, root_count=len(rows),
        local_root_acceptance_equal=True, accepted_roots=sorted(observed),
        cpu_s=sum(r["cpu_s"] for r in rows), wall_s=sum(r["wall_s"] for r in rows),
        wait4_peak_rss_kib=max(r["wait4_peak_rss_kib"] for r in rows),
        peak_tree_rss=max(r["peak_tree_rss"] for r in rows),
        cgroup_peak_bytes=max(r["cgroup_peak_bytes"] for r in rows),
        scope="One stock default leanchecker invocation per local root; trusts imports. All per-root startup/import costs charged. Not comparable with one batched invocation or native full-closure checking.")
    (a.out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
if __name__ == "__main__": main()
