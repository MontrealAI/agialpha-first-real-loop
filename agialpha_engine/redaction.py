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


def _redact_with_findings(text: str, run_id: str, root_hash: str) -> tuple[str, list[dict[str, Any]]]:
    salt = _stable_run_salt(run_id, root_hash)
    salt_hash = _salt_hash(salt)
    candidates: list[dict[str, Any]] = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            secret = match.group(0)
            digest = hashlib.sha256((salt + secret).encode()).hexdigest()[:16]
            candidates.append(
                {
                    "finding_type": name,
                    "salt_hash": salt_hash,
                    "salted_hash": digest,
                    "redacted_preview": "[REDACTED]",
                    "start": match.start(),
                    "end": match.end(),
                    "line": text.count("\n", 0, match.start()) + 1,
                }
            )

    selected: list[dict[str, Any]] = []
    occupied: list[tuple[int, int]] = []
    for candidate in sorted(candidates, key=lambda c: (c["start"], -(c["end"] - c["start"]))):
        span = (candidate["start"], candidate["end"])
        if any(span[0] < used_end and span[1] > used_start for used_start, used_end in occupied):
            continue
        selected.append(candidate)
        occupied.append(span)

    redacted_parts: list[str] = []
    cursor = 0
    for finding in sorted(selected, key=lambda f: f["start"]):
        redacted_parts.append(text[cursor:finding["start"]])
        redacted_parts.append("[REDACTED]")
        cursor = finding["end"]
    redacted_parts.append(text[cursor:])

    public_findings = [
        {
            "finding_type": finding["finding_type"],
            "salt_hash": finding["salt_hash"],
            "salted_hash": finding["salted_hash"],
            "redacted_preview": finding["redacted_preview"],
            "line": finding["line"],
        }
        for finding in sorted(selected, key=lambda f: f["start"])
    ]
    return "".join(redacted_parts), public_findings


def redact_text(text: str, run_id: str, root_hash: str) -> tuple[str, list[dict[str, Any]]]:
    redacted, findings = _redact_with_findings(text, run_id, root_hash)
    return redacted, [
        {k: v for k, v in finding.items() if k != "line"}
        for finding in findings
    ]


def redact_document(text: str, *, run_id: str, root_hash: str, path: str) -> dict[str, Any]:
    """Redact a fixture/report while retaining only type/path/line/salted digest metadata."""
    redacted_text, raw_findings = _redact_with_findings(text, run_id, root_hash)
    findings = [{**finding, "path": path} for finding in raw_findings]
    return {
        "schema_version": "agialpha.engine.redaction_report.v1",
        "path": path,
        "redacted_text": redacted_text,
        "findings": findings,
        "raw_secret_values_stored": False,
    }
