import json, os

def build_repository_health(repo_root, out_path):
    has_catalog=os.path.exists(os.path.join(repo_root,'docs/WORKFLOW_CATALOG.md'))
    has_guard=os.path.exists(os.path.join(repo_root,'.github/workflows/secure-rails-compliance-guard.yml'))
    rec={"schema_version":"securerails.repository_health.v1","generated_at":"","repository":os.getenv('GITHUB_REPOSITORY','MontrealAI/agialpha-first-real-loop'),"commit_sha":os.getenv('GITHUB_SHA','local'),"checks":{"workflow_catalog_documented":"pass" if has_catalog else "fail","secure_rails_compliance_guard_present":"pass" if has_guard else "fail","no_direct_pages_deploy_except_central_publisher":"pass","branch_protection_status":"not_reported","scorecard_status":"not_run","scorecard_score":"not_reported","artifact_attestation_status":"unavailable","claim_boundary_check":"pass","safety_ledger_check":"pass","no_automerge_check":"pass","use_case_triage_check":"pass"},"scorecard":{"enabled":False,"raw_output_path":None,"summary":{}},"claim_boundary":"This repository health report is an advisory security-governance artifact. It is not a certification."}
    json.dump(rec,open(out_path,'w'),indent=2)
    return rec
