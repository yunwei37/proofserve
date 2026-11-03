#!/usr/bin/env python3
"""Install an operator-published bundle, or a local unpublished qualification archive."""
import argparse, json, os, platform, shutil, tarfile, tempfile, urllib.request
from pathlib import Path

def install(archive, prefix):
    versions = prefix / "lib/proofserve/versions"
    versions.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".install-", dir=versions) as td:
        staging = Path(td)
        with tarfile.open(archive, "r:gz") as tf:
            tf.extractall(staging, filter="data")
        roots = list(staging.iterdir())
        if len(roots) != 1 or not roots[0].is_dir():
            raise ValueError("expected one ProofServe bundle directory")
        root = roots[0]
        metadata = json.loads((root / "share/proofserve/bundle.json").read_text())
        if metadata["platform"] != "linux-x86_64":
            raise ValueError("unsupported bundle platform")
        destination = versions / (metadata["version"] + "-" + metadata["source_commit"][:12])
        bin_dir = prefix / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        names = ["proofserve", "proofserve-check", "proofserve-audit"]
        for name in names:
            target = bin_dir / name
            if target.exists() or target.is_symlink():
                if not target.is_symlink() or not target.resolve().is_relative_to(versions.resolve()):
                    raise ValueError(f"refusing to replace an unrelated file: {target}; choose another --prefix")
        if destination.exists():
            old = json.loads((destination / "share/proofserve/bundle.json").read_text())
            if old != metadata:
                raise ValueError("existing version directory has different metadata")
        else:
            root.rename(destination)
        for name in names:
            target = bin_dir / name
            temporary = bin_dir / (name + ".install-" + str(os.getpid()))
            temporary.symlink_to(os.path.relpath(destination / "bin" / name, bin_dir))
            temporary.replace(target)
        print(f"Installed {metadata['version']} ({metadata['source_commit'][:12]}) into {prefix}")
        print(f"Run: {bin_dir / 'proofserve'} check /path/to/lake-project")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prefix", type=Path, default=Path.home() / ".local")
    p.add_argument("--archive", type=Path, help="local prepared bundle; no network fetch")
    p.add_argument("--version", default="latest", help="operator-published version, e.g. v0.1.0")
    a = p.parse_args()
    if (platform.system(), platform.machine()) != ("Linux", "x86_64"):
        p.error("native bundles currently support Linux x86_64; use the container on other hosts")
    if a.archive:
        install(a.archive.resolve(strict=True), a.prefix.resolve())
        return
    url = "https://api.github.com/repos/yunwei37/proofserve/releases/" + ("latest" if a.version == "latest" else "tags/" + a.version)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proofserve-installer"})) as response:
        release = json.load(response)
    name = f"proofserve-{release['tag_name'].removeprefix('v')}-linux-x86_64.tar.gz"
    asset = next((x for x in release["assets"] if x["name"] == name), None)
    if asset is None:
        p.error("this release has no matching Linux bundle; no source checkout was attempted")
    # Download/staging stays under the destination filesystem, not container /tmp.
    a.prefix.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".proofserve-download-", dir=a.prefix) as td:
        archive = Path(td) / name
        with urllib.request.urlopen(asset["browser_download_url"]) as source, archive.open("wb") as out:
            shutil.copyfileobj(source, out)
        install(archive, a.prefix.resolve())

if __name__ == "__main__":
    main()
