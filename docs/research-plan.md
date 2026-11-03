# ProofServe closure plan

The project now has two deliverables: a usable open-source Lean verification tool and a six-page empirical + system paper. This replaces the earlier instruction to keep four research directions open indefinitely.

The title and four research questions stay unchanged. RQ1 and RQ2 use measurement evidence; RQ3 and RQ4 use the tool and its evaluation. The coordinator proposes 17 November as a working target, not a user-imposed deadline. The venue is undecided.

## Deliverables and owners

| Owner | Paths | Remaining delivery |
|---|---|---|
| M | checker/ | Native proofserve-check, receipt v1, committed release matrix and functional evidence |
| W | tools/audit/, data/openai-math-4eaee875/ | Portable audit command and fixed public measurement package |
| O | crates/, CLI, README, Docker, CI, release workflow, data/external-projects/ | Clean-start packaging and three unseen public projects, including one published AI project |
| Root | docs/paper/, documentation and research/README.md | Six-page paper, evidence map, current status and integration |

ProofServe has three commands: check a Lake project's compiled dependency closure; audit source/default-target coverage, kernel-computation sites, reported axioms and measured costs; and maintain the existing Kimina-compatible serve path. Serve receives defect fixes only.

## Fixed evaluation; do not expand it

- M runs Mathlib, Grid and Barrier with the released checker at 1/2/4/8 workers, three repeats each. The existing matrix names Mathlib.Data.Nat.Basic; this is a selected closure, not all Mathlib. Keep that distinction explicit.
- At eight workers, Grid and Mathlib each receive three repeats without persistence and three without split fallback. Record executable commit and keep CPU and wall separate.
- Compare official leanchecker default and --fresh only at demonstrated common scope. Record ledger differences instead of manufacturing speedup ratios.
- Verify acceptance sets, three bad-proof classes in CI, and one interrupted/resumed versus uninterrupted pair with restart overhead.
- O records three previously unused public projects, immutable commits, AI provenance, module counts, both tools' CPU/wall, acceptance parity, audit findings and problems.
- W's original sample and already fixed precision design stay separate. Preserve existing in-flight work and raw attempts; no extra draw or precision threshold is added.
- The current separate whole-Mathlib run, if already underway, remains separately scoped; root starts no additional native collection.

System evaluation numbers come only from checker/results/ and data/external-projects/, with commits. Measurement numbers come from data/openai-math-4eaee875/. Research prototypes may explain causes but cannot fill release results.

## Acceptance and publication boundary

A stranger must run the package or container without Workspace paths. README's first 30 lines must explain purpose, invocation, demonstrated speed, trust and limitations. Unsupported toolchains must fail clearly or select an explicitly labeled official path. Axioms, exclusions, incomplete coverage and cached work remain visible.

No tags, crates.io publication, upstream issue/PR or announcement is authorized. Prepare the deliverables and hand them to the coordinator for user confirmation. Ordinary validated repository commits and pushes remain authorized.

## Paper closure

Use the existing 10pt two-column format, six pages including references, and at most four figures/tables. Established measurements are written now; designated release results occupy clearly pending positions until they return. Submission must contain no missing result macros; unsupported claims belong in limitations. The manuscript no longer embeds inline evidence-grade markers or a claim-to-evidence table. [Evidence map](paper/evidence.md) carries those details. No alternative long paper is maintained.

The empirical story must disclose our -M and persistence corrections, the broad sampling interval, and the prior art behind all mechanisms. Lean 4.35 already ships lake check; do not describe it only as a future roadmap item or claim an unmeasured advantage over it.

Scheduling, early failure prediction, certificate repair, cost prediction, GPU work, serving features and deeper attribution are stopped. Existing results remain intact. Do not restart a collector to match this plan.

## Operations and next action

Use the existing Workspace/PVC and Cloudflare CLI path. Timed work is one task at a time under the P-core lock; untimed work uses E cores. Omit -M, preserve headroom below 85%, and preserve foreign dirty work. A later host outage remains subject to the direct instruction to preserve the scene and wait for the user, without recovery or scheduling changes.

Root integrates the existing owners' committed returns, checks scope and versions, compiles and visually reviews the six-page paper, then commits owned paths on main. No per-edit step directories or outer-audit files are created for this closure.
