from agialpha_engine.semantic_tests import run_semantic_negative_tests


def test_semantic_negative_tests_reject_bad_cases():
    result = run_semantic_negative_tests()
    assert result["pass"] is True
    assert all(row["blocked"] for row in result["tests"].values())
    assert "[REDACTED_SECRET_LIKE_FIXTURE]" in result["tests"]["secret_like_fixture_redaction"]["input"]
