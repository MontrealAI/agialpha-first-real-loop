import datetime as dt, uuid

def make_decision(context, kernel, decision, severity, matched_rules, violations, warnings):
    return {
      "schema_version":"securerails.policy_decision.v1",
      "decision_id":str(uuid.uuid4()),
      "generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
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
