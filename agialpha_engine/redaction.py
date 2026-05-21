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
    "ssh_private_key": re.compile(r"-----BEGIN OPENSSH PRIVATE KEY-----[\s\S]+?-----END OPENSSH PRIVATE KEY-----"),
    "pem_private_key": re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |DSA )?PRIVATE KEY-----"),
    "jwt_like": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "high_entropy_hex": re.compile(r"\b[a-fA-F0-9]{40,}\b"),
    "high_entropy_b64": re.compile(r"\b[A-Za-z0-9+/]{48,}={0,2}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "card_like": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
}


def redact_text(text: str, run_id: str, root_hash: str) -> tuple[str, list[dict[str, Any]]]:
    salt = hashlib.sha256(f"{run_id}{root_hash}redaction-salt".encode()).hexdigest()
    findings: list[dict[str, Any]] = []
    out_lines = text.splitlines()
    for i, line in enumerate(out_lines):
        updated = line
        for name, pattern in PATTERNS.items():
            for m in list(pattern.finditer(updated)):
                secret = m.group(0)
                digest = hashlib.sha256((salt + secret).encode()).hexdigest()[:16]
                findings.append({"line": i + 1, "finding_type": name, "salted_hash": digest, "redacted_preview": "[REDACTED]"})
                updated = updated.replace(secret, "[REDACTED]")
        out_lines[i] = updated
    return "\n".join(out_lines), findings
