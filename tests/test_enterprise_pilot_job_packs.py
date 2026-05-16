from agialpha_enterprise_pilot.job_packs import create_job_pack,PACKS
def test_job_pack_fields():
 for p in PACKS:
  j=create_job_pack('p1',p,'synthetic_only')
  assert 'validator_plan' in j

def test_invalid_customer_mode_rejected():
 try:
  create_job_pack('p1','software_quality_pack','not_reported')
  assert False, 'expected ValueError'
 except ValueError:
  assert True
