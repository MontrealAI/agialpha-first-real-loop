import unittest
from secure_rails.redaction_guard import find_secret_like

class TestRedaction002(unittest.TestCase):
    def test_detects_github_token_without_leak(self):
        token='ghp_'+'A'*24
        f=find_secret_like('x='+token)
        self.assertTrue(f)
        self.assertNotIn(token,str(f))
