from engine_proof_helpers import make_run, read_json
from agialpha_engine.context import atomic_write_json
from agialpha_engine.validate import validate_run


def test_validate_fails_when_replay_report_is_false(tmp_path):
    out = make_run(tmp_path)
    report_path = out / "13_replay/replay_report.json"
    report = read_json(report_path)
    report["replay_pass"] = False
    atomic_write_json(report_path, report)
    result = validate_run(out)
    assert result["replay_report_pass"] is False
    assert result["replay_validation_pass"] is False
    assert result["validation_pass"] is False
