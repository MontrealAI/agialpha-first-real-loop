import os
import unittest

from secure_rails.redaction_guard import find_secret_like


class TestSecureRailsRedactionGuardSemantic(unittest.TestCase):
    def test_detects_multiple_patterns_without_raw_leak(self):
        fixture = "\n".join([
            "token=ghp_" + "A" * 24,
            "aws=AKIA1234567890ABCD12",
            "auth=Bearer " + "x" * 24,
            "jwt=eyJabc.def.ghi",
            "password = fakePassword12345",
        ])
        findings = find_secret_like(fixture, path="fixtures/synthetic.txt")
        self.assertGreaterEqual(len(findings), 4)
        self.assertNotIn("ghp_" + "A" * 24, str(findings))
        self.assertTrue(all("path" in f and "line" in f and "hash" in f and "type" in f for f in findings))

    def test_salt_is_configurable(self):
        token_line = "x=ghp_" + "B" * 24
        os.environ["SECURERAILS_REDACTION_SALT"] = "salt-one"
        h1 = find_secret_like(token_line)[0]["hash"]
        os.environ["SECURERAILS_REDACTION_SALT"] = "salt-two"
        h2 = find_secret_like(token_line)[0]["hash"]
        self.assertNotEqual(h1, h2)

