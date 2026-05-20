from agialpha_engine.measured_recursive_claim import claim_status_from_gate


def test_claim_gate_public_text_blocked():
    out = claim_status_from_gate({"status": "blocked"})
    assert out["public_text"] == "Not demonstrated yet."


def test_claim_gate_public_text_supported():
    out = claim_status_from_gate({"status": "supported"})
    assert "recursively improves" in out["public_text"]
