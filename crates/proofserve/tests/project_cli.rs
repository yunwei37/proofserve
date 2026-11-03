//! Launcher contracts only; native proof acceptance is checked by checker CI.
use std::{os::unix::fs::PermissionsExt, path::PathBuf, process::Command};

fn directory(name: &str) -> PathBuf {
    let p = std::env::temp_dir().join(format!("proofserve-project-{}-{name}", std::process::id()));
    std::fs::create_dir(&p).unwrap();
    p
}
fn backend(dir: &std::path::Path, name: &str, body: &str) {
    let p = dir.join(name);
    std::fs::write(&p, format!("#!/bin/sh\n{body}\n")).unwrap();
    std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o700)).unwrap();
}
#[test]
fn check_forwards_project_and_options_without_starting_a_service() {
    let p = directory("check");
    backend(&p, "proofserve-check", "printf '<%s>\\n' \"$@\"");
    let out = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .env("PATH", &p)
        .args([
            "check",
            "project with spaces",
            "--workers",
            "2",
            "--checkpoint-dir",
            "state with spaces",
        ])
        .output()
        .unwrap();
    assert!(out.status.success(), "{:?}", out.stderr);
    assert_eq!(
        String::from_utf8(out.stdout).unwrap(),
        "<project with spaces>\n<--workers>\n<2>\n<--checkpoint-dir>\n<state with spaces>\n"
    );
    std::fs::remove_dir_all(p).unwrap();
}
#[test]
fn audit_preserves_backend_stdout_stderr_and_nonzero_status() {
    let p = directory("audit");
    backend(
        &p,
        "proofserve-audit",
        "printf 'receipt-fixture\\n'; printf 'diagnostic-fixture\\n' >&2; exit 23",
    );
    let out = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .env("PATH", &p)
        .args(["audit", "project", "--json", "-"])
        .output()
        .unwrap();
    assert_eq!(out.status.code(), Some(23));
    assert_eq!(out.stdout, b"receipt-fixture\n");
    assert_eq!(out.stderr, b"diagnostic-fixture\n");
    std::fs::remove_dir_all(p).unwrap();
}
#[test]
fn missing_component_fails_explicitly() {
    let p = directory("missing");
    let out = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .env("PATH", &p)
        .args(["check", "project"])
        .output()
        .unwrap();
    assert!(!out.status.success());
    assert!(
        String::from_utf8_lossy(&out.stderr).contains("Install the full ProofServe release bundle")
    );
    assert!(out.stdout.is_empty());
    std::fs::remove_dir_all(p).unwrap();
}
