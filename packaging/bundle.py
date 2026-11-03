#!/usr/bin/env python3
"""Assemble the unpublished Linux bundle from already-built release components."""
import argparse, json, os, platform, shutil, subprocess, tarfile, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def link_or_copy(source, target):
    try:
        return os.link(source, target)
    except OSError:
        return shutil.copy2(source, target)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rust-bin", type=Path, required=True)
    p.add_argument("--checker-bin", type=Path, required=True)
    p.add_argument("--lean-sysroot", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if (platform.system(), platform.machine()) != ("Linux", "x86_64"):
        p.error("this release recipe supports Linux x86_64 only")
    for f in [a.rust_bin, a.checker_bin, a.lean_sysroot / "bin/lean", a.lean_sysroot / "bin/lake"]:
        if not f.is_file():
            p.error(f"missing built component: {f}")
    version = tomllib.loads((ROOT / "Cargo.toml").read_text())["workspace"]["package"]["version"]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    name = f"proofserve-{version}-linux-x86_64"
    a.out.mkdir(parents=True, exist_ok=True)
    tree = a.out / name
    if tree.exists():
        p.error(f"output already exists; retain it and choose another --out: {tree}")
    # Reuse SDK files on the build filesystem; the tar is standalone, with no
    # symlink to the SDK or Workspace. Preserve upstream SDK licensing files.
    shutil.copytree(a.lean_sysroot, tree, symlinks=True, copy_function=link_or_copy)
    (tree / "libexec").mkdir(exist_ok=True)
    share = tree / "share/proofserve"
    share.mkdir(parents=True, exist_ok=True)
    for source, target in [
        (a.rust_bin, tree / "bin/proofserve"),
        (a.checker_bin, tree / "libexec/proofserve-check"),
        (ROOT / "packaging/proofserve-check", tree / "bin/proofserve-check"),
        (ROOT / "packaging/proofserve-audit", tree / "bin/proofserve-audit"),
        (ROOT / "tools/audit/audit.py", tree / "libexec/proofserve-audit.py"),
        (ROOT / "checker/lean-toolchain", share / "lean-toolchain"),
        (ROOT / "LICENSE", share / "LICENSE"),
        (ROOT / "packaging/install.py", share / "install.py"),
        (ROOT / "packaging/README.md", share / "README.md"),
        (ROOT / "checker/docs/receipt-schema.md", share / "receipt-schema.md"),
    ]:
        shutil.copy2(source, target)
    for target in [tree / "bin/proofserve", tree / "bin/proofserve-check", tree / "bin/proofserve-audit", tree / "libexec/proofserve-check"]:
        target.chmod(0o755)
    metadata = dict(version=version, source_commit=commit, platform="linux-x86_64",
        lean_toolchain=(share / "lean-toolchain").read_text().strip(),
        python_requirement="3.11+",
        input="compiled Lake project; no source checkout or build-host paths required")
    (share / "bundle.json").write_text(json.dumps(metadata, indent=2) + "\n")
    archive = a.out / (name + ".tar.gz")
    with tarfile.open(archive, "w:gz", compresslevel=5) as tf:
        tf.add(tree, arcname=name)
    print(json.dumps(dict(archive=str(archive), bytes=archive.stat().st_size, metadata=metadata)))

if __name__ == "__main__":
    main()
