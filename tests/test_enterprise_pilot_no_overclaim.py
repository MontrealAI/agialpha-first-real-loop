from pathlib import Path

def test_docs_no_agi_claim():
    txt=Path("README_ENTERPRISE_PILOT.md").read_text(encoding="utf-8").lower()
    assert "achieved agi" not in txt
