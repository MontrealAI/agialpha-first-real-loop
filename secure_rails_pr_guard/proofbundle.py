import hashlib, json
from pathlib import Path

def build_proofbundle(outdir):
    pb=Path(outdir)/'10_proofbundle'; pb.mkdir(parents=True,exist_ok=True)
    hashes={}
    for p in Path(outdir).glob('0*.json'):
        hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    (pb/'artifact_hashes.json').write_text(json.dumps(hashes,indent=2))
    (pb/'proofbundle.json').write_text(json.dumps({'schema_version':'securerails.proofbundle.v1','artifacts':list(hashes),'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'},indent=2))
    (pb/'replay_instructions.md').write_text('Replay by rerunning CLI on same inputs.\n\nNo Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.')
