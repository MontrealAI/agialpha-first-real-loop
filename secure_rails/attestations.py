import json
from datetime import datetime, timezone


def build_attestation_record(
    out_path,
    attempt=False,
    supported=False,
    reason='local run',
    attestation_paths=None,
):
    status = 'not_attempted'
    method = 'local_provenance_record'
    if attempt and supported:
        status = 'generated'
        method = 'github_artifact_attestation'
    elif attempt and not supported:
        status = 'unavailable'
        method = 'github_artifact_attestation'

    rec = {
        'schema_version': 'securerails.attestation_record.v1',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'attestation': {
            'status': status,
            'method': method,
            'reason': reason,
            'attestation_paths': attestation_paths or [],
            'verification_instructions': (
                'Use `gh attestation verify` when GitHub attestation is available; '
                'otherwise validate file hashes against artifact_manifest.json.'
            ),
        },
        'claim_boundary': (
            'This attestation record is supply-chain evidence and does not certify security.'
        ),
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(rec, f, indent=2)
    return rec
