from pathlib import Path
import json

def test_public_experience_inventory_exists():
    p=Path('docs/_generated/public-experience/site_manifest.json')
    assert p.exists()
    data=json.loads(p.read_text())
    assert 'workflow_count' in data or 'workflows' in data
