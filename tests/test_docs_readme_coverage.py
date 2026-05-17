from pathlib import Path

def test_readme_has_start_here_and_pages():
    t=Path('README.md').read_text().lower()
    assert 'start here' in t
    assert 'github pages' in t
