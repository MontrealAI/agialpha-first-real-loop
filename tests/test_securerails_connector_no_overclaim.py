import unittest
class T(unittest.TestCase):
  def test_no_eu_exempt_claim(self):
    s=open('docs/secure-rails/github-app-connector.md').read().lower();self.assertNotIn('eu ai act exempt',s)
