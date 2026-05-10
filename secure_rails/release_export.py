from __future__ import annotations

import json
from pathlib import Path


def build_export_plan(release_id: str, out: Path) -> dict:
    """Build a Marketplace-ready export plan for a future dedicated action repository."""
    plan = {
        "schema_version": "securerails.export_plan.v1",
        "release_id": release_id,
        "marketplace_publication_allowed_now": False,
        "recommended_target_repository": "MontrealAI/securerails-pr-guard-action",
        "required_repository_shape": {
            "public_repository": True,
            "root_action_yml": True,
            "workflow_files_present": False,
            "action_only_scope": True,
        },
        "required_release_controls": [
            "semantic_version_tags",
            "release_notes",
            "checksums",
            "provenance_record_when_available",
            "claim_boundary",
            "no_certification_claims",
        ],
        "next_step": "export to dedicated action repository",
    }
    out.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return plan
