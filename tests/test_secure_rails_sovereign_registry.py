import json, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_sov_present(self):
        d=json.loads(Path('secure_rails_registry/sovereigns/workflow-permission-sovereign.json').read_text())
        self.assertEqual(d.get('schema_version'),'agialpha.sovereign.v1')
