from pathlib import Path
r=Path('/workspaces/repository')
p=r/'docs/research-status.md'
v=p.read_text().replace(' |\\n\\n## Terminal failures',' |\n\n## Terminal failures').replace('\n\n| Whole-source producer diagnostics','\n| Whole-source producer diagnostics')
p.write_text(v)
p=r/'docs/evaluation.md';v=p.read_text();p.write_text(v[:-2]+'\n'if v.endswith('\\n')else v)
