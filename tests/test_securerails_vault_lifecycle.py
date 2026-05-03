import json,unittest
class T(unittest.TestCase):
    def test_deterministic_ids(self):
        v=json.load(open('securerails-runs/demo/work-vault.json'))
        self.assertEqual(v['vault_id'],'vault-demo-001')
