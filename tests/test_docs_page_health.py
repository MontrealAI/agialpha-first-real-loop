from pathlib import Path
import json

def test_page_health_json_exists():
    data=json.loads(Path('docs/_generated/public-experience/page_health.json').read_text())
    assert 'status' in data
