from __future__ import annotations

from typing import Any

from .work_vault import make_skill_publication_receipt


def settle_skill_publication(*, run_id: str, accepted_skill_packages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for skill in accepted_skill_packages:
        receipts.append(
            make_skill_publication_receipt(
                run_id=run_id,
                skill_id=str(skill.get("skill_id", "unknown-skill")),
                source_job_id=str(skill.get("source_job_id", "unknown-job")),
                units=1,
            )
        )
    return receipts
