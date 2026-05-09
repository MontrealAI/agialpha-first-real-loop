import hmac,hashlib,unittest
from secure_rails.github_webhook_verify import verify_github_webhook_signature
class T(unittest.TestCase):
  def test_ok(self):
    sec=b'a';p=b'{}';sig='sha256='+hmac.new(sec,p,hashlib.sha256).hexdigest();self.assertTrue(verify_github_webhook_signature(sec,p,sig))
  def test_empty_payload_ok(self):
    sec=b'a';p=b'';sig='sha256='+hmac.new(sec,p,hashlib.sha256).hexdigest();self.assertTrue(verify_github_webhook_signature(sec,p,sig))
  def test_bad(self): self.assertFalse(verify_github_webhook_signature(b'a',b'{}','sha256=deadbeef'))
