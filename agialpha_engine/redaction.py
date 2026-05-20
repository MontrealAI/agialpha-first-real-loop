"""Redaction helpers for secret-like patterns."""
from __future__ import annotations
import hashlib, re

_PATTERNS = [
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("bearer", re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}", re.I)),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
]

def redact_text(text: str, run_id: str, root_hash: str) -> tuple[str, list[dict[str, str]]]:
    salt = hashlib.sha256(f"{run_id}{root_hash}redaction-salt".encode()).hexdigest()
    findings = []
    redacted = text
    for name, pattern in _PATTERNS:
        for m in list(pattern.finditer(redacted)):
            token = m.group(0)
            digest = hashlib.sha256(f"{salt}:{token}".encode()).hexdigest()
            findings.append({"type": name, "salted_hash": digest, "redacted_preview": token[:4] + "...[REDACTED]"})
            redacted = redacted.replace(token, "[REDACTED_SECRET]")
    return redacted, findings
