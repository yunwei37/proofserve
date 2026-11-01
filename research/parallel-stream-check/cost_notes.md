# Cost staircase scope

For the exact 1,330-module Mathlib closure, construction is O's sum of per-module
source compiler wall times (622.3794 s), not elapsed parallel Lake build wall.
The fresh v14 O-reference and repaired stream runs check the same root/artifact
path. Final ratios must use that new reference's repetitions.

For Grid, O's constructed leaf is byte-identical to the W artifact selected for
the new checker. Its 3,793-module closure source-work sum is 3,878.7067 s; O's
matched closure stream was 563.0822 s in its own run. The v12 computational
experiment instead checks the 3,792-module prefix once then runs five leaf
variants; its 1,097.5916 s whole wall is not a single parallel configuration.
Do not divide these whole-process quantities to claim a service speedup.

The matched W Grid leaf source compiler run is 317.1915 s, including cached
imports and source elaboration; the new stream leaf serial check is 265.7846 s.
These are different operations on the same resulting leaf artifact. The
93.6616 s four-worker leaf result has its own same-process serial denominator.
One repetition; additional CPU 40.61%; requested-eight uses ~four mean cores.

Barrier and Envelope source compiler leaf walls are 63.0296 and 64.8681 s.
The new entire-leaf stream curves are not yet complete. No prior single-fact
kernel timing or imported-prefix positive control fills these table cells.
Cold Envelope's resource stop before reaching the leaf remains an explicit
missing performance/acceptance cell, not zero time or proof rejection.
