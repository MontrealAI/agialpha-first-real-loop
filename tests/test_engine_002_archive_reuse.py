from engine_proof_helpers import make_run, read_json


def test_engine_002_archive_reuse_records_non_negative_lift(tmp_path):
    out = make_run(tmp_path)
    metrics = read_json(out / "08_comparison" / "computed_metrics.json")
    assert metrics["archive_reuse_lift_pct"] >= 0
    assert metrics["B6_beats_B5_computed"] in {True, False}
