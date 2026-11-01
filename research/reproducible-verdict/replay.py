"""Versioned evidence API for the native Probe; no production failure cache.

A receipt is a rerun package, never a mathematical certificate of rejection.
The native executable, source, imported environment and budget scope must match.
This module does not execute untrusted proof code or accept a result by hashing it.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
SCHEMA="lean-budget-observation-v1"

def rows_from_log(text: str):
    return [json.loads(line.removeprefix("REPRO "))
            for line in text.splitlines() if line.startswith("REPRO ")]

def key(row):
    return tuple(row[k] for k in ("id","mode","observer","budget","target"))

def bundle(requests,rows,environment,native_result):
    """Bind every observed row to its exact request and operational completion.

    Duplicate request keys are rejected instead of silently choosing a producer.
    An interrupted process can have completed prefix observations; those remain
    observations but do not imply the rest failed. Unobserved requests are missing.
    """
    index={}
    for request in requests:
        k=key(request)
        if k in index:raise ValueError("duplicate request identity")
        index[k]=request
    seen=set();observations=[]
    for row in rows:
        k=key(row)
        if k not in index or k in seen:raise ValueError("unknown/duplicate observation")
        seen.add(k)
        required=("verdict","command_raw_heartbeats","axioms","new_axioms",
                  "theorem_present","errors","warnings","accounting")
        if any(x not in row for x in required):raise ValueError("incomplete observation")
        if row["verdict"]=="accepted" and (
            not row["theorem_present"] or "sorryAx" in row["axioms"] or
            row["new_axioms"] or row["errors"] or row.get("kernel_replay","checked")!="checked"):
            raise ValueError("invalid accepted observation")
        observations.append({"request":index[k],"result":row})
    return dict(schema=SCHEMA,environment=environment,
        budget_scope="stock Lean maxHeartbeats per Core context, NOT a global candidate quota",
        unit="1000 small-allocation heartbeats per user-facing unit; command deltas are raw",
        trusted_status="observational receipt; rerun original Lean, do not trust verdict on receipt alone",
        complete_work_accounting=False,unobserved_work=["native kernel polls","arbitrary asynchronous child work"],
        native_result=native_result,ordered_requests=requests,observations=observations,
        missing=[x for k,x in index.items() if k not in seen])

def compare(recorded,rerun):
    """Return all divergences; hardware/time are evidence, not ignored work changes."""
    if recorded["schema"]!=SCHEMA or rerun["schema"]!=SCHEMA:
        raise ValueError("unsupported receipt schema")
    a={key(x["request"]):x for x in recorded["observations"]}
    b={key(x["request"]):x for x in rerun["observations"]}
    diffs=[]
    for k in sorted(a.keys()|b.keys()):
        if k not in a or k not in b:
            diffs.append(dict(key=k,field="missing_observation"));continue
        if a[k]["request"]!=b[k]["request"]:
            diffs.append(dict(key=k,field="request"));continue
        for f in ["verdict","command_raw_heartbeats","axioms","new_axioms","errors","warnings"]:
            if a[k]["result"][f]!=b[k]["result"][f]:
                diffs.append(dict(key=k,field=f,recorded=a[k]["result"][f],rerun=b[k]["result"][f]))
    semantics_a=recorded["environment"].get("semantics")
    semantics_b=rerun["environment"].get("semantics")
    return dict(same_request_order=recorded.get("ordered_requests")==rerun.get("ordered_requests"),
                same_declared_semantics=bool(semantics_a) and semantics_a==semantics_b,
                differences=diffs,matching_observations=len(a.keys()&b.keys()),
                recorded_missing=len(recorded["missing"]),rerun_missing=len(rerun["missing"]),
                universal_determinism_proved=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest="command",required=True)
    q=sub.add_parser("bundle")
    for name in ["requests","log","environment","native","out"]:q.add_argument("--"+name,required=True,type=Path)
    q=sub.add_parser("compare")
    for name in ["recorded","rerun","out"]:q.add_argument("--"+name,required=True,type=Path)
    a=p.parse_args()
    read=lambda x:json.loads(x.read_text())
    result=(bundle(read(a.requests),rows_from_log(a.log.read_text()),read(a.environment),read(a.native))
        if a.command=="bundle" else compare(read(a.recorded),read(a.rerun)))
    with a.out.open("x")as f:f.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__":main()
