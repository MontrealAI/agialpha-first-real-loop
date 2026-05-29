from agialpha_engine.redaction import redact_document, redact_text


def test_network_redaction_report_stores_salt_hash_not_raw_secret():
    text = "token ghp_abcdefghijklmnopqrstuvwxyz and email reviewer@example.com and phone 415-555-1212"
    report = redact_document(text, run_id="run-003", root_hash="root", path="fixture.txt")
    assert "ghp_abcdefghijklmnopqrstuvwxyz" not in report["redacted_text"]
    assert "reviewer@example.com" not in report["redacted_text"]
    assert "415-555-1212" not in report["redacted_text"]
    assert report["raw_secret_values_stored"] is False
    assert {finding["path"] for finding in report["findings"]} == {"fixture.txt"}
    assert all(finding["line"] == 1 for finding in report["findings"])
    assert all(finding.get("salt_hash") for finding in report["findings"])
    assert all("ghp_abcdefghijklmnopqrstuvwxyz" not in str(finding) for finding in report["findings"])


def test_redact_text_finding_includes_salt_hash_for_replayable_digest():
    redacted, findings = redact_text("Bearer abcdefghijklmnopqrstuvwxyz123456", "run-003", "root")
    assert "abcdefghijklmnopqrstuvwxyz123456" not in redacted
    assert findings and findings[0]["salt_hash"]
    assert findings[0]["salted_hash"]


def test_redact_document_redacts_multiline_private_key_before_line_splitting():
    pem = """safe prefix
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASC
raw-private-key-material
-----END PRIVATE KEY-----
contact reviewer@example.com
"""
    report = redact_document(pem, run_id="run-003", root_hash="root", path="fixture.pem")
    assert "-----BEGIN PRIVATE KEY-----" not in report["redacted_text"]
    assert "raw-private-key-material" not in report["redacted_text"]
    assert "-----END PRIVATE KEY-----" not in report["redacted_text"]
    assert "reviewer@example.com" not in report["redacted_text"]
    private_key_findings = [f for f in report["findings"] if f["finding_type"] == "private_key_block"]
    assert private_key_findings
    assert private_key_findings[0]["line"] == 2
    assert private_key_findings[0]["path"] == "fixture.pem"
    assert all("raw-private-key-material" not in str(finding) for finding in report["findings"])
