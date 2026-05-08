import json, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_exists(self):
        d=json.loads(Path('docs/secure-rails/templates/external-repo-record-example.json').read_text())
        self.assertEqual(d['schema_version'],'securerails.external_repo_record.v1')
