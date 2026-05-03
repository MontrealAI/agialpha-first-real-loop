import json,unittest
class T(unittest.TestCase):
    def test_deterministic_ids(self):
        with open('securerails-runs/demo/work-vault.json', encoding='utf-8') as fh:
            v=json.load(fh)
        self.assertEqual(v['vault_id'],'vault-demo-001')
