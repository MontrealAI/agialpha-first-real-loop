from pathlib import Path
from datetime import datetime
from .registry import register
from .validate import default_manifest

def backfill(repo_root='.', registry='evidence_registry'):
    root=Path(repo_root)
    candidates=['coldchain-energy-loop-001','l4-l7-evidence-autopilot','helios-001','helios-002','helios-003','helios-004','cyber-sovereign-001','cyber-sovereign-002','cyber-sovereign-003','benchmark-gauntlet-001','omega-gauntlet-001']
    for slug in candidates:
        if any(root.glob(f'**/*{slug}*')):
            m=default_manifest(slug)
            m.update({'source':'historical_backfill','status':'discovered','generated_at':datetime.utcnow().isoformat()+'Z','run_id':f'historical-{slug}'})
            register(m,registry)
