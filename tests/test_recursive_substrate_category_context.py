import json
import pathlib
import unittest


class TestRecursiveSubstrateCategoryContext(unittest.TestCase):
    def test_category_context_registry_shape(self):
        path = pathlib.Path('recursive_substrate_registry/category_context.json')
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data.get('schema_version'), 'agialpha.recursive_category_context.v1')
        self.assertIn('claim_boundary', data)
        self.assertIn('reference_families', data)
        self.assertIsInstance(data['reference_families'], list)


if __name__ == '__main__':
    unittest.main()
