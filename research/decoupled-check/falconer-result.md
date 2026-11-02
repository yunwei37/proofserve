# Complete Falconer project extension: observed status

Self-review.

- closure_modules: 13205
- successful_source_nodes: 12567
- construction_complete: False
- reused_same_capture_nodes: 5077
- source_compiler_wall_s: 20578.094975524582
- successful_source_work_s: 20578.041878368706
- retained_failed_native_work_s: 0.05309715587645769
- matched_stream_wall_s: None
- acceptance_parity_complete: False
- finalized_check_over_source_ratio: None
- module_local_fallbacks: None
- status: partial
- failure: None

Only complete exit0 cells and the full per-module acceptance comparison finalize a ratio. The numerator consumes exact newly constructed artifacts. Common dependency nodes reuse actual successful compiler cells and immutable artifacts from this same pinned experiment; their work is charged once per complete dependency closure. This is summed native compiler work, not parallel Lake wall time, a whole AI source-verification speedup, or a fresh reconstruction of shared nodes. Source failure, missing typed inputs, resource/timeout and graph mismatch stay explicit. A nonzero module-local fallback count means context segmentation, not one global environment. Memory checkpoints belong to a separate profiling pass; primary timing has them disabled.
