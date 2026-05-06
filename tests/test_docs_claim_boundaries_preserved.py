from pathlib import Path

def test_boundary_phrases_present_and_forbidden_not_positive():
    txt = Path('docs/CLAIM_BOUNDARIES.md').read_text(encoding='utf-8').lower()
    assert 'does not claim achieved agi' in txt or 'not empirical sota' in txt
    assert 'offensive cyber' in txt
    assert 'investment product' in txt
