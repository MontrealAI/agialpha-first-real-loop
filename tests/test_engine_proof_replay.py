from engine_proof_helpers import make_run, run_cmd, read_json
from agialpha_engine.context import atomic_write_json


def test_replay_reproduces_metrics(tmp_path):
    out = make_run(tmp_path)
    run_cmd("replay-proof", "--run", str(out))
    assert read_json(out / "13_replay/replay_report.json")["replay_pass"] is True


def test_replay_fails_when_proofbundle_index_is_tampered(tmp_path):
    out = make_run(tmp_path)
    index_path = out / "10_proofbundles/proofbundle_index.json"
    index = read_json(index_path)
    index["proofbundle_complete"] = False
    atomic_write_json(index_path, index)
    run_cmd("replay-proof", "--run", str(out))
    report = read_json(out / "13_replay/replay_report.json")
    assert report["replay_pass"] is False
    assert report["recomputed_metrics"]["proofbundle_complete"] is False
