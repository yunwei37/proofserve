"""Qualify the pinned image and expose cold-load cost separately from batching."""
import atexit
import json
import os
import subprocess
import sys
import time
from urllib.request import urlopen

from proofserve import Client

if "--self-test" in sys.argv:
    env = os.environ.copy()
    env["RUST_LOG"] = "proofserve_engine::resources=info,proofserve_lean::prepared=info"
    # This bounded image test reserves 8 GiB inside a 10/11 GiB container;
    # the retained 5 GiB attempt preempted Mathlib at about 5.37 GiB RSS.
    server = subprocess.Popen(
        ["/bin/sh", "/usr/local/bin/start-proofserve", "serve",
         "--listen", "127.0.0.1:3000", "--memory-gib", "8"],
        env=env,
    )

    def retire():
        if server.poll() is None:
            server.terminate()
        try:
            server.wait(timeout=30)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()

    atexit.register(retire)
    url = "http://localhost:3000"
else:
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"

for attempt in range(60):
    try:
        with urlopen(url + "/health", timeout=2) as response:
            assert json.load(response)["status"] == "ok"
        break
    except OSError:
        time.sleep(1)
else:
    raise RuntimeError("container service did not become healthy")

client = Client(url, request_timeout=240)
observations = []


def check(phase, snippets, timeout):
    started = time.monotonic()
    result = client.check(snippets, timeout=timeout, reuse=False)
    observations.append({
        "phase": phase,
        "request_budget_seconds": timeout,
        "wall_seconds": time.monotonic() - started,
        "result": result,
    })
    print(json.dumps(observations[-1]), flush=True)
    assert [r["id"] for r in result["results"]] == [s["id"] for s in snippets], result
    return result["results"]


cold = check("first_mathlib", [{
    "id": "cold",
    "code": "import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num",
}], 180)
repeat = check("repeat_mathlib_different_source", [{
    "id": "repeat",
    "code": "import Mathlib\nexample : (2 : Nat) + 3 = 5 := by norm_num",
}], 180)
batch = check("small_native_batch", [
    {"id": "accepted", "code": "example : (2 : Nat) + 2 = 4 := by rfl"},
    {"id": "rejected", "code": "example : False := by decide"},
    {"id": "incomplete", "code": "example : False := by sorry"},
], 30)

rows = cold + repeat + batch
assert all(r["error"] is None and isinstance(r["response"], dict) for r in rows), observations
for row in cold + repeat + batch[:1]:
    native = row["response"]
    assert not any(m.get("severity") == "error" for m in native.get("messages", [])), row
    assert not native.get("sorries"), row
assert any(m.get("severity") == "error" for m in batch[1]["response"].get("messages", [])), batch[1]
assert batch[2]["response"].get("sorries"), batch[2]
print(json.dumps({"qualification": "passed", "observations": observations}), flush=True)


# Retire the fully qualified service before starting independent project controls.
if "--self-test" in sys.argv:
    retire()

# Installed-form project controls, distinct from the full-Mathlib service import.
if "--self-test" in sys.argv:
    from pathlib import Path
    import tempfile
    with tempfile.TemporaryDirectory(prefix="proofserve-image-", dir="/opt") as td:
        project = Path(td)
        (project / "lean-toolchain").write_text(Path("/opt/proofserve/share/proofserve/lean-toolchain").read_text())
        (project / "lakefile.toml").write_text('name = "containerQualification"\ndefaultTargets = ["Qualification"]\n[[lean_lib]]\nname = "Qualification"\n')
        (project / "Qualification.lean").write_text('prelude\nimport Init.Prelude\ntheorem container_roundtrip : True := True.intro\n')
        subprocess.run(["lake", "build"], cwd=project, check=True, timeout=120)
        receipt = json.loads(subprocess.check_output(
            ["/opt/proofserve/bin/proofserve", "check", str(project), "--workers", "1"],
            text=True, timeout=240))
        assert receipt["status"] == "complete" and "Qualification" in receipt["accepted"], receipt
        assert receipt["theorem_body_policy"] == "shared-checked" and receipt["checker_checkpoint_abi"] == 6
        help_text = subprocess.check_output(
            ["/opt/proofserve/bin/proofserve", "check", "--help"], text=True, timeout=30)
        assert "--strict-theorem-bodies" in help_text
        strict = json.loads(subprocess.check_output(
            ["/opt/proofserve/bin/proofserve", "check", str(project), "--workers", "1",
             "--strict-theorem-bodies", "--checkpoint-dir", str(project / "strict-state")],
            text=True, timeout=240))
        assert strict["status"] == "complete" and strict["theorem_body_policy"] == "strict"
        assert strict["accepted"] == receipt["accepted"] and strict["axioms"] == receipt["axioms"]
        # Reuse the archive qualifier's existing three kernel mutation cases.
        lean_path = subprocess.check_output(
            ["lake", "env", "printenv", "LEAN_PATH"], cwd=project, text=True, timeout=30).strip()
        for mutation in ["bvar", "unknown", "sort"]:
            case_env = dict(os.environ, LEAN_PATH=lean_path,
                            DECOUPLED_MUTATE_MODULE="Qualification", PROOFSERVE_WORKERS="1")
            rejected = subprocess.run(
                ["/opt/proofserve/libexec/proofserve-check", "--internal-segment",
                 "audit", mutation, "Qualification"],
                cwd=project, env=case_env, text=True, capture_output=True, timeout=120)
            assert rejected.returncode != 0, (mutation, rejected.stdout)
            diagnostic = rejected.stdout + rejected.stderr
            assert "kernel_reject:" in diagnostic or (
                "while replaying declaration" in diagnostic and "(kernel)" in diagnostic), diagnostic
            events = [json.loads(line) for line in rejected.stdout.splitlines() if line.startswith("{")]
            assert any(e.get("event") == "reject" and e.get("module") == "Qualification" for e in events)
            assert not any(e.get("event") == "accept" and e.get("module") == "Qualification" for e in events)


        audit = json.loads(subprocess.check_output(
            ["/opt/proofserve/bin/proofserve", "audit", str(project), "--json", "-",
             "--receipt", str(project / ".proofserve/receipt.json")],
            text=True, timeout=60))
        assert audit["source_modules"] == 1 and not audit["errors"], audit
        declared = (project / "lean-toolchain").read_text()
        (project / "lean-toolchain").write_text('leanprover/lean4:v4.33.0\n')
        unsupported = subprocess.run(["/opt/proofserve/bin/proofserve", "check", str(project)],
                                     text=True, capture_output=True, timeout=10)
        assert unsupported.returncode == 2 and "unsupported" in unsupported.stderr, unsupported
        (project / "lean-toolchain").write_text(declared)
        print(json.dumps({"installed_project_check": "passed", "accepted_modules": len(receipt["accepted"]),
                          "audit_source_modules": audit["source_modules"], "unsupported_version_rejected": True, "strict_theorem_bodies_forwarded": True,
                          "theorem_body_policy": receipt["theorem_body_policy"], "strict_policy": strict["theorem_body_policy"],
                          "checker_checkpoint_abi": receipt["checker_checkpoint_abi"],
                          "kernel_bad_proofs_rejected": 3}), flush=True)
