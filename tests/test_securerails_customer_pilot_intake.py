import json
import tempfile
import unittest
from pathlib import Path
from secure_rails.pilot_validate import validate_intake_file, validate_intake_record

class T(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_intake_file(Path('docs/secure-rails/templates/customer-pilot-intake-example.json')).ok)

    def test_missing_identity_fails(self):
        rec = json.loads(Path('docs/secure-rails/templates/customer-pilot-intake-example.json').read_text())
        rec.pop('pilot_id', None)
        rec['repo'] = {}
        out = validate_intake_record(rec)
        self.assertFalse(out.ok)
        self.assertTrue(any('pilot_id missing' in x for x in out.errors))

    def test_malformed_nested_type_fails_not_crash(self):
        rec = json.loads(Path('docs/secure-rails/templates/customer-pilot-intake-example.json').read_text())
        rec['scope'] = None
        out = validate_intake_record(rec)
        self.assertFalse(out.ok)
