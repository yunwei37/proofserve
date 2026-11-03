# Step030: real record inherited-worker and stack qualification
EXPERIMENT: corrected q3record completed actual650 reference modules,42,301
ordinary checks/298,241,118allocation units, all native/cgroup retired, no
memory stop. File7.57MiB on PVC. Native wall33.397s differs from application
wall32.59s; perf flush/setup is retained, not folded into ordinary timings.
Read actual attrs: seven inherited PMUevents, cycles99Hz, six auxiliary
count-onlyperiod0.3980cycles samples,1120READrecords,zero lost samples in
report. All10observed historical worker TIDs have positivecycles/instructions
and allseven counters in the actual report-Ttable;10is not active concurrency.
Parent/time/coordinator totals are not summed with workers.

Native Python decoder actually ran on E8-15, all3980samples have positive
period. Ordinary-check+CPPkernel anchored116.332billion sampled periods;
unanchored worker kernel9.109billion; workerother/truncated2.372billion;
serial/other kernel29.331billion;outside9.314billion. Original event total
166.458billion periods. Anchored coverage is reported, not assumed100%.
Actual demangled leaf symbols include environmentfind,RCcold,hashmaps,
allocator and typechecker; decoder call order is leaf-to-root.

The first decoder category version is retained on PVC. Before full study,
source-informed family mapping includes mi_new_n/cfree and explicit environment
lookup paths. This changes analysis classification, not measured native code.
Inline RC remains unresolved inside other named operations; symbols alone
cannot decide RCcontention. Stat control is not a closure scaling result.

WRITE: small terminal/attrs/native counter table/scope metadata archived.
Use report --stats for READ/loss inventory separately: it exits before
report-Ttable printing. Ordinary report-T -g none emits the actual counters.
Record with no inherited-event coverage would have been invalid, not zero.

REVIEW 自审: real eventinherit1 and per-workerpositivevalues inspected, Cworker
set covered10/10, input/verdict reference preserved. Separate timed native,
decode CPU, whole-command counters, worker counters, anchored sample periods
and uncovered categories. No host settings or Lean code changed. Finite full
4/8/1/2 comparisons now admitted under the predeclared lock/budget design.
