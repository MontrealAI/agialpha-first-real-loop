from pathlib import Path
import unittest
class T(unittest.TestCase):
  def test_workflow(self):
    s=Path('.github/workflows/securerails-human-review-console-001.yml').read_text(); self.assertIn('contents: read',s); self.assertNotIn('deploy-pages',s)
  def test_promotion_gate_defaults_to_pending_human_review(self):
    from secure_rails.human_review import validate_promotion_gate
    errs = validate_promotion_gate({
      "schema_version": "securerails.promotion_gate.v1",
      "promotion_gate_id": "pg-001",
      "source_decision_id": "decision-001",
      "promotion_target": "safe_pr",
      "claim_boundary": "local bounded evidence only",
      "required_conditions": {
        "human_review_decision_present": True,
        "hard_safety_counters_zero": True,
        "auto_merge_allowed": False,
        "evidence_docket_present": True,
      },
    })
    self.assertIn("promotion pending human review", errs)
