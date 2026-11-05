//! Local engine executable. Library use does not require a network service.
mod project;
mod resources;
use proofserve_core::{Batch, VerificationBackend};
use proofserve_engine::{
    Config, Engine, Fifo, HeadroomAdmission, MemoryCache, SourceSize, TaskInterleave, TaskMemory,
    linux::ProcMonitor,
};
use proofserve_lean::{NativeLean, NativeRepl};
use std::{
    collections::HashMap,
    path::PathBuf,
    sync::Arc,
    time::{Instant, SystemTime, UNIX_EPOCH},
};
use tokio::io::{AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader};

fn cpu_eligibility() -> Result<Vec<usize>, String> {
    let mut set = libc_cpu::CpuSet::new()?;
    set.cpus()
}
// Keep Linux ABI in one small public-free module; the engine has no affinity override.
mod libc_cpu {
    pub struct CpuSet(String);
    impl CpuSet {
        pub fn new() -> Result<Self, String> {
            let status = std::fs::read_to_string("/proc/self/status").map_err(|e| e.to_string())?;
            let line = status
                .lines()
                .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
                .ok_or("CPU eligibility unavailable")?;
            Ok(Self(line.trim().into()))
        }
        pub fn cpus(&mut self) -> Result<Vec<usize>, String> {
            let mut out = vec![];
            for group in self.0.split(',') {
                let mut ends = group.split('-');
                let start = ends
                    .next()
                    .unwrap()
                    .parse::<usize>()
                    .map_err(|e| e.to_string())?;
                let end = ends
                    .next()
                    .map(|s| s.parse::<usize>())
                    .transpose()
                    .map_err(|e| e.to_string())?
                    .unwrap_or(start);
                out.extend(start..=end);
            }
            Ok(out)
        }
    }
}
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let started = Instant::now();
    let started_unix_ms = SystemTime::now()
        .duration_since(UNIX_EPOCH)?
        .as_millis()
        .try_into()?;
    tracing_subscriber::fmt()
        .json()
        .with_writer(std::io::stderr)
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "proofserve_engine::resources=info".into()),
        )
        .init();
    let mut args = std::env::args().skip(1);
    let command = args.next().unwrap_or_else(|| "--help".into());
    if command == "--help" || command == "help" {
        println!(
            "proofserve check PROJECT [--workers N] [--checkpoint-dir DIR] [--root MODULE ... | --root-file FILE] [--closure-roots N] [--strict-theorem-bodies]\nproofserve audit PROJECT [--json FILE|-] [--receipt FILE]\nproofserve serve (--repl PATH | --lean PATH) --project DIR --environment ID [OPTIONS]\n\nAdvanced candidate interfaces: batch, measure, compare.\nProject commands require the full release bundle: proofserve-check and proofserve-audit beside this executable or on PATH."
        );
        return Ok(());
    }
    if command == "--version" || command == "-V" {
        println!("proofserve {}", env!("CARGO_PKG_VERSION"));
        return Ok(());
    }
    if matches!(command.as_str(), "check" | "audit") {
        return project::run(&command, std::env::args_os().skip(2).collect());
    }
    if command == "compare" {
        let baseline = args.next().ok_or("baseline capture path required")?;
        let candidate = args.next().ok_or("candidate capture path required")?;
        if args.next().is_some() {
            return Err("compare takes exactly two capture paths".into());
        }
        let baseline = serde_json::from_slice(&std::fs::read(baseline)?)?;
        let candidate = serde_json::from_slice(&std::fs::read(candidate)?)?;
        let report = proofserve::measurement::compare(&baseline, &candidate)?;
        println!("{}", serde_json::to_string_pretty(&report)?);
        return Ok(());
    }
    if !matches!(command.as_str(), "serve" | "batch" | "measure") {
        return Err("expected check, audit, serve, batch, measure or compare".into());
    }
    let mut options = HashMap::new();
    let mut lean_args = Vec::new();
    while let Some(key) = args.next() {
        if ![
            "--repl",
            "--lean",
            "--lean-arg",
            "--source-file",
            "--stderr-dir",
            "--project",
            "--environment",
            "--cpus",
            "--worker-cores",
            "--memory-gib",
            "--listen",
            "--policy",
            "--prepared-host",
            "--sysroot",
        ]
        .contains(&key.as_str())
        {
            return Err(format!("unknown option {key}").into());
        }
        let value = args
            .next()
            .ok_or_else(|| format!("missing value for {key}"))?;
        if key == "--lean-arg" {
            lean_args.push(value);
            continue;
        }
        if options.insert(key.clone(), value).is_some() {
            return Err(format!("duplicate {key}").into());
        }
    }
    let required = |key: &str| {
        options
            .get(key)
            .cloned()
            .ok_or_else(|| format!("{key} is required"))
    };
    let eligible = cpu_eligibility()?;
    let cpus = if let Some(text) = options.get("--cpus") {
        text.split(',')
            .map(str::parse::<usize>)
            .collect::<Result<Vec<_>, _>>()?
    } else {
        resources::cpus(eligible.clone())?
    };
    if cpus.iter().any(|cpu| !eligible.contains(cpu)) {
        return Err("CPU outside current eligibility".into());
    }
    let config = Config {
        memory_bytes: match options.get("--memory-gib") {
            Some(text) => text
                .parse::<u64>()?
                .checked_mul(1024 * 1024 * 1024)
                .ok_or("memory size overflow")?,
            None => resources::memory_bytes()?,
        },
        cpus,
        cores_per_worker: options
            .get("--worker-cores")
            .map(|s| s.parse())
            .transpose()?
            .unwrap_or(1),
    };
    let environment = required("--environment")?;
    let project = PathBuf::from(required("--project")?).canonicalize()?;
    let verifier: Arc<dyn VerificationBackend> =
        match (options.get("--repl"), options.get("--lean")) {
            (Some(program), None) => {
                if !lean_args.is_empty()
                    || options.contains_key("--source-file")
                    || options.contains_key("--stderr-dir")
                {
                    return Err("--lean-arg, --source-file and --stderr-dir require --lean".into());
                }
                let backend = NativeRepl {
                    program: PathBuf::from(program).canonicalize()?,
                    args: vec![],
                    project,
                    environment: environment.clone(),
                };
                match (options.get("--prepared-host"), options.get("--sysroot")) {
                    (None, None) => Arc::new(backend),
                    (Some(host), Some(sysroot)) => Arc::new(proofserve_lean::PreparedRepl::new(
                        backend,
                        PathBuf::from(host).canonicalize()?,
                        PathBuf::from(sysroot).canonicalize()?,
                    )),
                    _ => return Err("--prepared-host and --sysroot are required together".into()),
                }
            }
            (None, Some(program)) => {
                if options.contains_key("--prepared-host") || options.contains_key("--sysroot") {
                    return Err("prepared import parent requires --repl".into());
                }
                let backend = NativeLean {
                    program: PathBuf::from(program).canonicalize()?,
                    project,
                    environment: environment.clone(),
                };
                let mut configured = match options.get("--source-file") {
                    Some(path) => backend.with_source_file(PathBuf::from(path), lean_args),
                    None => backend.with_args(lean_args),
                };
                if let Some(directory) = options.get("--stderr-dir") {
                    configured = configured.with_stderr_dir(PathBuf::from(directory));
                }
                Arc::new(configured)
            }
            _ => return Err("specify exactly one of --repl or --lean".into()),
        };
    proofserve_engine::linux::bind_current_thread(&config.cpus)?;
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(config.cpus.len())
        .enable_all()
        .build()?;
    let result = runtime.block_on(run(
        command,
        options,
        config,
        verifier,
        environment,
        started,
        started_unix_ms,
    ));
    // Engine shutdown has awaited native retirement. Tokio's blocking stdin
    // read cannot be cancelled; do not wait for caller EOF after a signal.
    runtime.shutdown_background();
    result
}

async fn run(
    command: String,
    options: HashMap<String, String>,
    config: Config,
    verifier: Arc<dyn VerificationBackend>,
    environment: String,
    started: Instant,
    started_unix_ms: u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let policy_name = options
        .get("--policy")
        .map(String::as_str)
        .unwrap_or("fifo");
    let policy: Arc<dyn proofserve_core::SchedulingPolicy> = match policy_name {
        "fifo" => Arc::new(Fifo),
        "source-size" => Arc::new(SourceSize),
        "task-interleave" => Arc::new(TaskInterleave::new(Fifo)),
        "task-memory" => Arc::new(TaskMemory::new(Fifo)),
        _ => return Err("unknown scheduling policy".into()),
    };
    let backend_identity = verifier.identity();
    let engine = Engine::new(
        config.clone(),
        verifier,
        policy,
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )?;
    // Install termination handling before any candidate can start. SIGTERM
    // otherwise bypasses Drop and leaves native children outside accounting.
    let mut terminate = tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())?;
    let stopping = async move {
        tokio::select! {
            signal = tokio::signal::ctrl_c() => signal.map(|_| "SIGINT"),
            _ = terminate.recv() => Ok::<_, std::io::Error>("SIGTERM"),
        }
    };
    if command == "serve" {
        let listener = tokio::net::TcpListener::bind(
            options
                .get("--listen")
                .map(String::as_str)
                .unwrap_or("127.0.0.1:3000"),
        )
        .await?;
        let shutdown = engine.clone();
        axum::serve(listener, proofserve::router(engine))
            .with_graceful_shutdown(async move {
                if let Err(error) = stopping.await {
                    tracing::warn!(%error, "shutdown signal handler failed");
                }
                shutdown.shutdown().await;
            })
            .await?;
        return Ok(());
    }
    let work = async {
        if command == "measure" {
            let mut source = String::new();
            tokio::io::stdin().read_to_string(&mut source).await?;
            let batch: Batch = serde_json::from_str(&source)?;
            let results = engine.verify_batch(batch.clone()).await?;
            engine.shutdown().await;
            let capture = proofserve::measurement::Capture {
                schema_version: 1,
                engine_version: env!("CARGO_PKG_VERSION").into(),
                environment,
                backend: backend_identity,
                policy: policy_name.into(),
                resources: config,
                batch,
                results,
                started_unix_ms,
                lifecycle_seconds: started.elapsed().as_secs_f64(),
            };
            let mut stdout = tokio::io::stdout();
            stdout
                .write_all(serde_json::to_string(&capture)?.as_bytes())
                .await?;
            stdout.write_all(b"\n").await?;
            stdout.flush().await?;
        } else if command == "batch" {
            let mut lines = BufReader::new(tokio::io::stdin()).lines();
            let mut stdout = tokio::io::stdout();
            while let Some(line) = lines.next_line().await? {
                let response = match serde_json::from_str::<Batch>(&line) {
                    Ok(batch) => match engine.verify_batch(batch).await {
                        Ok(results) => serde_json::json!({"results":results}),
                        Err(error) => serde_json::json!({"error":error}),
                    },
                    Err(error) => serde_json::json!({"error":error.to_string()}),
                };
                stdout
                    .write_all(serde_json::to_string(&response)?.as_bytes())
                    .await?;
                stdout.write_all(b"\n").await?;
                stdout.flush().await?;
            }
            engine.shutdown().await;
        }
        Ok::<_, Box<dyn std::error::Error>>(())
    };
    tokio::select! {
        result = work => {
            if result.is_err() {
                engine.shutdown().await;
            }
            result
        },
        signal = stopping => {
            engine.shutdown().await;
            Err(format!("{}; owned verification attempts retired", signal?).into())
        }
    }
}
