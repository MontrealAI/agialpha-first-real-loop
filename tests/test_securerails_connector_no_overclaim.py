import unittest


class T(unittest.TestCase):
    def test_no_eu_exempt_claim(self):
        with open('docs/secure-rails/github-app-connector.md', encoding='utf-8') as f:
            s = f.read().lower()
        self.assertNotIn('eu ai act exempt', s)
