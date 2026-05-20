from agialpha_engine.redaction import redact_text


def test_redaction_no_raw_secret_leak():
    text = "token ghp_abcdefghijklmnopqrstuvwxyz and email x@y.com"
    redacted, findings = redact_text(text, "run1", "root1")
    assert "ghp_abcdefghijklmnopqrstuvwxyz" not in redacted
    assert "x@y.com" not in redacted
    assert findings
