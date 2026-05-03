import json,unittest
class T(unittest.TestCase):
    def test_utility_only(self):
        with open('securerails-runs/demo/settlement-receipt.json', encoding='utf-8') as fh:
            s=json.load(fh)
        self.assertIn('utility accounting',s['notice'])
