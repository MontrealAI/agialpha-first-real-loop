import unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_dispatch_path_uses_event_payload(self):
        t = Path('.github/workflows/securerails-customer-pilot-intake-001.yml').read_text()
        self.assertIn('dispatch-ingest --payload "$GITHUB_EVENT_PATH"', t)
