from agialpha_enterprise_pilot.proofbundle import create_proofbundle

def test_proofbundle_generated():
    p=create_proofbundle("p1","j1")
    assert p["proofbundle_id"]
