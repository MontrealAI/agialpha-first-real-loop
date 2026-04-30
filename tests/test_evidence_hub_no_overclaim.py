import pytest
from agialpha_evidence_hub.validate import validate_manifest

def test_overclaim_rejected():
    with pytest.raises(ValueError):
        validate_manifest({"schema_version":"agialpha.evidence_run.v1","experiment_slug":"x","run_id":"1","status":"success","claim_boundary":"achieved AGI","metrics":{}})
