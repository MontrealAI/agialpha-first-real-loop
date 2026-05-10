import unittest
from pathlib import Path
from secure_rails.canary_fixtures import list_fixtures
class T(unittest.TestCase):
    def test_fixtures(self):
        fx=list_fixtures(Path('tests/fixtures/securerails_e2e_canary'))
        self.assertEqual(len(fx),7)
