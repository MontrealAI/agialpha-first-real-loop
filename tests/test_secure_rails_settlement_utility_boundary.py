import json, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_settlement_utility(self):
        d=json.loads(Path('secure_rails_registry/settlements/settlement-example-001.json').read_text())
        self.assertEqual(d.get('utility_asset'),'$AGIALPHA')
