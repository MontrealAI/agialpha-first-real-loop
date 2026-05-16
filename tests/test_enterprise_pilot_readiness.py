from agialpha_enterprise_pilot.pilot_readiness import compute_pilot_readiness_score

def test_readiness_cap_pending():
    r=compute_pilot_readiness_score(customer_review_status="pending", customer_review_status_score=100)
    assert r["pilot_readiness_score"]<=70
