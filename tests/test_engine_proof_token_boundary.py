from engine_proof_helpers import make_run, read_json


def test_token_boundary_zero_and_utility_only(tmp_path):
    out = make_run(tmp_path)
    assert read_json(out / "08_comparison/computed_metrics.json")["token_boundary_violations"] == 0
    assert "utility-only" in (out / "01_claim_boundary.md").read_text()
