from pathlib import Path
import json

def write_generated_docs(out_dir, repo_root):
    root=Path(repo_root); d=root/'docs'/'_generated'/'secure-rails'/'repo-security'; d.mkdir(parents=True, exist_ok=True)
    latest={'baseline':'securerails-repo-security-baseline-001'}
    (d/'latest.json').write_text(json.dumps(latest,indent=2))
    (d/'baselines.json').write_text(json.dumps([latest],indent=2))
    (d/'summary.json').write_text(json.dumps({'status':'advisory'},indent=2))
