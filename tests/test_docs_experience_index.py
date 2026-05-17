from pathlib import Path
import json

def test_experience_index_contains_major_experiences():
    p=Path('docs/_generated/public-experience/experience_index.json')
    data=json.loads(p.read_text())
    ids={e['experience_id'] for e in data['experiences']}
    assert 'secure-rails' in ids
    assert 'enterprise-pilot' in ids
