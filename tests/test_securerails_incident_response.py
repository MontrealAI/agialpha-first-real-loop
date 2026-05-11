import unittest
from pathlib import Path
from secure_rails.incident_response import validate_incident

class T(unittest.TestCase):
    def test_runbook(self): self.assertTrue(Path('docs/secure-rails/incident-response-runbook.md').exists())
    def test_incident_example(self):
        ok,_=validate_incident(Path('docs/secure-rails/templates/security-incident-record-example.json')); self.assertTrue(ok)
