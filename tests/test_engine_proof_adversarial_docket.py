from engine_proof_helpers import make_run, read_json


def test_adversarial_docket_preserves_failures(tmp_path):
    out = make_run(tmp_path)
    for name in ["failed_runs", "rejected_claims", "evaluator_disagreements", "baseline_regressions", "falsification_attempts"]:
        data = read_json(out / "12_adversarial_docket" / f"{name}.json")
        assert data[name]
