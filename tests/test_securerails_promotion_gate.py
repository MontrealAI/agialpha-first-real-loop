import json
from pathlib import Path
import unittest
from secure_rails.human_review import validate_promotion_gate
class T(unittest.TestCase):
  def test_valid(self): self.assertEqual(validate_promotion_gate(json.loads(Path("tests/fixtures/securerails_human_review/valid_promotion_gate_pass.json").read_text())),[])
  def test_invalid(self): self.assertTrue(validate_promotion_gate(json.loads(Path("tests/fixtures/securerails_human_review/invalid_promotion_gate_no_human_review.json").read_text())))
