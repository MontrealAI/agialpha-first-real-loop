from engine_proof_helpers import make_run, read_json


def test_regulated_boundary_zero(tmp_path):
    out = make_run(tmp_path)
    assert read_json(out / "08_comparison/computed_metrics.json")["regulated_boundary_violations"] == 0
