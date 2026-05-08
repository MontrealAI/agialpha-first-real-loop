from pathlib import Path
import unittest

class TestSecureRailsCustomerTemplate(unittest.TestCase):
    def test_customer_template(self):
        txt = Path('docs/secure-rails/templates/customer-securerails-pr-guard.yml').read_text(encoding='utf-8')
        self.assertIn('uses: MontrealAI/agialpha-first-real-loop/.github/workflows/securerails-pr-guard-reusable.yml@main', txt)
        self.assertIn('contents: read', txt)
        self.assertIn('pull-requests: read', txt)
        self.assertIn('actions: read', txt)
