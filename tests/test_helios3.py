from pathlib import Path
from agialpha_helios3.core import run_experiment, replay, falsification_audit


def test_helios3_run_replay_audit(tmp_path: Path):
    root = tmp_path / "helios003"
    manifest = run_experiment(str(root))
    assert manifest["experiment_id"] == "HELIOS-003"
    assert manifest["B6_beats_B5_count"] == 8
    assert manifest["safety_incidents"] == 0
    assert (root / "00_manifest.json").exists()
    assert (root / "docs" / "index.html").exists()
    report = replay(str(root))
    assert report["status"] == "pass"
    audit = falsification_audit(str(root))
    assert audit["status"] == "pass"
