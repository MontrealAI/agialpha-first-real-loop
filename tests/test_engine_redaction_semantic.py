from agialpha_engine.redaction import redact_text


def test_redaction_no_raw_secret_leak():
    text = "token ghp_abcdefghijklmnopqrstuvwxyz and email x@y.com"
    redacted, findings = redact_text(text, "run1", "root1")
    assert "ghp_abcdefghijklmnopqrstuvwxyz" not in redacted
    assert "x@y.com" not in redacted
    assert findings


def test_high_entropy_redaction_does_not_redact_plain_hash_with_later_uppercase_text():
    sha256_digest = "a" * 64
    redacted, findings = redact_text(f"artifact_hash={sha256_digest} status OK AB 12", "run1", "root1")
    assert sha256_digest in redacted
    assert not any(f["finding_type"] == "high_entropy_string" for f in findings)


def test_high_entropy_redaction_redacts_mixed_candidate_token():
    token = "AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
    redacted, findings = redact_text(f"secret={token}", "run1", "root1")
    assert token not in redacted
    assert any(f["finding_type"] == "high_entropy_string" for f in findings)
