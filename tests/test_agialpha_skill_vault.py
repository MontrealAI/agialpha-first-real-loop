from agialpha_engine.skill_vault import make_vault, publish_skill_package


def _skill():
    return {
        "skill_id": "skill-1",
        "source_job_id": "job-1",
        "source_agent_id": "agent-1",
        "raw_task_result_ids": ["raw-job-1"],
        "proofbundle_id": "pb-skill-1",
        "evidence_docket_id": "ed-skill-1",
        "allowed_import_scope": "sandbox_only",
        "claim_boundary": "bounded local evidence only",
        "token_boundary": "$AGIALPHA utility-only accounting",
        "regulated_boundary": "regulated decisioning blocked",
    }


def test_publish_skill_package_requires_raw_logs_and_evidence_ids():
    entry = publish_skill_package(_skill())
    assert entry["published"] is True
    assert entry["activation_status"] == "sandbox_registered_inactive_outside_sandbox"
    assert entry["raw_task_result_ids"] == ["raw-job-1"]
    assert entry["proofbundle_id"] == "pb-skill-1"
    assert entry["evidence_docket_id"] == "ed-skill-1"
    assert entry["human_review_required"] is True
    assert entry["autonomous_persistence_allowed"] is False
    assert entry["no_auto_merge"] is True


def test_publish_skill_package_rejects_missing_required_evidence():
    for field in ["raw_task_result_ids", "proofbundle_id", "evidence_docket_id"]:
        skill = _skill()
        skill[field] = [] if field == "raw_task_result_ids" else ""
        try:
            publish_skill_package(skill)
        except ValueError:
            pass
        else:
            raise AssertionError(f"missing {field} should fail")


def test_make_vault_preserves_skill_packages_and_counts_entries():
    vault = make_vault([_skill()])
    assert vault["schema_version"] == "agialpha.network_skill_vault.v1"
    assert vault["skill_count"] == 1
    assert vault["skill_packages"][0]["skill_id"] == "skill-1"
    assert vault["vault_entries"][0]["skill_id"] == "skill-1"
