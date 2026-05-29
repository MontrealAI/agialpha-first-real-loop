from agialpha_engine.work_vault import RECEIPT_TEXT, make_skill_publication_receipt


def test_skill_work_vault_receipt_is_utility_only_and_non_payment():
    receipt = make_skill_publication_receipt(
        run_id="run-1",
        skill_id="skill-1",
        source_job_id="job-1",
        source_agent_id="agent-1",
        target_agent_ids=["agent-2", "agent-3", "agent-4"],
    )
    assert receipt["wallet_used"] is False
    assert receipt["custody_used"] is False
    assert receipt["payment_executed"] is False
    assert receipt["token_price_used"] is False
    assert receipt["investment_claim_made"] is False
    assert receipt["settlement_mode"] == "synthetic_local_json_receipt_only"
    assert receipt["receipt_note"] == RECEIPT_TEXT
    assert "No wallet, custody, payment" in receipt["receipt_note"]
    assert "investment return" in receipt["receipt_note"]


def test_skill_work_vault_receipt_rejects_empty_target_agents():
    try:
        make_skill_publication_receipt(run_id="run", skill_id="skill", source_job_id="job", source_agent_id="agent", target_agent_ids=[])
    except ValueError as exc:
        assert "target_agent_ids" in str(exc)
    else:
        raise AssertionError("empty target_agent_ids should fail")
