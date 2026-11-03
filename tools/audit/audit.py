#!/usr/bin/env python3
"""Read-only Lake source audit. Python 3.11+, standard library only."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tomllib

SCHEMA = "proofserve-audit/v1"
TOKENS = ("decide", "native_decide", "bv_decide", "ofReduceBool", "omega",
          "simp", "simp_all", "norm_num", "grind", "rfl")
NAME = r"(?!\d)[\w][\w'.]*"
IMPORT = re.compile(r"(?m)^\s*(?:(?:public|private|meta)\s+)*import[ \t]+([^\n;]+)")

SPECIAL = re.compile(r"""--|/-|(?<![\w])r(?P<hashes>\#*)"|'(?:\\.|[^'\\\n])'|" """.rstrip())
BLOCK = re.compile(r"/-|-/")
STRING = re.compile(r'(?:\\.|[^"\\])*"', re.S)

def mask(text):
    """Mask nested comments and quoted strings, retaining offsets/newlines."""
    pieces = []
    position = 0
    while (match := SPECIAL.search(text, position)) is not None:
        start = match.start()
        pieces.append(text[position:start])
        token = match[0]
        if token == "--":
            end = text.find("\n", match.end())
            if end < 0:
                end = len(text)
        elif token == "/-":
            end, depth = match.end(), 1
            while depth:
                next_token = BLOCK.search(text, end)
                if next_token is None:
                    raise ValueError("unterminated block comment")
                depth += 1 if next_token[0] == "/-" else -1
                end = next_token.end()
        elif match.group("hashes") is not None:
            delimiter = '"' + match.group("hashes")
            closing = text.find(delimiter, match.end())
            if closing < 0:
                raise ValueError("unterminated raw string")
            end = closing + len(delimiter)
        elif token == '"':
            literal = STRING.match(text, match.end())
            if literal is None:
                raise ValueError("unterminated string literal")
            end = literal.end()
        else:
            end = match.end()
        pieces.append(re.sub(r"[^\n]", " ", text[start:end]))
        position = end
    pieces.append(text[position:])
    return "".join(pieces)

def lexical(text):
    code = mask(text)
    counts = {k: len(re.findall(r"(?<![\w'])" + k + r"(?![\w'])", code)) for k in TOKENS}
    counts["decide_plus_kernel"] = len(re.findall(r"\bdecide\s*\+\s*kernel\b", code))
    imports = []
    for match in IMPORT.finditer(code):
        imports.extend(x for x in re.findall(NAME, match[1]) if x not in ("all", "in"))
    # Same frozen W stratification proxy: any explicit decide +kernel occurrence.
    return dict(counts=counts, imports=sorted(set(imports)),
                regime_proxy="computation_certificate" if counts["decide_plus_kernel"] else "ordinary_mathematics")

def inside(project, path):
    p = (project / path).resolve()
    if not p.is_relative_to(project):
        raise ValueError("source directory escapes project: " + str(path))
    return p

def configuration(project, config_override=None):
    """Never evaluate arbitrary Lake/Lean code. Unsupported default scope is unknown."""
    toml = config_override if config_override is not None else project / "lakefile.toml"
    lean = project / "lakefile.lean"
    if config_override is not None or toml.exists():
        raw = tomllib.loads(toml.read_text(encoding="utf-8"))
        package_src = raw.get("srcDir", ".")
        targets = []
        for kind in ("lean_lib", "lean_exe"):
            for spec in raw.get(kind, []):
                if not isinstance(spec.get("name"), str):
                    raise ValueError("target has no literal name")
                targets.append(dict(name=spec["name"], kind=kind,
                    srcDir=str(Path(package_src) / spec.get("srcDir", ".")),
                    roots=spec.get("roots", [spec.get("root", spec["name"])]),
                    globs=spec.get("globs"), needs=spec.get("needs", []),
                    extraDepTargets=spec.get("extraDepTargets", [])))
        defaults = raw.get("defaultTargets")
        return dict(file=str(toml) if config_override else "lakefile.toml", targets=targets, defaults=defaults,
            supplied_config=config_override is not None,
            default_scope_supported=isinstance(defaults, list),
            reasons=[] if isinstance(defaults, list) else ["defaultTargets absent; do not guess Lake fallback behavior"])
    if lean.exists():
        # Only names/source roots are advisory. No default build coverage claims
        # from regex parsing an executable Lean configuration.
        text = lean.read_text(encoding="utf-8")
        code = mask(text)
        targets = []
        pattern = re.compile(r"(?m)^\s*(lean_lib|lean_exe)\s+(" + NAME + r")\b")
        found = list(pattern.finditer(code))
        for i, m in enumerate(found):
            end = found[i + 1].start() if i + 1 < len(found) else len(text)
            block = text[m.end():end]
            # Restrict literals to lines whose srcDir token survived comment masking.
            src = "."
            for sm in re.finditer(r'(?m)^\s*srcDir\s*:=\s*"([^"\n]+)"\s*$', block):
                absolute = m.end() + sm.start()
                if "srcDir" in code[absolute:absolute + len(sm[0])]:
                    src = sm[1]
                    break
            targets.append(dict(name=m[2], kind=m[1], srcDir=src,
                                roots=[m[2]], globs=None))
        return dict(file="lakefile.lean", targets=targets, defaults=None,
            default_scope_supported=False,
            reasons=["executable lakefile.lean is not evaluated; pass --build-roots for an explicitly declared import-closure audit"])
    raise ValueError("expected lakefile.toml or lakefile.lean in project root")

def roots_for(target, modules):
    if target.get("needs") or target.get("extraDepTargets"):
        raise ValueError("custom dependency targets require an evaluated build inventory")
    roots = target["roots"]
    if not isinstance(roots, list) or not all(isinstance(x, str) for x in roots):
        raise ValueError("non-literal target roots")
    globs = target["globs"]
    if globs is None:
        return set(roots)
    result = set()
    if not isinstance(globs, list):
        raise ValueError("unsupported globs")
    for glob in globs:
        if not isinstance(glob, str):
            raise ValueError("unsupported glob")
        if glob.endswith(".+"):
            result.update(m for m in modules if m.startswith(glob[:-1]))
        elif glob.endswith(".*"):
            root = glob[:-2]
            result.update(m for m in modules if m == root or m.startswith(root + "."))
        elif re.fullmatch(NAME, glob):
            result.add(glob)
        else:
            raise ValueError("unsupported glob: " + glob)
    return result

def reachable(seeds, modules):
    seen, pending, missing = set(), list(seeds), set()
    while pending:
        m = pending.pop()
        if m in seen:
            continue
        if m not in modules:
            missing.add(m)
            continue
        seen.add(m)
        pending.extend(x for x in modules[m]["imports"] if x in modules and x not in seen)
    return seen, missing

def uint64(value, field):
    """Lean may encode UInt64 as an unsigned decimal JSON string."""
    if isinstance(value, str) and re.fullmatch(r"0|[1-9][0-9]*", value):
        value = int(value)
    if type(value) is not int or not 0 <= value < 2**64:
        raise ValueError("invalid checker " + field)
    return value

def official_receipt(receipt, path):
    state = receipt.get("status")
    if state not in ("complete", "official_failure") or receipt.get("parallel") is not False:
        raise ValueError("malformed official checker receipt")
    for key in ("roots", "accepted_roots"):
        if not isinstance(receipt.get(key), list) or not all(isinstance(v, str) for v in receipt[key]):
            raise ValueError("invalid official " + key)
    if not isinstance(receipt.get("rejected_roots"), list):
        raise ValueError("invalid official rejected_roots")
    if state == "complete" and receipt["rejected_roots"]:
        raise ValueError("complete official receipt has failed roots")
    return dict(status="reported_official_complete" if state == "complete" else "reported_official_failure", file=str(path),
        execution_path="official-leanchecker", parallel=False,
        lean_version=receipt.get("lean_version"), roots=receipt["roots"],
        accepted_roots=receipt["accepted_roots"], rejected_roots=receipt["rejected_roots"],
        accepted=None, rejected=None, axioms=None, axioms_scope="unavailable_on_official_path",
        invocation_cpu_s=uint64(receipt.get("cpu_ns"), "cpu_ns")/1e9,
        invocation_wall_s=uint64(receipt.get("wall_ns"), "wall_ns")/1e9,
        per_module_costs_available=False,
        coverage=receipt.get("coverage"),
        source_binding="not established: official root receipt is not a source certificate",
        receipt=receipt), {}

def load_receipt(path):
    """Consume M checker v1 as reported compiled evidence, not source acceptance."""
    if path is None:
        return dict(status="unavailable", reason="no compiled checker receipt supplied"), {}
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict) or receipt.get("schema_version") != 1:
        return dict(status="supplied_uninterpreted", file=str(path),
            reason="unrecognized checker receipt schema; no inferred axioms", receipt=receipt), {}
    state = receipt.get("status")
    if state == "error":
        return dict(status="checker_error", file=str(path), error=receipt.get("error"),
                    axioms=None, receipt=receipt), {}
    if receipt.get("execution_path") == "official-leanchecker":
        return official_receipt(receipt, path)
    required = ("accepted", "rejected", "roots", "axioms", "lean_version",
                "module_set_hash", "module_set_hash_algorithm", "workers", "cpu_ns", "wall_ns")
    absent = [k for k in required if k not in receipt]
    if absent or state not in ("complete", "rejected", "incomplete"):
        raise ValueError("malformed checker v1 receipt: " + ", ".join(absent or ["invalid status"]))
    for key in ("accepted", "roots", "axioms"):
        if not isinstance(receipt[key], list) or not all(isinstance(v, str) for v in receipt[key]):
            raise ValueError("checker receipt " + key + " must be a string array")
    if not isinstance(receipt["rejected"], list):
        raise ValueError("checker receipt rejected must be an array")
    for key in ("cpu_ns", "wall_ns"):
        uint64(receipt[key], key)
    if type(receipt["workers"]) is not int or receipt["workers"] < 1:
        raise ValueError("invalid checker workers")
    if state == "complete" and receipt["rejected"]:
        raise ValueError("complete checker receipt contains rejection diagnostics")
    if len(set(receipt["accepted"])) != len(receipt["accepted"]):
        raise ValueError("checker receipt has duplicate accepted module names")
    return dict(status="reported_" + state, file=str(path),
        execution_path=receipt.get("execution_path", "native_v1_without_path_field"),
        parallel=receipt.get("parallel"),
        lean_version=receipt["lean_version"], accepted=receipt["accepted"],
        rejected=receipt["rejected"], roots=receipt["roots"], axioms=receipt["axioms"],
        axioms_scope="complete_checked_closure" if state == "complete" else "last_successful_prefix_only",
        module_set_hash=receipt["module_set_hash"],
        module_set_hash_algorithm=receipt["module_set_hash_algorithm"],
        workers=receipt["workers"], invocation_cpu_s=uint64(receipt["cpu_ns"], "cpu_ns")/1e9,
        invocation_wall_s=uint64(receipt["wall_ns"], "wall_ns")/1e9,
        cumulative_segment_cpu_s=(uint64(receipt["cumulative_segment_cpu_ns"], "cumulative_segment_cpu_ns")/1e9
            if receipt.get("cumulative_segment_cpu_ns") is not None else None),
        per_module_costs_available=False,
        source_binding="not established: receipt v1 covers compiled artifacts; source digest is not included",
        trusted_local_checkpoints=receipt.get("trusted_local_checkpoints"),
        mathlib_manifest=receipt.get("mathlib_manifest"), receipt=receipt), {}

def read_costs(path, modules):
    if path is None:
        return {}, []
    costs, rejected = {}, []
    with path.open(encoding="utf-8", newline="") as f:
        for n, row in enumerate(csv.DictReader(f), 2):
            try:
                m = row["module"]
                if m not in modules or row["source_digest_blake2b"] != modules[m]["source_digest_blake2b"]:
                    raise ValueError("module/source digest mismatch")
                if m in costs:
                    raise ValueError("duplicate module cost; select a run explicitly")
                values = {k: float(row[k]) for k in ("user_cpu_s", "system_cpu_s", "wall_s")}
                if not all(math.isfinite(v) and v >= 0 for v in values.values()):
                    raise ValueError("invalid cost")
                costs[m] = dict(**values, cpu_s=values["user_cpu_s"] + values["system_cpu_s"],
                    status=row["status"], source="supplied_cost_log", file=str(path), line=n)
            except (KeyError, ValueError) as e:
                rejected.append(dict(line=n, error=str(e)))
    return costs, rejected

def audit(project, build_roots=None, receipt=None, cost_log=None, lake_config=None):
    project = Path(project).resolve(strict=True)
    receipt = Path(receipt) if receipt is not None else None
    cost_log = Path(cost_log) if cost_log is not None else None
    if build_roots is not None and (isinstance(build_roots, str)
            or not all(isinstance(m, str) and m for m in build_roots)):
        raise ValueError("build_roots must be an array of nonempty module names")
    config = configuration(project, Path(lake_config) if lake_config is not None else None)
    root_paths = {project}
    for target in config["targets"]:
        root_paths.add(inside(project, target["srcDir"]))
    # Dependencies are intentionally not traversed as local source. M's checker
    # receipt owns the compiled dependency/axiom closure.
    excluded = {".lake", ".git", ".proofserve", "__pycache__"}
    paths = []
    for folder, dirs, files in os.walk(project, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excluded and not Path(folder, d).is_symlink())
        for f in sorted(files):
            p = Path(folder, f)
            if f.endswith(".lean") and f != "lakefile.lean" and not p.is_symlink():
                paths.append(p)
    modules, errors = {}, []
    for p in paths:
        source_root = max((x for x in root_paths if p.is_relative_to(x)), key=lambda x: len(x.parts))
        name = ".".join(p.relative_to(source_root).with_suffix("").parts)
        if name in modules:
            errors.append(dict(path=str(p.relative_to(project)), error="ambiguous source-root module identity: " + name))
            continue
        data = p.read_bytes()
        try:
            row = lexical(data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as e:
            errors.append(dict(path=str(p.relative_to(project)), error=str(e)))
            continue
        row.update(module=name, path=p.relative_to(project).as_posix(), source_bytes=len(data),
                   source_digest_blake2b=hashlib.blake2b(data, digest_size=32).hexdigest(),
                   cost=None)
        modules[name] = row
    reasons = list(config["reasons"])
    scope = "unknown"
    covered, seeds, missing = set(), set(), set()
    if build_roots is not None:
        seeds = set(build_roots)
        covered, missing = reachable(seeds, modules)
        scope = "explicit_import_roots" if not missing and not errors else "incomplete_explicit_import_roots"
    elif config["default_scope_supported"]:
        by_name = {x["name"]: x for x in config["targets"]}
        try:
            for target in config["defaults"]:
                if target not in by_name:
                    raise ValueError("unknown/custom default target: " + str(target))
                seeds.update(roots_for(by_name[target], modules))
            covered, missing = reachable(seeds, modules)
            if missing:
                raise ValueError("default module roots absent: " + ", ".join(sorted(missing)))
            scope = ("supplied_declarative_config" if config.get("supplied_config") else "static_declarative_defaults") if not errors else "incomplete_static_defaults"
        except ValueError as e:
            reasons.append(str(e))
            scope = "unknown"
    totals = {key: sum(row["counts"][key] for row in modules.values())
              for key in (*TOKENS, "decide_plus_kernel")}
    compiled, _ = load_receipt(receipt)
    costs, cost_errors = read_costs(cost_log, modules)
    for m, cost in costs.items():
        if m in modules:
            modules[m]["cost"] = cost
    identity = "\n".join(m + "\0" + modules[m]["source_digest_blake2b"] for m in sorted(modules))
    return dict(schema=SCHEMA, project=str(project),
        lean_toolchain=(project / "lean-toolchain").read_text().strip() if (project / "lean-toolchain").exists() else None,
        source_modules=len(modules), source_files_discovered=len(paths),
        source_files_parsed=len(modules), lexical_counts_complete=not errors, source_bytes=sum(x["source_bytes"] for x in modules.values()),
        module_source_digest_blake2b=hashlib.blake2b(identity.encode(), digest_size=32).hexdigest(),
        configuration=config,
        coverage=dict(status=scope, roots=sorted(seeds), covered_modules=sorted(covered),
            omitted_modules=sorted(set(modules)-covered) if scope in ("static_declarative_defaults", "explicit_import_roots", "supplied_declarative_config") else None,
            missing_roots=sorted(missing), reasons=reasons,
            scope="local source import closure only; custom targets and external compiled dependencies require evaluated evidence"),
        lexical_counts=totals, modules=[modules[m] for m in sorted(modules)], errors=errors,
        cost_errors=cost_errors, compiled_evidence=compiled, costs_status="unavailable" if not costs else "supplied_log",
        limitations=[
            "Lexical occurrences outside comments/strings are not tactic executions, elaborated identities, kernel costs or an axiom closure.",
            "Regime proxy is any explicit decide +kernel occurrence; no occurrence does not establish low computation cost.",
            "Executable Lake configuration is never evaluated. Unknown coverage is not zero omitted modules.",
            "No native Lean invocation, build, network fetch or acceptance decision is performed.",
            "Source digest is provenance, not a download or acceptance gate."])

def summary(report):
    coverage = report["coverage"]
    omitted = coverage["omitted_modules"]
    return (f'{report["source_files_parsed"]}/{report["source_files_discovered"]} local source files parsed; {report["source_bytes"]} parsed source bytes.\n'
        f'Default/build coverage: {coverage["status"]}; omitted: '
        + ("unknown" if omitted is None else str(len(omitted))) + ".\n"
        + f'Explicit decide +kernel sites: {report["lexical_counts"].get("decide_plus_kernel", 0)} (lexical).\n'
        + f'Costs: {report["costs_status"]}; compiled axioms: {report["compiled_evidence"]["status"]}.\n')

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", type=Path)
    ap.add_argument("--json", type=Path, help="write JSON here; '-' writes JSON to stdout, summary to stderr")
    ap.add_argument("--build-roots", nargs="+", help="explicit roots; does not claim these are Lake defaults")
    ap.add_argument("--receipt", type=Path, help="compiled checker receipt (no axioms guessed from source)")
    ap.add_argument("--costs", type=Path, help="source-matched per-module CPU/wall CSV; see README")
    ap.add_argument("--lake-config", type=Path, help="caller-supplied evaluated Lake TOML export; never evaluates Lake here")
    args = ap.parse_args(argv)
    try:
        report = audit(args.project, args.build_roots, args.receipt, args.costs, args.lake_config)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as e:
        ap.exit(2, f"proofserve audit: {e}\n")
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json and str(args.json) == "-":
        print(payload, end="")
        print(summary(report), file=sys.stderr, end="")
    else:
        if args.json:
            args.json.write_text(payload, encoding="utf-8")
        print(summary(report), end="")
    return 1 if report["errors"] or report["cost_errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
