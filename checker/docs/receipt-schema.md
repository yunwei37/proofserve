# Receipt format, version 1

The executable prints one JSON object and saves the same object as receipt.json
in the checkpoint directory. Native exit codes are 0 for complete checking,
1 for a kernel rejection, and 2 for an unsupported configuration or an operational
failure. An interrupted process may leave successful segment records without a
final receipt; these are not a complete verification.

## Native path

The execution_path field is proofserve-parallel and parallel is true. The fields
are schema_version, lean_version, mathlib_manifest (the unaltered Lake lock),
roots, accepted (ordered module names), rejected (kernel diagnostics), status,
module_set_hash, module_set_hash_algorithm, axioms, workers, cpu_ns, wall_ns,
cumulative_segment_cpu_ns, segments, and trusted_local_checkpoints.

The module hash is Lean's deterministic 64-bit hash of sorted accepted names.
It is not cryptographic. The axiom list contains declarations in the accepted
closure, including accepted segregated modules; it is not a minimal per-theorem
axiom dependency set.

cpu_ns measures this invocation's CPU, including waited child processes.
cumulative_segment_cpu_ns also includes reused successful segment work.
wall_ns includes this invocation's discovery, input identity checks, checkpoint
imports and exports. Each segment entry identifies whether it was reused.
These quantities must remain separate when reporting resume overhead.

No complete receipt is produced for an unfinished requested closure. Input-part
hashes and the Lake manifest must match before a success is reused. This detects
ordinary stale inputs, not adversarial checkpoint modification.

## Official fallback

The execution_path field is official-leanchecker and parallel is false. A warning
is written to stderr. The receipt contains accepted_roots, rejected_roots,
official_results, coverage, version, CPU and wall time. accepted, rejected,
module_set_hash, and axioms are null because the official CLI does not expose the
corresponding per-module ledger or axiom report.

Official --fresh checks a final imported environment per root. It has a distinct
duplicate-proof policy and must not be presented as identical to the native
per-module procedure. A failed official invocation is official_failure and exits
2; its diagnostic is retained without inventing a kernel-rejection classification.

## JSON types

UInt64 values are decimal strings, following Lean's JSON instances. In particular,
cpu_ns, cumulative_segment_cpu_ns, and module_set_hash are strings, not JSON
floating-point numbers. wall_ns, workers, schema_version, and segment indices
are JSON integers. Consumers should parse decimal strings losslessly.

| Field | Native type | Official fallback type |
|---|---|---|
| execution_path | proofserve-parallel | official-leanchecker |
| parallel | true | false |
| project_revision | string or null | string or null |
| mathlib_manifest | object or null | object or null |
| roots | array of strings | array of strings |
| accepted | array of module names | null |
| rejected | array of diagnostic objects | null |
| module_set_hash | decimal UInt64 string | null |
| axioms | array of declared axiom names | null |
| workers | positive integer | absent |
| segments | array of {segment: integer, reused: boolean} | absent |
| accepted_roots | absent | array of strings |
| rejected_roots | absent | array of official-result objects |
| official_results | absent | array of {root, exit_code, stdout, stderr} |

A native rejected diagnostic identifies a module that did not verify; inspect
its error text before classifying the cause. It does not mean the theorem's
statement is false. Configuration errors can instead produce only an error JSON
object on stderr and no new receipt. A caller must respect the process exit code
and must not treat an older receipt file as the output of that failed invocation.
