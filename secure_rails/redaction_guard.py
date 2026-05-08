import hashlib
import re

SECRET_PATTERNS = [re.compile(r"(ghp_[A-Za-z0-9]{20,})"), re.compile(r"(AKIA[0-9A-Z]{16})")]

def find_secret_like(text: str):
    findings = []
    for idx, line in enumerate(text.splitlines(), start=1):
        for pat in SECRET_PATTERNS:
            for m in pat.finditer(line):
                findings.append({"line": idx, "hash": hashlib.sha256(("salt:"+m.group(1)).encode()).hexdigest(), "type": "secret_like"})
    return findings
