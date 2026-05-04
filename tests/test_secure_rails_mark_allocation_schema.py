import json,unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_mark(self):
        obj=json.loads(Path('docs/secure-rails/templates/mark-allocation-example.json').read_text())
        self.assertEqual(obj['schema_version'],'agialpha.mark_allocation.v1')
        self.assertTrue(obj['human_review_required'])
        self.assertFalse(obj['auto_merge_allowed'])
        self.assertEqual(obj['utility_asset'],'$AGIALPHA')
        self.assertTrue(obj['validators_required'])
