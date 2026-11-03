# Ramsey finite source windows and unchanged native measurements

Review: 自审. 2026-11-03 UTC.

The first two source calls used0.837190 and3.734883 wall seconds, but each
separately rejoined the cross-line P-core queue. The source dispatcher now
groups at most25 sequential compiler calls in one finite lock window.
It starts another call only while the window has used less than200 seconds;
each native call retains its original1400-second timeout, flags, inputs,
cgroup, rusage and independent start/end clock. The1740-second outer task
remains. The longest possible fresh call therefore still fits the window.
Every window joins the existing FIFO flock after all earlier waiters.

The old Python dispatcher was retired while waiting on its separate-session
worker. No Lean or queued flock worker was signalled, cancelled or restarted.
At handoff, the already queued source worker491365/birth771791896 (index9974)
was preserved. Its original frozen version2 file remains unchanged.
Version3 waits for that exact worker to retire before reading its state and
continuing; all preceding source cells and logs remain in place. This is a
dispatcher continuation, not a new measured denominator or an overlapping run.

Every completed window now publishes source x/444, kernel x/444, dependency
count, source/kernel CPU and remaining segment lower bound into both
Ramsey and whole-library progress. Kernel and reference tasks retain their
previous per-task lock/timeout protocol. No source-body or compiled adapter
was modified. Before acquiring another task, the controller checks the user's
85% PVC ceiling and stops its own queue if already reached; a sample cannot
promise a global filesystem hard quota or control another line's writes.

The primary full ratio still requires444/444 source targets,11188/11188
stream modules and11188/11188 module-local qualifications. Existing2488/163097
global acceptance is not relabelled as full coverage.
