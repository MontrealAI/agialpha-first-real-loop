from .boundaries import boundary_fields
BLOCK = ["hr", "credit", "insurance", "medical", "legal", "investment", "kyc", "aml", "bank", "broker", "custody", "procurement", "contract"]
def triage(intended_use: str):
    t = intended_use.lower(); blocked = any(k in t for k in BLOCK)
    r = {"regulated_boundary_result": "blocked" if blocked else "passed", "regulated_boundary_blocked": blocked, "documentation_only": blocked}
    r.update(boundary_fields()); return r
