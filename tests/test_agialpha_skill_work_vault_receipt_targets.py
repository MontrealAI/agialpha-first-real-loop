import pytest

from agialpha_engine.work_vault import build_skill_work_vault_receipt


def test_receipt_requires_at_least_one_target_agent():
    with pytest.raises(ValueError, match="target_agent_ids"):
        build_skill_work_vault_receipt(
            receipt_id="r1",
            skill_id="s1",
            source_job_id="j1",
            source_agent_id="a1",
            target_agent_ids=[],
            utility_budget_units=100,
        )
