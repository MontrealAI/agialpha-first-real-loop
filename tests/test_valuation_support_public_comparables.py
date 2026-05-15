import json

def test_public_comparables_fixture_parses():
    data=json.load(open('config/valuation_support_public_comparables.example.json'))
    assert data['comparables'][0]['reported_valuation_usd']==4650000000
