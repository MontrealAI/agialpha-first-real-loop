import pytest
from agialpha_evidence_hub.validate import validate_manifest

def test_reject_overclaim():
    with pytest.raises(ValueError):
        validate_manifest({'schema_version':'agialpha.evidence_run.v1','experiment_slug':'x','claim_boundary':'achieved AGI','run_id':'1','status':'success','metrics':{}})
