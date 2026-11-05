# ProofServe closure plan

Deliver ProofServe and the six-page empirical + system paper by
**6 November 2026, 20:00 UTC**. **The latest six-hour continuation supersedes
the preceding stop. W continues segment 2 with a hard 03:00 UTC reporting
cutoff; final N means modules completed by that cutoff.**

## Current execution and cutoff

Segment 1 is retained unchanged: 128,331 completed executable modules,
134.651176 P CPUh / 256.667855 E CPUh and 24.624733 supervisor wall-hours.
This is a baseline snapshot, not final N. Segment 2 actually executes under
05c91979; the earlier b781 preparation had no native launches and is not a
third measured segment.

Segment 1 uses fixed 22-slot admission with reserve drains/exclusive retry.
Segment 2 uses memory/headroom admission and limits exposure to interrupted
families. The actual 05c implementation defers specified high-memory families
and dependents instead of applying positive family concurrency caps.
Record the real reasons, without inventing cap values. Compiler argv, -j8,
Lean settings and P/E pools stay fixed.

Report successful costs by segment and P/E, measured segment wall and its
sum, with transition gaps and unsuccessful work separate. Later completions
stay retained but do not enter the 03:00 cutoff count/costs. This is
dependency-ordered, selectively deferred coverage, not random sampling or
a full-library cost estimate.

W's current invocation stops admission at 03:00 and drains until 03:30,
which differs from the latest hard cutoff. Root does not modify foreign
controllers. Keep the discrepancy visible, restrict paper reporting to
03:00 and retain later drain time separately. Do not declare the machine
quiet or M running merely because the clock passed the cutoff.

## Measured source scope and scientific interpretation

At final publication W reports N completed executable modules out of 163,096
plus the distinct configuration unit, retaining failed, deferred, blocked,
unattempted and post-cutoff outcomes. The first-segment 128,331 observations
and 34,765 then-unfinished modules are historical, not final campaign scope.
No missing unit receives a successful status or zero cost.

This is a dependency-ordered observed subset, not a probability sample.
Later dependencies include the memory-intensive families that prompted the
second admission phase. Their missing costs may be higher. Do not infer
a full-library total, multiply by inverse coverage, or fill missing work with
the original 42 samples, a model or stratum weights. Successfully observed
P-core and E-core work supplies separate hardware-specific lower bounds on
the campaign's full-source work, not a converted hardware-independent total.

All CPU distributions, lexical marked/unmarked cost comparisons and
inside/outside-default-graph cost shares apply only to the measured subset.
Distinguish these from the full-frame lexical/source coverage inventory,
which retains its original known denominator. Show observed and unmeasured
coverage when joining these labels; neither subset representativeness nor
whole-corpus cost shares follow from the static frame.

Keep CPU=user+system by segment and P/E pool. Segment reporting wall is
bounded by the cutoff; actual later drain/supervisor wall is separate.
Transition gaps and summed native-module wall are distinct clocks.
Unsuccessful-attempt CPU is excluded from successful module costs.
No admission-policy speedup follows from the nonrandom segment split.

## Closure handoffs (all UTC, 2026)

| Milestone or budget | Owner and handoff |
|---|---|
| 5 November, 06:00 | M froze native e000ed62; retain shared-checked/strict semantics and review limits. |
| 5 November, 12:00 | Root prose and figure/table scripts prepared; update for the actual stopped scope and returned numbers. |
| 5 November, 14:00 | O frozen-native installation functional qualification; test-time preview provenance remains explicit. |
| 6 November, 03:00 | W cutoff; publish N completed-by-cutoff modules over both segments, retaining all other outcomes. |
| After 03:00, at most 6 hours | M executes the final matrix after actual retirement, lease release and a quiet machine. |
| Then, at most 2 hours | O executes final external-project timing. |
| Last, stop by 6 November, 17:00 | M checks only actually built artifacts, reporting the reached scope; partial or not-started remains possible. |
| 6 November, 18:00 | Root integrates actual numbers, six pages, zero missing macros. |
| 6 November, 20:00 | Close with tool, paper and explicit limitations. |

M's earlier c8f2a0c5 stopped-handoff preparation is superseded by this continuation boundary. Root reads actual owner
launch/terminal/receipt/PID-birth evidence and starts no replacement run.
The final matrix retains Nat.Basic/Grid at workers 1/2/4/8 and Barrier 1/8,
three repeats. Nat.Basic/Grid retain 8-worker no-persistence/no-split and
strict points. Barrier 2/4 is deliberately unmeasured. Official controls,
bad-proof checks and interruption/resumption keep their actual scope.
The 71-attempt design and planning models are not final performance.

The last checking phase is limited to available built artifacts, not all
163,096 source modules. Report unique accepted/input frame, attempted roots,
proof rejects, operational stops and unattempted inputs with tool/input
commits and available official references. A verified prefix is not complete
official parity. If no time remains, report not attempted without zero costs
or invented counts; this supplementary result is not required for the paper.
No separate PlanarPacking comparison is scheduled.

## Gate, tool policy and data handoff

The original total-instruction invariance gate remains failed: median
1.3312% and P95 3.1498% exceed unchanged 1%/3% criteria. Its 20-module,
four-condition, three-repeat foreground/control matrix and 1,413 background
attempts returned; aggregate counter-overhead medians passed. Root previously
recomputed the raw statistics. Cross-module workload comparison uses user-mode
instructions, explicitly selected after those results. This is not a passing
replacement gate or a guarantee of arbitrary-load invariance.

Lean 4.34.1, OpenAI math 4eaee875 and Mathlib d13f23b7 remain the input pins;
the original campaign used P0–7 and E10–23, -j8 and no -M (including -M0).
Its actual elapsed interval and resource interruptions describe that machine
and admission policy. Segment 2 is actual changed-admission execution, not the original fixed-admission protocol.

The frozen checker is e000ed62. Shared-checked default can accept a crafted
artifact through another module's checked same-interface theorem body while
official original-context replay rejects it. The proposition remains derivable
in the checked shared closure with its reported axioms; artifact-context parity
is a different guarantee. --strict-theorem-bodies selects the body-context
agreement route, retaining other IR/artifact/operational differences.
Strict cost comes only from matching final matrix rows, never old e155
isolation previews. Two read-only reviews have regression repairs; repaired
source has no independent runtime review.

Artifacts label the cutoff-completed observed subset and all deferred,
unmeasured and late identities. The first segment stays a separate snapshot
until actual cutoff artifacts return. No running snapshot becomes final N
or complete census coverage. W's final CSVs feed
distributions and P/E totals; no earlier sample/model supplies missing costs.
Final system data comes only from checker/results/ and data/external-projects/
with tool/input commits, policy and scope. Preview/fixture values cannot fill
final tables. Official default trusts imports and is not equal full-closure
work; no speedup or product of ratios is inferred from different obligations.

Keep original42 and superseded precision7/12 separately as historical evidence.
They are not pooled, resumed or used to complete stopped work.
The nealmcb report's 13.8h/32vCPU is measured wall; approximately 330 compiler
CPUh is extrapolated from 26 modules, and approximately 410 includes Comparator.
Those observations do not fill this campaign's missing work.

## Owners, paper and operations

M owns checker/; W tools/audit/ and data/openai-math-4eaee875/; O crates/,
CLI/README/Docker/CI/release, packaging/ and data/external-projects/.
Root owns docs/paper/, documentation/status and research/README.md.
No competing collector, agent, session, queue, journal injection or native run
is started by root. Owners choose implementation; do not add research
thresholds, approval loops or investigation limits. Freeze changes only for
real bugs, with affected evidence rerun by its owner.

Keep six pages including references, 10pt two columns, current scoped RQs and
at most four displays; no second long paper or step/audit directory.
Evidence and historical dispositions stay in docs/paper/evidence.md.
The tool delivers check/audit and the existing Kimina-compatible service;
serve receives defect fixes only. Unknown toolchains fail clearly or use an
explicit official path. Lean 4.35 lake check is already shipped.

**All root Workspace reads, analysis, Git and PDF compilation enter through
taskset -c 8,9 and inherit CPUs 8–9.** Never reuse CPU22–23 or rebind owners.
Preserve the same Workspace/PVC, raw/failed/interrupted/foreign work and disk
headroom below 85%. No restoration of deleted caches or repeated cleanup claims.
A real host outage still means preserve the scene and await its dedicated
operator handling; no recovery, replacement or scheduling change.
No UI/new login/network/Tailscale/credential/permission/infra change;
all CronJobs remain untouched.

Main only, commit --only owned paths. Try pull --rebase before push; on
foreign dirty refusal do not stash/reset/revert/amend/force. Fetch, verify
origin ancestry and push normally. Validated ordinary pushes are authorized;
tags, registries, upstream issues/PRs and announcements remain unapproved.
