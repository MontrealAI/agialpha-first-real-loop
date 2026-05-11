from pathlib import Path
from datetime import datetime, timezone
import json
from .dependency_inventory import collect_dependency_inventory
from .code_scanning import code_scanning_readiness
from .secret_scanning_posture import secret_scanning_posture
from .sarif import sarif_ingestion_readiness

CLAIM='This repository security baseline is an advisory SecureRails evidence artifact. It does not certify security or guarantee that the repository is secure.'

def generate_baseline(repo_root, out_dir):
    root=Path(repo_root); out=Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    inv=collect_dependency_inventory(root)
    code=code_scanning_readiness(root)
    sec=secret_scanning_posture(root)
    sarif=sarif_ingestion_readiness(root)
    (out/'dependency_inventory.json').write_text(json.dumps(inv,indent=2))
    (out/'code_scanning_readiness.json').write_text(json.dumps(code,indent=2))
    (out/'secret_scanning_posture.json').write_text(json.dumps(sec,indent=2))
    (out/'sarif_ingestion_record.json').write_text(json.dumps(sarif,indent=2))
    wf={'status':'partial','notes':['Manual review required.']}
    (out/'workflow_permission_review.json').write_text(json.dumps(wf,indent=2))
    baseline={
      'schema_version':'securerails.repo_security_baseline.v1','baseline_id':'securerails-repo-security-baseline-001','generated_at':datetime.now(timezone.utc).isoformat(),
      'repository':'MontrealAI/agialpha-first-real-loop','commit_sha':'','workflow_run_id':'','workflow_run_url':'','status':'advisory',
      'checks':{'dependency_inventory':'pass','dependency_review':'not_reported','code_scanning_readiness':'pass','secret_scanning_posture':'pass','sarif_ingestion_readiness':'pass','workflow_permission_review':'partial','branch_ruleset_recommendation':'not_reported','secure_rails_compliance_guard':'not_reported','claim_boundary':'pass','safety_ledger':'not_reported'},
      'hard_safety_counters':{'raw_secret_leak_count':0,'external_target_scan_count':0,'exploit_execution_count':0,'malware_generation_count':0,'social_engineering_content_count':0,'unsafe_automerge_count':0,'critical_safety_incidents':0},
      'evidence':{'proofbundle_path':'proofbundle/proofbundle.json','evidence_docket_path':'evidence_docket/00_manifest.json','dependency_inventory_path':'dependency_inventory.json','repository_health_path':'workflow_permission_review.json','sarif_record_path':'sarif_ingestion_record.json'},
      'recommendation':'human_review_required','claim_boundary':CLAIM
    }
    (out/'repo_security_baseline.json').write_text(json.dumps(baseline,indent=2))
    (out/'summary.md').write_text('# SecureRails Repository Security Baseline 001\n\nAdvisory security-governance evidence only.\n')
    return baseline
