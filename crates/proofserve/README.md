# proofserve

Independent Lean project checking and audit CLI, with the existing
Kimina-compatible verification service.

The complete release bundle installs three executables together:

    proofserve check PROJECT --workers 4
    proofserve audit PROJECT --json -
    proofserve serve --repl REPL --project PROJECT --environment ID

The check/audit launchers find proofserve-check/proofserve-audit beside the
binary, then on PATH. Arguments, stdout, stderr, exit codes and Unix signals
pass directly to that component. The checker owns receipt v1 and explicit
Lean-version rejection. The audit component owns its JSON report; it is not
a kernel acceptance receipt. No Workspace path is embedded.

cargo install provides only this Rust launcher and service. Use the complete
release bundle or container for project commands. The previous candidate
JSONL check command is now batch; HTTP /check is unchanged. measure and
compare remain available for existing research captures.

[API documentation](https://docs.rs/proofserve) ·
[Project and quick start](https://github.com/yunwei37/proofserve)

Rust1.98+, Linux. Apache-2.0. Research data stays in the repository and is
excluded from this source package.
