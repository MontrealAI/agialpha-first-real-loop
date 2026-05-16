from agialpha_enterprise_pilot.regulated_boundary import triage

def test_blocked_domain_is_blocked():
    t=triage({"domain":"medical advice"})
    assert t["status"] in {"blocked_human_review_required","blocked"}
