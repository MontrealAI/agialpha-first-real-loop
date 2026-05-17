from pathlib import Path
import json

def test_page_health_json_exists():
    data=json.loads(Path('docs/_generated/public-experience/page_health.json').read_text())
    assert 'status' in data

def test_page_health_counts_home_route():
    data=json.loads(Path('docs/_generated/public-experience/page_health.json').read_text())
    assert data['routes_checked'] >= 15

def test_route_manifest_includes_cybersecurity_sovereign():
    manifest=json.loads(Path('docs/_generated/public-experience/route_manifest.json').read_text())
    assert '/cybersecurity-sovereign/' in manifest['routes']
