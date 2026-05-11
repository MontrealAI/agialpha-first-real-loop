from pathlib import Path
import json, hashlib

def build_evidence(out_dir):
    out=Path(out_dir); pb=out/'proofbundle'; ed=out/'evidence_docket'; pb.mkdir(exist_ok=True); ed.mkdir(exist_ok=True)
    (pb/'proofbundle.json').write_text(json.dumps({'claim_boundary':'Advisory security-governance evidence only.'},indent=2))
    hashes={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.json')}
    (pb/'artifact_hashes.json').write_text(json.dumps(hashes,indent=2))
    (pb/'replay_instructions.md').write_text('Re-run secure_rails repo-security baseline.')
    (ed/'00_manifest.json').write_text(json.dumps({'claim_boundary':'Advisory security-governance evidence only.'},indent=2))
    for n in ['01_claims_matrix.json','03_dependency_inventory.json','04_code_scanning_readiness.json','05_secret_scanning_posture.json','06_sarif_ingestion_record.json','07_safety_ledger.json']:
        (ed/n).write_text('{}')
    (ed/'02_scope_and_claim_boundary.md').write_text('No Evidence Docket, no empirical SOTA claim.')
    (ed/'08_human_review_checklist.md').write_text('- [ ] Human review required')
