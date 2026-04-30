from agialpha_evidence_hub.validate import validate_manifest

def test_schema_required_fields():
    m={'schema_version':'agialpha.evidence_run.v1','experiment_slug':'helios-001','claim_boundary':'does not claim achieved AGI','run_id':'1','status':'success','metrics':{}}
    validate_manifest(m)
