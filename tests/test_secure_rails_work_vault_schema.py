import json,unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_work_vault_example_has_required_shape(self):
        obj=json.loads(Path('docs/secure-rails/templates/work-vault-example.json').read_text())
        self.assertEqual(obj['schema_version'],'securerails.work_vault.v1')
        self.assertTrue(obj['scope']['human_review_required'])
        self.assertFalse(obj['scope']['auto_merge_allowed'])
        for k in ["raw_secret_leak_count","external_target_scan_count","exploit_execution_count","malware_generation_count","social_engineering_content_count","unsafe_automerge_count","critical_safety_incidents"]:
            self.assertIn(k,obj['hard_safety_counters'])
            self.assertIsInstance(obj['hard_safety_counters'][k],(int,float))

    def test_schema_declares_numeric_counters(self):
        schema=json.loads(Path('schemas/securerails_work_vault.schema.json').read_text())
        counters=schema['properties']['hard_safety_counters']['properties']
        for k in ["raw_secret_leak_count","external_target_scan_count","exploit_execution_count","malware_generation_count","social_engineering_content_count","unsafe_automerge_count","critical_safety_incidents"]:
            self.assertEqual(counters[k]['type'],'number')
