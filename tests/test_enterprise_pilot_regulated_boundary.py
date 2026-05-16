from agialpha_enterprise_pilot.regulated_boundary import triage
def test_blocked_fixture():
 o=triage({'pilot_id':'p1','intended_use':'medical decisioning','workflow_family':'x'})
 assert o['regulated_boundary_blocked'] is True
