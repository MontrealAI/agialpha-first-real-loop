from pathlib import Path

def test_start_here_exists_and_has_first_10_minutes():
    p = Path('docs/START_HERE.md')
    assert p.exists()
    t = p.read_text(encoding='utf-8').lower()
    assert 'first 10 minutes' in t
