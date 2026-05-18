from pathlib import Path


def test_no_hardcoded_vrci_in_engine_modules():
    text = Path("agialpha_engine/metrics.py").read_text() + Path("agialpha_engine/recursive_improvement.py").read_text()
    assert "vRCI_formula" in text
    assert "vRCI_computed\": 0" not in text
    assert "vRCI_computed\": 1" not in text
