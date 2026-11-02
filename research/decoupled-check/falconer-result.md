> Completed 2026-11-02: all 13,205 modules have matching source, segmented
> original-kernel and module-local reference acceptance. Checking costs
> 2,043.59 s / 22,077.77 s = 9.26%, including checkpoint I/O.
> See [paper-ready result](falconer-paper-result.md) and
> [full completed reduction](falconer-final-analysis.md).
> The earlier partial observation below remains historical evidence.

# Complete Falconer project extension: observed status

Self-review.

- closure_modules: 13205
- successful_source_nodes: 13205
- construction_complete: True
- reused_same_capture_nodes: 5077
- source_compiler_wall_s: 22077.823345420882
- successful_source_work_s: 22077.770248265006
- retained_failed_native_work_s: 0.05309715587645769
- matched_stream_wall_s: None
- acceptance_parity_complete: False
- finalized_check_over_source_ratio: None
- module_local_fallbacks: None
- status: partial
- failure: None

Only complete exit0 cells and the full per-module acceptance comparison finalize a ratio. The numerator consumes exact newly constructed artifacts. Common dependency nodes reuse actual successful compiler cells and immutable artifacts from this same pinned experiment; their work is charged once per complete dependency closure. This is summed native compiler work, not parallel Lake wall time, a whole AI source-verification speedup, or a fresh reconstruction of shared nodes. Source failure, missing typed inputs, resource/timeout and graph mismatch stay explicit. A nonzero module-local fallback count means context segmentation, not one global environment. Memory checkpoints belong to a separate profiling pass; primary timing has them disabled.
