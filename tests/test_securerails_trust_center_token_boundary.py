import unittest
from pathlib import Path

class T(unittest.TestCase):
  def test_token_boundary(self):
    txt=Path('docs/secure-rails/customer-security-faq.md').read_text().lower(); self.assertIn('utility-only',txt)
