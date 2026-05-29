from agialpha_engine.skill_import import create_skill_import_event


def test_create_skill_import_event_sets_activation_status_for_proof_bound_import():
    skill = {
        "skill_id": "skill-1",
        "proofbundle_id": "pb-skill-1",
        "evidence_docket_id": "ed-skill-1",
        "raw_task_result_ids": ["raw-job-1"],
    }
    event = create_skill_import_event("import-1", skill, "agent-2")

    assert event["import_status"] == "imported_inactive_outside_sandbox"
    assert event["activation_status"] == "inactive"
    assert event["active_outside_sandbox"] is False
    assert event["production_activation_allowed"] is False
    assert event["proofbundle_id"] == "pb-skill-1"
    assert event["evidence_docket_id"] == "ed-skill-1"
    assert event["skill_import_hash"]


def test_create_skill_import_event_quarantines_missing_evidence_without_empty_schema_fields():
    event = create_skill_import_event("import-2", {"skill_id": "skill-2"}, "agent-3")

    assert event["import_status"] == "quarantined_missing_evidence"
    assert event["activation_status"] == "quarantined"
    assert event["active_outside_sandbox"] is False
    assert event["production_activation_allowed"] is False
    assert event["proofbundle_id"] == "unavailable"
    assert event["evidence_docket_id"] == "unavailable"
    assert "missing ProofBundle" in event["quarantine_reason"]
