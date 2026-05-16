from .boundaries import boundary_fields
import re
BLOCK = [
    "hr", "credit", "insurance", "medical", "legal", "investment",
    "financial advice", "financial advisor", "financial advisory",
    "kyc", "aml", "bank", "banking", "broker", "brokerage",
    "custody", "procurement", "contract",
]
def triage(intended_use: str):
    t = intended_use.lower()
    blocked = any(re.search(rf"\b{re.escape(k)}\b", t) for k in BLOCK)
    r = {"regulated_boundary_result": "blocked" if blocked else "passed", "regulated_boundary_blocked": blocked, "documentation_only": blocked}
    r.update(boundary_fields()); return r
