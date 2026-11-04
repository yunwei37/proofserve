#!/usr/bin/env python3
"""Reduce three completed installed-tool cells; never infer a missing result."""
from pathlib import Path
import argparse, csv, json

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    projects = json.loads((Path(__file__).parent / "projects.json").read_text())
    by_repo = {p["repo"]: p for p in projects["projects"]}
    rows, summaries = [], []
    for name in ["newspeak", "solar", "croc"]:
        raw = args.raw_root / (name + "-evaluation-v1")
        result = json.loads((raw / "result.json").read_text())
        serial = None
        if name == "croc" and not result["complete"]:
            serial = json.loads((args.raw_root / "croc-official-serial-v1/result.json").read_text())
            assert serial["complete"] and serial["local_root_acceptance_equal"]
            assert result["measurements"][1]["resource_failure"]
        else:
            assert result["complete"] and result["local_root_acceptance_equal"]
        assert result["bundle"]["source_commit"] == projects["tool_bundle_commit"]
        assert result["checker_commit"] == projects["checker_commit"]
        project = by_repo[result["project"]]
        assert result["upstream_commit"] == project["pin"]
        receipt = json.loads((raw / "checkpoint/receipt.json").read_text())
        roots, accepted = set(result["roots"]), set(receipt["accepted"])
        assert receipt["status"] == "complete" and not receipt["rejected"]
        assert roots <= accepted and len(accepted) == result["native_closure_modules"]
        official = set(serial["accepted_roots"]) if serial else {
            line.removeprefix("replaying ").strip()
            for line in (raw / "official-default.stdout").read_text().splitlines()
            if line.startswith("replaying ")}
        assert official == roots
        audit = result["audit"]
        assert not audit["errors"] and not audit["cost_errors"]
        assert set(audit["coverage"]["covered_modules"]) <= roots
        for measure in result["measurements"]:
            events = dict(line.split() for line in measure["memory_events"].splitlines())
            interrupted = measure["resource_failure"] or int(events.get("oom_kill", "0")) > 0
            assert not measure["disk_failure"]
            assert measure["returncode"] == 0 or (serial and interrupted)
            row = {k: v for k, v in measure.items() if k != "memory_events"}
            row["raw_wait4_cpu_s"] = measure["cpu_s"]
            row["cpu_accounting_complete"] = not interrupted
            row["outcome"] = "resource_interrupted" if interrupted else "completed"
            if interrupted:
                # Killing the timeout parent and child together can orphan CPU
                # accounting. The retained0.001787s is not total solver CPU.
                row["cpu_s"] = ""
                row["wait4_peak_rss_kib"] = ""
            # An operation shorter than the 1-second sampler has no RSS sample.
            row["peak_tree_rss"] = row["peak_tree_rss"] or ""
            row.update(source_modules=audit["source_modules"], local_roots=len(roots),
                       native_closure_modules=len(accepted),
                       official_default_modules=len(official),
                       local_root_acceptance_equal="" if interrupted else True,
                       timing_scope_equal=False, ai_written=project["ai_written"])
            rows.append(row)
        if serial:
            row = {k: v for k, v in rows[-1].items()}
            row.update(arm="official-default-serialpool", returncode=0,
                cpu_s=serial["cpu_s"], wall_s=serial["wall_s"],
                wait4_peak_rss_kib=serial["wait4_peak_rss_kib"],
                cgroup_peak_bytes=serial["cgroup_peak_bytes"],
                peak_tree_rss=serial["peak_tree_rss"], resource_failure=False,
                outcome="completed", cpu_accounting_complete=True,
                raw_wait4_cpu_s=serial["cpu_s"], local_root_acceptance_equal=True)
            rows.append(row)
        summaries.append(dict(
            project=result["project"], upstream_commit=result["upstream_commit"],
            bundle_commit=result["bundle"]["source_commit"], checker_commit=result["checker_commit"],
            lean_toolchain=result["bundle"]["lean_toolchain"], ai_written=project["ai_written"],
            source_modules=audit["source_modules"], local_roots=sorted(roots),
            native_closure_modules=len(accepted), module_set_hash=receipt["module_set_hash"],
            module_set_hash_algorithm=receipt["module_set_hash_algorithm"],
            axioms=receipt["axioms"], axiom_scope="declared axioms in accepted closure; not per-theorem dependencies",
            official_local_roots=sorted(official), local_root_acceptance_equal=True,
            timing_scope_equal=False,
            official_protocol="default prefix selection, LEAN_NUM_THREADS=1, after retained resource stops" if serial else "batched defaults, runtime default",
            original_batch_complete=result["complete"],
            static_default_omitted=audit["coverage"]["omitted_modules"],
            compiled_evidence_status={k:v for k,v in audit["compiled_evidence"].items()
                                      if k not in ["accepted", "modules"] and not isinstance(v,(list,dict))},
            raw_results=str(raw)))
    args.out.mkdir(parents=True, exist_ok=True)
    controls = []
    for f in sorted((args.raw_root / "croc-official-isolated-v1").glob("[0-9][0-9][0-9].json")):
        rec = json.loads(f.read_text())
        interrupted = bool(rec["stop_reason"]) or rec["returncode"] != 0
        controls.append(dict(argument=rec["root"], returncode=rec["returncode"],
            outcome="resource_interrupted" if interrupted else "completed",
            cpu_s="" if interrupted else rec["cpu_s"], raw_wait4_cpu_s=rec["cpu_s"],
            cpu_accounting_complete=not interrupted, wall_s=rec["wall_s"],
            sampled_peak_tree_rss_bytes=rec["peak_tree_rss"],
            cgroup_peak_bytes=rec["cgroup_peak_bytes"],
            selection="default prefix expansion; not an exact-module selector"))
    with (args.out / "prefix-controls.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(controls[0]), lineterminator="\\n")
        writer.writeheader()
        writer.writerows(controls)
    with (args.out / "measurements.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "acceptance.json").write_text(json.dumps(dict(
        review="自审", complete=True, repeats_per_arm=1,
        no_equal_scope_speedup_claim=True, projects=summaries), indent=2) + "\n")
    print(json.dumps(dict(complete=True, projects=len(summaries), timed_cells=len(rows))))

if __name__ == "__main__":
    main()
