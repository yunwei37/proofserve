#!/usr/bin/env python3
"""Reduce committed observations and render paper figures; launches no Lean experiment."""
import argparse, csv, gzip, json, math, pathlib, shutil, statistics, subprocess, tempfile

def read_csv(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", newline="") as f:
        return list(csv.DictReader(f))

def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        for k in range(i, j):
            result[order[k]] = (i + j - 1) / 2 + 1
        i = j
    return result

def correlation(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    return math.fsum((a-mx)*(b-my) for a,b in zip(x,y)) / math.sqrt(
        math.fsum((a-mx)**2 for a in x) * math.fsum((b-my)**2 for b in y))

def quantile(v, q):
    s = sorted(v); p = (len(s)-1)*q; i = int(p)
    return s[i] + (s[min(i+1,len(s)-1)]-s[i])*(p-i)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=pathlib.Path, default=pathlib.Path("."))
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("docs/paper/generated/observations"))
    ap.add_argument("--tectonic", required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    out = (args.out if args.out.is_absolute() else root/args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    census = root/"data/openai-math-4eaee875/census/modules.csv.gz"
    all_rows = read_csv(census)
    rows = [r for r in all_rows if r["status"] == "completed"]
    assert len(all_rows) == 163097 and len(rows) == 162170
    assert len({r["module"] for r in all_rows}) == len(all_rows)
    summary = {"input": str(census.relative_to(root)), "complete_modules": len(rows),
               "core_conversion": None, "rank_definition": "ceil(1% of completed modules within each pool)",
               "source_size_correlation": "Spearman ranks, averaging ties; association, not causation",
               "pools": {}}
    for pool in ["P","E"]:
        rr = [r for r in rows if r["pool"] == pool]
        v = sorted((float(r["cpu_s"]) for r in rr), reverse=True)
        n = len(v); total = math.fsum(v); top = math.ceil(n*.01)
        marked = [r for r in rr if r["marked"] == "1"]
        summary["pools"][pool] = {
            "modules": n, "cpu_s": total, "median_cpu_s": statistics.median(v),
            "top_one_percent_n": top, "top_one_percent_cpu_pct": 100*math.fsum(v[:top])/total,
            "marked_n": len(marked),
            "marked_cpu_pct": 100*math.fsum(float(r["cpu_s"]) for r in marked)/total,
            "source_bytes_cpu_spearman": correlation(ranks([int(r["source_bytes"]) for r in rr]),
                                                    ranks([float(r["cpu_s"]) for r in rr]))}
        cumulative = [0.0]
        for value in v: cumulative.append(cumulative[-1]+value)
        indices = sorted({0,n,top,*[min(n,math.ceil(n*p/100)) for p in
                                  [.01,.05,.1,.2,.5,*range(1,101)]]})
        with (out/f"cost-share-{pool}.csv").open("w",newline="") as f:
            w=csv.writer(f);w.writerow(["modules_pct","cpu_pct"])
            w.writerows((100*k/n,100*cumulative[k]/total) for k in indices)
    user_counts = [int(r["instructions_user"]) for r in rows]
    summary["user_instructions"] = {"total": sum(user_counts),
        "median": statistics.median(user_counts), "p95": quantile(user_counts, .95)}
    names = ["OAI.Analysis.FreeWords.UltraExpectationFull",
             "OAI.Combinatorics.Ramsey.CycleClique.Construction.CertificatesK17Part012"]
    summary["examples"] = [{k:r[k] for k in
        ["module","pool","source_bytes","decide_plus_kernel_occurrences","cpu_s"]}
        for name in names for r in rows if r["module"] == name]
    gate = read_csv(root/"data/openai-math-4eaee875/measurement/census-gate/census-gate-modules.csv")
    summary["counter_comparison"] = {k:{"median_pct":100*statistics.median([float(r[k]) for r in gate]),
        "p95_pct":100*quantile([float(r[k]) for r in gate],.95)}
        for k in ["user_instruction_spread","kernel_instruction_spread","cross_condition_spread"]}
    native = read_csv(root/"research/profile-2026-10-31/systime/final/native-summary.csv")
    def guard(module, config, metric):
        matches=[r for r in native if r["module"]==module and r["config"]==config
                 and r["mode"]=="plain" and r["metric"]==metric]
        assert len(matches)==1 and matches[0]["n"]=="3"
        return float(matches[0]["median"])
    table = [r"\begin{tabular}{lrrrr}",r"\toprule",
             r"& \multicolumn{2}{c}{Wall} & \multicolumn{2}{c}{System CPU}\\",
             r"Module & Guard & No guard & Guard & No guard\\",r"\midrule"]
    summary["memory_guard"]={}
    for m in ["Grid","UMoments9","EnvelopePsiB"]:
        values=[guard(m,c,k) for k in ["wall_s","system_s"] for c in ["baseline","noM"]]
        summary["memory_guard"][m]=values
        table.append(m+" & "+" & ".join(f"{x:.3f}" for x in values)+r"\\")
    table += [r"\bottomrule",r"\end{tabular}"]
    (out/"memory-guard-table.tex").write_text("\n".join(table)+"\n")
    matrix=read_csv(root/"docs/paper/generated/system/system-summary.csv")
    def native_point(dataset, workers):
        r=[r for r in matrix if r["dataset"]==dataset and r["arm"]=="native"
           and r["policy"]=="default" and int(r["workers"])==workers]
        assert len(r)==1 and r[0]["successful"]=="3"
        return float(r[0]["cpu_s_median"]),float(r[0]["wall_s_median"])
    table=[r"\begin{tabular}{lrrr}",r"\toprule",
           r"Closure & 1 worker & 8 workers & Wall gain\\",r"\midrule"]
    for dataset,label in [("math","Nat.Basic"),("grid","Grid"),("barrier","Barrier")]:
        c1,w1=native_point(dataset,1);c8,w8=native_point(dataset,8)
        table.append(f"{label} & {c1:.1f}/{w1:.1f} & {c8:.1f}/{w8:.1f} & {w1/w8:.2f}"+r"$\times$\\")
    table += [r"\bottomrule",r"\end{tabular}",r"\par\medskip",
              r"\begin{tabular}{lrrr}",r"\toprule",
              r"Project & N/O modules & ProofServe & Official\\",r"\midrule"]
    external=read_csv(root/"docs/paper/generated/system/external-summary.csv")
    for project,label in [("newspeak","Newspeak"),("solar","Solar"),("samuelburbulla-proofs","AI proofs")]:
        points={}
        for arm in ["proofserve","official-default"]:
            r=[r for r in external if r["project"]==project and r["arm"]==arm]
            assert len(r)==1 and r[0]["successful"]=="1" and r[0]["observations"]=="1"
            points[arm]=r[0]
        r=points["proofserve"]
        cells=[f"{float(points[a]['cpu_s_median']):.1f}/{float(points[a]['wall_s_median']):.1f}"
               for a in ["proofserve","official-default"]]
        table.append(f"{label} & {r['native_closure_modules']}/{r['local_roots']} & "+" & ".join(cells)+r"\\")
    table += [r"\bottomrule",r"\end{tabular}"]
    (out/"release-evaluation-table.tex").write_text("\n".join(table)+"\n")
    inputs=[census, root/"data/lean-observations/README.md",
            root/"research/profile-2026-10-31/startup-replay/repaired-replay-analysis.md",
            root/"research/profile-2026-10-31/startup-replay/perf-hotspots.csv",
            root/"research/profile-2026-10-31/systime/final/native-summary.csv",
            root/"docs/paper/generated/system/system-summary.csv",
            root/"docs/paper/generated/system/external-summary.csv"]
    summary["input_publications"]={}
    for p in inputs:
        relative=str(p.relative_to(root))
        subprocess.run(["git","ls-files","--error-unmatch",relative],cwd=root,
                       check=True,stdout=subprocess.DEVNULL)
        summary["input_publications"][relative]=subprocess.check_output(
            ["git","log","-1","--format=%H","--",relative],cwd=root,text=True).strip()
    (out/"observation-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    tex = r"""\documentclass[tikz,border=2pt]{standalone}
\usepackage{pgfplots}\pgfplotsset{compat=1.18}
\begin{document}\begin{tikzpicture}
\begin{axis}[width=8.4cm,height=5.1cm,xmin=0,xmax=100,ymin=0,ymax=100,
xlabel={Modules, most expensive first (\%)},ylabel={Cumulative CPU time (\%)},
label style={font=\small},tick label style={font=\footnotesize},
legend style={font=\small,at={(0.98,0.04)},anchor=south east},
grid=major,grid style={gray!20}]
\addplot[gray,dashed,no marks] coordinates {(0,0)(100,100)};
\addlegendentry{Equal cost}
\addplot[blue,thick,no marks] table[x=modules_pct,y=cpu_pct,col sep=comma]{cost-share-P.csv};
\addlegendentry{P cores}
\addplot[red,dashed,thick,no marks] table[x=modules_pct,y=cpu_pct,col sep=comma]{cost-share-E.csv};
\addlegendentry{E cores}
\node[font=\small,anchor=west,fill=white] at (axis cs:7,27){Top 1\%: 25--26\% CPU};
\draw[->] (axis cs:7,26) -- (axis cs:1,25.4);
\end{axis}\end{tikzpicture}\end{document}
"""
    (out/"cpu-concentration.tex").write_text(tex)
    def compile_figure(source, companions, destination):
        with tempfile.TemporaryDirectory(prefix="proofserve-paper-") as td:
            temp=pathlib.Path(td)
            for p in [source,*companions]:shutil.copy2(p,temp/p.name)
            q=subprocess.run([args.tectonic,"--keep-logs",source.name],cwd=temp,text=True,
                             stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            warnings = [line for line in q.stdout.splitlines() if "warning:" in line.lower()]
            known = "warning: accessing absolute path " + chr(96) + "/dev/null"
            if q.returncode or any(not line.startswith(known) for line in warnings):
                raise RuntimeError(q.stdout)
            if warnings:
                summary.setdefault("figure_build_notes", {})[source.name] = warnings
                print("FIGURE_REPRODUCIBILITY_NOTE", source.name, warnings)
            shutil.copy2(temp/source.with_suffix(".pdf").name,destination)
    compile_figure(out/"cpu-concentration.tex",[out/"cost-share-P.csv",out/"cost-share-E.csv"],
                   out/"cpu-concentration.pdf")
    figure=root/"docs/paper/figures/cost-regimes.tex"
    compile_figure(figure,[figure.with_name("cost-regimes-cpu.csv"),
                          figure.with_name("cost-regimes-target-wall.csv")],figure.with_suffix(".pdf"))
    (out/"observation-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({"pools":summary["pools"],"output":str(out),"native_runs":0}))
if __name__=="__main__":
    main()
