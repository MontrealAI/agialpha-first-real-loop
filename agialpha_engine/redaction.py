from __future__ import annotations

import hashlib
import re
from typing import Any

PATTERNS = {
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{16,}\b"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "bearer": re.compile(r"\bBearer\s+[A-Za-z0-9\-_.=]{16,}\b", re.IGNORECASE),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "jwt_like": re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    "private_key_block": re.compile(
        r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP |ENCRYPTED )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |OPENSSH |EC |DSA |PGP |ENCRYPTED )?PRIVATE KEY-----"
    ),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b"),
    "stripe_key": re.compile(r"\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{16,}\b"),
    "phone_pii": re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?[2-9][0-9]{2}\)?[-.\s]?)[0-9]{3}[-.\s]?[0-9]{4}(?!\d)"),
    "high_entropy_string": re.compile(r"\b(?=[A-Za-z0-9_/-]{32,}\b)(?=[A-Za-z0-9_/-]*[A-Z][A-Za-z0-9_/-]*[A-Z])(?=[A-Za-z0-9_/-]*[a-z][A-Za-z0-9_/-]*[a-z])(?=[A-Za-z0-9_/-]*[0-9][A-Za-z0-9_/-]*[0-9])[A-Za-z0-9_/-]{32,}\b"),
}


def _stable_run_salt(run_id: str, root_hash: str) -> str:
    """Return a replayable run-scoped salt; reports expose only its hash."""
    return hashlib.sha256(f"{run_id}:{root_hash}:redaction-run-salt".encode()).hexdigest()


def _salt_hash(salt: str) -> str:
    return hashlib.sha256(f"{salt}:salt-hash".encode()).hexdigest()


def redact_text(text: str, run_id: str, root_hash: str) -> tuple[str, list[dict[str, Any]]]:
    salt = _stable_run_salt(run_id, root_hash)
    salt_hash = _salt_hash(salt)
    findings = []
    out = text
    for name, pattern in PATTERNS.items():
        for m in list(pattern.finditer(out)):
            secret = m.group(0)
            digest = hashlib.sha256((salt + secret).encode()).hexdigest()[:16]
            findings.append({"finding_type": name, "salt_hash": salt_hash, "salted_hash": digest, "redacted_preview": "[REDACTED]"})
            out = out.replace(secret, "[REDACTED]")
    return out, findings


def redact_document(text: str, *, run_id: str, root_hash: str, path: str) -> dict[str, Any]:
    """Redact a fixture/report while retaining only type/path/line/salted digest metadata."""
    redacted_lines: list[str] = []
    findings: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        redacted_line, line_findings = redact_text(line, run_id, root_hash)
        redacted_lines.append(redacted_line)
        for finding in line_findings:
            findings.append({**finding, "path": path, "line": line_number})
    return {
        "schema_version": "agialpha.engine.redaction_report.v1",
        "path": path,
        "redacted_text": "\n".join(redacted_lines),
        "findings": findings,
        "raw_secret_values_stored": False,
    }
