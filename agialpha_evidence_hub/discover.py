from pathlib import Path
import json,re

def slugify(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def discover(repo_root='.'):
    root=Path(repo_root)
    manifests=[str(p) for p in root.rglob('evidence-run-manifest.json')]
    workflows=[]
    for wf in (root/'.github/workflows').glob('*.yml'):
        txt=wf.read_text(errors='ignore')
        m=re.search(r'^name:\s*(.+)$',txt,re.M)
        workflows.append({'file':str(wf.relative_to(root)),'name':m.group(1).strip() if m else wf.stem,'slug':slugify(wf.stem)})
    docs=[str(p) for p in root.rglob('docs/**/*.html')]
    return {'manifests':manifests,'workflows':workflows,'docs':docs}

def discover_to_file(repo_root,out):
    Path(out).write_text(json.dumps(discover(repo_root),indent=2))
