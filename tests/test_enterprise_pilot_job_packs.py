from agialpha_enterprise_pilot.job_packs import create_job_pack,PACKS
def test_job_pack_fields():
 for p in PACKS:
  j=create_job_pack('p1',p,'synthetic_only')
  assert 'validator_plan' in j

def test_job_pack_rejects_unsupported_customer_mode():
 try:
  create_job_pack('p1','software_quality_pack','not_reported')
  raise AssertionError('expected ValueError for unsupported customer mode')
 except ValueError:
  pass
