import unittest
from secure_rails.github_webhooks import normalize_webhook_payload
class T(unittest.TestCase):
  def test_redact(self):
    n=normalize_webhook_payload({'sender':{'login':'alice','email':'a@b.com'}},'pull_request','d');self.assertTrue(n['sender']['raw_login_redacted']);self.assertNotIn('email',str(n))
  def test_unverified_flag(self):
    n=normalize_webhook_payload({},'ping','d',False);self.assertFalse(n['security']['signature_verified'])
