import json

def test_public_comparables_fixture_parses():
    data = json.load(open('config/valuation_support_public_comparables.example.json'))
    cmp0 = data['comparables'][0]
    assert cmp0['reported_category_valuation_comparable'] == 'not_reported'
    assert 'reported_valuation_usd' not in cmp0
