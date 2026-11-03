# Ramsey complete-closure measurement: actual progress

Review: 自审.

**Historical whole-library point:2488 /163097accepted source IDs;10744dependencies;0.694505kernelCPUh;32attempts/31successful;9124producer errors/151485blocked. It is partial and retired, not this Ramsey denominator.**

**Ramsey phase source: baseline source coverage 10934/11188 closure nodes (reused 10744, new 190) (190/444targets); kernel accepts 0/444targets and 0dependencies; kernelCPU 0.000000h; current segment 0; at least 23 segments (500 nodes each) remain.**

These are separate experiment costs. No global CPU estimate is formed by adding or rescaling this prefix. Producer uses official SDK/cache Meta/IR; checker consumes exact source-produced terms. Same-capture immutable shared source artifacts and actual compiler costs are charged once per complete closure; newly built targets use -o/-i/-c. This is summed source compiler work, not a fresh parallel Lake wall time. Oracle cost is a separate qualification. All timing uses P0–7/shared flock/no-M,12GiB total allocation. A complete CPU ratio requires full source, stream and original module-local coverage.

- complete: False
- phase: source
- target_modules: 444
- closure_modules: 11188
- source_built: 10934
- reused_source_nodes: 10744
- new_source_nodes_built: 190
- source_targets_built: 190
- source_cpu_s: 47519.846815
- source_reused_cpu_s: 25373.748385
- source_new_cpu_s: 22146.098430000002
- kernel_accepted_targets: 0
- kernel_accepted_dependencies: 0
- kernel_cpu_s: 0
- kernel_cpu_h: 0.0
- current_segment: 0
- remaining_segments_min: 23
- oracle_qualified: 10745
- kernel_peak_rss_gib: 0.0
- kernel_over_source_cpu: None

## User-directed stop after the last completed window

Review: 自审. Stopped at **190/444** target source builds (**10934/11188** closure nodes), including one window completed after the earlier189 count. New target production consumed **22146.098430 CPU-s (6.151694 h)**; retained common source work is **25373.748385 CPU-s**. No full-closure stream ran: **0/444 stream-accepted targets**, **0 stream CPU-s**. The existing K10 module-local reference remains separate.

The current native window had already exited. PID548230/birth773592704 was confirmed only as a **waiting** flock request in /proc/locks; only that next waiter was cancelled. Controller491697/birth771798493 then retired normally. No Lean was signalled. The shared lock is owned by another line; no Ramsey waiter remains. Reason: sustained heavy certificate production, near-budget11.53GiB K10, and shared P-core opportunity cost. Complete Ramsey production is cancelled; all190 typed outputs and raw/failed/partial records remain. Subsequent numbers will be size-stratified module-local samples of this dependency-ordered, nonrandom prefix, not a complete directory ratio.

<!-- retained-prefix-sample -->
Production stopped190/444; full stream0/444,0CPUh. Size sample **16/20 accepted**, **0 failures**, **0.003655 referenceCPUh**. [Sample](ramsey-sample-result.md).
