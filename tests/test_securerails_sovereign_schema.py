import json,unittest
class T(unittest.TestCase):
    def test_promotion_policy(self):
        with open('securerails-runs/demo/sovereign.json', encoding='utf-8') as fh:
            s=json.load(fh)
        p=s['promotion_policy'];self.assertFalse(p['autonomous_promotion_allowed']);self.assertTrue(p['human_review_required'])
