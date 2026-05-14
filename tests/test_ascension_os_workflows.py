from pathlib import Path

def test_workflow_exists_and_no_pages_deploy():
    p=Path('.github/workflows/agialpha-ascension-os-001.yml')
    text=p.read_text()
    assert 'workflow_dispatch' in text
    assert 'pages' not in text.lower()
    assert 'auto-merge' not in text.lower()
