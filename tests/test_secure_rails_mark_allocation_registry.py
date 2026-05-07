import json, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_mark_present(self):
        d=json.loads(Path('secure_rails_registry/mark_allocations/mark-alloc-example-001.json').read_text())
        self.assertEqual(d.get('schema_version'),'agialpha.mark_allocation.v1')
