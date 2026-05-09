import unittest, json
from pathlib import Path
class T(unittest.TestCase):
    def test_required(self):
        d=json.loads(Path('config/securerails_required_checks.json').read_text())
        self.assertIn('SecureRails Compliance Guard', d['required_checks'])
