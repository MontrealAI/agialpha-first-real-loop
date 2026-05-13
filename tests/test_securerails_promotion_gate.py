import json
from pathlib import Path
import unittest
from secure_rails.human_review import validate_promotion_gate
class T(unittest.TestCase):
  def test_valid(self): self.assertEqual(validate_promotion_gate(json.loads(Path("tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json").read_text())),[])
  def test_invalid(self): self.assertTrue(validate_promotion_gate(json.loads(Path("tests/fixtures/securerails_human_review/invalid_promotion_gate_no_human_review.json").read_text())))
  def test_invalid_unknown_target(self):
    gate=json.loads(Path("tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json").read_text())
    gate["promotion_target"]="unknown_target"
    errs=validate_promotion_gate(gate)
    self.assertTrue(any("invalid promotion_target" in e for e in errs))
  def test_missing_source_decision_id(self):
    gate=json.loads(Path("tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json").read_text())
    gate["source_decision_id"]=""
    errs=validate_promotion_gate(gate)
    self.assertTrue(any("source_decision_id required" in e for e in errs))
