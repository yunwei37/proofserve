# SubexponentialSAT complete-closure measurement: actual progress

Review: 自审.

**Historical whole-library point:2488 /163097accepted source IDs;10744dependencies;0.694505kernelCPUh;32attempts/31successful;9124producer errors/151485blocked. It is partial and retired, not this SubexponentialSAT denominator.**

**SubexponentialSAT phase source: baseline source coverage 10769/14721 closure nodes (reused 10744, new 25) (25/3977targets); kernel accepts 0/3977targets and 0dependencies; kernelCPU 0.000000h; current segment 0; at least 30 segments (500 nodes each) remain.**

These are separate experiment costs. No global CPU estimate is formed by adding or rescaling this prefix. Producer uses official SDK/cache Meta/IR; checker consumes exact source-produced terms. Same-capture immutable shared source artifacts and actual compiler costs are charged once per complete closure; newly built targets use -o/-i/-c. This is summed source compiler work, not a fresh parallel Lake wall time. Oracle cost is a separate qualification. All timing uses P0–7/shared flock/no-M,12GiB total allocation. A complete CPU ratio requires full source, stream and original module-local coverage.

- complete: False
- phase: source
- target_modules: 3977
- closure_modules: 14721
- source_built: 10769
- reused_source_nodes: 10744
- new_source_nodes_built: 25
- source_targets_built: 25
- source_cpu_s: 25479.438249
- source_reused_cpu_s: 25373.748385
- source_new_cpu_s: 105.689864
- kernel_accepted_targets: 0
- kernel_accepted_dependencies: 0
- kernel_cpu_s: 0
- kernel_cpu_h: 0.0
- current_segment: 0
- remaining_segments_min: 30
- oracle_qualified: 10744
- kernel_peak_rss_gib: 0.0
- kernel_over_source_cpu: None

## User12h route decision after the finite pilot

Review: 自审. All25source calls succeeded; mean4.227595CPU-s/target. Full comparison projection **12.350CPUh**, including7.048263h retained common source work, exceeds12h. Remaining native forecast including2h reference reserve is7.272h; this is not charged as already executed. Conservatively honoring the total-comparison condition, the full queue is not launched. All25typed inputs/raw results are retained, fresh stream0/3977. Next: complete Transonic466. This25-file dependency-ordered pilot is not an unbiased3977cost estimate or proof failure.


## Active user clarification (supersedes preceding route stop)

Resume from25/3977successful target builds.12hmeans remaining new work:
5.272200h projected production+stream,7.272200h including2h reference reserve.
The7.048263h completed dependency source work will not rerun and remains
charged only in the full-closure comparison denominator. Wait for the already
started Transonic pilot to retire, then continue. Previous stop interpretation
is retained above as history; it is no longer the current route decision.
