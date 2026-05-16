from agialpha_enterprise_pilot.customer_review import create_customer_review

def test_customer_review_default_pending():
    c=create_customer_review("p1")
    assert c["decision"]=="pending"
