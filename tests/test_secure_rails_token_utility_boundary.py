import unittest
from pathlib import Path
FORBIDDEN=['equity','debt','yield','dividend','passive income','guaranteed return','investment return','token appreciation','claim on revenue','claim on assets']
class T(unittest.TestCase):
    def test_forbidden_token_language_absent(self):
        corpus='\n'.join(Path(p).read_text(encoding='utf-8').lower() for p in [
            'docs/secure-rails/work-vaults-mark-sovereigns.md',
            'docs/secure-rails/templates/work-vault-example.json',
            'docs/secure-rails/templates/mark-allocation-example.json',
            'docs/secure-rails/templates/sovereign-example.json',
            'docs/secure-rails/templates/vault-settlement-example.json'])
        for w in FORBIDDEN:
            self.assertNotIn(w,corpus)
