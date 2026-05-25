from __future__ import annotations

from typing import Any

from .work_vault import make_skill_publication_receipt


def settle_skill_publication(*, run_id: str, accepted_skill_packages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for skill in accepted_skill_packages:
        skill_id = skill.get("skill_id")
        source_job_id = skill.get("source_job_id")
        source_agent_id = skill.get("source_agent_id")
        target_agent_ids = skill.get("target_agent_ids")
        if not isinstance(skill_id, str) or not skill_id:
            raise ValueError("skill package missing required non-empty skill_id")
        if not isinstance(source_job_id, str) or not source_job_id:
            raise ValueError(f"skill package {skill_id} missing required non-empty source_job_id")
        if not isinstance(source_agent_id, str) or not source_agent_id:
            raise ValueError(f"skill package {skill_id} missing required non-empty source_agent_id")
        if not isinstance(target_agent_ids, list) or not target_agent_ids:
            raise ValueError(f"skill package {skill_id} missing required non-empty target_agent_ids")
        receipts.append(
            make_skill_publication_receipt(
                run_id=run_id,
                skill_id=skill_id,
                source_job_id=source_job_id,
                source_agent_id=source_agent_id,
                target_agent_ids=[str(t) for t in target_agent_ids],
            )
        )
    return receipts
