# Receipt v1
One JSON stdout object,also checkpoint-dir/receipt.json. Exit0 complete,
1 kernel rejection,2 unsupported/configuration/operational failure.
Fields: schema_version=1;lean_version;mathlib_manifest (unaltered Lake lock);
roots;accepted ordered module names;rejected kernel diagnostic events;
status complete/rejected/incomplete;module_set_hash;module_set_hash_algorithm;
axioms;workers;cpu_ns;wall_ns;segments(index,reused);trusted_local_checkpoints=true. Axioms lists declarations in the accepted closure,\nincluding accepted segregated modules; it is not a per-theorem minimal axiom set.
Hash is deterministic Lean4.34.1 hash64 of sorted accepted names,not cryptographic.
cpu_ns is this invocation self+waited-child CPU; cumulative_segment_cpu_ns also\nincludes successful reused segments. Wall is this
invocation including discovery/input identity and checkpoint restoration.
Interrupted segments are never certified. No complete receipt for an unfinished
closure. Input-part hashes and manifest must match before success is reused;
this detects ordinary stale artifacts,not malicious collision or tampering.
