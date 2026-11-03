# Step050: source-checked causal persistence ablation
EXPERIMENT_GATE: user requests a causal removal test for RQ3 negative scaling.
Matched SDK4.34.1commit5045d005 source and frozen fd1e9be core read. The stream
does not explicitly mark reconstructed bases. Input compacted objects may
already have RC0: direct root/CI probes are prepared before claiming anything.
Stock leanchecker module tasks call finalizeImport false/false, so the user's
stock-already-marked premise is not assumed. Public leakEnv defaults false.

WRITE_GATE: persistent/plan.md freezes same-binary flag0/1,3plain+1stat per
arm×1/2/4/8P, fixed full4,449 closure, no-M, P lock,14GiB guards inside16GiB,
fresh bad-proof controls, object-state/memory/mark-cost observations. Thin
adapter calls the official one-argument lean_runtime_mark_persistent export;
does not modify the kernel or skip checking. No data yet.
Prior exact build~14s/~1.7GiB motivates an untimed E-core serial build, not a
Mathlib rebuild. Initial source-write syntax error occurred before execution;
corrected files are prepared, not qualified or benchmark results.

REVIEW_GATE 自审: task closure consumption and recursive result mark_mt precede
result publication in matched runtime source, consistent with joining all prior
tasks before next marking. No current workers exist at the mark site. Unsafe
runtime precondition and process-lifetime memory leakage stay explicit. Stock
leaf/default/fresh scopes will not be silently equated to independent closure
checking. Build/source qualification and full evidence remain to execute.
