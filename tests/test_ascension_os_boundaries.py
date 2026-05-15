import tempfile
from agialpha_ascension_os.regulated_boundary import regulated_boundary_triage

def test_regulated_fixture_blocked():
    triage=regulated_boundary_triage({"workflow_type":"medical advice"})
    assert triage["regulated_boundary_blocked"] is True

def test_missing_metrics_not_fake_zero():
    assert "not_reported" != 0

def test_internal_scoring_not_regulated_by_substring():
    triage=regulated_boundary_triage({
        "workflow_type":"education access",
        "description":"Uses an internal scoring rubric for project prioritization."
    })
    assert triage["regulated_boundary_blocked"] is False

def test_slash_delimited_regulated_phrase_still_blocked():
    triage=regulated_boundary_triage({"workflow_type":"payment custody controls"})
    assert triage["regulated_boundary_blocked"] is True
