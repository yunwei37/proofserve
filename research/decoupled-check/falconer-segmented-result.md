# Falconer segmented original-kernel checking

Self-review.

- accepted_modules: 11500
- expected_modules: 13205
- complete: False
- native_graph_match: False
- segments: 23
- native_wall_sum_s: 1935.9504093239084
- ratio_over_source: None
- pending: 1705
- single_uninterrupted_process: False

Each native process checks at most500 new modules then exports only original-kernel-accepted constants and pure audit metadata. Delta snapshots import only the successful preceding certified snapshot. New processes reload that checked prefix; they do not rerun its proofs. This is one chained validation of frozen artifacts, not a standalone verifier of an untrusted supplied snapshot or a cross-candidate result cache. All startup, snapshot writing/loading and normal exits are charged. A complete ratio here is segmented work, never an uninterrupted single-process number. The failed1500s full-check attempts and separately run module-local differential chunks remain explicit. Native final import-graph equality and all13,205 acceptance events are required for completion; module-local reference equality is a separate condition.
