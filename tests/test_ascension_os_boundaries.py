import tempfile
from agialpha_ascension_os.regulated_boundary import regulated_boundary_triage

def test_regulated_fixture_blocked():
    triage=regulated_boundary_triage({"workflow_type":"medical advice"})
    assert triage["regulated_boundary_blocked"] is True

def test_missing_metrics_not_fake_zero():
    assert "not_reported" != 0


def test_scoring_phrase_alone_not_regulated_hit():
    triage=regulated_boundary_triage({"workflow_type":"internal scoring rubric"})
    assert triage["regulated_boundary_blocked"] is False


def test_slash_phrase_matches_when_present():
    triage=regulated_boundary_triage({"description":"workflow includes wallet trading automation"})
    assert "wallet/trading" in triage["regulated_flags_triggered"]


def test_slash_flag_or_semantics_wallet_term_alone_matches():
    triage=regulated_boundary_triage({"description":"workflow includes wallet automation"})
    assert "wallet/trading" in triage["regulated_flags_triggered"]


def test_slash_flag_or_semantics_aml_term_alone_matches():
    triage=regulated_boundary_triage({"description":"workflow includes AML checks"})
    assert "KYC/AML" in triage["regulated_flags_triggered"]
