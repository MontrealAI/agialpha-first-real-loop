from pathlib import Path


def test_no_hardcoded_b6_win_in_engine002_metrics():
    text = Path("agialpha_engine/metrics.py").read_text()
    assert "B6_vs_B5_formula" in text
    assert "B6_beats_B5_computed\": True" not in text
