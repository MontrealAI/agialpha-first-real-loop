import unittest
import tempfile
from pathlib import Path
from secure_rails.dependency_inventory import collect_dependency_inventory
class T(unittest.TestCase):
    def test_inventory(self):
        d=collect_dependency_inventory('.')
        self.assertEqual(d['schema_version'],'securerails.dependency_inventory.v1')
        self.assertIn('claim_boundary',d)

    def test_missing_lockfile_per_manifest_instance(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / 'a'
            b = Path(td) / 'b'
            a.mkdir(); b.mkdir()
            (a / 'package.json').write_text('{\"dependencies\":{\"x\":\"1.0.0\"}}', encoding='utf-8')
            (a / 'package-lock.json').write_text('{}', encoding='utf-8')
            (b / 'package.json').write_text('{\"dependencies\":{\"y\":\"1.0.0\"}}', encoding='utf-8')
            d = collect_dependency_inventory(td)
            self.assertIn('b/package-lock.json', d['lockfiles_missing'])
