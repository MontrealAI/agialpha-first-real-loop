from agialpha_engine.redaction import redact_text


def test_redaction_no_raw_secret_leak():
    text = "token ghp_abcdefghijklmnopqrstuvwxyz and email x@y.com"
    redacted, findings = redact_text(text, "run1", "root1")
    assert "ghp_abcdefghijklmnopqrstuvwxyz" not in redacted
    assert "x@y.com" not in redacted
    assert findings


def test_high_entropy_redaction_does_not_consume_plain_hash_with_later_uppercase_text():
    digest = "0" * 64
    redacted, findings = redact_text(f"artifact_hash={digest} status OK AB 12", "run1", "root1")
    assert digest in redacted
    assert not any(f["finding_type"] == "high_entropy_string" for f in findings)


def test_high_entropy_redaction_still_catches_mixed_secret_like_token():
    secret = "Aa11" * 10
    redacted, findings = redact_text(f"secret={secret}", "run1", "root1")
    assert secret not in redacted
    assert any(f["finding_type"] == "high_entropy_string" for f in findings)
