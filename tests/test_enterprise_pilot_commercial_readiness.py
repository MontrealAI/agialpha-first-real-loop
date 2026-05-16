from agialpha_enterprise_pilot.commercial_readiness import build_scorecard
def test_caps():
 s=build_scorecard(has_attestation=False)
 assert s['commercial_readiness_tier'] in {'C0','C1'}
