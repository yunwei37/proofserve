#!/usr/bin/env python3
"""Prepare the next finite directory; no native task is launched here."""
import json, os, shutil, tarfile
from pathlib import Path
B = Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
A = B / "transonic-20261103"
O = B / "whole-library-20261102"
PIN = "4eaee87548250b2682affda7d05d947c05554bae"
def main():
    os.sched_setaffinity(0, {8})
    disk = shutil.disk_usage("/workspaces")
    assert disk.used / disk.total < .85, "PVC already at the user's 85% ceiling"
    A.mkdir(exist_ok=True)
    frame = json.loads((O / "frame.json").read_text())
    targets = [v for v in frame if v["cohort"] == "OAI.MathematicalPhysics.Transonic"]
    assert len(targets) == 466
    names = {v["module"] for v in targets}
    external = sorted({m for v in targets for m in v["imports"] if m not in names})
    assert not any(m.startswith("OAI.") for m in external)
    production = json.loads((B / "ramsey-20261102/prepare.json").read_text())["production_providers"]
    for m in external:
        assert any(Path(root).joinpath(*m.split(".")).with_suffix(".olean").is_file() for root in production), m
    wanted = {v["path"]: v["bytes"] for v in targets}
    archive = Path("/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz")
    done = set()
    with tarfile.open(archive, "r|gz", stream=True) as tar:
        for member in tar:
            path = member.name.partition("/")[2]
            if not member.isfile() or path not in wanted:
                continue
            assert member.size == wanted[path]
            dest = A / "sources" / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Repeated preparation never overwrites a prior raw input.
            if dest.exists():
                assert dest.stat().st_size == member.size
            else:
                with tar.extractfile(member) as inp, dest.open("xb") as out:
                    shutil.copyfileobj(inp, out)
            done.add(path)
    assert done == set(wanted)
    (A / "transonic-targets.json").write_text(json.dumps(targets, indent=2))
    (A / "external-roots.txt").write_text(chr(10).join(external) + chr(10))
    (A / "producer-ai").mkdir(exist_ok=True)
    summary = dict(source_pin=PIN, targets=466, extracted_files=len(done),
                   target_source_bytes=sum(wanted.values()), external_roots=len(external),
                   production_providers=production, timed=False, native_launched=False,
                   protected_core_namespaces=["Init", "Std", "Lean", "Lake"])
    (A / "prepare.json").write_text(json.dumps(summary, indent=2))
    # The dependency graph comes from retained original native headers.
    # No new Meta/runtime namespace is synthesized.
    import graphlib
    old_frame = json.loads((B / "ramsey-20261102/frame.json").read_text())
    by = {v["module"]: v for v in old_frame if not v["target"]}
    needed = set()
    def visit(m):
        if m in needed:
            return
        needed.add(m)
        for q in by[m]["imports"]:
            visit(q)
    for m in external:
        visit(m)
    nodes = {m: by[m] for m in needed}
    for v in targets:
        nodes[v["module"]] = dict(module=v["module"], imports=v["imports"],
            source=str(A / "sources" / v["path"]),
            source_root=str(A / "sources/lean"), target=True)
    order = list(graphlib.TopologicalSorter(
        {m: set(v["imports"]) for m, v in nodes.items()}).static_order())
    selected = [nodes[m] for m in order]
    reused = [m for m in order if m in needed]
    for m in reused:
        source = Path(by[m]["reused"]["artifact"]).with_suffix("")
        dest = A / "check-lib" / Path(*m.split("."))
        dest.parent.mkdir(parents=True, exist_ok=True)
        for suffix in [".olean", ".olean.server", ".olean.private", ".ir", ".ir.sig"]:
            src, dst = source.with_suffix(suffix), dest.with_suffix(suffix)
            if src.exists():
                if dst.exists():
                    assert os.path.samefile(src, dst)
                else:
                    os.link(src, dst)
    state = A / "state.json"
    assert not state.exists() or json.loads(state.read_text())["tasks"] == 0, "do not reprepare an active capture"
    (A / "frame.json").write_text(json.dumps(selected, indent=2))
    state.write_text(json.dumps(dict(phase="source", built=reused, stream_ids=[],
        oracle_ids=reused, snapshot=None, segments=0, tasks=0), indent=2))
    (A / "roots.txt").write_text(chr(10).join(v["module"] for v in targets) + chr(10))
    checker = A / "checkpoint-audit"
    if not checker.exists():
        os.link(B / "ramsey-20261102/checkpoint-audit", checker)
    receipt = dict(targets=466, dependencies=len(needed), closure_nodes=len(selected),
        reused_cpu_s=sum(v["reused"]["source_cpu_s"] for v in selected if "reused" in v),
        native_launched=False,
        frame_basis="original native dependency headers; pending native equality check",
        source_pin=PIN)
    (A / "frame-receipt.json").write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt, indent=2))
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
