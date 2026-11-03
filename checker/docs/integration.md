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
