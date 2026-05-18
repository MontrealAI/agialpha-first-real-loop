from agialpha_engine.heldout import check_leakage
from agialpha_engine.adjacent_mandate import default_mandate_pairs
from engine_proof_helpers import make_run, read_json


def test_heldout_leakage_absent_and_detectable(tmp_path):
    out = make_run(tmp_path)
    assert read_json(out / "05_heldout_mandate_B/leakage_check.json")["heldout_leakage_detected"] is False
    pairs = default_mandate_pairs(1)
    pairs[0]["mandate_B"]["heldout_fixtures"][0]["fixture_id"] = pairs[0]["mandate_A"]["training_fixtures"][0]["fixture_id"]
    assert check_leakage(pairs)["heldout_leakage_detected"] is True
