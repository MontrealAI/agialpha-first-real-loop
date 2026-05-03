import json,unittest
class T(unittest.TestCase):
    def test_has_counters(self):
        v=json.load(open('securerails-runs/demo/work-vault.json'))
        for k in ["raw_secret_leak_count","external_target_scan_count","exploit_execution_count","malware_generation_count","social_engineering_content_count","unsafe_automerge_count","critical_safety_incidents"]:
            self.assertIn(k,v['hard_safety_counters'])
