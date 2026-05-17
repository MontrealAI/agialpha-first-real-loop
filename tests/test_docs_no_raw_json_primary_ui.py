from pathlib import Path

def test_readme_not_raw_json_primary_ui():
    assert '.json' not in Path('README.md').read_text()[:200]
