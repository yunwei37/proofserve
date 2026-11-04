# CLI integration contract

Build with the matching toolchain by running lake build in checker/.
The native executable is .lake/build/bin/proofserve-check. Its CLI and receipt
format are documented in README.md and docs/receipt-schema.md.

Invoke the executable directly. It discovers the project search path through
lake env. The wrapper must preserve native exit codes 0, 1, and 2, JSON stdout,
and stderr warnings. Custom layouts can repeat --root MODULE.
--max-segments N stops a finite batch; repeating the command resumes it.

After building, run python3 tests/contract.py. This creates a temporary portable
Lake project and checks correctness, worker parity, official acceptance parity,
three bad proof terms, axiom reporting, bounded resume, and version errors.
CI wiring and release packaging are O-owned and are not modified here.

Each timing cell requires a fresh checkpoint directory. A cached complete
receipt is not a fresh verification. Record the exact executable commit.
Official fallback is identified in the receipt and is excluded from native
parallel performance results.

Large root manifests use --root-file FILE. --closure-roots N bounds the number
of requested roots in each independent complete closure; its default is 500.
Zero selects the original single frontier. These flags also work with explicit
--root arguments; --root-file is honored by the official fallback.

The top-level receipt can include batches and context_strategy. Wrappers should
preserve these fields and accept additive version-1 fields. Do not equate
cumulative_segment_cpu_ns with one check of each unique declaration: separate
batches can repeat dependencies.

The independent-batch default reuses exact-input completed imports. Additive
receipt fields identify the reused local certificates and distinguish
module_check_entries from trusted_import_entries. --replay-shared-imports
selects the earlier repeated-replay behavior. Wrappers must preserve the trust
metadata and must not call a certificate import a fresh kernel proof check.
