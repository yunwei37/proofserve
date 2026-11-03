//! Executable runtime hardware accounting, with no native proof workload.
use std::{
    collections::BTreeSet,
    io::Read,
    process::{Command, Stdio},
    time::Duration,
};
fn mask(text: &str) -> BTreeSet<usize> {
    let mut result = BTreeSet::new();
    for group in text.trim().split(',') {
        let parts: Vec<_> = group.split('-').collect();
        let a = parts[0].parse::<usize>().unwrap();
        let b = parts.get(1).map(|s| s.parse().unwrap()).unwrap_or(a);
        result.extend(a..=b);
    }
    result
}
#[test]
fn runtime_threads_inherit_the_same_cpu_budget() {
    let status = std::fs::read_to_string("/proc/self/status").unwrap();
    let eligible = mask(
        status
            .lines()
            .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
            .unwrap(),
    );
    let chosen: BTreeSet<_> = eligible.into_iter().take(2).collect();
    let args = chosen
        .iter()
        .map(usize::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .args([
            "batch",
            "--repl",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "affinity-only-no-verification",
            "--cpus",
            &args,
        ])
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let pid = child.id();
    let mut observed = vec![];
    for _ in 0..100 {
        if let Ok(entries) = std::fs::read_dir(format!("/proc/{pid}/task")) {
            observed = entries
                .filter_map(Result::ok)
                .filter_map(|e| std::fs::read_to_string(e.path().join("status")).ok())
                .filter_map(|s| {
                    s.lines()
                        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
                        .map(mask)
                })
                .collect();
        }
        if observed.len() >= chosen.len() + 2 {
            break;
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    let alive = child.try_wait().unwrap().is_none();
    if alive {
        child.kill().unwrap();
    }
    child.wait().unwrap();
    let mut errors = String::new();
    child
        .stderr
        .take()
        .unwrap()
        .read_to_string(&mut errors)
        .unwrap();
    assert!(alive, "CLI exited early: {errors}");
    assert!(
        observed.len() >= chosen.len() + 2,
        "runtime did not initialize: {errors}"
    );
    assert!(
        observed.iter().all(|cpus| *cpus == chosen),
        "{observed:?} outside {chosen:?}"
    );
}

#[test]
fn structured_resource_logs_do_not_corrupt_jsonl_results() {
    use std::io::{BufRead, Write};
    let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .args([
            "batch",
            "--repl",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "jsonl-logging-no-native-proof",
        ])
        .env("RUST_LOG", "proofserve_engine::resources=info")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let mut input = child.stdin.take().unwrap();
    input.write_all(b"{\"candidates\":[]}\n").unwrap();
    input.flush().unwrap();
    let mut output = std::io::BufReader::new(child.stdout.take().unwrap());
    let mut line = String::new();
    output.read_line(&mut line).unwrap();
    std::thread::sleep(Duration::from_millis(30));
    drop(input);
    child.wait().unwrap();
    let mut errors = String::new();
    child
        .stderr
        .take()
        .unwrap()
        .read_to_string(&mut errors)
        .unwrap();
    let response: serde_json::Value = serde_json::from_str(&line).unwrap();
    assert_eq!(response["results"], serde_json::json!([]));
    assert!(
        errors
            .lines()
            .filter_map(|l| serde_json::from_str::<serde_json::Value>(l).ok())
            .any(|v| v["fields"]["rss_bytes"].is_u64()),
        "{errors}"
    );
}

#[test]
fn measure_capture_and_compare_round_trip_retire_native_fixture() {
    use std::io::Write;
    use std::os::unix::fs::PermissionsExt;
    let path = std::env::temp_dir().join(format!(
        "proofserve-measure-fixture-{}.py",
        std::process::id()
    ));
    let mut fixture = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&path)
        .unwrap();
    fixture.write_all(b"#!/usr/bin/python3\nimport sys\nwhile sys.stdin.readline().strip(): pass\nprint('{\"env\":0}',flush=True)\nprint('',flush=True)\nsys.stdin.read()\n").unwrap();
    drop(fixture);
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
    for policy in ["source-size", "task-interleave", "task-memory"] {
        let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
            .args([
                "measure",
                "--repl",
                path.to_str().unwrap(),
                "--project",
                "/tmp",
                "--environment",
                "fixture-not-a-native-proof",
                "--policy",
                policy,
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .unwrap();
        let mut stdin = child.stdin.take().unwrap();
        stdin.write_all(br#"{"candidates":[{"id":"a","task_id":"same-task","code":"a","reuse":false},{"id":"b","task_id":"same-task","code":"b","reuse":false}]}"#).unwrap();
        drop(stdin);
        let result = child.wait_with_output().unwrap();
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
        let capture: proofserve::measurement::Capture =
            serde_json::from_slice(&result.stdout).unwrap();
        assert_eq!(capture.policy, policy);
        assert_eq!(capture.results.len(), 2);
        for v in &capture.results {
            assert_eq!(v.outcome.status, proofserve_core::Status::Accepted);
            assert_eq!(v.attempts.len(), 1);
            for p in &v.attempts[0].processes {
                assert!(!std::path::Path::new(&format!("/proc/{}", p.pid)).exists());
            }
        }
        assert!(capture.lifecycle_seconds > 0.0);
        assert_eq!(
            proofserve::measurement::compare(&capture, &capture).unwrap()["lifecycle_speedup"],
            1.0
        );
    }
    std::fs::remove_file(&path).unwrap();
}

#[test]
fn native_source_arguments_reach_process_and_capture_identity() {
    use std::io::Write;
    let fixture = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("proofserve-lean/tests/fixtures/source.py");
    let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .args([
            "measure",
            "--lean",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "source-argv-fixture-not-Lean",
            "--lean-arg",
            fixture.to_str().unwrap(),
            "--lean-arg",
            "--tstack=400000",
            "--lean-arg",
            "one argument with spaces",
        ])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let code = "original α\r\n";
    child
        .stdin
        .take()
        .unwrap()
        .write_all(
            serde_json::to_string(&serde_json::json!({"candidates":[
            {"id":"argv","code":code,"reuse":false}]}))
            .unwrap()
            .as_bytes(),
        )
        .unwrap();
    let output = child.wait_with_output().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let capture: proofserve::measurement::Capture = serde_json::from_slice(&output.stdout).unwrap();
    assert!(capture.backend.contains("--tstack=400000"));
    assert_eq!(
        capture.results[0].outcome.status,
        proofserve_core::Status::Accepted
    );
    let result = capture.results[0].outcome.response.as_ref().unwrap();
    let detail: serde_json::Value =
        serde_json::from_str(result["messages"][0]["data"].as_str().unwrap()).unwrap();
    assert_eq!(detail["source"], code);
    assert_eq!(
        detail["argv"],
        serde_json::json!([
            "--tstack=400000",
            "one argument with spaces",
            "--json",
            "--stdin"
        ])
    );
    for process in capture.results[0]
        .attempts
        .iter()
        .flat_map(|a| &a.processes)
    {
        assert!(!std::path::Path::new(&format!("/proc/{}", process.pid)).exists());
    }
}

#[test]
fn original_source_file_mode_reaches_native_file_context() {
    use std::io::Write;
    let path = std::env::temp_dir().join(format!(
        "proofserve-cli-original-{}.lean",
        std::process::id()
    ));
    let directory =
        std::env::temp_dir().join(format!("proofserve-cli-logs-{}", std::process::id()));
    std::fs::create_dir(&directory).unwrap();
    let code = "unchanged original α\n";
    std::fs::write(&path, code).unwrap();
    let fixture = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("proofserve-lean/tests/fixtures/source.py");
    let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
        .args([
            "measure",
            "--lean",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "file-fixture-not-Lean",
            "--lean-arg",
            fixture.to_str().unwrap(),
            "--source-file",
            path.to_str().unwrap(),
            "--stderr-dir",
            directory.to_str().unwrap(),
        ])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    child
        .stdin
        .take()
        .unwrap()
        .write_all(
            serde_json::to_string(&serde_json::json!({"candidates":[
                {"id":"original","code":code,"reuse":false}
            ]}))
            .unwrap()
            .as_bytes(),
        )
        .unwrap();
    let output = child.wait_with_output().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let capture: proofserve::measurement::Capture = serde_json::from_slice(&output.stdout).unwrap();
    assert!(capture.backend.contains("source-file:"));
    assert_eq!(
        capture.results[0].outcome.status,
        proofserve_core::Status::Accepted
    );
    let result = capture.results[0].outcome.response.as_ref().unwrap();
    let detail: serde_json::Value =
        serde_json::from_str(result["messages"][0]["data"].as_str().unwrap()).unwrap();
    assert_eq!(detail["source"], code);
    assert_eq!(
        detail["argv"],
        serde_json::json!(["--json", path.to_str().unwrap()])
    );
    for process in capture.results[0]
        .attempts
        .iter()
        .flat_map(|a| &a.processes)
    {
        assert!(!std::path::Path::new(&format!("/proc/{}", process.pid)).exists());
    }
    let attempt = &capture.results[0].attempts[0];
    let event = attempt
        .backend_events
        .iter()
        .find(|e| e.stage == "stderr_log_complete")
        .unwrap();
    let event: serde_json::Value = serde_json::from_str(&event.detail).unwrap();
    assert_eq!(event["complete"], true);
    assert_eq!(event["bytes_read"], 0);
    let log = std::path::PathBuf::from(event["path"].as_str().unwrap());
    assert_eq!(std::fs::read(&log).unwrap(), b"");
    std::fs::remove_file(log).unwrap();
    std::fs::remove_dir(directory).unwrap();
    std::fs::remove_file(path).unwrap();
}

#[test]
fn termination_retires_owned_attempts_in_all_cli_modes() {
    use std::io::Write;
    use std::net::{TcpListener, TcpStream};
    use std::os::unix::fs::PermissionsExt;
    use std::time::Instant;
    let directory = std::env::temp_dir().join(format!("proofserve-stop-{}", std::process::id()));
    std::fs::create_dir(&directory).unwrap();
    let fixture = directory.join("hold.py");
    std::fs::write(
        &fixture,
        b"#!/usr/bin/python3\nimport json,os,sys,time\nfrom pathlib import Path\nsource=json.loads(sys.stdin.readline())['cmd']\nmarker=Path(source)\nready=marker.with_suffix('.ready')\nready.write_text(str(os.getpid()))\nready.rename(marker)\ntime.sleep(60)\n",
    ).unwrap();
    std::fs::set_permissions(&fixture, std::fs::Permissions::from_mode(0o700)).unwrap();
    let eligible = std::fs::read_to_string("/proc/self/status").unwrap();
    let cpu = mask(
        eligible
            .lines()
            .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
            .unwrap(),
    )
    .into_iter()
    .next()
    .unwrap()
    .to_string();
    for (mode, signal) in [
        ("serve", "-TERM"),
        ("batch", "-TERM"),
        ("measure", "-TERM"),
        ("batch", "-INT"),
    ] {
        let marker = directory.join(format!("{mode}{signal}.pid"));
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let address = listener.local_addr().unwrap();
        drop(listener);
        let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
            .args([
                mode,
                "--repl",
                fixture.to_str().unwrap(),
                "--project",
                "/tmp",
                "--environment",
                "signal-fixture-not-Lean",
                "--cpus",
                &cpu,
                "--listen",
                &address.to_string(),
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .unwrap();
        let mut native = None;
        let result = (|| -> Result<(), String> {
            let payload = serde_json::json!({"candidates":[
                {"id":"held","code":marker.to_str().unwrap(),"reuse":false}]})
            .to_string();
            let mut connection = if mode == "serve" {
                let until = Instant::now() + Duration::from_secs(5);
                let mut stream = loop {
                    match TcpStream::connect(address) {
                        Ok(stream) => break stream,
                        Err(_) if Instant::now() < until => {
                            std::thread::sleep(Duration::from_millis(10))
                        }
                        Err(error) => return Err(error.to_string()),
                    }
                };
                write!(stream, "POST /v1/verify HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nConnection: close\r\nContent-Length: {}\r\n\r\n{}", payload.len(), payload).map_err(|e|e.to_string())?;
                Some(stream)
            } else {
                let mut input = child.stdin.take().unwrap();
                writeln!(input, "{payload}").map_err(|e| e.to_string())?;
                drop(input);
                None
            };
            let until = Instant::now() + Duration::from_secs(5);
            while !marker.exists() && Instant::now() < until {
                if child.try_wait().map_err(|e| e.to_string())?.is_some() {
                    return Err("CLI exited before held attempt".into());
                }
                std::thread::sleep(Duration::from_millis(10));
            }
            let pid: u32 = std::fs::read_to_string(&marker)
                .map_err(|e| e.to_string())?
                .parse()
                .map_err(|e| format!("{e}"))?;
            let stat =
                std::fs::read_to_string(format!("/proc/{pid}/stat")).map_err(|e| e.to_string())?;
            let birth = stat
                .rsplit_once(')')
                .unwrap()
                .1
                .split_whitespace()
                .nth(19)
                .unwrap()
                .to_owned();
            native = Some((pid, birth));
            assert!(
                Command::new("kill")
                    .args([signal, &child.id().to_string()])
                    .status()
                    .unwrap()
                    .success()
            );
            let until = Instant::now() + Duration::from_secs(5);
            let status = loop {
                if let Some(status) = child.try_wait().map_err(|e| e.to_string())? {
                    break status;
                }
                if Instant::now() >= until {
                    return Err("CLI failed to retire after signal".into());
                }
                std::thread::sleep(Duration::from_millis(10));
            };
            if status.success() != (mode == "serve") || (mode != "serve" && status.code().is_none())
            {
                return Err(format!("incorrect termination status: {status}"));
            }
            if std::path::Path::new(&format!("/proc/{pid}")).exists() {
                return Err("owned verifier still exists after CLI exit".into());
            }
            if let Some(stream) = connection.as_mut() {
                stream
                    .set_read_timeout(Some(Duration::from_secs(2)))
                    .unwrap();
                let mut response = String::new();
                stream
                    .read_to_string(&mut response)
                    .map_err(|e| e.to_string())?;
                if !response.contains("backend_error") {
                    return Err(response);
                }
            } else if mode == "measure" {
                let mut output = String::new();
                child
                    .stdout
                    .take()
                    .unwrap()
                    .read_to_string(&mut output)
                    .map_err(|e| e.to_string())?;
                if !output.is_empty() {
                    return Err("interrupted measure emitted a complete capture".into());
                }
            }
            Ok(())
        })();
        if child.try_wait().unwrap().is_none() {
            let _ = child.kill();
        }
        let _ = child.wait();
        // Failure cleanup targets only the fixture's still-matching process birth.
        if let Some((pid, birth)) = native
            && std::fs::read_to_string(format!("/proc/{pid}/stat"))
                .ok()
                .and_then(|s| {
                    s.rsplit_once(')')
                        .map(|(_, t)| t.split_whitespace().nth(19).unwrap_or("").to_owned())
                })
                .as_ref()
                == Some(&birth)
        {
            let _ = Command::new("kill")
                .args(["-KILL", "--", &format!("-{pid}")])
                .status();
        }
        let _ = std::fs::remove_file(marker);
        assert!(result.is_ok(), "{mode}/{signal}: {result:?}");
    }
    std::fs::remove_file(fixture).unwrap();
    std::fs::remove_dir(directory).unwrap();
}

#[test]
fn termination_interrupts_idle_cli_input_without_waiting_for_eof() {
    for mode in ["batch", "measure"] {
        let mut child = Command::new(env!("CARGO_BIN_EXE_proofserve"))
            .args([
                mode,
                "--repl",
                "/usr/bin/python3",
                "--project",
                "/tmp",
                "--environment",
                "idle-signal-no-native",
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        std::thread::sleep(Duration::from_millis(100));
        assert!(child.try_wait().unwrap().is_none());
        assert!(
            Command::new("kill")
                .args(["-TERM", &child.id().to_string()])
                .status()
                .unwrap()
                .success()
        );
        let until = std::time::Instant::now() + Duration::from_secs(3);
        let mut stopped = false;
        while std::time::Instant::now() < until {
            if let Some(status) = child.try_wait().unwrap() {
                stopped = status.code().is_some() && !status.success();
                break;
            }
            std::thread::sleep(Duration::from_millis(10));
        }
        if child.try_wait().unwrap().is_none() {
            child.kill().unwrap();
        }
        child.wait().unwrap();
        assert!(stopped, "{mode}: shutdown waited for stdin EOF");
    }
}

#[test]
fn automatic_resources_and_explicit_override_need_no_native_process() {
    use std::io::Write;
    for override_memory in [false, true] {
        let mut command = Command::new(env!("CARGO_BIN_EXE_proofserve"));
        command.args([
            "measure",
            "--repl",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "empty-batch-resource-defaults",
        ]);
        if override_memory {
            command.args(["--memory-gib", "1"]);
        }
        let mut child = command
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .unwrap();
        child
            .stdin
            .take()
            .unwrap()
            .write_all(br#"{"candidates":[]}"#)
            .unwrap();
        let output = child.wait_with_output().unwrap();
        assert!(
            output.status.success(),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
        let capture: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(capture["results"], serde_json::json!([]));
        assert!(!capture["resources"]["cpus"].as_array().unwrap().is_empty());
        let memory = capture["resources"]["memory_bytes"].as_u64().unwrap();
        assert!(memory > 0);
        if override_memory {
            assert_eq!(memory, 1024 * 1024 * 1024);
        }
    }
}
