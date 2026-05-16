from agialpha_enterprise_pilot.settlement_receipt import create_receipt

def test_receipt_has_token_boundary_notice():
    r=create_receipt("p1","w1")
    assert "No wallet" in r["notice"]
