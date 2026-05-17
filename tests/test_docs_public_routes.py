from pathlib import Path
import json

def test_major_routes_indexed():
    data=json.loads(Path('docs/_generated/public-experience/route_manifest.json').read_text())
    assert '/secure-rails/' in data['routes']
