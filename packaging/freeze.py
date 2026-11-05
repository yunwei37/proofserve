#!/usr/bin/env python3
"""Rebuild and qualify unpublished packages. Preview never takes the P-core lock."""
import argparse
import csv
import signal
import fcntl
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import time

ROOT = Path(__file__).resolve().parents[1]


def export_external_results(out, manifest, destination, preview):
    """Export small receipts and cost rows; never turn interrupted CPU into zero."""
    destination.mkdir(parents=True, exist_ok=True)
    stage = "preview" if preview else "final"
    cases, measurements = [], []
    for index, item in enumerate(manifest["projects"]):
        value = json.loads((out / f"external-{index}" / "result.json").read_text())
        assert value["complete"] and value["local_root_acceptance_equal"]
        assert value["final_system_timing_eligible"] == (not preview)
        audit = value["audit"]
        native_receipt = json.loads((out / f"external-{index}" / "checkpoint/receipt.json").read_text())
        policy = native_receipt.get("theorem_body_policy")
        checkpoint_abi = native_receipt.get("checker_checkpoint_abi")
        coverage = audit["coverage"]
        cases.append(dict(
            project=value["project"], upstream_commit=value["upstream_commit"],
            ai_generated=item.get("ai_generated"),
            checker_commit=value["checker_commit"],
            theorem_body_policy=policy, checker_checkpoint_abi=checkpoint_abi,
            bundle_commit=value["bundle"]["source_commit"],
            bundle_dirty_preview=value["bundle"].get("source_worktree_dirty", False),
            source_modules=audit["source_modules"], local_roots=len(value["roots"]),
            native_closure_modules=value["native_closure_modules"],
            official_default_modules=value["official_default_modules"],
            common_local_root_acceptance_equal=value["local_root_acceptance_equal"],
            timing_scope_equal=False, final_system_timing_eligible=not preview,
            resumed_preview=value.get("resumed_preview", False),
            complete_native_cost_available=value.get("complete_native_cost_available", True),
            declared_closure_axioms=audit.get("compiled_evidence", {}).get("axioms"),
            source_binding=audit.get("compiled_evidence", {}).get("source_binding"),
            static_covered=len(coverage["covered_modules"]),
            static_omitted=len(coverage["omitted_modules"]),
            roots=value["roots"], scope_note=value["scope_note"]))
        for row in value["measurements"]:
            cell = {k: v for k, v in row.items() if k != "memory_events"}
            cell.update(native_theorem_body_policy=policy,
                        native_checker_checkpoint_abi=checkpoint_abi,
                        source_modules=audit["source_modules"],
                        ai_generated=item.get("ai_generated"),
                        native_closure_modules=value["native_closure_modules"],
                        official_default_modules=value["official_default_modules"],
                        common_local_root_acceptance_equal=value["local_root_acceptance_equal"],
                        static_covered=len(coverage["covered_modules"]),
                        static_omitted=len(coverage["omitted_modules"]),
                        cpu_accounting_valid=row.get("cpu_accounting_valid", row["returncode"] == 0))
            measurements.append(cell)
    report = dict(review="自审", timing_stage=stage, projects=cases,
                  final_system_timing_eligible=not preview,
                  scope="Native complete closure vs official default common local roots; no equal-obligation speedup.")
    acceptance = destination / f"freeze-{stage}-acceptance.json"
    acceptance.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    costs = destination / f"freeze-{stage}-measurements.csv"
    with costs.open("w", newline="") as stream:
        columns = list(dict.fromkeys(k for row in measurements for k in row))
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(measurements)
    return dict(acceptance=str(acceptance), measurements=str(costs))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--lean-sysroot", type=Path, required=True)
    parser.add_argument("--checker-commit", default="HEAD")
    parser.add_argument("--results-dir", type=Path, default=ROOT / "data/external-projects", help="Small CSV and acceptance summary destination")
    parser.add_argument("--manifest", type=Path, required=True,
                        help="JSON projects: name, project, source_audit, upstream_commit")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview", action="store_true")
    mode.add_argument("--final", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Continue this same interrupted preview; never final timing")
    parser.add_argument("--prepared-from", type=Path,
                        help="Final external run: use this completed preview's frozen checker/SDK; rebuild and install a fresh archive, skip already-qualified container/contract work")

    parser.add_argument("--lock", type=Path, help="Shared P-core lock; required for final timing")
    args = parser.parse_args()
    started = time.monotonic()
    if args.prepared_from and not args.final:
        parser.error("--prepared-from is only for the final external timing window")

    if args.final and args.lock is None:
        parser.error("--final requires the existing shared --lock; run only after census")
    os.sched_setaffinity(0, {8, 9})
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=args.resume)
    assert not args.resume or args.preview, "only a preview may resume"
    previous = json.loads((out / "freeze.json").read_text()) if args.resume else None
    source = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    checker = subprocess.check_output(["git", "rev-parse", args.checker_commit],
                                      cwd=ROOT, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--", "crates",
             "Cargo.toml", "Cargo.lock", "packaging", "Dockerfile", "tools/audit", "checker"],
             cwd=ROOT, text=True).splitlines()
    if args.final and dirty:
        raise SystemExit("Final freeze needs committed runtime inputs; unrelated docs/data may stay dirty")
    manifest = json.loads(args.manifest.read_text())
    prepared = None
    if args.prepared_from:
        prepared = json.loads((args.prepared_from / "freeze.json").read_text())
        if not prepared.get("complete") or not prepared.get("preview") or prepared["checker_commit"] != checker:
            raise SystemExit("Need a completed preview at the identical frozen checker commit")
        if prepared.get("projects") != manifest["projects"]:
            raise SystemExit("Final manifest must preserve the qualified project inputs and options")

    if previous:
        assert previous["checker_commit"] == checker
        # Shared writers may advance documentation/data commits during a preview.
        # Never reuse a stage across a committed runtime change.
        subprocess.run(["git", "diff", "--exit-code", previous["source_commit"],
             source, "--", "crates", "Cargo.toml", "Cargo.lock", "tools/audit",
             "clients/python", "packaging/proofserve-check", "packaging/proofserve-audit",
             "Dockerfile"], cwd=ROOT, check=True, stdout=subprocess.PIPE)
        source = previous["source_commit"]
        retained = out / ("freeze-before-resume-" + str(os.getpid()) + ".json")
        retained.write_text(json.dumps(previous, indent=2) + "\n")
    records = list(previous["commands"]) if previous else []
    result = dict(complete=False, preview=args.preview, final_system_timing_eligible=args.final,
                  source_commit=source, checker_commit=checker, dirty_runtime_paths=dirty, resumed_preview=args.resume,
                  commands=records, publishes=False, preparation_affinity=[8, 9], projects=manifest["projects"],
                  prepared_from=str(args.prepared_from.resolve()) if args.prepared_from else None)
    def save():
        (out / "freeze.json").write_text(json.dumps(result, indent=2) + "\n")
    def run(label, command, cwd=ROOT, env=None, limit=3600, reuse=True):
        if args.prepared_from:
            remaining = 7200 - int(time.monotonic() - started)
            if remaining <= 0:
                raise RuntimeError("Final external two-hour window exhausted")
            limit = min(limit, remaining)
        prior = [v for v in records if v["label"] == label]
        if reuse and args.resume and prior and prior[-1]["returncode"] == 0:
            return
        logfile = label + (("-retry-" + str(len(prior))) if prior else "") + ".log"
        with (out / logfile).open("x") as log:
            p = subprocess.Popen(list(map(str, command)), cwd=cwd, env=env,
                                 stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                p.wait(timeout=limit)
            except subprocess.TimeoutExpired:
                # Stop only this command's process group, including its children.
                # In particular, let the evaluator retire its own native cgroup.
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    p.wait()
                p.returncode = 124
        records.append(dict(label=label, command=list(map(str, command)), returncode=p.returncode, log=logfile))
        save()
        if p.returncode:
            raise RuntimeError(f"{label}: exit{p.returncode}; see retained log")
    env = os.environ.copy()
    env.update(PATH=str(args.lean_sysroot / "bin") + os.pathsep + env.get("PATH", ""),
               LEAN_SYSROOT=str(args.lean_sysroot), LEAN_NUM_THREADS="1", CARGO_BUILD_JOBS="1")
    (out / "tmp").mkdir(exist_ok=args.resume)
    # AF_UNIX sockets have a short pathname limit. Keep test data on the output
    # filesystem, but expose a short alias; raw results still live under --out.
    short_tmp = None
    for parent in out.parents:
        candidate = parent / ("pst-" + str(os.getpid()))
        if len(str(candidate).encode()) < 35 and parent.stat().st_dev == out.stat().st_dev:
            try:
                candidate.symlink_to(out / "tmp", target_is_directory=True)
                short_tmp = candidate
                break
            except OSError:
                continue
    if short_tmp is None:
        raise SystemExit("Need a writable short path on the output filesystem for Unix socket tests")
    env["TMPDIR"] = str(short_tmp)
    save()
    builder = None
    try:
        if args.prepared_from:
            checker_src = args.prepared_from.resolve() / "checker-source"
            frozen = subprocess.check_output(["git", "archive", checker, "checker"], cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(frozen)) as archived:
                for member in archived:
                    if member.isfile():
                        expected = archived.extractfile(member).read()
                        if (checker_src / member.name).read_bytes() != expected:
                            raise RuntimeError("Prepared frozen checker source changed: " + member.name)
            if not (checker_src / "checker/.lake/build/bin/proofserve-check").is_file():
                raise RuntimeError("Prepared checker executable is missing")
            run("rust-release", ["cargo", "build", "--release", "--locked", "-p", "proofserve"], env=env)
        else:
            run("rust-format", ["cargo", "fmt", "--all", "--", "--check"], env=env)
            run("rust-contracts", ["cargo", "test", "--workspace", "--all-targets", "--locked"], env=env)
            run("rust-clippy", ["cargo", "clippy", "--workspace", "--all-targets", "--locked", "--", "-D", "warnings"], env=env)
            publish = ["cargo", "publish", "--workspace", "--dry-run", "--locked"]
            if args.preview:
                publish.append("--allow-dirty")
            run("cargo-dry-run", publish, env=env)
            run("rust-release", ["cargo", "build", "--release", "--locked", "-p", "proofserve"], env=env)
            checker_src = out / "checker-source"
            checker_src.mkdir(exist_ok=args.resume)
            data = subprocess.check_output(["git", "archive", checker, "checker"], cwd=ROOT)
            if not args.resume:
                with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                    archive.extractall(checker_src, filter="data")
            run("checker-build", ["lake", "build"], cwd=checker_src / "checker", env=env)
            run("checker-contract", ["python3", "tests/contract.py"], cwd=checker_src / "checker", env=env)
            run("audit-contract", ["python3", ROOT / "tools/audit/test_audit.py"], env=env)
        target = Path(env.get("CARGO_TARGET_DIR", ROOT / "target"))
        run("assemble", ["python3", ROOT / "packaging/bundle.py", "--rust-bin",
             target / "release/proofserve", "--checker-bin",
             checker_src / "checker/.lake/build/bin/proofserve-check", "--source-commit", source, "--checker-source",
             checker_src / "checker", "--checker-commit", checker,
             "--lean-sysroot", args.lean_sysroot, "--out", out / "prepared"], env=env)
        bundle_archive = next((out / "prepared").glob("*.tar.gz"))
        run("install", ["python3", ROOT / "packaging/install.py", "--archive", bundle_archive,
             "--prefix", out / "installed"], env=env)
        run("stranger-bundle", ["python3", ROOT / "packaging/qualify_bundle.py",
             "--prefix", out / "installed", "--out", out / "bundle-qualification"], env=env)
        for index, item in enumerate(manifest["projects"]):
            cmd = ["python3", ROOT / "data/external-projects/evaluate.py",
                   "--name", item["name"], "--project", item["project"],
                   "--source-audit", item["source_audit"], "--upstream-commit",
                   item["upstream_commit"], "--checker-commit", checker, "--prefix",
                   out / "installed", "--out", out / f"external-{index}", "--workers", str(item.get("workers", 1))]
            if args.final:
                cmd += ["--timeout-seconds", str(max(1, 7200 - int(time.monotonic() - started)))]
            if args.preview:
                cmd.append("--preview")
                if args.resume and (out / f"external-{index}").exists():
                    cmd.append("--resume")
            if item.get("closure_roots"):
                cmd += ["--closure-roots", str(item["closure_roots"])]
            if args.final:
                # Lock only timed cells; preparations remain on E cores.
                with args.lock.open("a") as lock:
                    while True:
                        if time.monotonic() - started >= 7200:
                            raise RuntimeError("Final external window exhausted waiting for the P-core lock")
                        try:
                            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                            break
                        except BlockingIOError:
                            time.sleep(1)
                    remaining = 7200 - int(time.monotonic() - started)
                    if remaining <= 0:
                        raise RuntimeError("Final external two-hour window exhausted; retained partial result is not complete")
                    run(f"external-{index}", ["taskset", "-c", "0-7"] + cmd, env=env, limit=remaining)
            else:
                run(f"external-{index}", cmd, env=env, limit=7200)
        if not args.prepared_from:
            context = out / "image-source"
            context.mkdir(exist_ok=args.resume)
            members = ["Dockerfile", ".dockerignore", "Cargo.toml", "Cargo.lock", "crates",
                       "checker", "clients", "packaging", "tools/audit", "LICENSE", "README.md"]
            data = subprocess.check_output(["git", "archive", source, *members], cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                archive.extractall(context, filter="data")
            if args.preview:
                # O's pending changes only; never copy M's live checker source/build.
                for name in ["crates", "packaging"]:
                    shutil.copytree(ROOT / name, context / name, dirs_exist_ok=True,
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                shutil.copy2(ROOT / "Dockerfile", context / "Dockerfile")
            shutil.copytree(checker_src / "checker", context / "checker", dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".lake"))
            builder = "proofserve-freeze-" + str(os.getpid())
            run("container-builder", ["docker", "buildx", "create", "--name", builder,
                 "--driver", "docker-container", "--driver-opt", "network=host",
                 "--driver-opt", "memory=10g", "--driver-opt", "cpuset-cpus=8-9"], env=env, reuse=False)
            prior_builds = [v for v in records if v["label"] == "container-build"]
            old_command = prior_builds[-1]["command"] if prior_builds else []
            tag = (previous or {}).get("image_tag") or (
                old_command[old_command.index("--tag") + 1] if "--tag" in old_command
                else "proofserve:freeze-" + str(os.getpid()))
            result["image_tag"] = tag
            save()
            run("container-build", ["docker", "buildx", "build", "--builder", builder,
                 "--network", "host", "--load", "--metadata-file", out / "image-metadata.json",
                 "--tag", tag, context], env=env, limit=7200)
            run("stranger-container", ["docker", "run", "--rm", "--network", "none",
                 "--cpuset-cpus", "8-9", "--memory", "11g", "--entrypoint", "python3",
                 tag, "/opt/container_smoke.py", "--self-test"], env=env, limit=1200)
        result.update(archive=str(bundle_archive), external_exports=export_external_results(
            out, manifest, args.results_dir, args.preview))
        save()
    except BaseException as error:
        result["error"] = repr(error)
        save()
        raise
    finally:
        if short_tmp is not None and short_tmp.is_symlink():
            short_tmp.unlink()
        if builder:
            try:
                p = subprocess.run(["docker", "buildx", "rm", builder], env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
            except subprocess.TimeoutExpired as error:
                result.update(complete=False, builder_cleanup_error=repr(error))
                save()
                raise
            (out / "builder-cleanup.log").write_bytes(p.stdout)
            result["builder_cleanup_exit"] = p.returncode
            if p.returncode:
                result.update(complete=False, builder_cleanup_error="temporary container builder cleanup failed")
                save()
                raise RuntimeError(result["builder_cleanup_error"])
            save()
    result["complete"] = True
    save()
    print(json.dumps(dict(complete=True, preview=args.preview, source_commit=source)))


if __name__ == "__main__":
    main()
