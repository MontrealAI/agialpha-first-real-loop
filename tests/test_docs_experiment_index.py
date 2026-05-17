from pathlib import Path
import json

def test_experiment_index_exists():
    data=json.loads(Path('docs/_generated/public-experience/experiment_index.json').read_text())
    assert data['experiments']

def test_experiment_index_built_from_repo_state():
    data=json.loads(Path('docs/_generated/public-experience/experiment_index.json').read_text())
    slugs={e['slug'] for e in data['experiments']}
    assert 'agialpha-enterprise-pilot-001' in slugs
    assert 'agialpha-ascension-os-001' in slugs
