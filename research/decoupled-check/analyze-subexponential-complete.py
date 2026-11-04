#!/usr/bin/env python3
"""Reduce the completed prototype without mixing P timing and E correctness.

Requires native terminal evidence and exact module-set equality. Never changes
the original state/ledger, fills unknown elapsed times, or runs Lean.
"""
from pathlib import Path
import csv
import json
import math
import os

D = Path(__file__).resolve().parent
BASE = Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031")
A = BASE / "subexponential-20261103"
E = A / "correctness-cpu89-20261104"
F = BASE / "scale-study/falconer-project-20261101"


def read(path):
    return json.loads(path.read_text())


def events(path):
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.startswith("{")]


def accepts(rows):
    return [row["module"] for row in rows if row.get("event") == "accept"]


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def validate_reference(item):
    cell = item["cell"]
    assert item["valid"] and item["correctness_only"]
    assert item["performance_eligible"] is False
    assert cell["returncode"] == 0 and cell["measured"] is False
    assert cell["affinity"] == [8, 9]
    assert not any(k in cell for k in ("user_s", "system_s", "wall_s"))
    assert not item.get("parse_errors")
    assert accepts(item["events"]) == [item["module"]]
    assert not item["resource_observation"]["rss_budget_stop"]
    return item["module"]


def main():
    # Fail closed before writing any public conclusion for an active/partial run.
    assert (E / "terminal.json").is_file(), "E correctness still incomplete"
    terminal = read(E / "terminal.json")
    assert terminal["complete"] and terminal["accepted_set_equal"]
    assert terminal["correctness_only"] and not terminal["performance_eligible"]
    assert not (E / "failure.json").exists(), "unresolved operational failure"
    claim = read(E / "controller.json")
    proc = Path("/proc", str(claim["pid"]), "stat")
    assert not proc.exists() or (
        proc.read_text().split(") ")[1].split()[19] != claim["birth"]
    ), "wait for native controller retirement before reduction"

    frame = read(A / "frame.json")
    expected = {v["module"] for v in frame}
    targets = {v["module"] for v in frame if v["target"]}
    inherited = {v["module"] for v in frame if "reused" in v}
    state = read(A / "state.json")
    estate = read(E / "state.json")
    assert len(frame) == len(expected) == 14721 and len(targets) == 3977
    assert len(inherited) == 10744
    assert expected == set(state["built"]) == set(state["stream_ids"])
    assert estate["phase"] == "complete"

    # Dependencies were qualified earlier on these exact hard-linked artifacts.
    # Do not infer module-local replay merely from a successful source build.
    supported = set()
    inherited_calls = 0
    for line in (BASE / "measured.jsonl").open():
        row = json.loads(line)
        if row.get("operation") not in ("oracle", "matched_oracle"):
            continue
        if row.get("returncode") != 0:
            continue
        ids = row.get("accepted_modules", [])
        assert accepts(events(BASE / (row["key"] + ".stdout"))) == ids
        supported.update(ids)
        inherited_calls += 1
    inherited_terminals = 0
    for path in (F / "bounded-recheck-v1").glob("oracle-*-terminal.json"):
        row = read(path)
        assert row["complete"] and row["cell"]["returncode"] == 0
        ids = row["accepted"]
        raw = path.parent / (row["cell"]["key"] + ".stdout")
        assert accepts(events(raw)) == ids
        supported.update(ids)
        inherited_terminals += 1
    assert inherited <= supported, "missing retained native reference evidence"
    for row in frame:
        if "reused" in row:
            local = A / "check-lib" / Path(*row["module"].split(".")).with_suffix(".olean")
            assert os.path.samefile(row["reused"]["artifact"], local)

    ledger = [json.loads(line) for line in (A / "ledger.jsonl").open()]
    builds = [v for v in ledger if v["operation"] == "build"]
    streams = [v for v in ledger if v["operation"] == "stream"]
    refs = [v for v in ledger if v["operation"] == "oracle"]
    assert all(v["valid"] and v["cell"]["returncode"] == 0 for v in streams + refs)
    streamed = set()
    for row in streams:
        ids = accepts(events(A / (row["cell"]["key"] + ".stdout")))
        assert ids == row["accepted"]
        streamed.update(ids)
    assert streamed == expected
    legacy = set(inherited)
    for row in refs:
        ids = accepts(events(A / (row["cell"]["key"] + ".stdout")))
        assert ids == row["accepted"]
        legacy.update(ids)
    assert legacy == set(state["oracle_ids"]) and len(legacy) == 13208
    e_ids = {validate_reference(read(A / "qualification-cpu89-probe-20261104/terminal.json"))}
    for path in (E / "items").glob("reference-*.json"):
        item = read(path)
        assert events(E / (item["cell"]["key"] + ".stdout")) == item["events"]
        assert item["module"] not in e_ids
        e_ids.add(validate_reference(item))
    assert not legacy & e_ids
    assert e_ids == set(estate["qualified"]) and len(e_ids) == 1513
    assert legacy | e_ids == expected

    controls = []
    plan = read(E / "negative-control-plan.json")
    for i, module in enumerate(plan["roots"]):
        for mode in ("one", "audit"):
            key = f"negative-{i}-{mode}"
            item = read(E / "items" / (key + ".json"))
            cell = item["cell"]
            assert item["valid"] and item["module"] == module
            assert cell["returncode"] == 1 and cell["measured"] is False
            assert cell["affinity"] == [8, 9] and item["mutation"] == "bvar"
            raw = events(E / (key + ".stdout"))
            assert raw == item["events"] and module not in accepts(raw)
            assert any(v.get("event") == "reject" and v.get("module") == module
                       and "loose bound variables" in v.get("error", "") for v in raw)
            controls.append(dict(module=module, mode=mode, native_rejected=True,
                                 mutation="bvar", measured=False))
    assert len(controls) == 6 and len(estate["controls"]) == 6

    cpu = lambda v: v["cell"]["user_s"] + v["cell"]["system_s"]
    reused = [v["reused"] for v in frame if "reused" in v]
    nc, nw = sum(map(cpu, builds)), sum(v["cell"]["wall_s"] for v in builds)
    rc = sum(v["source_cpu_s"] for v in reused)
    rw = sum(v["source_wall_s"] for v in reused)
    kc, kw = sum(map(cpu, streams)), sum(v["cell"]["wall_s"] for v in streams)
    primary = read(D / "subexponential-primary-costs.json")
    for value, key in ((nc, "source_new_cpu_s"), (rc, "source_retained_cpu_s"),
                       (kc, "kernel_cpu_s"), (kw, "kernel_wall_s")):
        assert math.isclose(value, primary[key], rel_tol=1e-12)
    native_final = next(v for v in reversed(events(
        A / (streams[-1]["cell"]["key"] + ".stdout"))) if v.get("event") == "complete")
    assert native_final["modules"] == 14721
    provenance = read(E / "launch.json")
    result = dict(
        review="自审", complete=True, source_pin="4eaee87548250b2682affda7d05d947c05554bae",
        mathlib_pin="d13f23b723b8a846827a245b89c10fc7d3f11612",
        lean_version="4.34.1", source_targets=3977, dependencies=10744, closure=14721,
        stream_segments=len(streams), accepted_set_equal=True,
        retained_exact_artifact_references=len(inherited),
        retained_initial_raw_reference_calls=inherited_calls,
        retained_falconer_reference_terminals=inherited_terminals,
        new_legacy_pcore_references=len(legacy - inherited),
        untimed_e89_references=len(e_ids), complete_reference_count=14721,
        complete_reference_cpu_s=None, complete_reference_wall_s=None,
        reference_clock_scope="Mixed P historical and untimed E correctness; no combined cost.",
        source_target_cpu_s=nc, source_retained_dependency_cpu_s=rc,
        source_full_cpu_s=nc + rc, checker_cpu_s=kc, checker_cpu_h=kc / 3600,
        source_target_wall_s=nw, source_retained_dependency_wall_s=rw,
        checker_wall_s=kw, full_cpu_ratio=kc / (nc + rc),
        incremental_cpu_ratio=kc / nc, full_summed_child_wall_ratio=kw / (nw + rw),
        incremental_summed_child_wall_ratio=kw / nw,
        checker_peak_rss_gib=primary["kernel_wait4_peak_rss_gib"],
        checker_peak_cgroup_gib=primary["kernel_charged_cgroup_peak_gib"],
        native_final_event=native_final, malformed_theorem_bodies=3,
        native_rejection_processes=6, mutation_classes=1, controls=controls,
        source_attempts=len(builds), source_failures=sum(not v["valid"] for v in builds),
        source_sorry_warnings=sum(v.get("sorry_warning", False) for v in builds),
        e_controller_source=provenance.get("source_commit", provenance.get("commit")),
        historical_failures_preserved=[
            "host reboot: interrupted source attempt excluded, completed work retained",
            "disk ceiling after all source/stream accepts and 11448 reference IDs",
            "finite reference controller guard expired including queue waits",
            "legacy 16-root reference batch killed at sampled 12GiB RSS ceiling"],
        product_system_timing_eligible=False,
        scope="Prototype causal result, not a release-tool system benchmark or global census.")

    # All checks above must pass before any result file is emitted.
    dump(D / "subexponential-complete-metrics.json", result)
    dump(D / "subexponential-negative-controls.json",
         dict(review="自审", complete=True, theorem_bodies=3, mutation_classes=1,
              native_rejections=6, controls=controls, measured=False))
    parts = [
        dict(component="retained dependency source work", cpu_s=rc, child_wall_s=rw,
             performance_scope="historical P-core original compiler"),
        dict(component="new target source work", cpu_s=nc, child_wall_s=nw,
             performance_scope="P-core original compiler"),
        dict(component="full closure checkpointed checking", cpu_s=kc, child_wall_s=kw,
             performance_scope="P-core prototype, startup/restore/export included"),
        dict(component="full module-local reference qualification", cpu_s="",
             child_wall_s="", performance_scope="correctness only; mixed P and untimed E"),
    ]
    with (D / "subexponential-component-costs.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=parts[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(parts)
    text = f"""# SubexponentialSAT: complete source/stream costs and reference qualification

Review: 自审. This is a **research prototype result**, not a published ProofServe
system benchmark. Final product timing waits for the W census and a quiet machine.

The pinned openai/math revision4eaee87548250b2682affda7d05d947c05554bae,
Mathlibd13f23b723b8a846827a245b89c10fc7d3f11612, Lean4.34.1 frame contains
**3977 source targets +10744 dependencies =14721 modules**.
All were source-produced and accepted in **{len(streams)} segments**, at most500 new
modules per segment. The exact accepted set equals the original module-local
reference set:10744 inherited same-artifact references (raw native evidence
revalidated),2464 subsequent P-core references,1513 unmeasured E-core references.
No successful source, stream or reference input was repeated in the final continuation.

| Denominator | Source CPU-s | Checker CPU-s | CPU ratio | Summed child-wall ratio |
|---|---:|---:|---:|---:|
| Full closure, retained dependency production included | {nc+rc:.3f} | {kc:.3f} | **{kc/(nc+rc):.4%}** | {kw/(nw+rw):.4%} |
| Newly produced targets only; same full-closure checker | {nc:.3f} | {kc:.3f} | **{kc/nc:.4%}** | {kw/nw:.4%} |

Checker cost is **{kc/3600:.6f} CPU hours**. Both rows use the same full-closure
checking numerator. The incremental denominator excludes already-paid dependency
production, not dependency rechecking. Retained production costs are real matching
compiler records, not projections. Source emits olean/ilean/C, excluding C linking.
Native startup, checkpoint restore/export and module-local fallback are included.
Child-wall sums exclude lock waits, Git, host-reboot gaps and controller downtime;
this is not continuous from-scratch Lake wall time. Negative controls and reference
qualification are separate from the primary cost ratio. The E continuation
collected no CPU/wall clock: **no total reference cost is available**.

Three malformed theorem bodies were rejected in both original module-local replay
and certified-predecessor-restored replay (**six explicit original-kernel reject
events**, one loose-bound-variable mutation class, not three classes). Nonzero
process exit alone was not counted. This is semantic rejection evidence, not
hardened parsing of hostile olean files or independent trust in native compilation.

The stream shares905617 kernel declarations;64 module-local fallbacks are charged.
5318 unsafe/partial entries are outside the identical safe-declaration replay policy.
Acceptance equality does not assert that unsafe runtime definitions were replayed
or that the library is axiom-free. Local certified checkpoints are trusted state.

| Input | Check/source CPU | Scope |
|---|---:|---|
| Falconer | 6.31% | Complete13205-node segmented mathematical closure |
| Matched Mathlib | 8.95% | Complete1330-node matched segmented closure |
| SubexponentialSAT | {kc/(nc+rc):.2%} | Complete14721-node closure, full source denominator |
| Ramsey20sample | 35.91% | Biased built-prefix module-local sample, not a closure |
| RamseyK10 | 20.66% | One supplemental module, not a closure |

SubexponentialSAT's complete-directory ratio is close to the mathematical
closures. Zero explicit+kernel markers coexist with26593 plain by-decide sites in
1932files; aggregate checking costs cannot attribute individual tactic cost or
establish that every decide call is cheap. The pilot's25 sources are charged once.

The original disk-ceiling failure occurred after all stream acceptances.
A host reboot interrupted an unfinished source attempt. A later controller guard
expired while including queue waits, then a16-root reference window was stopped
at12,896,055,296 sampled own-tree RSS bytes. All failures, partial output and
completed records remain intact; none is a logical rejection. The final E-only
continuation ran only remaining references and controls on8–9 with no P lease.
Original A/state.json remains the retired P controller's logical oracle state;
the separate E terminal and exact union are authoritative for final qualification.

Historical stream wait4 peakRSS was **14.731289GiB**, charged-cgroup peak
**10.229065GiB**. These are different counters; the historical12GiB RSS budget
cannot be claimed satisfied from charged-memory enforcement. The final correctness
continuation separately sampled aggregate RSS each second and stopped on excess;
sampling may overshoot. Earlier retained180/300s calls and later1400s source calls
also have different parent reserves; see the retained-protocol audit.
No global163097-module total or extrapolation validation follows from this result.
"""
    (D / "subexponential-complete-result.md").write_text(text)
    progress = f"""# SubexponentialSAT final status

Review: 自审. Source **3977/3977 targets**, stream **3977 targets +10744dependencies**,
original module-local reference union **14721/14721**, three malformed bodies
rejected in both paths (**6rejections;1mutation class**). **Complete.**

Prototype P-core source CPU **{nc+rc:.6f}s**, stream CPU **{kc:.6f}s**
(**{kc/3600:.6f}h**); full/incremental-denominator CPU ratios
**{kc/(nc+rc):.4%}/{kc/nc:.4%}**. E-core qualification has no CPU/wall metric.
Final product timing remains deferred until W census completion and a quiet machine.

The retired P controller raw state stays oracle at13208 references; it is not
a running-process claim. Exact native evidence union adds1513 unmeasured E references.
[Complete result](subexponential-complete-result.md) records the source/stream
costs, safe-declaration policy, inherited evidence and all operational failures.

Historical whole-library prototype remains **partial, stopped**:2488/163097source
IDs,10744dependencies,0.694505kernelCPUh;9124old producer errors/151485blocked.
It is a different point, never a denominator for this complete directory.
Ramsey full, Transonic and the old whole-library route are not resumed.
"""
    (D / "subexponential-progress.md").write_text(progress)
    print(json.dumps({k:result[k] for k in ("complete", "closure",
          "accepted_set_equal", "checker_cpu_h", "full_cpu_ratio",
          "incremental_cpu_ratio", "native_rejection_processes")}, indent=2))


if __name__ == "__main__":
    main()
