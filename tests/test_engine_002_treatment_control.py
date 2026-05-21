from agialpha_engine.treatment_control import compute_delta, enforce_equal_budget


def test_enforce_equal_budget_uses_engine002_constraint_fields():
    control = {"budget_units": 100, "validator_gates": "identical", "score": 0.4}
    treatment = {"budget_units": 100, "validator_gates": "identical", "score": 0.6}
    assert enforce_equal_budget(control, treatment) is True


def test_enforce_equal_budget_rejects_missing_constraint_fields():
    control = {"score": 0.4}
    treatment = {"score": 0.6}
    assert enforce_equal_budget(control, treatment) is False


def test_compute_delta_blocks_missing_scores():
    control = {"budget_units": 100, "validator_gates": "identical"}
    treatment = {"budget_units": 100, "validator_gates": "identical", "score": 0.6}
    assert compute_delta(control, treatment) == {"status": "blocked", "reason": "missing_or_invalid_score"}


def test_compute_delta_ok_for_valid_scores():
    control = {"budget_units": 100, "validator_gates": "identical", "score": 0.25}
    treatment = {"budget_units": 100, "validator_gates": "identical", "score": 0.5}
    assert compute_delta(control, treatment) == {"status": "ok", "delta": 0.25, "treatment_wins": True}
