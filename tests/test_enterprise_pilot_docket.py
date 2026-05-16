from agialpha_enterprise_pilot.docket import create_docket

def test_docket_generated():
    d=create_docket("p1","pb1")
    assert d["evidence_docket_id"]
