from agialpha_enterprise_pilot.job_packs import create_job_pack,PACKS
def test_job_pack_fields():
 for p in PACKS:
  j=create_job_pack('p1',p,'synthetic_only','passed')
  assert 'validator_plan' in j

def test_job_pack_rejects_unsupported_customer_mode():
 try:
  create_job_pack('p1','software_quality_pack','not_reported','passed')
  raise AssertionError('expected ValueError for unsupported customer mode')
 except ValueError:
  pass


def test_job_pack_propagates_regulated_boundary_status():
 j=create_job_pack('p1','software_quality_pack','synthetic_only','blocked')
 assert j['regulated_boundary_result']=='blocked'
 assert j['regulated_boundary']=='blocked'
