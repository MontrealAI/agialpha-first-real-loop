import json
from pathlib import Path

SCAN_DIRS=['docs','evidence-docket','autonomous','runs','sample_outputs']

def discover(repo_root='.'):
    root=Path(repo_root)
    manifests=[]
    for pat in ['**/evidence-run-manifest.json','**/00_manifest.json','**/*scoreboard*.json','.github/workflows/*.yml']:
      for p in root.glob(pat):
        if '.git/' in str(p):
            continue
        manifests.append(str(p.relative_to(root)))
    out={'repo_root':str(root), 'discovered_files':sorted(set(manifests))}
    return out

def discover_to_file(repo_root='.', out='evidence_registry/discovered.json'):
    payload=discover(repo_root)
    p=Path(out); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(payload,indent=2))
    return payload
