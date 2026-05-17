from pathlib import Path

def test_regulated_boundary_present():
    assert 'does not perform regulated financial' in Path('README.md').read_text().lower()
