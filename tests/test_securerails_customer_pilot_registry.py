import tempfile, unittest
from pathlib import Path
from secure_rails.pilot_intake import ingest_intake
from secure_rails.pilot_registry import validate_registry
class T(unittest.TestCase):
    def test_registry(self):
        with tempfile.TemporaryDirectory() as td:
            ingest_intake(Path('docs/secure-rails/templates/customer-pilot-intake-example.json'), Path(td))
            self.assertTrue(validate_registry(Path(td)))
