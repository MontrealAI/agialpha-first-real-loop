import json
from pathlib import Path
import unittest
from secure_rails.review_decision import validate_review_decision
class T(unittest.TestCase):
  def test_valid(self): self.assertEqual(validate_review_decision(json.loads(Path("tests/fixtures/securerails_human_review/valid_decision_accept.json").read_text())),[])
  def test_invalid(self): self.assertTrue(validate_review_decision(json.loads(Path("tests/fixtures/securerails_human_review/invalid_decision_automerge.json").read_text())))
  def test_missing_decision_id(self):
    d=json.loads(Path("tests/fixtures/securerails_human_review/valid_decision_accept.json").read_text()); d.pop("decision_id", None)
    self.assertTrue(any("decision_id required" in e for e in validate_review_decision(d)))
  def test_evidence_reviewed_must_be_object(self):
    d=json.loads(Path("tests/fixtures/securerails_human_review/valid_decision_accept.json").read_text()); d["evidence_reviewed"]=[]
    self.assertTrue(any("evidence_reviewed must be an object" in e for e in validate_review_decision(d)))
