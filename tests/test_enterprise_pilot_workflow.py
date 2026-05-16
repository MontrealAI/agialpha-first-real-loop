from pathlib import Path

def test_workflow_exists_and_no_pages_deploy():
    p=Path(".github/workflows/agialpha-enterprise-pilot-001.yml")
    t=p.read_text(encoding="utf-8").lower()
    assert "pages" not in t
    assert "automerge" not in t
