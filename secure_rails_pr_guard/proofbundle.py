import hashlib, json
from pathlib import Path


def build_proofbundle(outdir):
    out_root = Path(outdir)
    pb = out_root / '10_proofbundle'
    pb.mkdir(parents=True, exist_ok=True)

    hashes = {}
    for p in sorted(out_root.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(out_root)
        if rel.parts and rel.parts[0] == '10_proofbundle':
            continue
        if p.name == 'summary.md':
            continue
        hashes[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()

    (pb / 'artifact_hashes.json').write_text(json.dumps(hashes, indent=2))
    (pb / 'proofbundle.json').write_text(json.dumps({
        'schema_version': 'securerails.proofbundle.v1',
        'artifact_count': len(hashes),
        'artifacts': list(hashes.keys()),
        'claim_boundary': 'SecureRails is AI-agent security governance and proof-bound defensive remediation.'
    }, indent=2))
    (pb / 'replay_instructions.md').write_text('Replay by rerunning CLI on same inputs.\n\nNo Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.')
