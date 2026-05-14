from agialpha_ascension_os.context import BOUNDARY

def test_boundary_has_no_agi_claim():
 assert 'AGI achieved' not in BOUNDARY['claim_boundary']
