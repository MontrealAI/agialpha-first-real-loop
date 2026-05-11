from pathlib import Path
from datetime import datetime, timezone
import json

def sarif_ingestion_readiness(repo_root):
    root=Path(repo_root)
    files=[str(p.relative_to(root)) for p in root.rglob('*.sarif')]
    return {
      'schema_version':'securerails.sarif_ingestion_record.v1','generated_at':datetime.now(timezone.utc).isoformat(),'repository':'',
      'sarif_files_detected':files,'upload_supported':'not_reported','upload_attempted':False,'upload_status':'not_attempted',
      'claim_boundary':'SARIF ingestion is advisory code-scanning integration and not certification.'
    }

def write_sarif_readiness(repo_root,out):
    d=sarif_ingestion_readiness(repo_root); Path(out).write_text(json.dumps(d,indent=2)); return d
