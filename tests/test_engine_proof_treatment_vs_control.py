from engine_proof_helpers import make_run, read_json


def test_treatment_control_comparison_exists_and_treatment_wins(tmp_path):
    out = make_run(tmp_path)
    metrics = read_json(out / "08_comparison/computed_metrics.json")
    assert metrics["treatment_score"] > metrics["shadow_control_score"]
    assert metrics["B6_beats_B5_computed"] is True
