from pathlib import Path
import unittest

FORBIDDEN = [
    'certified secure', 'guaranteed security',
    'eu ai act exempt', 'investment return', 'yield', 'dividends', 'profit rights', 'ownership rights'
]

class TestSecureRailsActionNoOverclaim(unittest.TestCase):
    def test_no_overclaim_language(self):
        files = [
            '.github/actions/securerails-pr-guard/README.md',
            'docs/secure-rails/installable-action.md',
            'docs/secure-rails/reusable-workflow.md',
            'docs/secure-rails/customer-pilot-installation.md',
            'docs/secure-rails/external-repo-security-model.md',
        ]
        blob = '\n'.join(Path(f).read_text(encoding='utf-8').lower() for f in files)
        for banned in FORBIDDEN:
            self.assertNotIn(banned, blob)
