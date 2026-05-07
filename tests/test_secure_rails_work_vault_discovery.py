import json, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_example_discovery(self):
        w=json.loads((Path('secure_rails_registry/work_vaults/sr-vault-example-001.json')).read_text())
        self.assertEqual(w.get('source'),'example_template')
