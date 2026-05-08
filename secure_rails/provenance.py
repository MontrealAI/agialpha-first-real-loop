import hashlib, json, os
from datetime import datetime, timezone

def build_provenance(repo_root, manifest_path, out_path):
    data=open(manifest_path,'rb').read()
    rec={"schema_version":"securerails.provenance_record.v1","generated_at":datetime.now(timezone.utc).isoformat(),"repository":os.getenv('GITHUB_REPOSITORY','MontrealAI/agialpha-first-real-loop'),"commit_sha":os.getenv('GITHUB_SHA','local'),"branch":os.getenv('GITHUB_REF_NAME','local'),"workflow_name":os.getenv('GITHUB_WORKFLOW','local'),"workflow_file":'.github/workflows/securerails-supply-chain-provenance-001.yml',"workflow_run_id":os.getenv('GITHUB_RUN_ID','local'),"workflow_run_url":f"https://github.com/{os.getenv('GITHUB_REPOSITORY','MontrealAI/agialpha-first-real-loop')}/actions/runs/{os.getenv('GITHUB_RUN_ID','0')}","event_name":os.getenv('GITHUB_EVENT_NAME','local'),"actor":os.getenv('GITHUB_ACTOR','local'),"artifact_manifest_sha256":hashlib.sha256(data).hexdigest(),"builder":{"type":"github_actions" if os.getenv('GITHUB_ACTIONS') else 'local','runner':os.getenv('RUNNER_NAME','local'),'permissions_summary':{}},"attestation":{"status":"unavailable" if not os.getenv('GITHUB_ACTIONS') else "not_attempted","method":"local_provenance_record","attestation_paths":[],"verification_instructions":"Use sha256sum on artifact files and compare to artifact_manifest.json."},"claim_boundary":"This provenance record documents where and how artifacts were produced. It is not a security certification."}
    json.dump(rec,open(out_path,'w'),indent=2)
    return rec
