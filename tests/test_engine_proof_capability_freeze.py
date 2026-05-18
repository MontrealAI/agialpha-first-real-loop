from engine_proof_helpers import make_run, read_json


def test_capability_freezes_and_mutation_fails(tmp_path):
    out = make_run(tmp_path)
    check = read_json(out / "04_capability_freeze/mutation_check.json")
    assert check["capability_freeze_valid"] is True
    assert check["mutation_after_freeze_negative_test"]["mutation_detected"] is True
