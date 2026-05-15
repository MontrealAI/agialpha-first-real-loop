from pathlib import Path

def test_workflow_no_pages_or_automerge():
    t=Path('.github/workflows/agialpha-valuation-support-002.yml').read_text().lower()
    assert 'pages' not in t
    assert 'automerge' not in t
