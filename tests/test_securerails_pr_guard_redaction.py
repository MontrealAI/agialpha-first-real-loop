import unittest
from secure_rails_pr_guard.secret_redaction import scan_text
class T(unittest.TestCase):
    def test_redact(self):
        f=scan_text("x","secret = AKIAABCDEFGHIJKLMNOP")
        self.assertTrue(f and f[0]["redacted_preview"]=="[REDACTED]")
