from agialpha_enterprise_pilot.regulated_boundary import triage


def test_throughput_not_false_blocked_by_hr_substring():
    result = triage("throughput analysis for software quality evidence")
    assert result["regulated_boundary_result"] == "passed"


def test_hr_is_blocked_on_word_match():
    result = triage("HR workflow automation")
    assert result["regulated_boundary_result"] == "blocked"
