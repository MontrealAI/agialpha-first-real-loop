import json
import tempfile
import unittest

from agialpha_valuation_support.public_comparables import load_public_comparables


class TestValuationSupportPublicComparables(unittest.TestCase):
    def test_public_comparables_fixture_parses(self):
        with open('config/valuation_support_public_comparables.example.json', encoding='utf-8') as handle:
            data = json.load(handle)
        cmp0 = data['comparables'][0]
        self.assertEqual(cmp0['reported_valuation_usd'], 4650000000)
        self.assertEqual(cmp0['reported_valuation_date'], '2026-05-13')

    def test_public_comparables_invalid_schema_fails_fast(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
            json.dump({'schema_version': 'bad.v1', 'comparables': []}, fh)
            path = fh.name
        with self.assertRaisesRegex(ValueError, 'schema_version'):
            load_public_comparables(path)

    def test_public_comparables_non_list_comparables_fails_fast(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
            json.dump({'schema_version': 'agialpha.valuation_support_public_comparables.v2', 'comparables': {}}, fh)
            path = fh.name
        with self.assertRaisesRegex(ValueError, 'comparables'):
            load_public_comparables(path)


if __name__ == '__main__':
    unittest.main()
