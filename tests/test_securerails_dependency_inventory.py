import unittest
from secure_rails.dependency_inventory import collect_dependency_inventory
class T(unittest.TestCase):
    def test_inventory(self):
        d=collect_dependency_inventory('.')
        self.assertEqual(d['schema_version'],'securerails.dependency_inventory.v1')
        self.assertIn('claim_boundary',d)
