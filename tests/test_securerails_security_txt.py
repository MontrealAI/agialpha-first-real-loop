import unittest
from pathlib import Path
from secure_rails.security_txt import validate_security_txt_template

class T(unittest.TestCase):
    def test_template(self):
        p=Path('docs/secure-rails/templates/security.txt.template'); self.assertTrue(p.exists()); ok,_=validate_security_txt_template(p); self.assertTrue(ok)
    def test_no_fake_production(self):
        p=Path('docs/.well-known/security.txt')
        if p.exists(): self.assertNotIn('example.invalid', p.read_text())

