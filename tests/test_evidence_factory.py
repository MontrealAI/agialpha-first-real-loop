from pathlib import Path
from agialpha_evidence_factory.core import complete_docket, lint_docket, build_scoreboard
import json


def test_seed_docket_completes(tmp_path: Path):
    src = Path(__file__).resolve().parents[1] / "evidence-docket"
    out = tmp_path / "complete"
    complete_docket(src, out)
    assert (out / "claim_level.json").exists()
    assert lint_docket(out, strict=True)["status"] == "pass"


def test_scoreboard_builds(tmp_path: Path):
    src = Path(__file__).resolve().parents[1] / "evidence-docket"
    out = tmp_path / "complete"
    docs = tmp_path / "docs"
    complete_docket(src, out)
    index = build_scoreboard([out], docs)
    assert index["runs"]
    assert index["experiments"]
    assert (docs / "index.html").exists()
    html = (docs / "index.html").read_text(encoding="utf-8")
    assert "Experiments:" in html


def test_scoreboard_preserves_non_hyphen_run_id_and_encodes_anchor(tmp_path: Path):
    docs = tmp_path / "docs"
    docket = tmp_path / "alpha dossier"
    docket.mkdir(parents=True)
    (docket / "00_manifest.json").write_text(json.dumps({"docket_id": "alpha dossier"}), encoding="utf-8")
    index = build_scoreboard([docket], docs)
    assert index["experiments"]["alpha dossier"] == 1
    html = (docs / "index.html").read_text(encoding="utf-8")
    assert "href='#alpha%20dossier'" in html
