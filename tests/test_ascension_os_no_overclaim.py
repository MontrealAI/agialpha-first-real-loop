import unittest
from pathlib import Path


class TestNoOverclaim(unittest.TestCase):
    def test_docs_no_forbidden_claims(self):
        text = Path("README_ASCENSION_OS.md").read_text(encoding="utf-8").lower()
        for bad in ["achieved agi", "achieved asi", "superintelligence", "empirical sota"]:
            self.assertNotIn(bad, text)


if __name__ == '__main__':
    unittest.main()
