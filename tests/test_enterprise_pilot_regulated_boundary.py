from agialpha_enterprise_pilot.regulated_boundary import triage


def test_throughput_not_false_blocked_by_hr_substring():
    result = triage("throughput analysis for software quality evidence")
    assert result["regulated_boundary_result"] == "passed"


def test_hr_is_blocked_on_word_match():
    result = triage("HR workflow automation")
    assert result["regulated_boundary_result"] == "blocked"


def test_banking_variant_is_blocked():
    result = triage("banking workflow automation")
    assert result["regulated_boundary_result"] == "blocked"


def test_brokerage_variant_is_blocked():
    result = triage("brokerage operations helper")
    assert result["regulated_boundary_result"] == "blocked"


def test_financial_advice_is_blocked():
    result = triage("financial advice assistant for teams")
    assert result["regulated_boundary_result"] == "blocked"


def test_payment_processing_is_blocked():
    result = triage("payment processing assistant")
    assert result["regulated_boundary_result"] == "blocked"


def test_human_resources_is_blocked():
    result = triage("human resources screening helper")
    assert result["regulated_boundary_result"] == "blocked"
