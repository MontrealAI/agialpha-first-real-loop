from agialpha_ascension_os.regulated_boundary import triage

def test_blocked_domain():
 r=triage('i1','w1',{'medical_advice':True})
 assert r['allowed_mode']!='safe_enterprise_workflow'
