from pathlib import Path
import unittest

class TestSecureRailsCustomerTemplate(unittest.TestCase):
    def test_customer_template(self):
        text = Path('docs/secure-rails/templates/customer-securerails-pr-guard.yml').read_text(encoding='utf-8')
        self.assertIn('MontrealAI/agialpha-first-real-loop/.github/workflows/securerails-pr-guard-reusable.yml@main', text)
        self.assertIn('contents: read', text)
        self.assertIn('pull-requests: read', text)
        self.assertIn('actions: read', text)
