import json

def test_public_comparables_fixture_parses():
    data = json.load(open('config/valuation_support_public_comparables.example.json'))
    cmp0 = data['comparables'][0]
    assert cmp0['reported_valuation_usd'] == 4650000000
    assert cmp0['reported_valuation_date'] == '2026-05-13'
