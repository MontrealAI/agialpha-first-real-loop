from pathlib import Path
import unittest

class TestSecureRailsActionNoOverclaim(unittest.TestCase):
    def test_no_overclaim_language(self):
        files = [
            Path('.github/actions/securerails-pr-guard/README.md'),
            Path('docs/secure-rails/installable-action.md'),
            Path('docs/secure-rails/reusable-workflow.md'),
        ]
        banned = ['cybersecurity certification', 'guaranteed security', 'investment return', 'dividends', 'profit rights']
        corpus = '\n'.join(p.read_text(encoding='utf-8').lower() for p in files)
        for b in banned:
            self.assertNotIn(b, corpus)
