import unittest, tempfile
from secure_rails.repo_security_baseline import generate_baseline
class T(unittest.TestCase):
    def test_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            b=generate_baseline('.',td)
            self.assertEqual(b['baseline_id'],'securerails-repo-security-baseline-001')
