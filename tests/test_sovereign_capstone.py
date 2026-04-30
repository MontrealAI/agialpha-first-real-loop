import json
import tempfile
from pathlib import Path

from agialpha_sovereign_capstone.core import cyber_sovereign, complete_helios, external_replay


def test_cyber_sovereign_generates_docket():
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "cyber"
        summary = cyber_sovereign(out, Path.cwd())
        assert summary["task_count"] >= 6
        assert summary["safety_incidents"] == 0
        assert (out / "00_manifest.json").exists()
        assert (out / "10_security_archive" / "CyberSecurityCapabilityArchive-v0.json").exists()
        assert (out / "index.html").exists()


def test_helios_completion_generates_manifest():
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "helios"
        status = complete_helios(out)
        assert status["next_experiment"] == "CYBER-SOVEREIGN-001"
        assert (out / "00_helios_completion_manifest.json").exists()


def test_external_replay_reports_source():
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "src"
        src.mkdir()
        (src / "00_manifest.json").write_text(json.dumps({"ok": True}))
        out = Path(td) / "replay"
        report = external_replay(src, out)
        assert report["source_exists"] is True
        assert report["replay"] == "pass"
