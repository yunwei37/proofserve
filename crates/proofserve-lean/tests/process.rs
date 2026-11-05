use proofserve_core::*;
use proofserve_engine::{Config, Engine, Fifo, HeadroomAdmission, MemoryCache, linux::ProcMonitor};
use proofserve_lean::NativeRepl;
use std::{path::PathBuf, sync::Arc, time::Duration};

fn cpu() -> usize {
    let status = std::fs::read_to_string("/proc/self/status").unwrap();
    status
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim()
        .split([',', '-'])
        .next()
        .unwrap()
        .parse()
        .unwrap()
}
fn candidate(id: &str, code: &str, ms: u64) -> Candidate {
    Candidate {
        id: id.into(),
        task_id: None,
        code: code.into(),
        timeout_ms: ms,
        reuse: false,
    }
}
fn engine() -> Engine {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/repl.py");
    let backend = NativeRepl {
        program: PathBuf::from("/usr/bin/python3"),
        args: vec!["-u".into(), fixture.to_string_lossy().into()],
        project: std::env::temp_dir(),
        environment: "protocol-fixture-not-Lean".into(),
    };
    Engine::new(
        Config {
            memory_bytes: 1024 * 1024 * 1024,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap()
}
#[tokio::test]
async fn pipe_protocol_errors_admissions_and_stderr_drain() {
    let engine = engine();
    let result = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("accepted", "ok", 5000),
                candidate("rejected", "bad", 5000),
                candidate("incomplete", "sorry", 5000),
                candidate("stderr", "stderr", 5000),
                candidate("eof_flush", "eof_flush", 5000),
            ],
        })
        .await
        .unwrap();
    assert_eq!(
        result
            .iter()
            .map(|r| r.outcome.status.clone())
            .collect::<Vec<_>>(),
        [
            Status::Accepted,
            Status::Rejected,
            Status::Incomplete,
            Status::Accepted,
            Status::Accepted
        ]
    );
    for row in &result {
        let observations: Vec<_> = row
            .attempts
            .iter()
            .flat_map(|a| &a.backend_events)
            .filter(|e| e.stage == "rss_observation")
            .map(|e| serde_json::from_str::<serde_json::Value>(&e.detail).unwrap())
            .collect();
        assert!(
            observations.iter().any(|v| {
                v["kind"] == "leader_current_rss"
                    && v["bytes"].as_u64().unwrap() > 0
                    && row.attempts.iter().flat_map(|a| &a.processes).any(|p| {
                        v["pid"].as_u64() == Some(p.pid as u64)
                            && v["start_ticks"].as_u64() == Some(p.start_ticks)
                    })
            }),
            "before-retirement sample lacks its process/kind provenance"
        );
    }
    engine.shutdown().await;
}
#[tokio::test]
async fn malformed_native_diagnostics_are_not_cached_between_requests() {
    let engine = engine();
    for id in ["first-malformed", "second-malformed"] {
        let mut input = candidate(id, "invalid_message", 5000);
        input.reuse = true;
        let rows = engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![input],
            })
            .await
            .unwrap();
        let row = &rows[0];
        assert_eq!(row.outcome.status, Status::BackendError);
        assert!(!row.outcome.cacheable());
        assert!(!row.cached && !row.coalesced);
        assert_eq!(row.attempts.len(), 1);
        assert_eq!(
            row.outcome.response,
            Some(serde_json::json!({"env": 0, "messages": [null]}))
        );
        assert!(row.outcome.error.as_deref().unwrap().contains("malformed"));
        for process in &row.attempts[0].processes {
            assert!(
                proofserve_engine::linux::identity(process.pid).is_err(),
                "fixture process survives the operational response"
            );
        }
    }
    engine.shutdown().await;
}

#[tokio::test]
async fn timeout_retires_process_before_next_attempt() {
    let engine = engine();
    let result = tokio::time::timeout(
        Duration::from_secs(10),
        engine.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("timeout", "slow", 30),
                candidate("next", "ok", 5000),
            ],
        }),
    )
    .await
    .unwrap()
    .unwrap();
    assert_eq!(result[0].outcome.status, Status::Timeout);
    assert_eq!(result[1].outcome.status, Status::Accepted);
    engine.shutdown().await;
}

struct SmallForecast;
impl SchedulingPolicy for SmallForecast {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
        Some(4 * 1024 * 1024)
    }
}
#[tokio::test]
async fn real_owned_rss_watchdog_kills_reaps_and_retries_exclusively() {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/repl.py");
    let status = std::fs::read_to_string("/proc/self/status").unwrap();
    let text = status
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim();
    let first = text
        .split([',', '-'])
        .next()
        .unwrap()
        .parse::<usize>()
        .unwrap();
    // This process integration needs two actually eligible CPUs.
    let second = if text.contains('-') {
        first + 1
    } else {
        text.split(',').nth(1).unwrap().parse().unwrap()
    };
    let backend = NativeRepl {
        program: PathBuf::from("/usr/bin/python3"),
        args: vec!["-u".into(), fixture.to_string_lossy().into()],
        project: std::env::temp_dir(),
        environment: "real-rss-fixture".into(),
    };
    let e = Engine::new(
        Config {
            memory_bytes: 50 * 1024 * 1024,
            cpus: vec![first, second],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(SmallForecast),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let rows = tokio::time::timeout(
        Duration::from_secs(15),
        e.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("a", "memory_a", 10000),
                candidate("b", "memory_b", 10000),
            ],
        }),
    )
    .await
    .unwrap()
    .unwrap();
    assert!(
        rows.iter().all(|r| r.outcome.status == Status::Accepted),
        "{rows:?}"
    );
    let retry = rows
        .iter()
        .find(|r| r.attempts.len() > 1)
        .expect("actual RSS excess must exercise requeue");
    assert_eq!(retry.attempts[0].status, Status::Preempted);
    assert!(retry.attempts[1].exclusive);
    e.shutdown().await;
}

#[tokio::test]
async fn unavailable_prepared_host_uses_unchanged_native_fallback() {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/repl.py");
    let fresh = NativeRepl {
        program: "/usr/bin/python3".into(),
        args: vec!["-u".into(), fixture.to_string_lossy().into()],
        project: std::env::temp_dir(),
        environment: "prepared-fallback-fixture-not-Lean".into(),
    };
    let backend = proofserve_lean::PreparedRepl::new(
        fresh,
        "/no-such-proofserve-prepared-host".into(),
        "/no-such-sdk".into(),
    );
    let e = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("a", "ok", 5000),
                candidate("b", "bad", 5000),
                candidate("c", "sorry", 5000),
            ],
        })
        .await
        .unwrap();
    assert_eq!(
        result
            .iter()
            .map(|r| r.outcome.status.clone())
            .collect::<Vec<_>>(),
        [Status::Accepted, Status::Rejected, Status::Incomplete]
    );
    assert!(!e.prepared_state_ready());
    assert!(result.iter().all(|r| {
        r.attempts[0]
            .backend_events
            .iter()
            .any(|e| e.stage == "fresh_fallback")
    }));
    for p in result
        .iter()
        .flat_map(|r| r.attempts.iter().flat_map(|a| &a.processes))
    {
        assert!(
            proofserve_engine::linux::identity(p.pid).is_err(),
            "fallback child not retired"
        );
    }
    e.shutdown().await;
}

#[tokio::test]
async fn source_arguments_preserve_tokens_source_and_cache_context() {
    use proofserve_lean::NativeLean;
    let base = NativeLean {
        program: "/usr/bin/python3".into(),
        project: std::env::temp_dir(),
        environment: "argv-fixture-not-Lean".into(),
    };
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/source.py");
    let arguments = vec![
        fixture.to_string_lossy().into_owned(),
        "--tstack=400000".into(),
        "one argument with spaces".into(),
    ];
    assert_eq!(base.clone().with_args(vec![]).identity(), base.identity());
    let configured = base.clone().with_args(arguments.clone());
    assert_ne!(configured.identity(), base.identity());
    assert_ne!(
        configured.identity(),
        base.with_args(vec!["other".into()]).identity()
    );
    let engine = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(configured),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let code = "original UTF8: α\r\nsecond line\n";
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("argv", code, 5000)],
        })
        .await
        .unwrap();
    let row = &results[0];
    assert_eq!(row.outcome.status, Status::Accepted);
    let envelope = row.outcome.response.as_ref().unwrap();
    let detail: serde_json::Value =
        serde_json::from_str(envelope["messages"][0]["data"].as_str().unwrap()).unwrap();
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
    engine.shutdown().await;
    for process in row.attempts.iter().flat_map(|attempt| &attempt.processes) {
        assert!(proofserve_engine::linux::identity(process.pid).is_err());
    }
}

#[tokio::test]
async fn original_source_file_preserves_context_and_refuses_different_bytes() {
    use proofserve_lean::NativeLean;
    let path = std::env::temp_dir().join(format!(
        "proofserve-original-source-{}.lean",
        std::process::id()
    ));
    let code = "original α\r\n";
    std::fs::write(&path, code).unwrap();
    let base = NativeLean {
        program: "/usr/bin/python3".into(),
        project: std::env::temp_dir(),
        environment: "original-file-fixture-not-Lean".into(),
    };
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/source.py");
    let args = vec![
        fixture.to_string_lossy().into_owned(),
        "--tstack=400000".into(),
    ];
    let stdin_identity = base.clone().with_args(args.clone()).identity();
    let configured = base.with_source_file(path.file_name().unwrap().into(), args);
    assert_ne!(configured.identity(), stdin_identity);
    let engine = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(configured),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("original", code, 5000)],
        })
        .await
        .unwrap();
    assert_eq!(results[0].outcome.status, Status::Accepted);
    let response = results[0].outcome.response.as_ref().unwrap();
    let detail: serde_json::Value =
        serde_json::from_str(response["messages"][0]["data"].as_str().unwrap()).unwrap();
    assert_eq!(detail["source"], code);
    assert_eq!(
        detail["argv"],
        serde_json::json!(["--tstack=400000", "--json", path.to_str().unwrap()])
    );
    let mismatch = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("mismatch", "different source", 5000)],
        })
        .await
        .unwrap();
    assert_eq!(mismatch[0].outcome.status, Status::BackendError);
    assert!(mismatch[0].outcome.response.is_none());
    assert!(mismatch[0].attempts.iter().all(|a| a.processes.is_empty()));
    engine.shutdown().await;
    for process in results[0].attempts.iter().flat_map(|a| &a.processes) {
        assert!(proofserve_engine::linux::identity(process.pid).is_err());
    }
    assert_eq!(std::fs::read(&path).unwrap(), code.as_bytes());
    std::fs::remove_file(path).unwrap();
}

#[tokio::test]
async fn complete_stderr_log_preserves_events_beyond_response_tail() {
    use proofserve_lean::NativeLean;
    let directory = std::env::temp_dir().join(format!("proofserve-stderr-{}", std::process::id()));
    std::fs::create_dir(&directory).unwrap();
    let base = NativeLean {
        program: "/usr/bin/python3".into(),
        project: std::env::temp_dir(),
        environment: "raw-stderr-fixture-not-Lean".into(),
    };
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/source.py");
    let args = vec![fixture.to_string_lossy().into_owned()];
    let plain = base.clone().with_args(args.clone());
    let logged = base.with_args(args).with_stderr_dir(directory.clone());
    assert_ne!(plain.identity(), logged.identity());
    let engine = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(logged),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("events", "large-stderr", 5000)],
        })
        .await
        .unwrap();
    // Arbitrary stderr still cannot establish native proof acceptance.
    assert_eq!(results[0].outcome.status, Status::BackendError);
    let response = results[0].outcome.response.as_ref().unwrap();
    assert!(
        response["stderr"]
            .as_str()
            .unwrap()
            .starts_with("[stderr tail truncated] ")
    );
    let attempt = &results[0].attempts[0];
    let opened = attempt
        .backend_events
        .iter()
        .find(|e| e.stage == "stderr_log")
        .unwrap();
    let opened: serde_json::Value = serde_json::from_str(&opened.detail).unwrap();
    let path = PathBuf::from(opened["path"].as_str().unwrap());
    assert_eq!(path.parent().unwrap(), directory);
    assert_eq!(opened["pid"], attempt.processes[0].pid);
    assert_eq!(opened["start_ticks"], attempt.processes[0].start_ticks);
    let bytes = std::fs::read(&path).unwrap();
    assert!(bytes.len() > 65536);
    let rows: Vec<serde_json::Value> = std::str::from_utf8(&bytes)
        .unwrap()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    assert_eq!(rows.len(), 1024);
    for (index, row) in rows.iter().enumerate() {
        assert_eq!(row["row"], index);
        assert_eq!(row["payload"], "α".repeat(64));
    }
    let complete = attempt
        .backend_events
        .iter()
        .find(|e| e.stage == "stderr_log_complete")
        .unwrap();
    let complete: serde_json::Value = serde_json::from_str(&complete.detail).unwrap();
    assert_eq!(complete["bytes_read"], bytes.len());
    assert_eq!(complete["complete"], true);
    engine.shutdown().await;
    for p in &attempt.processes {
        assert!(proofserve_engine::linux::identity(p.pid).is_err());
    }
    std::fs::remove_file(path).unwrap();
    std::fs::remove_dir(directory).unwrap();
}

#[tokio::test]
async fn stderr_log_setup_fault_retires_native_attempt() {
    use proofserve_lean::NativeLean;
    let absent = std::env::temp_dir().join(format!("proofserve-absent-log-{}", std::process::id()));
    assert!(!absent.exists());
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/source.py");
    let backend = NativeLean {
        program: "/usr/bin/python3".into(),
        project: std::env::temp_dir(),
        environment: "log-fault-fixture-not-Lean".into(),
    }
    .with_args(vec![fixture.to_string_lossy().into_owned()])
    .with_stderr_dir(absent);
    let engine = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("fault", "input", 5000)],
        })
        .await
        .unwrap();
    assert_eq!(results[0].outcome.status, Status::BackendError);
    assert!(results[0].outcome.response.is_none());
    assert!(
        results[0]
            .outcome
            .error
            .as_ref()
            .unwrap()
            .contains("cannot create native stderr log")
    );
    assert_eq!(results[0].attempts[0].processes.len(), 1);
    engine.shutdown().await;
    for p in &results[0].attempts[0].processes {
        assert!(proofserve_engine::linux::identity(p.pid).is_err());
    }
}

#[tokio::test]
async fn source_exit_retires_background_pipe_holders_before_returning() {
    use proofserve_lean::NativeLean;
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/source.py");
    let backend = NativeLean {
        program: "/usr/bin/python3".into(),
        project: std::env::temp_dir(),
        environment: "background-pipe-fixture-not-Lean".into(),
    }
    .with_args(vec![fixture.to_string_lossy().into_owned()]);
    let engine = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    for code in ["hold-stderr", "hold-stdout"] {
        let started = std::time::Instant::now();
        let rows = engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![candidate(code, code, 500)],
            })
            .await
            .unwrap();
        assert!(
            started.elapsed() < Duration::from_secs(2),
            "retired native leader left a pipe-holding descendant on the resource lease"
        );
        assert_eq!(
            rows[0].outcome.status,
            Status::Accepted,
            "{:?}",
            rows[0].outcome
        );
        let response = rows[0].outcome.response.as_ref().unwrap();
        let detail: serde_json::Value =
            serde_json::from_str(response["messages"][0]["data"].as_str().unwrap()).unwrap();
        let pid = detail["background"].as_u64().unwrap() as u32;
        // SIGKILL/pipe closure can precede the final kernel zombie transition.
        // Observe actual exit, rather than racing that short transition.
        tokio::time::timeout(Duration::from_secs(2), async {
            loop {
                match std::fs::read_to_string(format!("/proc/{pid}/stat")) {
                    Err(error)
                        if error.kind() == std::io::ErrorKind::NotFound
                            || error.raw_os_error() == Some(libc::ESRCH) =>
                    {
                        break;
                    }
                    Ok(stat)
                        if stat.rsplit_once(')').unwrap().1.split_whitespace().next()
                            == Some("Z") =>
                    {
                        break;
                    }
                    Err(error) => panic!("cannot inspect owned fixture: {error}"),
                    _ => tokio::time::sleep(Duration::from_millis(1)).await,
                }
            }
        })
        .await
        .expect("owned background pipe holder survived native retirement");
        assert!(
            proofserve_engine::linux::identity(detail["pid"].as_u64().unwrap() as u32).is_err()
        );
    }
    engine.shutdown().await;
}
