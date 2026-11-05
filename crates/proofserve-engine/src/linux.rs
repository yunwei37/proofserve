//! Linux owned-process accounting. Never enumerate another tree as owned.
use proofserve_core::{ProcessIdentity, ProcessSample, ResourceMonitor, ResourceSnapshot};
use std::{
    collections::{HashMap, HashSet},
    fs,
    sync::Mutex,
};

#[derive(Clone)]
struct Stat {
    identity: ProcessIdentity,
    parent: u32,
    rss: u64,
}

fn stat(pid: u32) -> Result<Option<Stat>, String> {
    parse_stat(pid, fs::read_to_string(format!("/proc/{pid}/stat")))
}

fn parse_stat(pid: u32, read: std::io::Result<String>) -> Result<Option<Stat>, String> {
    let raw = match read {
        Ok(s) => s,
        // /proc can disappear before open (ENOENT) or during read (ESRCH).
        // Neither means a retired owned process still has memory to account.
        Err(e)
            if e.kind() == std::io::ErrorKind::NotFound
                || e.raw_os_error() == Some(libc::ESRCH) =>
        {
            return Ok(None);
        }
        Err(e) => return Err(e.to_string()),
    };
    let tail = raw.rsplit_once(')').ok_or("invalid proc stat")?.1;
    let fields: Vec<_> = tail.split_whitespace().collect();
    let n = |i: usize| -> Result<u64, String> {
        fields
            .get(i)
            .ok_or("short proc stat")?
            .parse()
            .map_err(|e| format!("{e}"))
    };
    // SAFETY: sysconf is thread safe and has no pointer arguments.
    let page = unsafe { libc::sysconf(libc::_SC_PAGESIZE) };
    if page <= 0 {
        return Err("cannot discover page size".into());
    }
    Ok(Some(Stat {
        identity: ProcessIdentity {
            pid,
            start_ticks: n(19)?,
        },
        parent: n(1)? as u32,
        rss: n(21)?.saturating_mul(page as u64),
    }))
}

/// Read the actual kernel birth identity; absent processes are not registered.
pub fn identity(pid: u32) -> Result<ProcessIdentity, String> {
    stat(pid)?
        .map(|s| s.identity)
        .ok_or_else(|| format!("process {pid} already exited"))
}

/// Linux /proc RSS, retaining discovered descendants across reparenting.
#[derive(Default)]
pub struct ProcMonitor {
    known: Mutex<HashMap<(u32, u64), Vec<ProcessIdentity>>>,
}
impl ResourceMonitor for ProcMonitor {
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        let mut table = HashMap::new();
        for e in fs::read_dir("/proc").map_err(|e| e.to_string())? {
            let e = e.map_err(|e| e.to_string())?;
            if let Ok(pid) = e.file_name().to_string_lossy().parse::<u32>() {
                // Registered identities below are checked strictly. Unrelated inaccessible
                // processes never become owned and need not be inspected.
                if let Ok(Some(s)) = stat(pid) {
                    table.insert(pid, s);
                }
            }
        }
        let mut accounted_roots = roots.to_vec();
        let own = identity(std::process::id())?;
        if !accounted_roots.contains(&own) {
            accounted_roots.push(own);
        }
        let mut known = self.known.lock().unwrap();
        let wanted: HashSet<_> = accounted_roots
            .iter()
            .map(|r| (r.pid, r.start_ticks))
            .collect();
        known.retain(|k, _| wanted.contains(k));
        let mut seen = HashSet::new();
        let mut result = ResourceSnapshot::default();
        for root in &accounted_roots {
            let key = (root.pid, root.start_ticks);
            let entries = known.entry(key).or_default();
            if let Some(current) = stat(root.pid)?
                && current.identity == *root
                && !entries.contains(root)
            {
                entries.push(root.clone());
            }
            // Retain only birth-matched live descendants. The engine root is
            // long-lived: retaining every retired child makes every admission
            // and watchdog tick revisit the whole request history.
            // Read known owned identities strictly before pruning: an access
            // error must not silently turn owned memory into unowned memory.
            let mut live = Vec::with_capacity(entries.len());
            for p in entries.iter() {
                if let Some(current) = stat(p.pid)?
                    && current.identity == *p
                {
                    table.insert(p.pid, current);
                    live.push(p.clone());
                }
            }
            *entries = live;
            loop {
                let before = entries.len();
                for s in table.values() {
                    if entries.iter().any(|p| {
                        p.pid == s.parent && table.get(&p.pid).is_some_and(|x| x.identity == *p)
                    }) && !entries.contains(&s.identity)
                    {
                        entries.push(s.identity.clone());
                    }
                }
                if entries.len() == before {
                    break;
                }
            }
            let mut rss = 0u64;
            for p in entries.iter() {
                if let Some(s) = stat(p.pid)?
                    && s.identity == *p
                {
                    rss = rss.saturating_add(s.rss);
                    if seen.insert((p.pid, p.start_ticks)) {
                        result.rss_bytes = result.rss_bytes.saturating_add(s.rss);
                    }
                }
            }
            if roots.contains(root) {
                result.processes.push(ProcessSample {
                    identity: root.clone(),
                    rss_bytes: rss,
                });
            }
        }
        if !seen.iter().any(|(pid, _)| *pid == std::process::id())
            && let Some(s) = stat(std::process::id())?
        {
            result.rss_bytes = result.rss_bytes.saturating_add(s.rss);
        }
        Ok(result)
    }
}

/// Bind the calling thread before constructing its runtime so new threads inherit
/// the same hardware budget. Existing unrelated threads are not reconfigured.
pub fn bind_current_thread(cpus: &[usize]) -> Result<(), String> {
    if cpus.is_empty() || cpus.iter().any(|id| *id >= libc::CPU_SETSIZE as usize) {
        return Err("invalid CPU mask".into());
    }
    // SAFETY: the CPU mask is initialized and sized for the kernel syscall.
    unsafe {
        let mut set: libc::cpu_set_t = std::mem::zeroed();
        libc::CPU_ZERO(&mut set);
        for cpu in cpus {
            libc::CPU_SET(*cpu, &mut set);
        }
        if libc::sched_setaffinity(0, std::mem::size_of_val(&set), &set) != 0 {
            return Err(std::io::Error::last_os_error().to_string());
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::process::{Child, Command};

    struct OwnedChild(Child);
    impl Drop for OwnedChild {
        fn drop(&mut self) {
            let _ = self.0.kill();
            let _ = self.0.wait();
        }
    }
    fn child() -> OwnedChild {
        use std::io::{BufRead, BufReader};
        let mut child = OwnedChild(
            Command::new("/usr/bin/python3")
                .args(["-u", "-c", "import time; print('ready'); time.sleep(60)"])
                .stdout(std::process::Stdio::piped())
                .spawn()
                .unwrap(),
        );
        // Successful exec alone can precede the first resident-page fault.
        // Synchronize with the real helper instead of racing an RSS>0 assertion.
        let mut ready = String::new();
        BufReader::new(child.0.stdout.take().unwrap())
            .read_line(&mut ready)
            .unwrap();
        assert_eq!(ready.trim(), "ready");
        child
    }

    #[test]
    fn stat_read_classifies_kernel_exit_races_as_absent() {
        for errno in [libc::ENOENT, libc::ESRCH] {
            let read = Err(std::io::Error::from_raw_os_error(errno));
            assert!(
                matches!(parse_stat(1, read), Ok(None)),
                "a process retired during /proc read must be absent (errno {errno})"
            );
        }
    }

    #[test]
    fn stat_read_keeps_access_and_io_errors_fatal() {
        for errno in [libc::EACCES, libc::EPERM, libc::EIO] {
            let error = std::io::Error::from_raw_os_error(errno);
            let expected = error.to_string();
            assert_eq!(parse_stat(1, Err(error)).err(), Some(expected));
        }
    }

    #[test]
    fn retired_descendants_do_not_accumulate_under_the_engine_root() {
        let own = identity(std::process::id()).unwrap();
        let monitor = ProcMonitor::default();
        for _ in 0..3 {
            let mut child = child();
            let born = identity(child.0.id()).unwrap();
            monitor.sample(&[]).unwrap();
            assert!(monitor.known.lock().unwrap()[&(own.pid, own.start_ticks)].contains(&born));
            child.0.kill().unwrap();
            child.0.wait().unwrap();
            monitor.sample(&[]).unwrap();
            assert!(
                !monitor.known.lock().unwrap()[&(own.pid, own.start_ticks)].contains(&born),
                "retired request identities must not grow every future RSS scan"
            );
        }
    }

    #[test]
    fn pruning_keeps_live_owned_births_and_discards_reused_pid_identity() {
        let own = identity(std::process::id()).unwrap();
        let child = child();
        let born = identity(child.0.id()).unwrap();
        let stale = ProcessIdentity {
            pid: born.pid,
            start_ticks: born.start_ticks + 1,
        };
        let monitor = ProcMonitor::default();
        monitor.known.lock().unwrap().insert(
            (own.pid, own.start_ticks),
            vec![own.clone(), born.clone(), stale.clone()],
        );
        let sample = monitor.sample(std::slice::from_ref(&born)).unwrap();
        assert!(sample.processes[0].rss_bytes > 0);
        let known = monitor.known.lock().unwrap();
        let retained = &known[&(own.pid, own.start_ticks)];
        assert!(retained.contains(&born));
        assert!(!retained.contains(&stale));
    }
}
