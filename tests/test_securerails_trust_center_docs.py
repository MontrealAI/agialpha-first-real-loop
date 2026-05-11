import unittest, json
from pathlib import Path

class T(unittest.TestCase):
  def test_docs(self):
    for p in ['docs/secure-rails/trust-center.md','docs/secure-rails/security-advisory-process.md','docs/secure-rails/coordinated-vulnerability-disclosure.md','docs/secure-rails/customer-security-faq.md']: self.assertTrue(Path(p).exists())
  def test_status(self):
    d=json.loads(Path('docs/_generated/secure-rails/trust-center/status.json').read_text()); self.assertEqual(d['schema_version'],'securerails.trust_center_status.v1')
