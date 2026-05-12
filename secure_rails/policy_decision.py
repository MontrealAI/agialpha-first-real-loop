import json
import uuid


_DEFAULT_GENERATED_AT = "1970-01-01T00:00:00+00:00"


def _stable_decision_id(context, kernel, decision, severity, matched_rules, violations, warnings):
    payload = {
        "context_id": context["context_id"],
        "kernel_id": kernel["kernel_id"],
        "kernel_version": kernel["kernel_version"],
        "decision": decision,
        "severity": severity,
        "matched_rules": matched_rules,
        "violations": violations,
        "warnings": warnings,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return str(uuid.uuid5(uuid.NAMESPACE_URL, encoded))

def make_decision(context, kernel, decision, severity, matched_rules, violations, warnings):
    generated_at = context.get("metadata", {}).get("generated_at", _DEFAULT_GENERATED_AT)
    return {
      "schema_version":"securerails.policy_decision.v1",
      "decision_id":_stable_decision_id(context, kernel, decision, severity, matched_rules, violations, warnings),
      "generated_at":generated_at,
      "kernel_id":kernel["kernel_id"],
      "kernel_version":kernel["kernel_version"],
      "context_id":context["context_id"],
      "context_type":context["context_type"],
      "source_path":context["source_path"],
      "decision":decision,
      "severity":severity,
      "matched_rules":matched_rules,
      "violations":violations,
      "warnings":warnings,
      "required_human_review":True,
      "auto_merge_allowed":False,
      "claim_boundary":"This policy decision is advisory governance evidence and does not certify security.",
    }
