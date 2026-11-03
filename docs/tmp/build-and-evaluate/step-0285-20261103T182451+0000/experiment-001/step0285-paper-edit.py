from pathlib import Path
import os,json,re,gzip,shutil,tarfile
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-hybrid-source40-root-step.txt').read_text().strip());e=s/'experiment-001'
m=json.loads((e/'reanalysis.json').read_text());w=json.loads((e/'source40-reanalysis.json').read_text())
for n in ['hybrid','source40']:shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0285-'+n+'-recompute.py',e/('step0285-'+n+'-recompute.py'))
for archive in ['source40-raw-source.tar.gz']:
 count=size=0
 with tarfile.open(e/archive,'r:gz')as tf:
  for x in tf:
   if x.isfile():data=tf.extractfile(x).read();assert len(data)==x.size;count+=1;size+=len(data)
 with gzip.open(e/archive,'rb')as f:
  while f.read(1024*1024):pass
 (e/'source40-archive-integrity.json').write_text(json.dumps(dict(archive=archive,compressed_B=(e/archive).stat().st_size,members=count,payload_B=size,gzip_EOF=True))+'\n')
sid=s.name.removeprefix('step-');tag=r'\expref{'+sid+r'}{0285}'
p=r/'docs/paper/main.tex';t=p.read_text()
t=t.replace(r'\measured{\expref{0284-20261103T172738+0000}{0284}}'+'\nSource-frame coverage is now 39/42 with 19 complete strata and 3 missing',r'\measured{'+tag+'}\nSource-frame coverage is now 40/42 with 20 complete strata and 2 missing')
t=t.replace('The 39 completed no-'+r'\texttt{-M}'+' random source targets sum to 634.212 seconds\nof native wall intervals and 954.511 user-plus-system CPU seconds.','The 40 completed no-'+r'\texttt{-M}'+' random source targets sum to 651.160 seconds\nof native wall intervals and 978.678 user-plus-system CPU seconds.')
a=t.index(r'\measured{\expref{0284-20261103T172738+0000}{0284}; one further original-frame source cost.}');b=t.index('\nThese are source-compilation estimates',a)
t=t[:a]+r'''\measured{TAG; one further original-frame source cost.}
PacketLocality completes in 16.948 native elapsed seconds and 24.167 CPU seconds.
Together with the earlier AllocatedForecastPrimitiveCapBound draw,
it completes the 2,023-module ordinary stratum.
The covered domain now contains 163,057 modules across 20 strata.
Stratified compiler CPU is 57.546 hours in marked files and 220.545 hours
in other files, a conditional marked share of 20.69\%.
All nine marked strata have both draws, covering 5,848 marked modules.
One 40-module ordinary stratum and its two original costs remain unobserved.
Untimed E-core prerequisites receive no sampling weight.'''.replace('TAG',tag)+t[b:]
a=t.index(r'\paragraph{Clock choice and nonresponse alter the estimand.}');b=t.index(r'\paragraph{Source features do not establish bounded prediction error.}',a)
t=t[:a]+r'''\paragraph{Clock choice and nonresponse alter the estimand.}
\measured{TAG; same 20 complete source strata, offline arithmetic.}
The conditional marked share is 20.69\% of weighted compiler CPU and
16.52\% of summed native elapsed time, a 4.18-percentage-point difference.
The latter adds native process durations; it is not parallel Lake makespan
or an isolated checking-phase share of whole-library time.
CPU weights include worker execution; elapsed weights reflect each module's
wall duration at the measured concurrency point.
Earlier clock contrasts use different covered domains and are not a
population time trend.

The incomplete stratum contains 40 of 163,097 modules (0.0245\%),
not necessarily that many unbuilt files. Two original source costs are absent.
The 40 known terms in the eventual complete-sample Horvitz--Thompson point
sum to 278.092 CPU-hours, here equal to the complete-stratum subtotal.
Neither is a lower confidence limit or a zero-filled population estimate.
Increasing each missing draw by one CPU second would increase the eventual
point by 0.011111 CPU-hours under the fixed original weights.
This sensitivity does not predict missing costs or variance.

\paragraph{Narrow missing-cost scenarios do not imply precise sampling.}
\partialev{TAG; nominal sampling uncertainty for the 20 complete strata.}
Recomputing finite-population stratified variance from the same two original
draws per stratum gives an approximate 95\% Student-$t$ interval of
94.15--462.04 CPU-hours around the covered-domain estimate of 278.092 hours,
with Satterthwaite effective degrees of freedom 2.61.
The new complete stratum adds sampling variance as well as cost.
This nominal interval remains fragile with two observations per cell; it omits
the incomplete 40-module stratum, nonresponse, runtime drift and
protocol-transfer uncertainty. It is neither a full-frame confidence interval
nor a guaranteed bound. The narrower missing-cost scenarios below address
a different uncertainty and do not establish population-estimate precision.

\paragraph{Whole-frame costs require explicit missing-cost scenarios.}
\partialev{TAG; fixed 40-source sensitivity, not measurements
or confidence limits.}
Preserving 40 known costs and original inclusion weights, assume the two
remaining ordinary-marker draws cost between the observed ordinary minimum
and maximum, 1.204525--86.977989 CPU-s.
Whole-frame construction scenarios then span 278.1--279.1 CPU-hours,
with endpoints rounded outward.
The earlier 39-draw 271.6--296.8-hour scenario remains a dated assumption;
the much narrower completion scenario does not remove sampling uncertainty.

A separate transfer model gives 18.7--24.8 checking CPU-hours.
It assigns ordinary modules the complete checkpoint-closure CPU
fractions 0.063124--0.089514 and marked modules the older unsegmented
computation fractions 0.084421--0.084671.
This deliberately mixes protocol-specific anchors; it is neither a measured
matched protocol nor evidence that source markers identify checking cost.
The earlier 18.3--26.3-hour transfer used the 39-cost snapshot.
Neither model is measured whole-library checking cost, a confidence interval
or a guaranteed saving. Their known terms use all 40 observed draws; they
also differ from RQ2's trusted-import target checks and complete selected closures.

The LowBlock15\_1 observation remains 184.589 CPU-s, above the old
31-draw marked-class maximum of 163.846 CPU-s; the 86.978-second Allocated
ordinary observation also exceeded its earlier class maximum of 40.792 seconds.
Observed support is only an assumption.
Without missing-cost assumptions, the completion-cost upper remains unbounded.
Assigning both missing draws ten times the current ordinary maximum raises
the source scenario to 287.8 CPU-hours.
A subunit checking factor assigned to unknown modules cannot establish
general benefit. Both unobserved original costs remain missing in the primary evidence.

'''.replace('TAG',tag)+t[b:]
addition=r'''
\paragraph{Whole-module fallback is an avoidable prototype policy.}
\measured{TAG; six fresh unprofiled processes, three per arm.}
A same-executable ablation retains default persistence and eight workers,
changing only whether nonordinary modules fall back as a whole.
The alternative retains a dependency-closed prefix of inductives,
constructors, recursors, quotient declarations and their ordinary prerequisites
for original-kernel replay; it then checks the remaining ordinary declarations
in parallel. It introduces no temporary axiom skeleton or mathematical
declaration rewriting. All six runs accept the identical ordered 4,449-module
closure, matching the original serial reference graph and counts:
425,463 entries, 3,595 upstream unsafe/partial exclusions and no module-local
context fallback.

Whole-module and prefix-only arms have native wall medians 257.659 and
196.669 seconds, with ranges 257.410--257.711 and 194.488--199.060 seconds.
The ratio of medians is 1.310, or 23.67\% less wall time.
Native CPU medians are 542.369 and 542.942 seconds, a 0.106\% increase;
three observations do not establish zero overhead.
Median wait4 peak RSS rises from 3.217 to 3.277 GiB,
an observed process peak rather than exact retained-object cost.
Repeat two reverses arm order; caches remain.
This compares two policies of the same eight-worker prototype, rather than
the original serial stream or an equivalent native module-task service.
It must not be multiplied by the Mathlib/Grid ratios or combined with
an older Barrier serial denominator.

\measured{TAG; a separate traced diagnostic pair.}
All 1,231 formerly complex-module fallbacks become plannable after the prefix.
Of their 183,645 incoming safe constants, 168,713 ordinary constants move
to parallel checking; 14,932 remain in original replay, including 1,636 ordinary
prerequisites, 3,819 inductive entries, 5,542 constructors, 3,931 recursors
and four quotient entries.
On this diagnostic's own clocks, upstream-replay wall falls from 94.479 to
1.792 seconds. Total native wall is 271.181 versus 211.675 seconds;
parallel batch windows rise from 112.951 to 141.024 seconds.
Read/context/planning windows are 4.166/25.540/8.897 versus
0.312/25.671/13.173 seconds; duplicate checks take 0.029 seconds in each,
leaving unassigned residuals of 25.119 and 29.674 seconds.
Read-cache and observer costs differ.
Observed parallel coverage grows from 237,863 checks and 3,283,925,639 allocation
units to 406,576 checks and 3,968,705,445 units; this is changed observer
coverage, not extra total mathematical work.
The retained 1.792-second prefix is a conservative implementation policy,
not a proved intrinsic serial lower bound. These diagnostic windows are not
rescaled into the plain medians or the earlier approximate 299-second partition.

All sixteen native/control scopes retire with complete wait4 records, no
OOM or sampled-RSS stop, P0--7, no \texttt{-M} and the existing external guards.
Four finite positive controls accept their two-module inputs; four corrupted
proof controls accept the Init prefix and then receive the original kernel's
loose-bound-variable rejection. These do not prove arbitrary context or unsafe
FFI safety. Reader, quiescence, prefix construction and checked-token trust
remain. The continuation controller may still execute a separate historical
protocol retest; completed cells do not imply controller retirement.
No full-library, source-build, service or cluster gain follows.
'''.replace('TAG',tag)
anchor='\n'+r'\paragraph{The complete counter matrix supports the prototype correction.}'
assert t.count(anchor)==1;t=t.replace(anchor,'\n'+addition+anchor)
p.write_text(t)
print('PAPER_UPDATED',len(t))
