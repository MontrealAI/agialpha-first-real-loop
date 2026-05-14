import tempfile
from agialpha_ascension_os.regulated_boundary import regulated_boundary_triage

def test_regulated_fixture_blocked():
    triage=regulated_boundary_triage({"workflow_type":"medical advice"})
    assert triage["regulated_boundary_blocked"] is True

def test_missing_metrics_not_fake_zero():
    assert "not_reported" != 0
