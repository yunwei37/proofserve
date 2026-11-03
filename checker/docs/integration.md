# O-lane integration contract
Build: cd checker && lake build. No dependencies beyond pinned4.34.1 SDK and C compiler.
Native executable .lake/build/bin/proofserve-check. CLI and receipt schema are
documented in README.md and docs/receipt-schema.md. Invoke executable directly;
it discovers project search paths through lake env and rejects unknown toolchains.
Current roots default to compiled project artifacts; --root repeats support
custom Lake layouts. Rust wrapper must preserve exit0/1/2 and JSON/stderr.
--max-segments N is a finite batch stop; repeat the command to continue.
CI command after build: python3 tests/contract.py. It creates a portable temporary
Lake project,checks1/2/4workers and stock CLI parity,three original-kernel bad
terms,axiom reporting,successful-prefix resume and unsupported-version error.
CI wiring is O-owned and not modified here. No publication performed.
Evaluation must use a fresh checkpoint directory for each timing cell; otherwise
the receipt explicitly reuses earlier successful work. Never time cached completion
as a new verification. Native command CPU and frontend reported CPU are distinct.
