import json
import pathlib
import unittest


class TestRecursiveSubstrateReferenceMap(unittest.TestCase):
    def test_reference_map_is_context_only(self):
        path = pathlib.Path('recursive_substrate_registry/research_reference_map.json')
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding='utf-8'))
        text = json.dumps(data)
        self.assertIn('Reference map only', text)
        self.assertNotIn('implemented all', text.lower())


if __name__ == '__main__':
    unittest.main()
