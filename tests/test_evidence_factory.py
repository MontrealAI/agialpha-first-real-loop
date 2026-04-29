from pathlib import Path
from agialpha_evidence_factory.core import complete_docket, lint_docket, build_scoreboard


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
    assert (docs / "index.html").exists()
