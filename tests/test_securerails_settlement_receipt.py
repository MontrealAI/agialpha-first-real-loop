import json,unittest
class T(unittest.TestCase):
    def test_utility_only(self):
        s=json.load(open('securerails-runs/demo/settlement-receipt.json'))
        self.assertIn('utility accounting',s['notice'])
