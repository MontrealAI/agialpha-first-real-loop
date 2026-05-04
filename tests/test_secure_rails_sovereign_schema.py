import json,unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_sovereign(self):
        obj=json.loads(Path('docs/secure-rails/templates/sovereign-example.json').read_text())
        self.assertEqual(obj['schema_version'],'agialpha.sovereign.v1')
        self.assertFalse(obj['promotion_policy']['autonomous_promotion_allowed'])
        self.assertTrue(obj['promotion_policy']['human_review_required'])
        self.assertFalse(obj['promotion_policy']['auto_merge_allowed'])
