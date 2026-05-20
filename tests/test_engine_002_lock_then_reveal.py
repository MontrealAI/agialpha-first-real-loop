from engine_proof_helpers import make_run, read_json


def test_engine_002_lock_then_reveal_records_holdout_lock(tmp_path):
    out = make_run(tmp_path)
    lock = read_json(out / "06_descendants" / "lock_then_reveal.json")
    assert lock["heldout_revealed_after_lock"] is True
    assert lock["lock_hash"]
