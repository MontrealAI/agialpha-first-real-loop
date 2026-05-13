import json
from pathlib import Path
import unittest
from secure_rails.review_request import validate_review_request
class T(unittest.TestCase):
  def test_valid(self):
    d=json.loads(Path("tests/fixtures/securerails_human_review/valid_request.json").read_text()); self.assertEqual(validate_review_request(d),[])
  def test_invalid(self):
    d=json.loads(Path("tests/fixtures/securerails_human_review/invalid_request_no_source.json").read_text()); self.assertTrue(validate_review_request(d))
  def test_missing_request_id(self):
    d=json.loads(Path("tests/fixtures/securerails_human_review/valid_request.json").read_text()); d.pop("review_request_id", None)
    self.assertTrue(any("review_request_id required" in e for e in validate_review_request(d)))
if __name__=='__main__':unittest.main()
