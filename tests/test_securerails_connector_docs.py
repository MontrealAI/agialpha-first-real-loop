import unittest


class T(unittest.TestCase):
    def test_docs_boundary(self):
        with open('docs/secure-rails/github-app-connector.md', encoding='utf-8') as f:
            s = f.read().lower()
        self.assertIn('least-privilege', s)
        self.assertIn('no certification claim', s)
