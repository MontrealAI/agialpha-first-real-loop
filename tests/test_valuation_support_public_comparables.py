import json

def test_public_comparables_fixture_parses():
    data = json.load(open('config/valuation_support_public_comparables.example.json', encoding='utf-8'))
    first = data['comparables'][0]
    assert first['reported_category_valuation_comparable'] == 'not_reported'
    assert first['source'] == 'not_reported'
