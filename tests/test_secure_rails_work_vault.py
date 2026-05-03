import json

from scripts.secure_rails_work_vault_pipeline import CLAIM_BOUNDARY, generate_record


def test_work_vault_pipeline_is_deterministic(tmp_path):
    payload = {
        "vault_id": "vault-defensive-001",
        "defensive_scope": "repo-owned defensive remediation planning",
        "job_type": "defensive_remediation",
        "mark_units": 42,
        "sovereign_id": "sovereign-defensive-alpha",
        "reviewers": ["human.security.reviewer"],
        "status": "completed",
        "decision": "safe_remediation",
        "reviewed_by": "human.security.reviewer",
        "created_at": "2026-05-03T00:00:00+00:00",
    }

    first = generate_record(payload)
    second = generate_record(dict(payload))

    assert first == second
    assert first["evidence_docket"]["claim_boundary_statement"] == CLAIM_BOUNDARY
    assert first["utility_settlement"]["real_transfer"] is False


def test_sample_output_matches_generator():
    payload = json.loads(open("sample_outputs/secure_rails_work_vault/sample_input.json", encoding="utf-8").read())
    expected = json.loads(open("sample_outputs/secure_rails_work_vault/sample_work_vault_run.json", encoding="utf-8").read())
    assert generate_record(payload) == expected
