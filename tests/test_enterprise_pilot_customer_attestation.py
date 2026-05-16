from agialpha_enterprise_pilot.customer_attestation import create_attestation
def test_attestation_excludes_regulated_uses():
 a=create_attestation('p1')
 assert 'credit / lending' in a['excluded_uses']
