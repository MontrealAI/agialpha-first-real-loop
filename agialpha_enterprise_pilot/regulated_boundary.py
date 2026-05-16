from .boundaries import boundary_fields
import re
BLOCK = [
    "hr", "human resources", "worker evaluation", "credit", "lending", "insurance", "medical", "legal", "investment",
    "financial advice", "financial advisor", "financial adviser",
    "kyc", "aml", "custody", "payment", "payment processing", "procurement", "contract"
]
BLOCK_PATTERNS = [
    rf"\b{re.escape(term)}\b" for term in BLOCK
] + [
    r"\bbank\w*\b",
    r"\bbroker\w*\b",
]
def triage(intended_use: str):
    t = intended_use.lower()
    t = re.sub(r"[-_/]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    blocked = any(re.search(pattern, t) for pattern in BLOCK_PATTERNS)
    r = {"regulated_boundary_result": "blocked" if blocked else "passed", "regulated_boundary_blocked": blocked, "documentation_only": blocked}
    r.update(boundary_fields()); return r
