
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import hashlib

@dataclass
class PolicyDecision:
    schema_version: str = 'securerails.policy_decision.v1'
    decision_id: str = ''
    generated_at: str = ''
    kernel_id: str = 'securerails-policy-kernel-001'
    kernel_version: str = '0.1.0'
    context_id: str = ''
    context_type: str = ''
    source_path: str = ''
    decision: str = 'escalate'
    severity: str = 'medium'
    matched_rules: list = field(default_factory=list)
    violations: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    required_human_review: bool = True
    auto_merge_allowed: bool = False
    claim_boundary: str = 'This policy decision is advisory governance evidence and does not certify security.'

    def finalize(self):
        if not self.generated_at:
            self.generated_at = datetime.now(timezone.utc).isoformat()
        if not self.decision_id:
            raw = f"{self.context_id}|{self.source_path}|{self.decision}|{self.generated_at}"
            self.decision_id = hashlib.sha256(raw.encode()).hexdigest()[:24]
        return self

    def to_dict(self):
        return asdict(self)
