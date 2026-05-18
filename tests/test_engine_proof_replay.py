from engine_proof_helpers import make_run, run_cmd, read_json


def test_replay_reproduces_metrics(tmp_path):
    out = make_run(tmp_path)
    run_cmd("replay-proof", "--run", str(out))
    assert read_json(out / "13_replay/replay_report.json")["replay_pass"] is True
