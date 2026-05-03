import json,unittest
class T(unittest.TestCase):
    def test_promotion_policy(self):
        s=json.load(open('securerails-runs/demo/sovereign.json'))
        p=s['promotion_policy'];self.assertFalse(p['autonomous_promotion_allowed']);self.assertTrue(p['human_review_required'])
