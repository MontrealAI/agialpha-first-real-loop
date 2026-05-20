from engine_proof_helpers import make_run, read_json


def test_engine_002_autonomous_persistence_is_blocked(tmp_path):
    out = make_run(tmp_path)
    summary = read_json(out / "15_public_summary" / "summary.json")
    assert summary["metrics"]["autonomous_persistence_attempts_blocked"] >= 1
