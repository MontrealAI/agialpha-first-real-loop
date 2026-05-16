from agialpha_enterprise_pilot.valuation_support_link import create_link
def test_link():
 assert create_link('p','C5')['not_an_investment_claim'] is True
