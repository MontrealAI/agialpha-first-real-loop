from pathlib import Path

def test_token_boundary_present():
    assert 'utility-only accounting' in Path('README.md').read_text().lower()
