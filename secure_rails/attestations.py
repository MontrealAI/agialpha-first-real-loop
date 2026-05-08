import json


def build_attestation_record(out_path, attempt=False, supported=False, reason='local run'):
    status = 'not_attempted'
    if attempt and supported:
        status = 'generated'
    elif attempt and not supported:
        status = 'unavailable'
    rec = {
        'schema_version': 'securerails.attestation_record.v1',
        'attestation': {
            'status': status,
            'method': 'github_artifact_attestation' if supported else 'local_provenance_record',
            'reason': reason,
        },
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(rec, f, indent=2)
    return rec
