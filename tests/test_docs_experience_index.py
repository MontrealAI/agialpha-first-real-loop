from pathlib import Path
import json

def test_experience_index_contains_major_experiences():
    p=Path('docs/_generated/public-experience/experience_index.json')
    data=json.loads(p.read_text())
    ids={e['experience_id'] for e in data['experiences']}
    assert 'secure-rails' in ids
    assert 'enterprise-pilot' in ids

def test_self_improvement_source_doc_correct():
    data=json.loads(Path('docs/_generated/public-experience/experience_index.json').read_text())
    item=next(e for e in data['experiences'] if e['experience_id']=='self-improvement-gauntlet')
    assert 'docs/self-improvement-gauntlet/README.md' in item['source_docs']
