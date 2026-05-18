from engine_proof_helpers import make_run, read_json


def test_metrics_computed_from_raw_results(tmp_path):
    out = make_run(tmp_path)
    metrics = read_json(out / "08_comparison/computed_metrics.json")
    treatment = read_json(out / "06_treatment_run/raw_results.json")["results"]
    shadow = read_json(out / "07_shadow_control_run/raw_results.json")["results"]
    expected_delta = round(sum(r["score"] for r in treatment)/len(treatment) - sum(r["score"] for r in shadow)/len(shadow), 6)
    assert metrics["improvement_delta"] == expected_delta
    assert metrics["vRCI_computed"] == round(expected_delta * metrics["mandate_pairs_run"], 6)
