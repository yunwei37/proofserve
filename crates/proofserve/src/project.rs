//! Project tools own their arguments, receipts, supported versions and exit codes.
use std::{ffi::OsString, path::PathBuf, process::Command};

pub fn run(command: &str, args: Vec<OsString>) -> Result<(), Box<dyn std::error::Error>> {
    if args.is_empty() {
        return Err(format!("usage: proofserve {command} PROJECT [OPTIONS]").into());
    }
    let name = format!("proofserve-{command}");
    let sibling = std::env::current_exe()?
        .parent()
        .map(|p| p.join(&name))
        .filter(|p| p.is_file());
    let program = sibling.unwrap_or_else(|| PathBuf::from(&name));
    let mut child = Command::new(program);
    child.args(args);
    // Replace the launcher so signals, native exit status, stdout receipts and
    // stderr diagnostics reach the caller unchanged. No service is started.
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        let error = child.exec();
        Err(format!(
            "cannot start {name}: {error}. Install the full ProofServe release bundle; cargo install alone provides the Rust launcher, not the project tools."
        )
        .into())
    }
    #[cfg(not(unix))]
    {
        Err("project checking currently requires the Linux release bundle".into())
    }
}
