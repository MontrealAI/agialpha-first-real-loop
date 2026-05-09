import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_docs_exist(self):
        for p in ['docs/secure-rails/quebecai-template-setup.md','docs/secure-rails/customer-template-setup.md','docs/secure-rails/github-pages-setup.md','docs/secure-rails/actions-and-checks-setup.md','docs/secure-rails/rulesets-and-branch-protection.md']:
            self.assertTrue(Path(p).exists(), p)
