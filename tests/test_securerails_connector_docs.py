import unittest
class T(unittest.TestCase):
  def test_docs_boundary(self):
    s=open('docs/secure-rails/github-app-connector.md').read().lower();self.assertIn('least-privilege',s);self.assertIn('no certification claim',s)
