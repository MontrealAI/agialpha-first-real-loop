import hashlib
import os
import re
from pathlib import Path

SECRET_PATTERNS = [
    ("github_token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key_header", re.compile(r"-----BEGIN (?:(?:RSA|OPENSSH|EC|DSA|PGP) )?PRIVATE KEY-----|-----BEGIN ENCRYPTED PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}")),
    ("openai_key", re.compile(r"sk-(?:proj|live|test)-[A-Za-z0-9_-]{10,}|sk-[A-Za-z0-9_-]{20,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("jwt_like", re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")),
    ("password_assignment", re.compile(r"(?i)(password|passwd|pwd|secret|api[_-]?key)\s*[:=]\s*\S{8,}")),
    ("secret_env", re.compile(r"(?i)(OPENAI_API_KEY|AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|SLACK_BOT_TOKEN)\s*[:=]\s*\S{8,}")),
]

def _salt() -> str:
    env = os.environ.get("SECURERAILS_REDACTION_SALT")
    if env:
        return env
    return hashlib.sha256(os.urandom(32)).hexdigest()


def _hashed(value: str, salt: str | None = None) -> str:
    effective_salt = salt if salt is not None else _salt()
    return hashlib.sha256((effective_salt + ":" + value).encode()).hexdigest()

def find_secret_like(text: str, *, path: str = "<memory>", salt: str | None = None):
    findings = []
    for idx, line in enumerate(text.splitlines(), start=1):
        for finding_type, pat in SECRET_PATTERNS:
            for m in pat.finditer(line):
                findings.append({"path": str(Path(path)), "line": idx, "hash": _hashed(m.group(0), salt=salt), "type": finding_type})
    return findings
