from dataclasses import dataclass

REQUIRED_CLAIM_BOUNDARY = (
    "SecureRails customer pilot intake records are evidence-governance artifacts. "
    "They do not certify security, do not authorize autonomous remediation, and do not make decisions about natural persons."
)
FORBIDDEN_UTILITY_TERMS = [
    "investment", "yield", "dividend", "ownership", "profit", "appreciation", "passive income", "financial product"
]
ALLOWED_STATUSES = {
    "pending_validation", "validated", "rejected", "quarantined", "incomplete", "artifact_expired", "display_private_only"
}

@dataclass
class ValidationResult:
    ok: bool
    errors: list
