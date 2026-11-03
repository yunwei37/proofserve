# Step031: first complete closure control; finite native matrix active
EXPERIMENT: frozen8512f8bcontroller actually running, PID521779/birth772750714.
First cell P4ordinary-before complete4,449accepted reference modules,
237,863ordinary checks/3,283,925,639allocation units. Wall360.887s,
user653.738s/system5.272s, sampled own tree peak3,273,822,208bytes.
Next P4stat really blocking on flock PID523189/birth772793965; original
native/cgroup retired. No duplicate or alternate measurement, no Lean patch.

The finite sequence retains ordinary-before/stat/record/ordinary-after at
4,8,1,2workers. Each cell owns only one lock/native and releases before
requeueing; overall16points is not complete. Fresh after-controls and other
workers cannot be borrowed from prior runs. Observation is via retained
native/controller terminals, not an old running label.

WRITE: added offline aggregator for native/PMU/thread/sample strata and
ordinary timing brackets. Ran it against actual partial native data:1/16,
no problems; it reports partial status and never fills missing cells.
Offline decode uses an explicit1GiBown analysis cgroup+RSSlimit, CPU8-15,
alongside native14GiBbound, leaving approximately1GiBfor lane parent processes
within16GiB. It is not another Lean process or timing sample. Initial decoder
qualification was serial and <=0.24GiBsampled RSS; native/cgroup resources
remain in raw files. Decoder inventory and thread counts use separate report
commands. This only prepares the already-admitted cause analysis.

REVIEW 自审: actual first-full accepted set/work/retirement verified. Complete
closure still has no worker-count PMUcomparison, so RCcontention cause remains
unknown. Source notes and prior CCPUinflation motivate a test, not a result.
Only owned path, no other lane lock/process touched; main/pull-rebase-before
push/foreign-dirty preservation retained. Rawperf files stayPVC.
