from agialpha_evidence_hub.validate import validate_manifest

def test_schema_required():
    m={"schema_version":"agialpha.evidence_run.v1","experiment_slug":"x","run_id":"1","status":"success","claim_boundary":"does not claim","metrics":{}}
    validate_manifest(m)
