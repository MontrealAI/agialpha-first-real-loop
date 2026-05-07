import unittest
from secure_rails_pr_guard.diff_parser import pr_diff_summary
class T(unittest.TestCase):
    def test_summary(self): self.assertIn("changed_files", pr_diff_summary("tests/fixtures/securerails_pr_guard/safe_docs_pr"))
