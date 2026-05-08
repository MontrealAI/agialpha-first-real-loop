import unittest
from pathlib import Path
from secure_rails.pilot_validate import validate_intake_file

class T(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_intake_file(Path('docs/secure-rails/templates/customer-pilot-intake-example.json')).ok)
