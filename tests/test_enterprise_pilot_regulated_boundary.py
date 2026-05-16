from agialpha_enterprise_pilot.regulated_boundary import triage
def test_blocked_fixture():
 o=triage({'pilot_id':'p1','intended_use':'medical decisioning','workflow_family':'x'})
 assert o['regulated_boundary_blocked'] is True

def test_whole_word_match_avoids_false_positive():
 o=triage({'pilot_id':'p2','intended_use':'throughput optimization','workflow_family':'docs_ops_pack'})
 assert o['regulated_boundary_blocked'] is False

def test_investment_advice_is_blocked():
 o=triage({'pilot_id':'p3','intended_use':'provide investment advice to clients','workflow_family':'evidence_ops_pack'})
 assert o['regulated_boundary_blocked'] is True

def test_lending_intent_is_blocked():
 o=triage({'pilot_id':'p4','intended_use':'lending decision support','workflow_family':'enterprise_pilot_readiness_pack'})
 assert o['regulated_boundary_blocked'] is True

def test_hyphenated_regulated_terms_are_blocked():
 o=triage({'pilot_id':'p5','intended_use':'financial-advice and human-resources guidance','workflow_family':'docs_ops_pack'})
 assert o['regulated_boundary_blocked'] is True
