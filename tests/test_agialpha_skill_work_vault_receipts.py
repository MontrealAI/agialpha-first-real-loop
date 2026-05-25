import pytest

from agialpha_engine.work_vault import build_skill_work_vault_receipt


def test_rejects_empty_target_agent_ids():
    with pytest.raises(ValueError, match="at least one target agent"):
        build_skill_work_vault_receipt(
            receipt_id="r-1",
            skill_id="s-1",
            source_job_id="j-1",
            source_agent_id="a-1",
            target_agent_ids=[],
        )


def test_receipt_has_positive_import_targets_and_fee():
    receipt = build_skill_work_vault_receipt(
        receipt_id="r-1",
        skill_id="s-1",
        source_job_id="j-1",
        source_agent_id="a-1",
        target_agent_ids=["a-2", "a-3"],
        utility_budget_units=100,
    )
    assert len(receipt["target_agent_ids"]) >= 1
    assert receipt["skill_import_fee_units"] >= 1
