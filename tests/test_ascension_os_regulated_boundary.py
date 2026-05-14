from agialpha_ascension_os.core import bfields

def test_boundary_flags():
 b=bfields(); assert b["human_review_required"] is True and b["autonomous_persistence_allowed"] is False
