from __future__ import annotations

import hashlib
import re
from typing import Any

PATTERNS = {
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{16,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer": re.compile(r"\bBearer\s+[A-Za-z0-9\-_.=]{16,}\b", re.IGNORECASE),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
}


def redact_text(text: str, run_id: str, root_hash: str) -> tuple[str, list[dict[str, Any]]]:
    salt = hashlib.sha256(f"{run_id}{root_hash}redaction-salt".encode()).hexdigest()
    findings = []
    out = text
    for name, pattern in PATTERNS.items():
        for m in list(pattern.finditer(out)):
            secret = m.group(0)
            digest = hashlib.sha256((salt + secret).encode()).hexdigest()[:16]
            findings.append({"finding_type": name, "salted_hash": digest, "redacted_preview": "[REDACTED]"})
            out = out.replace(secret, "[REDACTED]")
    return out, findings
