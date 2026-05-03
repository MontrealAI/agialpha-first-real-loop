import json,unittest
class T(unittest.TestCase):
    def test_required_flags(self):
        m=json.load(open('securerails-runs/demo/mark-allocation.json'))
        self.assertTrue(m['human_review_required']);self.assertFalse(m['auto_merge_allowed']);self.assertFalse(m['promotion_without_evidence_allowed'])
